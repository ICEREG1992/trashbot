# trashbot
trashbot is a comedy bot designed to spout inside jokes at a moment's notice, and also provide some fun games to play.

The main design principle of trashbot is being able to run as constantly as possible, but still be able to change responses frequently. trashbot relies on a [DynamoDB](https://aws.amazon.com/dynamodb/) instance to save and load its responses, so that its host doesn't need to worry about differences between cloud and local copies.

trashbot comes with very few programmed responses, permissions, and commands, other than those required to run the included modules.

## included modules

### permissions
Since trashbot can be heavily modified at runtime, some access control is needed to keep him free of bad actors. The Keycard system implemented does just that, and is scalable to your needs if you decide to fork trashbot. Currently, the only keycard colors in use are Blue (admin), Red (trusted), and Black (banned). By importing the permissions class and calling ``permissions.allowed(id, *colors)``, you can check any user's message for any arbitrarily named keycard color.

Any Blue keycard user can give or revoke keycards using the commands ``!give [color] keycard [@mention]`` or ``!revoke [color] keycard [@mention]`` respectively. Any user can see who has what color keycard by sending the command ``!keycard [color]``, or what keycards a user has by mentioning a user, like ``!keycard [@mention]``.

### instant humor
The instant humor modules (contains and equals) allow for the quick implementation of indiscriminant responses to phrases or words. As the names imply, the humor_contains module will respond to any message which contains one of the user-defined keywords with a randomly selected user-defined resposne for that keyword. The humor_equals module does the same thing, except only if the message matches exactly to one of the keywords, with no extra characters.

instant humor also supports a limited list of escape characters, which can be used to inject info about the triggerer into the response. Use them like any other escape sequence. ``$u`` injects the users username, ``$n`` does the same with nickname. ``$m`` injects a ping for the first user the triggerer mentioned, and ``$ms`` just injects the mentioned user's nickname (mention silent).

Blue keycard holders can add a new keyword by sending ``!containsadd [keyword] § [response]`` or ``!equalsadd [keyword] § [response]`` anywhere in a trashbot-joined server. Entire keywords can be removed (but not individual responses) with the commands ``!containsremove [keyword]`` or ``!equalsremove [keyword]``.

### karaoke
The karaoke module allows you to screamtype your favorite songs along with trashbot. Using an extremely flexible word-matching system, trashbot will know if you stop in the middle of a line, do multiple lines at once, hooooooolddd yourrrrr wooooooordsssss likee ethisssssss, or accidentally flub a few words, and the song will go on like nothing happened. trashbot will also match!!! your!!! excitement!!! or even go into ALL CAPS IF YOU DO!!!

Any user can start a karaoke for a channel by sending the ``!karaoke`` command, which will pull from the currently saved lyrics set. To change lyrics, a Red or Blue keycard holder can send the ``!givelyrics [lyrics]`` command, where ``[lyrics]`` is any set of lyrics broken up with each bar on its own line. Any user can exit karaoke mode prematurely by saying ``!exit``, ``!quit``, or ``!stop``.

### logging
Since trashbot is built to be run on Heroku, with storage in DynamoDB, it can be tough to tell exactly what's going on without some logging. Trashbot will store its own logs and print them to any channel upon request by a Blue keycard holder. When creating your own modules for trashbot, you can create new logs by importing ``logcommand, logging`` and using ``logcommand.log_globally([log level], [msg])``.

For more information on logging commands, a Blue keycard holder can send ``!log help`` to any trashbot-joined channel.

### todo
Notice a bug of yours? Make a note of it so you can get to fixing it later.

Any user can send the ``!todo`` command to view the todo list. Any Blue or Red keycard holder can send ``!todo [msg]`` to a trashbot-joined channel to add an item to the todo list. Any Blue keycard holder can send ``!todoclear [number]`` to wipe a particular item off the todo list.

### spam train
Channel found a new funny thing to spam? trashbot will eagerly hop on that train. After three completely similar messages, trashbot will send the same exact thing to the channel, joining in. From then on, each message that remains the same will have a small chance of trashbot jumping in again to say it.

### wordplay
Reward clever usages of words by having trashbot give a response when you hide a particular word within another in a unique way! In example, if "Ian" is a keyword, then "variant" would trigger a response, but only once! Admittedly a niche feature, but this bot's for me not for you. Add a new wordplay keyword with ``!wordplayadd [keyword] § [response]`` and remove the keyword with ``!wordplayremove [keyword]``.

### mcplayers
Running a Minecraft server and want a quick way to check if anybody's on? Trashbot can help you out. The pinged server can be set through environment variables or a text file as defined below. Trigger a check with ``!whosuprn``.

## installation

### initialization

1. clone the repo.
2. install requirements with ``pip install -r requirements.txt``
3. configure [awscli](https://github.com/aws/aws-cli) on your system, or equivalent AWS credentials
4. run ``main.py``, which will initialize the ``trashbot`` table in DynamoDB
5. add yourself to the "blue" permissions tier using the AWS dashboard, like this:
```
{
  "blue": {
    "[userid]": "[username]"
  }
}
```

### environment variables

In order to function, trashbot needs a Discord bot API token and an AWS programmatic access token. When running locally, the Discord API token can be stored in the main-level directory as ``key.txt``. Alternatively, it can be stored as an environment varibale named ``TRASHBOT_KEY``. The AWS token (consisting of a key ID and secret access key) can be received by configuring [awscli](https://github.com/aws/aws-cli) on your machine or, if you're on [Heroku](https://www.heroku.com), setting config vars ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` to their appropriate values. The Minecraft server pinged by mcplayers can be set through the variable ``MC_IP`` or by a file named ``ip.txt``.