import com.vdurmont.emoji.EmojiParser;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.server.Server;
import org.javacord.api.entity.user.User;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.List;

public class helperFunctions {
    private static final Logger logger = LogManager.getLogger(EmojiReactions.class);

    // From "<:emojiName:emojiID>", returns just emojiName
    static String name(String message) {
        String emojiName = "";
        try {
            int emojiStart = message.indexOf(":");
            String tempMessage = message.substring(emojiStart+1);
            int emojiEnd = tempMessage.indexOf(":");
            emojiName = tempMessage.substring(0, emojiEnd);
        } catch (StringIndexOutOfBoundsException e) {
            logger.warn("Emoji not found in message: " + message);
        }
        return emojiName;
    }

    // From "<:emojiName:emojiID>", returns just emojiID
    static String id(String message) {
        String fullEmoji = getFullEmoji(message);

        int indexOfFirstColon = fullEmoji.indexOf(":");
        String emojiNameWithId = fullEmoji.substring(indexOfFirstColon+1);
        int indexOfSecondColon = emojiNameWithId.indexOf(":");
        int indexOfEndBracket = emojiNameWithId.indexOf(">");

        return emojiNameWithId.substring(indexOfSecondColon + 1, indexOfEndBracket);
    }

    // Parses out the first custom emoji in a message and returns "<:emojiName:emojiID>"
    // if there are no custom emojis in the message, return the first unicode emoji.
    static String getFullEmoji(String message) {
        String fullEmoji = "";
        int emojiStart = message.indexOf("<:");
        int emojiEnd = message.indexOf(">");
        if (emojiStart < 0 || emojiEnd < 0) {
            List<String> emojis = EmojiParser.extractEmojis(message);
            if (!emojis.isEmpty()) {
                fullEmoji = emojis.get(0);
            }
        } else {
            fullEmoji = message.substring(emojiStart, emojiEnd + 1);
        }

        if (fullEmoji.equals("")) {
            logger.warn("No emoji found in message:" + message);
        }

        return fullEmoji;
    }

    static long getFirstMentionID(Message message) {
        List<User> mentions = message.getMentionedUsers();
        User firstMention = mentions.get(0);
        return firstMention.getId();
    }

    static String getFirstMentionName(Message message) {
        List<User> mentions = message.getMentionedUsers();
        User firstMention = mentions.get(0);
        return firstMention.getName();
    }

    static String pickString(String... set) {
        int rand = (int)(Math.random()*(set.length));
        return set[rand];
    }

    static String pickString(ArrayList<String> set) {
        int rand = (int)(Math.random() * (set.size()));
        return set.get(rand);
    }

    static TextChannel getGeneralChannel(Server server) {
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
            logger.error("A general channel was searched for in " + server.getName() + " but no suitable channel was found.");
        }
        return channel;
    }

    // Method that pauses the bot for 1 second
    static void botWait() {
        try {
            Thread.sleep(1500);
        } catch (InterruptedException e) {
            logger.error("Call to botWait threw " + e);
        }
    }

    static void botWaitLong() {
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            logger.error("Call to botWaitLong threw " + e);
        }
    }

    static void botWaitShort() {
        try {
            Thread.sleep(300);
        } catch (InterruptedException e) {
            logger.error("Call to botWaitShort threw " + e);
        }
    }
}
