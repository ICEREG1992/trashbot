# trashbot
trashbot is a comedy bot designed to spout inside jokes at a moment's notice, and also provide some fun games to play.

The main design principle of trashbot is being able to run as constantly as possible, but still be able to change responses frequently. trashbot relies on a [DynamoDB](https://aws.amazon.com/dynamodb/) instance to save and load its responses, so that its host doesn't need to worry about differences between cloud and local copies.

trashbot comes with very few programmed responses, permissions, and commands, other than those required to run the included modules.

## included modules

### permissions
Since trashbot can be heavily modified at runtime, some access control is needed to keep him free of bad actors. The Keycard system implemented does just that, and is scalable to your needs if you decide to fork trashbot. Currently, the only keycard colors in use are Blue (admin), Red (trusted), and Black (banned). By importing the permissions class and calling ``permissions.allowed(id, *colors)``, you can check any user's message for any arbitrarily named keycard color.

Any Blue keycard user can give or revoke keycards using the commands ``!give [color] keycard [@mention]`` or ``!revoke [color] keycard [@mention]`` respectively. Any user can see who has what color keycard by sending the command ``!keycard [color]``.

### instant humor
The instant humor modules (contains and equals) allow for the quick implementation of indiscriminant responses to phrases or words. As the names imply, the humor_contains module will respond to any message which contains one of the user-defined keywords with a randomly selected user-defined resposne for that keyword. The humor_equals module does the same thing, except only if the message matches exactly to one of the keywords, with no extra characters.

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

## installation
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
