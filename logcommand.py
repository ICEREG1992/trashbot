import logging
from helperfunctions import pick_string
# sorry if this is bad

LOG_ENTRIES_NUM = 30

class Log:
    def log_message(self, level, message):
        if self.logLevels[level]:
            self.log.append(logging.getLevelName(level) + ": " + message)
            if len(self.log) > LOG_ENTRIES_NUM:
                self.log.pop(0)

    def __init__(self):
        self.log = []
        self.logLevels = {logging.INFO: True, logging.WARNING: False, logging.DEBUG: False, logging.ERROR: True}

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
    await channel.send(string if len(string) != 0 else "Log is empty sorry")
