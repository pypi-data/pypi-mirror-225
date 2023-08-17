"""
Setup of the slack notification.  The default slack notifier that is provided by Prefect had two issues that
needed fixing:

    1) The URL of the link was wrong
    2) No rate limiting

"""
# pylint: disable=broad-except
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=no-member
# pylint: disable=too-many-branches

# Import standard libraries
import datetime
import json
import socket
from io import BytesIO
from typing import cast

# Related 3rd party imports
import azure.core.exceptions
import prefect
import requests
from prefect.engine.state import Failed, TimedOut, TriggerFailed
from prefect.utilities.graphql import with_args

from .storage import AzureStorage

DEBUG = False  # if set to True, notifications will also be sent when running locally

from .logger import logger

NOTIFICATION_FILEBUCKET = "runinfo"
NOTIFICATION_FILEPATH = "prefect/state/notification_state.json"
NOTIFICATION_RATE_LIMIT = (
    7200  # only allow 1 notification for every 7200 seconds (per flow)
)


def customized_slack_notifier(config, flow, new_state, _reference_task_states):
    """
    Customized version of the slack notifier.  Only send out notifications for a specific flow at most
    once every 2 hours.
    """
    webhook_url = config.get("SLACK_WEBHOOK_URL")
    if webhook_url is None:
        if DEBUG:
            # fallback to posting to '#pedgar-test'
            webhook_url = "https://hooks.slack.com/services/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"
        else:
            logger.warning(
                "No slack webhook found.  Not sending any failure notification."
            )
            return new_state
    send_notification = False
    if isinstance(new_state, Failed):
        flow_name = prefect.context.get("flow_name")
        notifications = get_notification_state(config)

        if flow_name in notifications:
            last_notified = datetime.datetime.fromisoformat(notifications[flow_name])
            if last_notified < datetime.datetime.now() - datetime.timedelta(
                seconds=NOTIFICATION_RATE_LIMIT
            ):
                send_notification = True
            else:
                logger.info(
                    "Last notified about '%s' at %s.  Not sending new notification for at least %s seconds",
                    flow_name,
                    last_notified,
                    (
                        last_notified
                        + datetime.timedelta(seconds=NOTIFICATION_RATE_LIMIT)
                        - datetime.datetime.now()
                    ).total_seconds(),
                )
        else:
            send_notification = True
            logger.info("Don't know the last time we notified about '%s'", flow_name)

        if send_notification:
            # Don't send notifications when testing locally
            if DEBUG or not is_running_locally():
                notifications[flow_name] = datetime.datetime.now().isoformat()
                set_notification_state(config, notifications)

                form_data = get_task_runs_for_flow_local(flow, new_state)
                if form_data is None:
                    form_data = get_task_runs_for_flow_cloud(flow, new_state)

                resp = requests.post(webhook_url, json=form_data)
                if not resp.ok:
                    raise ValueError("Slack notification for {} failed".format(flow))
            else:
                logger.info(
                    "Not sending slack notification because we're running locally and DEBUG isn't enabled"
                )
    return new_state


def get_task_runs_for_flow_cloud(flow, _new_state):
    """
    Get the list of task runs when the Prefect flow is run on the Prefect server (not locally)

    Uses the GraphQL API to find out the information because of the following bug:
        https://github.com/PrefectHQ/prefect/issues/4570
    """
    flow_run_id = prefect.context.get("flow_run_id")
    query_flows = {
        "query": {
            with_args(
                "task_run",
                {
                    "where": {
                        "flow_run_id": {"_eq": flow_run_id},
                    },
                },
            ): {
                "id": True,
                "name": True,
                "task": {
                    "name": True,
                },
                "state": True,
                "state_message": True,
            }
        }
    }

    prefect_client = prefect.client.Client()
    task_runs = prefect_client.graphql(query_flows).data.task_run
    failed_task = None
    failed_state = None
    failed_state_message = None
    for task_info in task_runs:
        if task_info["state"] == "Failed":
            failed_task = task_info["task"]["name"]
            failed_state = task_info["state"]
            failed_state_message = task_info["state_message"]
            break
        if task_info["state"] in ["TriggerFailed", "TimedOut"] and failed_task is None:
            failed_task = task_info["task"]["name"]
            failed_state = task_info["state"]
            failed_state_message = task_info["state_message"]

    if failed_task is not None:
        return slack_message_formatter(
            flow.name, failed_task, failed_state, failed_state_message
        )

    logger.warning(
        "Failed to find failed task info for flow %s. 'task_runs' = %s",
        flow.name,
        task_runs,
    )
    return None


