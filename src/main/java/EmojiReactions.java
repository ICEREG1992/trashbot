import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class EmojiReactions {
    private Map<String, ArrayList<String>> emojisAndKeywords = new HashMap<>();
    private File file;
    private AccessRestriction permissions;
    private static final Logger logger = LogManager.getLogger(EmojiReactions.class);

    private static ArrayList<Character> acceptableCharacters = new ArrayList<>();
    static {
        final char[] tempCharacters = {' ', '?', ',', '.', '!', '\'', '\"', ':', ';', '…', '*', '_', '/', '~', '`', '-'};
        for (char c: tempCharacters) {
            acceptableCharacters.add(c);
        }
    }

    EmojiReactions(String filename, AccessRestriction permissions) {
        this.file = new File(filename);
        this.permissions = permissions;
        prepareEmojiReactions();
    }

    public void run(MessageCreateEvent event, DiscordApi api) {
        addReactionsToMessages(event, api);
        checkForEmojiReactionCommands(event);
    }

    // Adds a reaction to a message
    private void addReactionsToMessages(MessageCreateEvent event, DiscordApi api) {
        // Parse message here so you don't have to later
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        for (String emoji: emojisAndKeywords.keySet()) {
            for (String keyword: emojisAndKeywords.get(emoji)) {
                if (keyword.contains("§")) {
                    keyword = keyword.substring(1);
                    if (containsExclusively(messageToString, keyword)) {
                        if (api.getCustomEmojiById(helperFunctions.id(emoji)).isPresent()) {
                            message.addReaction(api.getCustomEmojiById(helperFunctions.id(emoji)).get());
                        } else {
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

    2) Add a case to the switch case where the case is the name that you want to call the command

    3) Add the command name to the ArrayList command names right here: ----------------------
     */
    private void checkForEmojiReactionCommands(MessageCreateEvent event) {
        // Parse message here so you don't have to later
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();
        String out = "";
        ArrayList<String> commandNames = new ArrayList<>();
        commandNames.add("!keywords");
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

                    case "!printall":
                        out = printAllKeywords(event, permissions);
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
    private String getKeywords(org.javacord.api.entity.message.Message message) {
        // Parse message here so you don't have to later
        String messageToString = message.getContent().toLowerCase();
        String messageEmoji = helperFunctions.getFullEmoji(messageToString);
        boolean halfEmoji = false;
        if (messageEmoji.isEmpty()) {
            halfEmoji = true;
        }
        StringBuilder outString = new StringBuilder();
        outString.append("__Keywords for ").append(messageEmoji).append(":__");

        for (String emoji: emojisAndKeywords.keySet()) {
            String checkEmoji = emoji;
            if (halfEmoji) {
                checkEmoji = helperFunctions.name(emoji);
            }
            if(checkEmoji.equals(messageEmoji)) {

                for (String keyword: emojisAndKeywords.get(emoji)) {
                    if (keyword.contains("§")) {
                        keyword = keyword.substring(1);
                    }
                    outString.append("\n").append(keyword);
                }
            }
        }
        outString.append("\n");
        return outString.toString();
    }

    // Adds a keyword to an emoji when the !add command is called.
    // Proper use:  !add keyword \<:customemoji:123456789012345678>
    private String addKeyword(MessageCreateEvent event, AccessRestriction permissions) {
        // Parse message here so you don't have to later
        String message = event.getMessage().getContent();
        String userID = event.getMessage().getAuthor().getIdAsString();

        if(permissions.doesUserHaveAccess(userID, "blue")) {
            String fullEmoji = helperFunctions.getFullEmoji(message);

            int keywordStart = message.indexOf("!add") + 5;
            int keywordEnd = message.indexOf(fullEmoji) - 1;
            boolean exclusive = false;
            if (message.charAt(message.length()-1) == 'e') {
                exclusive = true;
            }

            if (!emojisAndKeywords.containsKey(fullEmoji)) {
                ArrayList<String> tempAddArray = new ArrayList<>();
                emojisAndKeywords.put(fullEmoji, tempAddArray);
                logger.info("New Emoji Added: " + fullEmoji);
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

            String out = newKeyWord + " was added as a keyword for " + fullEmoji;
            logger.info(out);
            return out;
        } else {
            return "You need the blue keycard to use that command.";
        }
    }

    // Removes a keyword from a certain reaction emoji.
    // Proper use:  !remove keyword <:customemoji:123456789012345678>
    private String removeKeyword(MessageCreateEvent event, AccessRestriction permissions) {
        String message = event.getMessage().getContent();
        String userID = event.getMessage().getAuthor().getIdAsString();

        if(permissions.doesUserHaveAccess(userID, "blue")) {
            String fullEmoji = helperFunctions.getFullEmoji(message);

            int keywordStart = message.indexOf("!add") + 9;
            int keywordEnd = message.indexOf(fullEmoji) - 1;

            String oldKeyWord = message.substring(keywordStart, keywordEnd);

            emojisAndKeywords.get(fullEmoji).remove(oldKeyWord);
            emojisAndKeywords.get(fullEmoji).remove("§" + oldKeyWord);
            if (emojisAndKeywords.get(fullEmoji).isEmpty()) {
                emojisAndKeywords.remove(fullEmoji);
                logger.info("Emoji Removed -- No Keywords: " + fullEmoji);
            }
            save();
            String out = "Successfully removed " + oldKeyWord + " as a keyword for \\" + fullEmoji;
            logger.info(out);
            return out;
        } else {
            return "You need the blue keycard to use that command.";
        }
    }

    private String printAllKeywords(MessageCreateEvent event, AccessRestriction permissions) {
        String userID = event.getMessage().getAuthor().getIdAsString();
        StringBuilder outString = new StringBuilder();
        outString.append("**Here ya go, bud.**\n\n");
        if (permissions.doesUserHaveAccess(userID, "blue")) {
            for (String key : emojisAndKeywords.keySet()) {
                outString.append("__").append(key).append("__\n");
                for (String emoji : emojisAndKeywords.get(key)) {
                    outString.append(emoji).append("\n");
                }
            }
            outString.append("\n\n");
        } else {
            outString = new StringBuilder("You need the blue keycard to use that command.");
        }
        return outString.toString();
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
    private void prepareEmojiReactions() {
        ArrayList<String> keywords;
        Scanner in = null;
        try {
            in = new Scanner(file, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            logger.error("EmojiReactions was unable to locate the file " + e);
        }

        if (in != null) {
            try {
                String keyword;
                String emoji = in.nextLine();
                do {
                    keywords = new ArrayList<>();
                    keyword = in.nextLine();
                    while (!keyword.equals("")) {
                        keywords.add(keyword);
                        keyword = in.nextLine();
                    }
                    emojisAndKeywords.put(emoji, keywords);
                    emoji = in.nextLine();
                } while (!emoji.equals("***"));
                logger.info("Emojis and keywords successfully loaded.");
            } catch (NoSuchElementException e) {
                logger.error("Incorrect formatting in " + this.file.getName() + ", correctly formatted entries have been loaded.");
            }
            in.close();
        }
    }

    // Saves all changes made to the emojiReactions keywords and such.
    private void save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8));
        } catch (FileNotFoundException e) {
            logger.error("File " + file + " not found: ");
        }
        if (out != null) {
            for (String emoji : emojisAndKeywords.keySet()) {
                out.println(emoji);
                for (String keyword : emojisAndKeywords.get(emoji)) {
                    out.println(keyword);
                }
                out.println();
            }
            out.println("***");
            out.close();
        }
    }
}
