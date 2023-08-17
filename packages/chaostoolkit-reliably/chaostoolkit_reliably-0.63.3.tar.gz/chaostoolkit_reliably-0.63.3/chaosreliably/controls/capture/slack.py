import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, cast

from chaoslib.types import Configuration, Experiment, Secrets
from logzero import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from chaosreliably.controls.capture import get_control_by_name

__all__ = ["start_capturing", "stop_capturing"]


def start_capturing(
    experiment: Experiment, configuration: Configuration, secrets: Secrets
) -> None:
    pass


def stop_capturing(
    experiment: Experiment, configuration: Configuration, secrets: Secrets
) -> Optional[Dict[str, Any]]:
    ctrl = get_control_by_name(experiment, "slack")
    if not ctrl:
        logger.debug("No slack integration configured, nothing to capture")
        return None

    args = ctrl["provider"]["arguments"]

    channel = args["channel"]
    limit = args.get("limit", 100)
    past = args.get("past", 15)
    include_metadata = True

    logger.debug(f"Capture Slack messages from {channel}")

    return get_channel_history(channel, limit, past, include_metadata, secrets)


###############################################################################
# Private functions
###############################################################################
def get_client(secrets: Secrets) -> WebClient:
    secrets = secrets or {}
    slack_token = secrets.get("slack", {}).get(
        "token", os.getenv("SLACK_BOT_TOKEN")
    )
    client = WebClient(token=slack_token)
    return client


def get_channel_id(client: WebClient, channel: str) -> Optional[str]:
    channel = channel.lstrip("#")

    result = client.conversations_list()

    for c in result["channels"]:
        if c["name"] == channel:
            return cast(str, c["id"])

    return None


def get_channel_history(
    channel: str,
    limit: int = 100,
    past: int = 15,
    include_metadata: bool = False,
    secrets: Secrets = None,
) -> Optional[Dict[str, Any]]:
    """
    Fetches the history of a channel up to a certain limit of messages or
    for the past minutes.

    By default no more than 100 messages in the last 15 minutes.
    """
    messages = []

    oldest = datetime.now().astimezone(tz=timezone.utc) - timedelta(
        minutes=past
    )
    ts = oldest.timestamp()

    try:
        client = get_client(secrets)
        channel_id = get_channel_id(client, channel)
        if not channel_id:
            logger.debug("Missing channel to initiate slack capture")
            return None

        logger.debug(
            f"Fetching the last {limit} messages for the past {past}mn "
            f"[{oldest}] from channel {channel} [{channel_id}]"
        )
        result = client.conversations_history(
            channel=channel_id,
            inclusive=True,
            limit=limit,
            include_metadata=include_metadata,
            oldest=ts,
        )
        messages.extend(result["messages"])

        while (result["ok"] is True) and (result["has_more"] is True):
            cursor = result["response_metadata"]["next_cursor"]
            result = client.conversations_history(
                channel=channel_id,
                cursor=cursor,
                inclusive=True,
                limit=limit,
                include_metadata=include_metadata,
                oldest=ts,
            )

            messages.extend(result["messages"])

    except SlackApiError as e:
        logger.error(f"Failed to retrieve Slack channel history: {e}")

    # collect user information
    users = {}
    threads = {}
    for m in messages:
        if m.get("bot_id") is not None:
            continue

        user_id = m.get("user")
        if not user_id:
            continue

        if user_id not in users:
            users[user_id] = get_user_info(client, user_id)

        thread_ts = m.get("thread_ts")
        if thread_ts:
            threads[thread_ts] = get_thread_history(
                client,
                channel_id,  # type: ignore
                thread_ts,
                limit,
                include_metadata,
            )

    context = {
        "conversation": messages,
        "users": users,
        "threads": threads,
    }

    return context


def get_user_info(client: WebClient, user_id: str) -> Dict[str, str]:
    result = client.users_info(
        user=user_id,
    )

    u = result["user"]

    return {
        "id": u["id"],
        "name": u["name"],
        "real_name": u["real_name"],
        "display_name": u["profile"]["display_name_normalized"],
        "image": u["profile"]["image_24"],
    }


def get_thread_history(
    client: WebClient,
    channel_id: str,
    thread_ts: float,
    limit: int = 100,
    include_metadata: bool = False,
) -> List[Dict[str, Any]]:
    messages = []
    try:
        result = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts,
            inclusive=True,
            limit=100,
            include_metadata=include_metadata,
        )
        messages.extend(result["messages"])

        while (result["ok"] is True) and (result["has_more"] is True):
            cursor = result["response_metadata"]["next_cursor"]
            result = client.conversations_replies(
                channel=channel_id,
                ts=thread_ts,
                cursor=cursor,
                inclusive=True,
                limit=limit,
                include_metadata=include_metadata,
            )

            messages.extend(result["messages"])

    except SlackApiError as e:
        logger.error(f"Failed to retrieve Slack thread history: {e}")

    return messages
