import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.*;

public class EmojiReactions {
    private static Map<String, ArrayList<String>> emojisAndKeywords = new HashMap<>();
    private static File file = null;
    private static AccessRestriction permissions = null;

    private static ArrayList<Character> acceptableCharacters = new ArrayList<>();

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
        // Parse message here so you don't have to later
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        for (String emoji: emojisAndKeywords.keySet()) {
            for (String keyword: emojisAndKeywords.get(emoji)) {
                if (keyword.contains("§")) {
                    keyword = keyword.substring(1);
                    if (containsExclusively(messageToString, keyword)) {
                        try {
                            message.addReaction(api.getCustomEmojiById(helperFunctions.id(emoji)).get());
                        } catch (Exception e){
                            message.addReaction(emoji);
                        }
                    }
                } else if (messageToString.contains(keyword)) {
                    try {
                        message.addReaction(api.getCustomEmojiById(helperFunctions.id(emoji)).get());
                    } catch (Exception e){
                        message.addReaction(emoji);
                    }
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
        // Parse message here so you don't have to later
        TextChannel channel = event.getChannel();                                                       //|
        org.javacord.api.entity.message.Message message = event.getMessage();                           //|
        String messageToString = message.getContent().toLowerCase();                                    //|
                                                                                                        //|
        String out = "";                                                                                //|
        ArrayList<String> commandNames = new ArrayList<>();                                             //|
        commandNames.add("!keywords"); //<----------------------------------------------------
        commandNames.add("!add");
        commandNames.add("!remove");
        commandNames.add("!printall");

        for (String command: commandNames) {
            if (messageToString.startsWith(command)) {
                switch (command) {
                    case "!keywords":
                        out = getKeywords(message);
                        break;

                    case "!add":
                        out = addKeyword(event, permissions);
                        break;

                    case "!remove":
                        out = removeKeyword(event, permissions);
                        break;

                    default:
                        out = "Command not recognized."; // this line should never ever be reached
                        break;
                }
            }
        }
        channel.sendMessage(out);
    }

    // Gets the keywords for an emoji
    public static String getKeywords(org.javacord.api.entity.message.Message message) {
        // Parse message here so you don't have to later
        String messageToString = message.getContent().toLowerCase();
        String messageEmoji = helperFunctions.getFullEmoji(messageToString, true);
        boolean halfEmoji = false;
        if (messageEmoji.isEmpty()) {
            messageEmoji = helperFunctions.name(messageToString, true);
            halfEmoji = true;
        }
        String out = "__Keywords for " + messageEmoji + ":__";

        //String emojiID = helperFunctions.id(fullEmoji);
        for (String emoji: emojisAndKeywords.keySet()) {
            String checkEmoji = emoji;
            if (halfEmoji) {
                checkEmoji = helperFunctions.name(emoji, false);
            }
            if(checkEmoji.equals(messageEmoji)) {
                for (String keyword: emojisAndKeywords.get(emoji)) {
                    if (keyword.contains("§")) {
                        keyword = keyword.substring(1);
                    }
                    out += "\n" + keyword;
                }
            }
        }

        return out + "\n";
    }

    // Adds a keyword to an emoji when the !add command is called.
    // Proper use:  !add keyword \<:customemoji:123456789012345678>
    private static String addKeyword(MessageCreateEvent event, AccessRestriction permissions) {
        // Parse message here so you don't have to later
        String message = event.getMessage().getContent();
        String userID = event.getMessage().getAuthor().getIdAsString();

        if(permissions.doesUserHaveAccess(userID, "blue")) {
            String fullEmoji = helperFunctions.getFullEmoji(message, true);

            int keywordStart = message.indexOf("!add") + 5;
            int keywordEnd = message.indexOf(fullEmoji) - 1;
            boolean exclusive = false;
            if (message.charAt(message.length()-1) == 'e') {
                exclusive = true;
            }

            if (!emojisAndKeywords.containsKey(fullEmoji)) {
                ArrayList<String> tempAddArray = new ArrayList<>();
                emojisAndKeywords.put(fullEmoji, tempAddArray);
                System.out.println("New Emoji Added: " + fullEmoji);
            }

            String newKeyWord = message.substring(keywordStart, keywordEnd);

            if (exclusive) {
                newKeyWord = "§" + newKeyWord;
            }

            emojisAndKeywords.get(fullEmoji).add(newKeyWord);
            save();

            if (exclusive) {
                newKeyWord = newKeyWord.substring(1);
            }

            return newKeyWord + " was added as a keyword for \\" + fullEmoji;
        } else {
            return "You need the blue keycard to use that command.";
        }
    }

    // Removes a keyword from a certain reaction emoji.
    // Proper use:  !remove keyword <:customemoji:123456789012345678>
    private static String removeKeyword(MessageCreateEvent event, AccessRestriction permissions) {
        String message = event.getMessage().getContent();
        String userID = event.getMessage().getAuthor().getIdAsString();

        if(permissions.doesUserHaveAccess(userID, "blue")) {
            String fullEmoji = helperFunctions.getFullEmoji(message, true);

            int keywordStart = message.indexOf("!add") + 9;
            int keywordEnd = message.indexOf(fullEmoji) - 1;

            String oldKeyWord = message.substring(keywordStart, keywordEnd);

            emojisAndKeywords.get(fullEmoji).remove(oldKeyWord);
            emojisAndKeywords.get(fullEmoji).remove("§" + oldKeyWord);
            if (emojisAndKeywords.get(fullEmoji).isEmpty()) {
                emojisAndKeywords.remove(fullEmoji);
                System.out.println("Emoji Removed -- No Keywords: " + fullEmoji);
            }
            save();
            return "Successfully removed " + oldKeyWord + " as a keyword for \\" + fullEmoji;
        } else {
            return "You need the blue keycard to use that command.";
        }
    }

    private static boolean containsExclusively(String line, String word) {
        boolean contains = false;

        if (line.contains(word)) {
            if (line.indexOf(word) > 0 && line.indexOf(word)+word.length() < line.length()) {
                if (acceptableCharacters.contains(line.charAt(line.indexOf(word)-1)) && acceptableCharacters.contains(line.charAt(line.indexOf(word)+word.length()))) {
                    contains = true;
                }
            }
            else if (line.indexOf(word) == 0) {
                if (line.indexOf(word)+word.length() >= line.length()) {
                    contains = true;
                } else if (acceptableCharacters.contains(line.charAt(line.indexOf(word)+word.length()))) {
                    contains = true;
                }
            }
            else if (line.indexOf(word)+word.length() == line.length()) {
                if (acceptableCharacters.contains(line.charAt(line.indexOf(word)-1))) {
                    contains = true;
                }
            }
        }
        return contains;
    }

/*------------------------------------------Data Manipulation Functions-------------------------------------------*/

    // Reads in all current emoji data and sets up acceptableCharacters
    public static void prepareEmojiReactions() {
        ArrayList<String> keywords;
        Scanner in = null;
        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("EmojiReactions was unable to locate the file: " + e);
        }

        String keyword;
        while(in.hasNextLine()) {
            System.out.println("Line read!");
            String emoji = in.nextLine();
            do {
                keywords = new ArrayList<>();
                keyword = in.nextLine();
                while (!keyword.equals("")) {
                    keywords.add(keyword);
                    keyword = in.nextLine();
                }
                emojisAndKeywords.put(emoji, keywords);
                System.out.println("Emoji added!");
                emoji = in.nextLine();
            } while (!emoji.equals("***"));
        }

        char[] tempCharacters = {' ', '?', ',', '.', '!', '\'', '\"', ':', ';', '…', '*', '_', '/', '~', '`', '-'};
        for (char c: tempCharacters) {
            acceptableCharacters.add(c);
        }
    }

    // TODO: Finish the save() method
    // Saves all changes made to the emojiReactions keywords and such.
    public static String save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        for (String emoji : emojisAndKeywords.keySet()) {
            out.println(emoji);
            for (String keyword : emojisAndKeywords.get(emoji)) {
                out.println(keyword);
            }
            out.println();
        }
        out.println("***");
        out.close();
        return "New EmojiReaction data successfully saved.";
    }
}
