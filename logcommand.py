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
        if self.logLevels[level]:
            self.log.append(logging.getLevelName(level) + ": " + message)
            if len(self.log) > LOG_ENTRIES_NUM:
                self.log.pop(0)

    def __init__(self):
        self.log = []
        self.logLevels = {logging.INFO: True, logging.WARNING: False, logging.DEBUG: False, logging.ERROR: True, logging.FEED: True}

globalLog = Log()
channelLogs = {}

def log_channel(level, message, channel):
    if channel in channelLogs:
        log = channelLogs[channel]
    else:
        log = Log()
        channelLogs[channel] = log
    log.log_message(level, message)


def log_globally(level, message):
    globalLog.log_message(level, message)


async def print_log(log, channel):
    string = "\n".join(log.log)
    await channel.send(string[-2000:] if len(string) != 0 else "Log is empty sorry")
