import os
from datetime import datetime, timedelta
import pytz

import json
from slack_sdk.errors import SlackApiError

# do all of my standard imports to start a script
from utilspkg import utils_init

# creates a logger
logger = utils_init.setup_logger(__name__)

# loads ENV file when running locally
if __name__ == '__main__':
    utils_init.load_env_variables_from_yaml('/Users/croft/VScode/ptagit/env_vars.yaml')

# my custom Slack, DB, GPT, etc connections file
from utilspkg import utils_connections #, utils_times

# creates instances of my Slack, DB, GPT, etc classes
db, slack, gpt = utils_connections.get_connections()

EXCLUDED_SLACK_IDS = ["U059UA4RPHB", #inna / cam 
                      "USLACKBOT", #slackbot
                      "U059UA4K953", #aron
                      "U05ALUWSL00", #kat
                      "U05A8HMUGKF", #welcome bot
                      "U059YQXHBCN" # troy 'bot' probably delete
                      , "U059X0WFVST" #troy 
                      ]

# DB Tables
tasks_table = 'Tasks'
messages_table = 'Messages' 
channels_table = 'Slack Channels'
students_table = 'Students'
slack_users_table = 'Slack Users'
all_messages_table = 'All Messages' 
profile_pic_changed_table = 'OB-ProfilePicChangedUsers'
introduction_posted_table = 'OB-IntroductionPostedUsers'
onboarding_done_table = 'OB-OnboardingDoneUsers'




def add_slack_id_to_db(user_id):
    #db, slack, gpt = utils_connections.get_connections()


    # Query Slack API to fetch user's profile data
    result = slack.slack_client.users_info(user=user_id)
    new_user = result['user']
    add_slack_user_to_db(new_user)


def add_slack_user_to_db (user):
    #db, slack, gpt = utils_connections.get_connections()


    profile = user.get('profile', {})
    email = profile.get('email', '')
    is_email_confirmed = user.get('is_email_confirmed', False)
    slack_id = user.get('id', '')
    real_name = user.get('real_name', '')
    tz_offset = user.get('tz_offset')
    tz = user.get('tz')
    raw_data = json.dumps(user)

    # Updated fields
    is_bot = user.get('is_bot', False)
    is_bot = True if slack_id in EXCLUDED_SLACK_IDS else is_bot
    custom_image = profile.get('is_custom_image', False)
    deactivated = user.get('deleted', False)

    link_to_student_table = get_student_link(email) if email else [] 

    fields = {
        'Email': email,
        'Student': link_to_student_table,
        'Confirmed Email?': is_email_confirmed,
        'Slack ID': slack_id,
        'Real Name': real_name,
        'Timezone': tz,
        'TZ Offset': tz_offset,
        'Raw Data': raw_data,
        'Ignore': is_bot,  # New field: checkbox true if user is a bot
        'Custom Profile Pic': custom_image,  # New field: checkbox true if custom image is true
        'Deactivated': deactivated,  # New field: checkbox true if "deleted" is true
    }

    # Check if record already exists
    records = db.search_table(slack_users_table, 'Slack ID', slack_id)

    if records:
        # Record exists, update the existing record
        record_id = records[0]['id']
        try:
            record = db.update_record(slack_users_table, record_id, fields)
        except Exception as e:
            print(f"Error updating record: {e}")
    else:
        # Record not found, insert new record
        try:
            record = db.insert_record(slack_users_table, fields)
        except Exception as e:
            print(f"Error inserting record: {e}")
    
    return record
    

def get_challenge_start_date(optional_date=None, optional_timezone='US/Eastern'):
    """
    Unless specified, uses NOW() and US/Eastern. Returns the MONDAY start date of the current challenge as a date-only datetime object. 
    
    Optional args: 
    - date (defaults to today)
    - timezone (defaults to US/Eastern)
    """
    # in case i accidentally override the default but send nothing
    if optional_timezone is None:
        optional_timezone='US/Eastern'

    timezone = pytz.timezone(optional_timezone)

    if optional_date is None:
        optional_date = datetime.now(timezone)

    # if its Sunday, return today's date. Otherwise, return the previous Sunday's date
    if optional_date.weekday() == 6:
        challenge_start_date = optional_date
    else:
        challenge_start_date = optional_date - timedelta(days=optional_date.weekday()+1)
    
    # adjust to the Monday (1 day later)
    challenge_start_date = challenge_start_date + timedelta(days=1)

    # return the date-only datetime object
    challenge_start_date = datetime(challenge_start_date.year, challenge_start_date.month, challenge_start_date.day)

    return challenge_start_date


