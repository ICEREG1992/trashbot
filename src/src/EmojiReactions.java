import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

/*
------------------------------------------------------------------------------------------------------------------------
README: HOW TO ADD A NEW EMOJI THAT REACTS TO A MESSAGE
------------------------------------------------------------------------------------------------------------------------

There is currently 1 way to add a new emoji to the current list of emoji reactions. To demonstrate, an example of
a custom emoji with the following properties will be added:

Emoji: <:customemoji:123456789012345678>
Keywords that we would like to trigger the Emoji: ["hi", "hello", "how are you", "what's your favorite color?"]


METHOD:
-----------------------
1) Access the file that the emojiReadtion data is currently kept in.


2) In the file, you will see data that looks something like this:

   money
   cash
   $
   dollar
   pay
   currency
   cheddar
   dough
   moolah
   €
   cent
   bank
   dosh
   check
   ¥
   dinero
   oh yeah mr krabs

   <:mrkrabs:451793501470982155>
   ***


3) To add to this list, insert the information 2 lines after the last emoji, but keep the "***" at the end of the file.

   money
   cash
   $
   dollar
   pay
   currency
   cheddar
   dough
   moolah
   €
   cent
   bank
   dosh
   check
   ¥
   dinero
   oh yeah mr krabs

   <:mrkrabs:451793501470982155>

   hi
   hello
   How are you
   what's your favorite color?

   <:customemoji:123456789012345678>
   ***


4) Finished. The new emoji <:customemoji:123456789012345678> will now be added as a reaction to any message containing
   the keywords "hi", "hello", "how are you", and "what's your favorite color".

 */

public class EmojiReactions {
    private static Map<ArrayList<String>, String> emojisAndKeywords = new HashMap<>();
    private static File file = null;
    private static AccessRestriction permissions = null;

    public EmojiReactions(String filename) {
        this.file = new File(filename);
    }

    public void run(MessageCreateEvent event, DiscordApi api, AccessRestriction permissions) {
        this.permissions = permissions;
        addReactionsToMessages(event, api);
        checkForEmojiReactionCommands(event, api);
    }

    // Adds a reaction to a message
    public static void addReactionsToMessages(MessageCreateEvent event, DiscordApi api) {
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        for (ArrayList<String> keywords: emojisAndKeywords.keySet()) {
            for (String keyword: keywords) {
                if (messageToString.contains(keyword)) {
                    message.addReaction(api.getCustomEmojiById(EmojiParser.id(emojisAndKeywords.get(keywords))).get());
                }
            }
        }
    }

    /*--------------------------------------EmojiReactions Commands----------------------------------------*/

    // Calls all the different command functions. Each command function returns a String of what the output of Trashbot
    // Should be.

    /*
    README: HOW TO ADD A NEW COMMAND

    METHOD
    -----------------------
    1) Write a function for what you would like the command to do that returns a String. In the command, a parameter event of type
       MessageCreateEvent should be passed, as well as a parameter for the access level one must have in order to be
       able to use the command. Ex:

       private static String newCommand(MessageCreateEvent event, Access Restriction permissions) {

            Your code here

            return "What you want the bot to put in the chat after the command has run";
       }


       private static String

    2) Add a case to the switch case where the case is the name that you want to call the command

    3) Add the command name to the ArrayList command names right here: ------------------------------------
     */                                                                                                 //|
                                                                                                        //|
    private static void checkForEmojiReactionCommands(MessageCreateEvent event, DiscordApi api) {       //|
        TextChannel channel = event.getChannel();                                                       //|
        org.javacord.api.entity.message.Message message = event.getMessage();                           //|
        String messageToString = message.getContent().toLowerCase();                                    //|
                                                                                                        //|
        String out = "";                                                                                //|
        ArrayList<String> commandNames = new ArrayList<>();                                             //|
        commandNames.add("!emojiReactionKeywords"); //<----------------------------------------------------
        commandNames.add("!add");

        for (String command: commandNames) {
            if (messageToString.contains(command)) {
                switch (command) {
                    case "!emojiReactionKeywords":
                        out = getKeywords(event);
                        break;

                    case "!add":
                        out = addKeyword(event, permissions);
                        break;

                    case "!remove":
                        out = removeKeyword(event, permissions);

                    default:
                        out = "Command not recognized.";
                        break;
                }
            }
        }
        channel.sendMessage(out);
    }

