import java.util.jar.JarException;

public class EmojiParser {
    public static String name(String message) {
        String emojiName = "";

        String fullEmoji = getFullEmoji(message);

        int indexOfFirstColon = fullEmoji.indexOf(":");
        String emojiNameWithId = fullEmoji.substring(indexOfFirstColon);
        int indexOfSecondColon = emojiNameWithId.indexOf(":");

        emojiName = emojiNameWithId.substring(0, indexOfSecondColon);

        return emojiName;
    }

    public static String id(String message) {
        String emojiID = "";

        String fullEmoji = getFullEmoji(message);

        int indexOfFirstColon = fullEmoji.indexOf(":");
        String emojiNameWithId = fullEmoji.substring(indexOfFirstColon);
        int indexOfSecondColon = emojiNameWithId.indexOf(":");

        emojiID = emojiNameWithId.substring(indexOfSecondColon - 1);

        return emojiID;
    }

    // Parses out the first emoji in a message and returns "<:emojiName:emojiID>"
    public static String getFullEmoji(String message) {
        int emojiStart = message.indexOf("<");
        int emojiEnd = message.indexOf(">") + 1;

        String fullEmoji = "";
        if (emojiEnd == message.length()) {
            fullEmoji = message.substring(emojiStart);
        } else {
            fullEmoji = message.substring(emojiStart, emojiEnd);
        }

        return fullEmoji;
    }
}
