import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
            else {
                System.out.println("Emoji not found: " + fullEmoji);
                fullEmoji = "";
            }
        }


        return fullEmoji;
    }
}
