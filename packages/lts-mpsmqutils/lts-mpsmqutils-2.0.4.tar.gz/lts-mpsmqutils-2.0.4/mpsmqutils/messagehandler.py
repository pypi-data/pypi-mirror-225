import datetime, email, json, os, re, smtplib, time, traceback, sys
import celery as celeryapp

# https://www.geeksforgeeks.org/python-import-from-parent-directory/
sys.path.append('../app')
from app import worker_task

from textwrap import dedent

import mpsmqutils.mqutils as mqutils
# Job tracker module
import mpsjobtracker.trackers.jobtracker as jobtracker
job_tracker = jobtracker.JobTracker()

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import mpsmqutils.log_wrapper as log_wrapper
logger = log_wrapper.LogWrapper()

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http_client = requests.Session()
http_client.mount("https://", adapter)
http_client.mount("http://", adapter)

_hostname_prefix = os.getenv('HOSTNAME') + ": "

# Notify config for use in the notify application
NOTIFY_QUEUE = os.getenv('MQ_NOTIFY_QUEUE', '/queue/iiif_notify')
DLQ_QUEUE = os.getenv('MQ_DLQ_QUEUE', '/queue/ActiveMQ.DLQ')

# Email SMTP host for use in notify
NOTIFY_MAIL_RELAY=os.getenv('MQ_NOTIFY_MAIL_RELAY', None)
NOTIFY_DEFAULT_EMAIL=os.getenv('MQ_NOTIFY_DEFAULT_EMAIL', None)

def call_worker_do_task(task_name, job_ticket_id = None, parent_job_ticket_id = None, worker_url_endpoint = 'do_task', worker_url = os.getenv('WORKER_API_URL'), add_params=None):
    logger.debug("************************ MQUTILS MQLISTENER - CALL WORKER DO TASK *******************************", end='')
    '''Call the worker task class do task method and process the response in a standard format'''

    result = {
      'success': False,
      'error': None,
      'message': None
    }
    job_ticket_id_str = f" job_ticket_id: {job_ticket_id}" if job_ticket_id else ""
    parent_job_ticket_id_str = f" parent_job_ticket_id: {parent_job_ticket_id}" if parent_job_ticket_id else ""
    logger.debug(f'mqlistener call_worker_do_task START{job_ticket_id_str}{parent_job_ticket_id_str} task_name {task_name}', end='')

    """
      Call worker task class do task method
    """
    try:
        message_data = { 'task_name': task_name }
        if add_params:
            message_data = {**json_params, **add_params}
        if job_ticket_id:
            message_data['job_ticket_id'] = job_ticket_id
        if parent_job_ticket_id:
            message_data['parent_job_ticket_id'] = parent_job_ticket_id
        logger.debug(message_data, end='')
        wt = worker_task.WorkerTask()
        response_json = wt.do_task(message_data)
    except Exception as e:
        logger.error(e, end='')
        raise Exception(e)

    logger.debug(f'mqlistener call_worker_do_task COMPLETE{job_ticket_id_str}{parent_job_ticket_id_str} task_name {task_name}', end='')

    logger.debug(response_json, end='')

    success = False if not response_json.get('success') else True
    logger.debug("mqlistener call_worker_do_task success:", end='')
    logger.debug(success, end='')
    result['success'] = success
    result['error'] = response_json.get('error', None)
    result['message'] = response_json.get('message', None)

    return result