    // Gets the keywords for an emoji
    private static String getKeywords(MessageCreateEvent event) {
        String message = event.getMessage().getContent();
        String fullEmoji = EmojiParser.getFullEmoji(message);
        String out = "Keywords for \\" + fullEmoji;

        String emojiID = EmojiParser.id(fullEmoji);
        for (ArrayList<String> keywords: emojisAndKeywords.keySet()) {
            if(emojisAndKeywords.get(keywords).equals(emojiID)) {
                for (String keyword: keywords) {
                    out += "\n" + keyword;
                }
            }
        }

        return out + "\n";
    }

    // Adds a keyword to an emoji when the !add command is called.
    // Proper use:  !add keyword \<:customemoji:123456789012345678>
    private static String addKeyword(MessageCreateEvent event, AccessRestriction permissions) {
        String message = event.getMessage().getContent();
        String userID = event.getMessage().getAuthor().getIdAsString();


        if(permissions.doesUserHaveAccess(userID, "blue")) {
            String fullEmoji = EmojiParser.getFullEmoji(message);
            String emojiID = EmojiParser.id(fullEmoji);

            int keywordStart = message.indexOf("!add") + 5;
            int keywordEnd = message.indexOf("\\") - 2;

            String newKeyWord = message.substring(keywordStart, keywordEnd);

            ArrayList<String> keywordsForThisEmoji = new ArrayList<>();

            for (ArrayList<String> keywords: emojisAndKeywords.keySet()) {
                if(emojisAndKeywords.get(keywords).equals(emojiID)) {
                    keywordsForThisEmoji = keywords;
                }
            }

            keywordsForThisEmoji.add(newKeyWord);

            return newKeyWord + " was added as a keyword for \\" + fullEmoji;
        } else {
            return "You don't have the necessary permissions to use this command.";
        }
    }

    // Removes a keyword from a certain reaction emoji.
    // Proper use:  !remove keyword <:customemoji:123456789012345678>
    private static String removeKeyword(MessageCreateEvent event, AccessRestriction permissions) {
        String message = event.getMessage().getContent();
        String userID = event.getMessage().getAuthor().getIdAsString();

        if(permissions.doesUserHaveAccess(userID, "blue")) {
            int keywordStart = message.indexOf("!remove") + 5;
            int keywordEnd = message.indexOf("\\") - 2;

            String oldKeyword = message.substring(keywordStart, keywordEnd);
            String fullEmoji = EmojiParser.getFullEmoji(message);

            ArrayList<String> keywordsForThisEmoji = new ArrayList<>();

            for (ArrayList<String> keywords: emojisAndKeywords.keySet()) {
                if(fullEmoji.equals(emojisAndKeywords.get(keywords))) {
                    keywordsForThisEmoji = keywords;
                }
            }

            keywordsForThisEmoji.remove(oldKeyword);

            return "Successfully removed " + oldKeyword + " as a keyword for \\" + fullEmoji;
        } else {
            return "You do not have the permissions required to use this command.";
        }
    }

/*------------------------------------------Data Manipulation Functions-------------------------------------------*/

    // Reads in all current emoji data
    public static void prepareEmojiReactions() {
        ArrayList<String> keys = new ArrayList<>();
        String isMoreData = "";
        Scanner in = null;
        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("EmojiReactions was unable to locate the file: " + e);
        }

        do {
            String key = in.nextLine();
            String value = "";
            keys.clear();
            do {
                keys.add(key);
                key = in.nextLine();
            } while (!key.equals(""));
            value = in.nextLine();
            emojisAndKeywords.put(keys,value);
            isMoreData = in.nextLine();
        } while (!isMoreData.equals("***"));
    }

    // TODO: Finish the save() method
    // Saves all changes made to the emojiReactions keywords and such.
    public static String save() {

        return "New EmojiReaction data successfully saved.";
    }
}
