import org.javacord.api.entity.channel.TextChannel;
import java.util.*;

public class Karaoke {

    private Queue<String> lyricsQueue;
    private TextChannel karaokeChannel;
    private String nextLine;

    // active is true when a song is currently being sung
    private boolean active;

    Karaoke(TextChannel channel, Queue<String> lyrics) {
        this.active = true;
        this.karaokeChannel = channel;
        this.lyricsQueue = lyrics;

        // pretend to enjoy the garbage you're about to go through
        channel.sendMessage("duuuuude i love this song. okay i'll start");
        helperFunctions.botWait();
        this.nextLine = lyricsQueue.remove();
        channel.sendMessage(this.nextLine);
        run(this.nextLine);
    }

    public void run(String message) {
        String uInput;
        if (this.active) {
            if (message.equals("!exit")) {
                karaokeChannel.sendMessage("yeah, i get kinda bored there too. thanks for singing with me.");
                active = false;
            } else if (this.lyricsQueue.size() > 0) { // if there's more lyrics to read, the song is still going.
                uInput = message;
                int exclamation = countExclamationMarks(uInput);
                String uLine = removePunctuation(uInput);
                boolean caps = false;
                if (isUppercase(uLine)) {
                    caps = true;
                }
                ArrayList<String> uWords = splitIntoWords(uLine);

                nextLine = lyricsQueue.remove();
                String formatLine = formatForScan(nextLine);
                ArrayList<String> formatWords = splitIntoWords(formatLine);
                ArrayList<String> words = splitIntoWords(nextLine);

                // filter any garbage first words from the user line
                // if the first word in the user line is not equal to the real line, but that word is actually contained in the real line,
                // then it means that the user started somewhere in the middle, so remove words from the real line until they equal.
                if (!isStringSimilar(uWords.get(0), formatWords.get(0)) && uWords.contains(formatWords.get(0))) {
                    while (!isStringSimilar(uWords.get(0), formatWords.get(0))) {
                        uWords.remove(0);
                    }
                } else if (!isStringSimilar(uWords.get(0), formatWords.get(0)) && formatWords.contains(uWords.get(0))) {
                    while (!isStringSimilar(uWords.get(0), formatWords.get(0))) {
                        formatWords.remove(0);
                        words.remove(0);
                    }
                }

                if (uWords.size() == 0) {
                    karaokeChannel.sendMessage("come on, man, sing the song please. or say !exit to stop.");
                } else {
                    // for as long as the first letter of the user line word matches the first letter of the actual line
                    // trim those that match, so that if the user didn't complete the line the actual line has the remainder of the words
                    while (uWords.size() > 0 && formatWords.size() > 0 && isStringSimilar(uWords.get(0), formatWords.get(0))) {
                        uWords.remove(0);
                        formatWords.remove(0);
                        words.remove(0);
                    }
                    // if there were words left over, print the rest of the line
                    if (formatWords.size() > 0) {
                        nextLine = words.get(0);
                        for (int i = 1; i < formatWords.size(); i++) {
                            nextLine = nextLine.concat(" " + words.get(i));
                        }
                    }
                    // if there weren't words left over, print the next line.
                    else {
                        nextLine = lyricsQueue.remove();
                    }
                }
                if (caps) {
                    nextLine = nextLine.toUpperCase();
                }
                for (int i = 0; i < exclamation; i++) {
                    nextLine = nextLine.concat("!");
                }

                karaokeChannel.sendMessage(nextLine);

                if (lyricsQueue.isEmpty()) {
                    karaokeChannel.sendMessage("i think that's where the song ends. thanks for singing with me.");
                    active = false;
                }
            } else { // if there's no next line, print the goodbye message
                karaokeChannel.sendMessage("i think that's where the song ends. thanks for singing with me.");
                active = false;
            }
        }
    }

    boolean isDead() {
        return !active;
    }

    /*
    Helper Functions
     */

    // removes characters if there are more than 1 in a row
    private static String removeElongation(String line) {
        StringBuilder outString = new StringBuilder();
        char previousChar = ' ';
        for (int i = 0; i < line.length(); i++) {
            char currentChar = line.charAt(i);
            if (currentChar != previousChar) {
                outString.append(currentChar);
                previousChar = currentChar;
            }
        }
        return outString.toString();
    }

    // removes a specific set of characters from a string
    // aids in formatting for scan
    private static String removePunctuation(String line) {
        StringBuilder outString = new StringBuilder();
        for (int i = 0; i < line.length(); i++) {
            char currentChar = line.charAt(i);
            if (Character.isLetter(currentChar) || currentChar=='(' || currentChar==')' || currentChar==' ' || currentChar=='？' || currentChar=='、') {
                outString.append(currentChar);
            } else if (i == line.length()-1 && (currentChar=='?' || currentChar=='!')) {
                outString.append(currentChar);
            }
        }
        return outString.toString();
    }

    // formats a string to make it easier to scan to compare to lyrics-- makes karaoke more forgiving for typos and elongations and extra punctuation
    private static String formatForScan(String line) {
        String out = removeElongation(line);
        out = removePunctuation(out);
        out = out.toLowerCase();
        return out;
    }

    // parses a string and returns an arraylist of strings, where each string in the list is an individual word from the input string
    private static ArrayList<String> splitIntoWords(String line) {
        ArrayList<String> words = new ArrayList<>();
        while (line.contains(" ")) {
            String word = line.substring(0, line.indexOf(" "));
            words.add(word);
            line = line.substring(line.indexOf(" ") + 1);
        }
        words.add(line);
        return words;
    }

    private static boolean isStringSimilar(String a, String b) {
        boolean match = false;
        a = a.toLowerCase();
        b = b.toLowerCase();
        int aLength = a.length();
        int bLength = b.length();
        if (a.charAt(0) == b.charAt(0) && a.charAt(aLength-1) == b.charAt(bLength-1)) {
            match = true;
        } else if (a.length() > 1 && b.length() > 1 && a.charAt(0) == b.charAt(0) && a.charAt(1) == b.charAt(1)) {
            match = true;
        } else if (a.length() > 2 && b.length() > 2 && a.charAt(aLength-3) == b.charAt(bLength-3) && a.charAt(aLength-2) == b.charAt(bLength-2) && a.charAt(aLength-1) == b.charAt(bLength-1)) {
            match = true;
        }
        return match;
    }

    private static boolean isUppercase(String line) {
        int buffer = 3;
        for (int i = 0; i < line.length(); i++) {
            if (Character.isAlphabetic(line.charAt(i)) && Character.isLowerCase(line.charAt(i))) {
                buffer -= 1;
            }
        }
        return buffer >= 0;
    }

    private static int countExclamationMarks(String line) {
        int count = 0;
        for (int i = 0; i < line.length(); i++) {
            if (line.charAt(i) == '!') {
                count++;
            }
        }
        return count;
    }
}