def call_worker_api(task_name, job_ticket_id = None, parent_job_ticket_id = None, worker_url_endpoint = 'do_task', worker_url = os.getenv('WORKER_API_URL'), add_params=None):
    logger.debug("************************ MQUTILS MQLISTENER - CALL WORKER API *******************************", end='')
    '''Call the worker API and process the response in a standard format'''

    result = {
      'success': False,
      'error': None,
      'message': None
    }
    job_ticket_id_str = f" job_ticket_id: {job_ticket_id}" if job_ticket_id else ""
    parent_job_ticket_id_str = f" parent_job_ticket_id: {parent_job_ticket_id}" if parent_job_ticket_id else ""
    logger.debug(f'mqlistener call_worker_api START{job_ticket_id_str}{parent_job_ticket_id_str} task_name {task_name}', end='')

    """
      Call worker API internally to perform the task
      This API call is calling the worker task in the same container and must use the internal container port
    """
    try:

        if not worker_url:
            error_msg = 'Missing configuration WORKER_API_URL'
            logger.error(error_msg, end='')
            raise Exception(error_msg)
        url = worker_url + '/' + worker_url_endpoint
        logger.debug('mqlistener call_worker_api url {}'.format(url), end='')
        json_params = { 'task_name': task_name }
        if add_params:
            json_params = {**json_params, **add_params}
        if job_ticket_id:
            json_params['job_ticket_id'] = job_ticket_id
        if parent_job_ticket_id:
            json_params['parent_job_ticket_id'] = parent_job_ticket_id
        logger.debug("json_params", end='')
        logger.debug(json_params, end='')
        # The worker uses a self-signed certificate and it does not need to be verified since the listener makes a request to the worker inside the same container internally
        response = http_client.post(url, json = json_params, verify=False)
        response.raise_for_status()
        logger.debug(response, end='')
    except Exception as e:
        logger.error(e, end='')
        if job_ticket_id:
            job_tracker.append_error(job_ticket_id, 'mqlistener call_worker_api API call failed', traceback.format_exc(), True)
        raise Exception(e)

    logger.debug(f'mqlistener call_worker_api COMPLETE{job_ticket_id_str}{parent_job_ticket_id_str} task_name {task_name} response.json() {response.json()}', end='')

    response_json = response.json()
    logger.debug(response_json, end='')

    success = False if not response_json.get('success') else True
    logger.debug("mqlistener call_worker_api success:", end='')
    logger.debug(success, end='')
    result['success'] = success
    result['error'] = response_json.get('error', None)
    result['message'] = response_json.get('message', None)

    return result

def call_generic_worker_api(message_data, worker_endpoint):
    logger.debug("************************ MQUTILS MQLISTENER - CALL GENERIC WORKER API *******************************", end='')
    '''Call the worker API and process the response in a standard format'''

    result = {
      'success': False,
      'error': None,
      'message': None,
      'next_queue': None
    }
    worker_url = os.getenv('WORKER_API_URL') + '/' + worker_endpoint

    """
      Call worker API internally to perform the task
      This API call is calling the worker task in the same container and must use the internal container port
    """
    try:
        if not worker_url:
            error_msg = 'Missing configuration WORKER_API_URL'
            logger.error(error_msg, end='')
            raise Exception(error_msg)
        url = worker_url
        logger.debug('mqlistener call_generic_worker_api url {}'.format(url), end='')
        # The worker uses a self-signed certificate and it does not need to be verified since the listener makes a request to the worker inside the same container internally
        response = http_client.post(url, json = message_data, verify=False)
        response.raise_for_status()
        logger.debug('response.raise_for_status', end='')
        logger.debug(response, end='')
    except Exception as e:
        logger.error(e, end='')
        raise Exception(e)

    response_json = response.json()
    logger.debug(response_json, end='')

    success = False if not response_json.get('success') else True
    logger.debug("success for call_generic_worker_api:", end='')
    logger.debug(success, end='')
    result['success'] = success
    result['error'] = response_json.get('error', None)
    result['message'] = response_json.get('message', None)
    result['next_queue'] = response_json.get('next_queue', None)

    return result

def handle_worker_response(job_ticket_id, worker_response, parent_job_ticket_id=None):
    logger.debug("************************ MQUTILS MQLISTENER - HANDLE_WORKER_RESPONSE *******************************", end='')
    """Handle the response from the worker API
    Capture any error messages returned in the json body
    Examples worker API responses:
    Response was successful: { success: true }
    Response had an error: { success: false, 'error': 'Example error', 'message': 'Example error message' }
    """
    task_success = True if worker_response.get('success') else False
    logger.debug("task success for handle_worker_response", end='')
    logger.debug(task_success, end='')
    if not task_success:
        # Set job failed if the job is a child job
        set_job_failed = True if parent_job_ticket_id else False
        job_tracker.append_error(job_ticket_id, worker_response.get('error'), worker_response.get('message'), set_job_failed)
    return task_success