def get_task_runs_for_flow_local(flow, new_state):
    """
    Get the list of task runs when the Prefect flow is run locally (not on the Prefect server)

    Uses a different method to find out the information because of the following bug:
        https://github.com/PrefectHQ/prefect/issues/4570
    """
    failed_task = None
    failed_state = None

    for task, task_state in new_state.result.items():
        if isinstance(task_state, Failed):
            if not isinstance(task_state, TriggerFailed) and not isinstance(
                task_state, TimedOut
            ):
                failed_task = task
                failed_state = task_state
                break
            if failed_task is None:
                failed_task = task
                failed_state = task_state

    if failed_task is not None:
        return slack_message_formatter_from_obj(flow, failed_task, failed_state)
    return None


def get_notification_state(config):
    """
    Get the list of flows and the last time a notification was sent for them
    """
    notifications = {}
    try:
        data_text = AzureStorage(
            config.get("AZURE_STORAGE_ACCOUNT_NAME"),
            config.get("AZURE_STORAGE_ACCOUNT_KEY"),
        ).read(
            NOTIFICATION_FILEBUCKET,
            NOTIFICATION_FILEPATH,
        )
        notifications = json.loads(data_text)
    except azure.core.exceptions.ResourceNotFoundError:
        pass
    except Exception:
        logger.exception("got an unexpected exception")
    return notifications


def set_notification_state(config, notifications):
    """
    Store the list of flows and the last time a notification was sent for them
    """
    try:
        AzureStorage(
            config.get("AZURE_STORAGE_ACCOUNT_NAME"),
            config.get("AZURE_STORAGE_ACCOUNT_KEY"),
        ).store(
            NOTIFICATION_FILEBUCKET,
            NOTIFICATION_FILEPATH,
            BytesIO(str.encode(json.dumps(notifications))),
            overwrite=True,
        )
    except Exception:
        logger.exception("Got an unexpected exception while storing notification state")


def is_running_locally():
    """
    Return False if running remotely on the Prefect server, True otherwise.

    So far, the only known way to determine this is by looking at the local hostname.  If running on the prefect
    server, the local hostname will look like:
        prefect-job-b5837576-2zlhs
        prefect-job-4e5eca28-zp4t9
    """
    return "prefect" not in socket.getfqdn()


def slack_message_formatter_from_obj(
    flow,
    task,
    state: "prefect.engine.state.State",
) -> dict:
    """Return a Slack message block"""
    state_name = type(state).__name__
    # flow_name = prefect.context.get("flow_name")
    if isinstance(state.result, Exception):
        state_message = repr(state.result)
    else:
        state_message = cast(str, state.message)
    return slack_message_formatter(flow.name, task.name, state_name, state_message)


def slack_message_formatter(
    flow_name: str, task_name: str, state_name: str, state_message: str
) -> dict:
    """Return a Slack message block"""
    fields = []
    value = "```{}```".format(state_message)
    fields.append({"title": "Message", "value": value, "short": False})

    url = None
    title = state_name
    if prefect.context.get("flow_run_id") and not is_running_locally():
        url = f"http://prefect.apps.optimeering.hawkai.site/default/flow-run/{prefect.context['flow_run_id']}"
        title += " (click for logs)"
        # notification_payload.update(title_link=url)

    notification_payload = {
        "fallback": f"{flow_name} failed",
        "color": "#eb0000",
        "author_name": "Prefect",
        "author_link": "https://www.prefect.io/",
        "author_icon": "https://emoji.slack-edge.com/TAN3D79AL/prefect/2497370f58500a5a.png",
        "title": title,
        "fields": fields,
        "title_link": url,
        "text": f"_{flow_name}_: '{task_name}' is now in a {state_name} state",
        "footer": "Prefect notification",
    }

    data = {"attachments": [notification_payload]}
    return data
