import logging
from helperfunctions import pick_string
# sorry if this is bad

LOG_ENTRIES_NUM = 30

# Define a custom log level "FEED"
FEED_LEVEL_NUM = 21
logging.addLevelName(FEED_LEVEL_NUM, "FEED")
def feed(self, message, *args, **kwargs):
    if self.isEnabledFor(FEED_LEVEL_NUM):
        self._log(FEED_LEVEL_NUM, message, args, **kwargs)
logging.Logger.feed = feed
logging.FEED = FEED_LEVEL_NUM

class Log:
    def log_message(self, level, message):
        if self.enabled[level]:
            self.log.append(get_level_name(level) + ": " + message)
            if len(self.log) > LOG_ENTRIES_NUM:
                self.log.pop(0)

    def __init__(self):
        self.log = []
        self.enabled = {logging.INFO: True, logging.WARNING: False, logging.DEBUG: False, logging.ERROR: True, logging.FEED: True}

globalLog = Log()
levelLogs = {}

def log_globally(level, message):
    globalLog.log_message(level, message)
    if level in levelLogs:
        log = levelLogs[level]
    else:
        log = Log()
        levelLogs[level] = log
    log.log_message(level, message)
    print("logged to level " + logging.getLevelName(level) + ": " + message)


async def print_log(log, channel):
    string = "\n".join(log.log)
    await channel.send(string[-2000:] if len(string) != 0 else "Log is empty sorry")

def get_level_num(level_name):
    return logging._nameToLevel.get(level_name, None)

def get_level_name(level_num):
    return logging.getLevelName(level_num)