completed_statuses = frozenset(['success', 'failed'])
class MqMessageHandler():
    def __init__(self, message):
        self.message = message

    def handle_message(self):
        logger.debug("************************ MQUTILS MQLISTENER - HANDLE_MESSAGE *******************************", end='')
        # headers, body = frame.headers, frame.body
        logger.info('handling message "%s"' % self.message, end='')

        category = self.message.get("category", "ingest")
        task_success = False
        job_ticket_id = self.message.get('job_ticket_id')
        logger.debug('job_ticket_id {}'.format(job_ticket_id), end='')
        try:
            job_tracker_doc = job_tracker.get_tracker_document(job_ticket_id)
        except Exception as e:
            import traceback
            logger.error("Exception trying to get tracker_document: " + traceback.format_exc(), end='')
            job_tracker_doc = None

        logger.debug('job_tracker_doc {}'.format(job_tracker_doc), end='')
        status = job_tracker_doc['job_management']['job_status']
        if status in completed_statuses:
            logger.debug(f'Status {status} counts as completed, assuming job is complete', end='')
            #Assume if the tracker is completed or not there, that this job is no longer running
            return

        logger.debug(f"Dispatching based on category: {category}", end='')
        if (category == "ingest"):
            task_success = self.__ingest_message_handler(self.message)
        elif (category == "task_management"):
            task_success = self.__task_management_message_handler(self.message)
        elif (category == "service"):
            task_success = self.__service_message_handler(self.message)
        elif (category == "cache_management"):
            task_success = self.__cache_management_message_handler(self.message)

        if (task_success != None):
            if not task_success:
                job_tracker.set_job_status('failed', job_ticket_id, "failed")
                logger.error('Task unsuccessful', end='')

        logger.info('successfully processed message for job id {}'.format(job_ticket_id), end='')

    def __ingest_message_handler(self, message_data):
        logger.debug("************************ MQUTILS MQLISTENER - INGEST_MESSAGE_HANDLER *******************************", end='')
        job_ticket_id = message_data.get('job_ticket_id')
        logger.debug('__ingest_message_handler job_ticket_id {}'.format(job_ticket_id), end='')
        parent_job_ticket_id = message_data.get('parent_job_ticket_id', None)
        logger.debug('parent_job_ticket_id {}'.format(parent_job_ticket_id), end='')
        task_name = message_data.get('task_name')
        logger.debug('task_name {}'.format(task_name), end='')
        previous_step_status = message_data.get('previous_step_status', 'success')
        logger.debug('previous_step_status {}'.format(previous_step_status), end='')
        task_success = False
        worker_url_endpoint = "do_task"

        try:
            logger.debug('set_job_status to running', end='')
            job_tracker.set_job_status('running', job_ticket_id)
        except Exception as e:
            logger.error(e, end='')
            return False

        # Run the service
        # Check if previous step status was successful
        if previous_step_status and 'fail' not in previous_step_status:
            # Update timestamp file before do task
            logger.debug('Calling do_task for job_ticket_id {} task_name {}'.format(job_ticket_id, task_name), end='')

            worker_url_endpoint = "do_task"

            nextmessage = mqutils.create_next_queue_message(job_ticket_id, parent_job_ticket_id)
            logger.debug('create_next_queue_message nextmessage {}'.format(nextmessage), end='')

        else:
            job_tracker.update_timestamp(job_ticket_id)

            logger.debug('Calling revert_task for job_ticket_id {} task_name {}'.format(job_ticket_id, task_name), end='')
            worker_url_endpoint = "revert_task"

            # Create next queue message
            nextmessage = mqutils.create_revert_message(job_ticket_id, parent_job_ticket_id)
            logger.debug('create_revert_message nextmessage {}'.format(nextmessage), end='')
        try:
            #Update the timestamp
            job_tracker.update_timestamp(job_ticket_id)
            logger.debug("Successfully updated timestamp for job_ticket_id {} parent_job_ticket_id {}".format(job_ticket_id, parent_job_ticket_id), end='')
        except Exception as e:
            logger.error(e, end='')
            return False

        # Call worker class do task method
        try:
            worker_response = call_worker_do_task(task_name, job_ticket_id, parent_job_ticket_id, worker_url_endpoint)
            task_success = handle_worker_response(job_ticket_id, worker_response, parent_job_ticket_id)
            logger.debug("SUCCESS IN WORKER RESPONSE TRY BLOCK", end='')
        except Exception as e:
            logger.error(e, end='')
            task_success = False
            job_tracker.append_error(job_ticket_id, str(e), traceback.format_exc(), True)

        if (task_success):
            # Update timestamp file after task is complete
            logger.debug('AFTER TASK UPDATING TIMESTAMP FILE job_ticket_id {}'.format(job_ticket_id), end='')
            job_tracker.update_timestamp(job_ticket_id)
            if nextmessage is None:
                job_tracker.set_job_status(previous_step_status, job_ticket_id)
                logger.debug('******** LAST TASK COMPLETED ********', end='')
                logger.debug('previous_step_status {} job_ticket_id {} parent_job_ticket_id {}'.format(previous_step_status, job_ticket_id, parent_job_ticket_id), end='')
            else:
                try:
                    json_message = json.loads(nextmessage)
                    logger.debug(json_message, end='')
                except ValueError as e:
                    logger.error(e, end='')
                    job_tracker.append_error(job_ticket_id, 'Unable to get parse the next queue message',  traceback.format_exc(), False)
                    raise e

                # Set the queue name to match the worker type
                worker_type = json_message["event"]
                queue = worker_type
                logger.debug('worker_type {}'.format(worker_type), end='')
                tracker_doc = job_tracker.get_tracker_document(job_ticket_id)
                # Update the number of tries in the tracker file
                tracker_doc["job_management"]["numberOfTries"] = 0
                tracker_doc["job_management"]["current_step"] = json_message["current_step"]
                tracker_doc["job_management"]["job_status"] = "queued"
                tracker_doc["job_management"]["previous_step_status"] = json_message["previous_step_status"]
                try:
                    logger.debug('******** UPDATE TRACKER FILE ********', end='')
                    updated_tracker_doc = job_tracker.replace_tracker_doc(tracker_doc)
                    logger.debug('updated_tracker_doc {}'.format(updated_tracker_doc), end='')
                except Exception as e:
                    #TODO what to do here - what does this mean if the tracker retrieval fails?
                    logger.error("TRACKER RETRIEVAL FAILED", end='')
                    logger.error(e, end='')
                    raise e
                celeryapp.execute.send_task("tasks.tasks.do_task", args=[nextmessage], kwargs={}, queue=queue)
        logger.debug('task_success for __ingest_message_handler:', end='')
        logger.debug(task_success, end='')
        return task_success

    def __task_management_message_handler(self, message_data):
        logger.debug("************************ MQUTILS MQLISTENER - TASK MANAGEMENT MESSAGE HANDLER *******************************", end='')
        logger.debug('__task_management_message_handler:', end='')
        job_ticket_id = message_data.get('job_ticket_id')
        parent_job_ticket_id = message_data.get('parent_job_ticket_id', None)
        task_name = message_data.get('task_name')
        logger.debug(task_name, end='')
        task_success = False

        #We want the task manager to watch the multi asset ingest jobs
        if (task_name == "multi_asset_ingest"):
            logger.debug("MULTI ASSET INGEST TASK", end='')

        try:
            job_tracker.set_job_status('running', job_ticket_id)
            # Run the service
            # Update timestamp file before do task
            logger.debug('BEFORE DO TASK UPDATING TIMESTAMP FILE job_ticket_id {}'.format(job_ticket_id), end='')
            job_tracker.update_timestamp(job_ticket_id)
        except Exception as e:
            logger.error(e, end='')
            task_success = False

        # Call do task
        logger.debug("******************* CALLING WORKER API DO TASK __task_management_message_handler *******************", end='')
        try:
            logger.debug("call_worker_do_task task_name {} job_ticket_id {} parent_job_ticket_id {} do_task", end='')
            worker_response = call_worker_do_task(task_name, job_ticket_id, parent_job_ticket_id, 'do_task')
            logger.debug("worker_response", end='')
            logger.debug(worker_response, end='')
        except Exception as e:
            logger.error("CALLING WORKER API DO TASK FAILED", end='')
            logger.error(e, end='')
            task_success = False
            job_tracker.append_error(job_ticket_id, str(e), traceback.format_exc(), True)

        logger.debug("******************* HANDLE WORKER RESPONSE *******************", end='')
        try:
            task_success = handle_worker_response(job_ticket_id, worker_response, parent_job_ticket_id)
        except Exception as e:
            logger.error("HANDLE WORKER RESPONSE FAILED", end='')
            logger.error(e, end='')
            task_success = False
            job_tracker.append_error(job_ticket_id, str(e), traceback.format_exc(), True)

        logger.debug("task_success in __task_management_message_handler:", end='')
        logger.debug(task_success, end='')

        #Ack message was already handled above
        if (task_name == "multi_asset_ingest"):
            try:
                job_status = job_tracker.get_job_status(job_ticket_id)
                if job_status == "failed":
                    logger.error('JOB STATUS: FAILED', end='')
                # Successful parent jobs will be handled by the task_manager's job monitor which periodically checks in-progress
                # jobs for stalled jobs or parent jobs where all children are complete. Upon successful completion of all child
                # jobs, the parent will be marked by that process as successful
            except Exception as e:
                job_tracker.append_error(job_ticket_id, f"Exception {str(e)} in job {job_ticket_id}", traceback.format_exc(), True)

            return None
        return task_success


    def __service_message_handler(self, message_data):
        logger.debug('services message', end='')
        return True

    def __cache_management_message_handler(self, message_data, message_id):
        logger.debug('cache management message', end='')
        try:
            worker_response = call_worker_api('update_cache')
        except Exception as e:
            import traceback;
            logger.error('Failure in cache management handler', end='')
            logger.error(traceback.format_exc(), end='')
            return False
        return True

