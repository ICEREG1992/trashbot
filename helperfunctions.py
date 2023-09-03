from os import read
import random
import time
import boto3
import logging
import re

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

def humor_escape(msg, text, match=None):
    text = text.replace("$u", msg.author.name)

    if match:
        for i in range(len(match.groups())):
            text = text.replace("$" + str(i+1), match[i+1])
    
    if (' ' in msg.content):
        text = text.replace("$pc", msg.content[msg.content.index(' '):])

    if hasattr(msg.author, 'nick') and msg.author.nick is not None:
        text = text.replace("$n", msg.author.nick)
    else:
        text = text.replace("$n", msg.author.name)

    if len(msg.mentions) > 0 and hasattr(msg.mentions[0], 'nick') and msg.mentions[0].nick is not None:
        text = text.replace("$ms", msg.mentions[0].nick)
    elif len(msg.mentions) > 0:
        text = text.replace("$ms", msg.mentions[0].name)
    else:
        text = text.replace("$ms", "Trashbot")

    if len(msg.mentions) > 0:
        text = text.replace("$m", msg.mentions[0].mention)
    else:
        text = text.replace("$m", "<@450507364768940034>")
    
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
    keynames = ["contains_phrases", "equals_phrases", "regex_phrases", "hunger", "lyrics", "mc_ip", "permissions", "uptime", "todo", "wordplay_keywords", "on", "lipo"]
    defaults = ["{}", "{}", "{}", "0", "•", "", "{}", "0", "[]", "{}", "True", "{}"]
    for i in range(len(keynames)):
        n = db.get_item(TableName="trashbot", Key={'name':{'S':keynames[i]}})
        if ('Item' not in n):
            logging.info("No " + keynames[i] + " value found, set to default.")
            db.put_item(TableName="trashbot", Item={'name':{'S':keynames[i]}, 'data':{'S':defaults[i]}})