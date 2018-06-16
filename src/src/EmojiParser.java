public class EmojiParser {

    // From "<:emojiName:emojiID>", returns just :emojiName:
    public static String name(String message) {
        String emojiName = "";

        String fullEmoji = getFullEmoji(message);

        int indexOfFirstColon = fullEmoji.indexOf(":");
        String emojiNameWithId = fullEmoji.substring(indexOfFirstColon);
        int indexOfSecondColon = emojiNameWithId.indexOf(":");

        emojiName = emojiNameWithId.substring(0, indexOfSecondColon+1);

        return emojiName;
    }

    // From "<:emojiName:emojiID>", returns just emojiID
    public static String id(String message) {
        String emojiID = "";

        String fullEmoji = getFullEmoji(message);

        int indexOfFirstColon = fullEmoji.indexOf(":");
        String emojiNameWithId = fullEmoji.substring(indexOfFirstColon+1);
        int indexOfSecondColon = emojiNameWithId.indexOf(":");

        emojiID = emojiNameWithId.substring(indexOfSecondColon + 1, emojiNameWithId.length()-1);
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
