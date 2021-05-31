# trashbot
trashbot is a comedy bot designed to spout inside jokes at a moment's notice, and also provide some fun games to play.

The main design principle of trashbot is being able to run as constantly as possible, but still be able to change responses frequently. trashbot relies on a [DynamoDB](https://aws.amazon.com/dynamodb/) instance to save and load its responses, so that its host doesn't need to worry about differences between cloud and local copies.

trashbot comes with very few programmed responses, permissions, and commands, other than those required to run the included modules.

## installation
1. clone the repo.
2. install requirements with ``pip install -r requirements.txt``
3. configure [awscli](https://github.com/aws/aws-cli) on your system, or equivalent AWS credentials
4. run ``main.py``
5. add yourself to the "blue" permissions tier, like this:
```
{
  "blue": {
    "[userid]": "[username]"
  }
}
```