# Generalized listener based on MQListener for use with components that do not use jobtracker
# If a next queue is returned from do_task, will place the same message it received on the specified queue
class GenericMessageHandler():
    def __init__(self, message, worker_endpoint='do_task'):
        self.message = message
        self.worker_endpoint = worker_endpoint

    def handle_message(self):
        logger.info('received a message headers "%s"' % self.message, end='')
        task_success = False

        task_success = self.__generic_message_handler(self.message, self.worker_endpoint)

        if (task_success != None):
            if not task_success:
                logger.error('Task unsuccessful', end='')

    def __generic_message_handler(self, message_data, worker_endpoint):
        logger.debug("************************ MQUTILS MQLISTENER - GENERIC_MESSAGE_HANDLER *******************************", end='')
        task_success = False

        # Call task
        try:
            worker_response = call_generic_worker_api(message_data, worker_endpoint)
            next_queue = os.getenv('NEXT_QUEUE')
            task_success = True if worker_response.get('success') else False
            logger.debug("SUCCESS IN WORKER RESPONSE TRY BLOCK", end='')
        except Exception as e:
            logger.error(e, end='')
            task_success = False

        if (task_success):
            # Update timestamp file after task is complete
            if next_queue is None:
                #There are no more items to queue so the job is actually finished.
                logger.debug('******** LAST TASK COMPLETED ********', end='')
            else:
                logger.debug('******** TASK COMPLETED - GOING TO NEXT QUEUE ********', end='')
                celeryapp.execute.send_task("tasks.tasks.do_task", args=[self.message], kwargs={}, queue=next_queue)
        logger.debug('task_success for __generic_message_handler', end='')
        logger.debug(task_success, end='')
        return task_success

