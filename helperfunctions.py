from os import read
import random
import time
import boto3
import logging

logging.basicConfig(level=logging.INFO)

def pick_string(set):
    return random.choice(set)

def bot_wait():
    time.sleep(1.5)

def bot_wait_long():
    time.sleep(3)

def bot_wait_short():
    time.sleep(.3)

def chance(rate):
    return random.uniform(0,100) < rate

def humor_escape(msg, text):
    text.replace("$u", msg.author.name)
    if hasattr(msg.author, 'nick'):
        text.replace("$n", msg.author.nick)
    if len(msg.mentions) > 0:
        text.replace("$m", msg.mentions[0].mention)
    if len(msg.mentions) > 0 and hasattr(msg.mentions[0], 'nick'):
        text.replace("$ms", msg.mentions[0].nick)
    return text

def ensure_table():
    db = boto3.client('dynamodb', region_name="us-east-2")
    if "trashbot" in db.list_tables()['TableNames']:
        logging.info("Table found, verifying data...")
        fill_defaults(db)
        logging.info("Booting...")
    else:
        logging.info("No trashbot table found on your DynamoDB instance.")
        logging.info("Creating table...")
        db.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
            ],
            TableName="trashbot",
            KeySchema=[
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # wait until the table exists
        db.get_waiter('table_exists').wait(TableName='trashbot')
        logging.info("Table created! Populating with initial values.")
        fill_defaults(db)
    return db

def fill_defaults(db):
    # fill empty required values with defaults
    keynames = ["contains_phrases", "equals_phrases", "lyrics", "permissions", "uptime", "todo", "wordplay_keywords"]
    defaults = ["{}", "{}", "§", "{}", "0", "[]", "{}"]
    for i in range(len(keynames)):
        n = db.get_item(TableName="trashbot", Key={'name':{'S':keynames[i]}})
        if ('Item' not in n):
            logging.info("No " + keynames[i] + " value found, set to default.")
            db.put_item(TableName="trashbot", Item={'name':{'S':keynames[i]}, 'data':{'S':defaults[i]}})