def get_student_link(email):
    #db, slack, gpt = utils_connections.get_connections()

    filter_formula = f'FIND("{email}", {{Email - Search}})'

    # get BOT_ALERTS_CHANNEL from env. if not available, get TESTING_CHANNEL
    bot_alerts_channel = os.getenv("BOT_ALERTS_CHANNEL")
    if not bot_alerts_channel:
        bot_alerts_channel = os.environ["TESTING_CHANNEL"]
        if not bot_alerts_channel:
            print("BOT_ALERTS_CHANNEL not found in env variables. Please add it to your env variables or to the env_vars.yaml file.")
            # exit(1)

    # print(f"Formula in get_student_link(): {filter_formula}")
    
    student_records = db.get_records(students_table, formula=filter_formula)

    if len(student_records) == 0:
        # print(f"No student found! {email}")
        link_to_student = []
    else:
        link_to_student = [student_records[0]['id']]
        # print(f"CHALLENGER FOUND: {link_to_student}. {email}")
    
    if len(student_records) > 1:
        print(f"WARNING: Found more than one challenger with email {email}")
        message = f"WARNING: Found more than one challenger with email {email}"
        slack.send_dm_or_channel_message (bot_alerts_channel, message)

    return link_to_student




def add_message_to_db (data, table=messages_table):
    #db, slack, gpt = utils_connections.get_connections()

    
    try:
        TESTING_FLAG = os.getenv("TESTING_FLAG")
        logger.debug(f"IN 'add message to db")
        
        event = data #.get('event', {})
        
        # Check if the user is in the exclusion list or if no user exists!
        if not event.get('user'):
            print(f"SKIPPING: NO USER FOUND.")
            return None
        
        if not TESTING_FLAG and (event.get('user') in EXCLUDED_SLACK_IDS or event.get('user') == 'USLACKBOT' or event.get('bot_id')):
            print(f"SKIPPING: MESSAGE FROM EXCLUDED BOT/USER.")
            return None
        
        print(f"Processing message from {event.get('user')}...")
        
        ts = event.get('ts')
        channel = event.get('channel')
        
        print(f"checking for existing message with ts: {ts}")
        # Check if the message with the same ts already exists in the Messages table
        existing_message = db.search_table(table, 'Timestamp', ts)

        if not existing_message:
            # Find the corresponding channel and student records
            channel_records = db.search_table(channels_table, 'Channel ID', channel)
            channel_record = channel_records[0] if channel_records else None

            student_records = db.search_table(students_table, 'Slack ID', event.get('user'))
            student_record = student_records[0] if student_records else None
            student_timezone = student_record['fields'].get('Timezone',[''])[0] if student_record else None
            # Call the chat.getPermalink method using the slackclient (part of slack object)
            try:
                result = slack.slack_client.chat_getPermalink(channel=channel, message_ts=ts)
                permalink = result.get('permalink')
            except SlackApiError as e:
                permalink = ''
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                print(f"Got an error: {e.response['error']}")
            
            # set the has files veraible if files are attached
            has_files = True if event.get('files') else False

            # need to add the challenge date to the message record
            challenge_start_date = get_challenge_start_date(optional_timezone=student_timezone)
            print(f"Calculated challenge start date: {challenge_start_date}")

            # but need to take into account that messages posted in goal for the week and introduce yourself should be the following week if they are posted on Thursday or later
            if channel_record and channel_record['fields'].get('Channel Name') in ['-goal-for-the-week', '--introduce-yourself']:
                if datetime.now().weekday() >= 3:
                    challenge_start_date = challenge_start_date + timedelta(days=7)
                    print(f"Adjusted challenge start date: {challenge_start_date}")

            # formatting for airtable iso format, date only
            challenge_start_date = challenge_start_date.date().isoformat()
            # Add a new row to the Messages table
            new_message = {
                'Channel ID': channel,
                'Channel': [channel_record['id']] if channel_record else [],
                'Timestamp': ts,
                'Challenge Date': challenge_start_date,
                'Raw Data': json.dumps(event),
                'Message Link': permalink,
                'Message Text': event.get('text'),
                'Student': [student_record['id']] if student_record else [],
                'Has Files': has_files,
            }
            #print(f"Airtable array to insert: {new_message}")
            new_record = db.insert_record(table, new_message)
            # new_record_id = new_record['id']
            print("SUCCESS! Written to airtable")
            return new_record
        # if the message is already in our database, return 'true' so pub/sub acknowledges (dismisses) it
        else:
            print("SKIPPING: MESSAGE ALREADY IN OUR DATABASE!")
            return None
        
    except Exception as e:
        print(f"**utils_pta.py - write_to_airtable fx error writing to Airtable: {e}")
        raise