# NOTIFY_SUB=2
# DLQ_SUB=3
# recipient_separators = re.compile(r'[,;]')
# class NotificationListener(stomp.ConnectionListener):
#     def __init__(self, conn):
#         self.conn = conn

#     def on_disconnected(self):
#         print('disconnected: reconnecting...')
#         connect_and_subscribe(self.conn, NOTIFY_QUEUE, sub_id=NOTIFY_SUB)
#         connect_and_subscribe(self.conn, DLQ_QUEUE, sub_id=DLQ_SUB)

#     def handle_direct_notification(self, frame):
#         print("Handling message from notification queue")
#         message = json.loads(frame.body)

#         if not 'to' in message:
#             message['to'] = [NOTIFY_DEFAULT_EMAIL]

#         if message['method'] == "email":
#             print("Method is email", flush=True)
#             if isinstance(message['to'], str):
#                 message['to'] = recipient_separators.split(message['to'])
#             msg = dedent(f"""\
#             From: {message['from']}
#             Subject: {message['subject']}

#             """) + message["message"]

#             print(f"Sending mail to {message['to']} via {NOTIFY_MAIL_RELAY}")
#             with smtplib.SMTP(NOTIFY_MAIL_RELAY) as smtp:
#                 try:
#                     result = smtp.sendmail(
#                         from_addr='no-reply@iiif.harvard.edu',
#                         to_addrs=message['to'],
#                         msg = msg
#                     )
#                 except Exception as e:
#                     print(f"Sendmail failed with exception {e}")
#                     import traceback
#                     print(traceback.format_exc())
#                 print(f"Result of sendmail: {result}", flush=True)
#         else:
#             raise RuntimeError('Unknown method for notification')


