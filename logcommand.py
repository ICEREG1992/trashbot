import logging
from permissions import permissions
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


class logging_manager:

    async def run(self, message):
        if message.content.startswith("!log "):
            if not permissions.allowed(message.author.id, "blue"):
                await message.channel.send(pick_string(["sorry bro you need a blue keycard for that",
                "no can do homie",
                "EHHHHHHHH. try again later lol",
                "hahahahahahehehehehehehahahahahhehehehaheahehahaahehehe no chance in hell bro"
                "it's the opposite of yessiree for you i call it nope-iree try gettin the blue keycard and comin back",
                "This Command Requires the Blue Keycard nd u dont have it LMFAO"]))
                return
            parts = message.content.split(" ")
            parts_len = len(parts)
            if parts[1] == "help" or parts_len == 1:
                await message.channel.send("!log <global/channel> <subcommand>\n"
                                           "Subcommands:\n"
                                           "print: Prints Log\n"
                                           "clear: Clears log\n"
                                           "levels: Displays the log levels\n"
                                           "setlevel <level name> <true/false>: Changes if the level is logged or not")
                return
            if parts_len < 3:
                await message.channel.send(pick_string(["what subcommand do you want to run?",
                "yea and do what???",
                "what do you want me to do about that",
                "howbow you tell me what u want to do"]))
                return
            if parts[1] == "channel":
                if message.channel in channelLogs:
                    cur_log = channelLogs[message.channel]
                else:
                    cur_log = Log()
                    channelLogs[message.channel] = cur_log
            elif parts[1] == "global":
                cur_log = globalLog
            else:
                await message.channel.send(pick_string(["please use channel or global",
                "you gotta say channel or global",
                "yea which one bro channel or global lol"]))
                return
            if parts[2] == "print":
                await print_log(cur_log, message.channel)
            elif parts[2] == "levels":
                levels = []
                for levelNum, logged in cur_log.logLevels.items():
                    levels.append(logging.getLevelName(levelNum) + ": " + ("logged" if logged else "not logged"))
                await message.channel.send("\n".join(levels))
                return
            elif parts[2] == "setlevel":
                if parts_len < 5:
                    await message.channel.send(pick_string(["LOL u even know what ur doin rn?",
                    "you gotta say other things to get this command to work lmfao",
                    "ok try again but next time say the level and state"]))
                    return
                level_num = logging._nameToLevel[parts[3]]
                if level_num is None:
                    await message.channel.send("thats not a level name")
                    return
                if parts[4] == "true":
                    cur_log.logLevels[level_num] = True
                elif parts[4] == "false":
                    cur_log.logLevels[level_num] = False
                else:
                    await message.channel.send("nope wrong")
                    return
                await message.channel.send("set " + parts[3] + " to " + parts[4])
            elif parts[2] == "clear":
                cur_log.log = []
                await message.channel.send("cleared log")
            else:
                await message.channel.send("invalid subcommand")
