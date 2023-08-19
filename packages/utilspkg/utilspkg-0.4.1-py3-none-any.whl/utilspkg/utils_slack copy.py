# Modifying the provided Slack utility
import os
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from utilspkg import utils_init

# allows local testing of functions
if __name__ == '__main__':
    utils_init.load_env_variables_from_yaml('/Users/croft/VScode/ptagit/env_vars.yaml')

logger = utils_init.setup_logger(__name__)

SLACK_API_KEY = os.environ["SLACK_ACCESS_TOKEN_TEAM"]
TESTING_DM = os.environ["TESTING_DM"]
TESTING_CHANNEL = os.environ["TESTING_CHANNEL"]  # not currently used since all goes to the DM's "channel"


class SlackConnect:
    """
    A utility class for sending messages and fetching conversation history from Slack.
    """

    def __init__(self, api_key=SLACK_API_KEY, testing_flag=False, logger=None):
        """
        Initialize the SlackSender with an API key, testing flag, and optional logger.
        """
        self.api_key = api_key
        self.slack_client = WebClient(token=self.api_key)
        self.logger = logger if logger else logging.getLogger(__name__)
        self.testing_flag = testing_flag
        self.testing_dm_or_channel = TESTING_DM

    def make_slack_api_call(self, api_function, **kwargs):
        """
        A generic function to make Slack API calls with error handling and rate limiting.
        """
        while True:
            try:
                response = api_function(**kwargs)
                return response
            except SlackApiError as e:
                if e.response["error"] == "ratelimited":
                    delay = int(e.response.headers.get('Retry-After'))
                    time.sleep(delay)
                else:
                    self.logger.error(f"Error making Slack API call: {e}")
                    return None

    def send_dm_or_channel_message(self, channel_or_slack_id, message, thread_ts=None, testing_flag=None):
        """
        Send a message to the given channel or user (by Slack ID) through Direct Message.
        Optionally, reply to a threaded message by providing a thread timestamp.
        """
        if testing_flag is None:
            testing_flag = self.testing_flag

        channel_or_slack_id = channel_or_slack_id if not testing_flag else self.testing_dm_or_channel

        if channel_or_slack_id.startswith("U"):  # check if it's a user ID
            dm = self.make_slack_api_call(self.slack_client.conversations_open, users=channel_or_slack_id)
            channel_or_slack_id = dm['channel']['id']

        self.make_slack_api_call(
            self.slack_client.chat_postMessage,
            channel=channel_or_slack_id,
            text=message,
            thread_ts=thread_ts
        )

    def get_conversation_history(self, channel_id, oldest_timestamp=None, newest_timestamp=None):
        """
        Fetch messages from the specified Slack channel.
        Optionally, filter the messages by providing the oldest and/or newest timestamp.
        Handles pagination and rate limits.
        """

        messages = []
        next_cursor = None

        while True:
            # Build kwargs dict based on parameters
            kwargs = {
                "channel": channel_id,
                "inclusive": False,
                "limit": 100,  # Get maximum number of messages per API call
                "cursor": next_cursor,
            }

            # Only add timestamp parameters if they are not None
            if oldest_timestamp:
                kwargs["oldest"] = oldest_timestamp
            if newest_timestamp:
                kwargs["latest"] = newest_timestamp

            # Request the conversation history
            response = self.make_slack_api_call(self.slack_client.conversations_history, **kwargs)
            if not response:
                break

            messages += response.data.get('messages')

            # Check if more messages are available
            next_cursor = response.data.get('response_metadata', {}).get('next_cursor')
            if not next_cursor:
                break

            # Pause before next API call to avoid hitting rate limits
            time.sleep(1)


if __name__ == '__main__':
    slack = SlackConnect()
    channels = slack.get_list_of_channels()
    print(len(channels))