#     def handle_dlq(self, frame):
#         print('Handling DLQ notification')
#         message = json.loads(frame.body)
#         job_ticket_id = message_data.get('job_ticket_id')
#         parent_job_ticket_id = message_data.get('parent_job_ticket_id', None)
#         tracker_doc = job_tracker.get_tracker_doc(job_ticket_id, parent_job_ticket_id)
#         parent_suffix = f" with Parent Job: {parent_job_ticket_id}" if parent_job_ticket_id else ""
#         msg = dedent(f"""\
#         From: IIIF Notifier <no-reply@iiif.harvard.edu>
#         Subject: Job: {job_ticket_id}{parent_suffix}

#         Job {job_ticket_id}{parent_suffix} has failed.

#         Job tracker file contents follow.

#         """) + json.dumps(tracker_doc)
#         with smtplib.SMTP(NOTIFY_MAIL_RELAY) as smtp:
#             try:
#                 result = smtp.sendmail(
#                     from_addr='no-reply@iiif.harvard.edu',
#                     to_addrs=[NOTIFY_DEFAULT_EMAIL],
#                     msg = msg
#                 )
#             except Exception as e:
#                 print(f"Sendmail failed with exception {e}")
#                 import traceback
#                 print(traceback.format_exc())
#                 raise(e)
#             print(f"Result of sendmail: {result}", flush=True)

#     def on_message(self, frame):
#         headers, body = frame.headers, frame.body
#         message_id = headers.get('message-id')
#         sub_id = int(headers.get('subscription'))
#         print(f'handling message {message_id} from sub {sub_id}')
#         try:
#             if sub_id == NOTIFY_SUB:
#                 print('received direct notification')
#                 self.handle_direct_notification(frame)
#             elif sub_id == DLQ_SUB:
#                 print('received DLQ notification')
#                 self.handle_dlq(frame)
#             else:
#                 raise RuntimeError(f"sub_id {sub_id} is unknown")
#         except Exception as e:
#             self.conn.nack(message_id, sub_id)
#             raise(e)
#         self.conn.ack(message_id, sub_id)

#     def on_error(self, frame):
#         print('received an error "%s"' % frame.body)
