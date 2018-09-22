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
}
