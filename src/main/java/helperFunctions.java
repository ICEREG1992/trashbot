import org.javacord.api.entity.channel.Channel;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.server.Server;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class helperFunctions {

    // From "<:emojiName:emojiID>", returns just emojiName
    public static String name(String message, boolean loud) {
        String emojiName = "";
        try {
            int emojiStart = message.indexOf(":");
            String tempMessage = message.substring(emojiStart+1);
            int emojiEnd = tempMessage.indexOf(":");
            emojiName = tempMessage.substring(0, emojiEnd);
        } catch (StringIndexOutOfBoundsException e) {
            if (loud) {
                System.out.println("Emoji not found in message: " + message);
            }
        }
        return emojiName;
    }

    // From "<:emojiName:emojiID>", returns just emojiID
    public static String id(String message) {
        String emojiID = "";

        String fullEmoji = getFullEmoji(message, false);

        int indexOfFirstColon = fullEmoji.indexOf(":");
        String emojiNameWithId = fullEmoji.substring(indexOfFirstColon+1);
        int indexOfSecondColon = emojiNameWithId.indexOf(":");

        emojiID = emojiNameWithId.substring(indexOfSecondColon + 1, emojiNameWithId.length()-1);
        return emojiID;
    }

    // Parses out the first emoji in a message and returns "<:emojiName:emojiID>"
    public static String getFullEmoji(String message, boolean loud) {
        String fullEmoji = "";
        try {
            int emojiStart = message.indexOf("<");
            int emojiEnd = message.indexOf(">") + 1;
            fullEmoji = message.substring(emojiStart, emojiEnd);
        } catch (StringIndexOutOfBoundsException e) {
            Pattern pattern = Pattern.compile("[\ud83c\udc00-\ud83c\udfff]|[\ud83d\udc00-\ud83d\udfff]|[\u2600-\u27ff]",
                    Pattern.UNICODE_CASE | Pattern.CASE_INSENSITIVE);
            Matcher matcher = pattern.matcher(message);
            if (matcher.find()) {
                fullEmoji = matcher.group();
            }
            else if (loud) {
                System.out.println("Emoji not found: " + fullEmoji);
            }
        }
        return fullEmoji;
    }

    public static String pickString(String... set) {
        int rand = (int)(Math.random()*(set.length-1));
        return set[rand];
    }

    public static TextChannel getGeneralChannel(Server server) {
        TextChannel channel;
        // Get a channel to send the welcome message to
        if (server.getSystemChannel().isPresent()) {
            channel = server.getSystemChannel().get();
        } else if (server.getTextChannelsByNameIgnoreCase("general").size() > 0) { // if there's no default channel for welcome messages, choose a "general" channel
            channel = server.getTextChannelsByNameIgnoreCase("general").get(0);
        } else if (server.getTextChannelsByNameIgnoreCase("off-topic").size() > 0) {
            channel = server.getTextChannelsByNameIgnoreCase("off-topic").get(0);
        } else if (server.getTextChannelsByNameIgnoreCase("casual").size() > 0) {
            channel = server.getTextChannelsByNameIgnoreCase("casual").get(0);
        } else {
            channel = null;
            System.out.println("A general channel was searched for in " + server.getName() + " but no suitable channel was found.");
        }
        return channel;
    }

    // Method that pauses the bot for 1 second
    public static void botWait() {
        try {
            Thread.sleep(1500);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }
}
