import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class KaraokeBot {
    private File lyricsFile;
    private TextChannel karaokeChannel;
    private Scanner lyricsReader;
    private String nextLine;
    private String uInput;
    private static AccessRestriction permissions = null;

    public KaraokeBot(String lyricsFilename, AccessRestriction perms) {
        // initialize file to filename given in constructor
        lyricsFile = new File(lyricsFilename);
        // set permissions
        permissions = perms;
    }

    // active is true when a song is currently being sung
    private boolean active = false;

    public void karaoke(MessageCreateEvent event) {
        // Parse message here so you don't have to later
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        // !karaoke sets active to true and spits out the first couple lines, if the user who called it has the blue keycard.
        if (messageToString.equals("!karaoke")) {
            String userID = event.getMessage().getAuthor().getIdAsString();
            if (permissions.doesUserHaveAccess(userID, "blue")) {
                active = true;
                karaokeChannel = channel;
                // declare the lyrics reader here to allow for restarts
                lyricsReader = null;
                try {
                    lyricsReader = new Scanner(lyricsFile);
                } catch (FileNotFoundException e) {
                    System.out.println("Something went wrong while loading the Karaoke lyrics.");
                }
                // pretend to enjoy the garbage you're about to go through
                channel.sendMessage("duuuuude i love this song. okay i'll start");
                botWait();
                nextLine = lyricsReader.nextLine();
                channel.sendMessage(nextLine);
                nextLine = lyricsReader.nextLine();
                channel.sendMessage(nextLine);
            } else {
                channel.sendMessage("Sorry, you need to have the blue keycard to use that command.");
            }
        }

        // once karaoke is active, any message sent in that channel is considered as an attempt at the next line.
        else if (active && channel.equals(karaokeChannel)) {
            // if this message equals !exit, the song is stopped at whatever point the bot is at.
            if (messageToString.equals("!exit")) {
                channel.sendMessage("yeah, i get kinda bored there too. thanks for singing with me.");
                active = false;
                lyricsReader.close();
            } else if (lyricsReader.hasNextLine()) { // if there's more lyrics to read, the song is still going.
                uInput = messageToString;
                String uLine = removePunctuation(uInput);
                ArrayList<String> uWords = splitIntoWords(uLine);

                nextLine = lyricsReader.nextLine();
                String formatLine = removePunctuation(nextLine);
                ArrayList<String> formatWords = splitIntoWords(formatLine);

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
                    }
                }

                if (uWords.size() == 0) {
                    channel.sendMessage("come on, man, sing the song please. or say !exit to stop.");
                } else {
                    // for as long as the first letter of the user line word matches the first letter of the actual line
                    // trim those that match, so that if the user didn't complete the line the actual line has the remainder of the words
                    while (uWords.size() > 0 && formatWords.size() > 0 && isStringSimilar(uWords.get(0), formatWords.get(0))) {
                        uWords.remove(0);
                        formatWords.remove(0);
                    }
                    // if there were words left over, print the rest of the line
                    if (formatWords.size() > 0) {
                        nextLine = formatWords.get(0);
                        for (int i = 1; i < formatWords.size(); i++) {
                            nextLine += " " + formatWords.get(i);
                        }
                    }
                    // if there weren't words left over, print the next line.
                    else {
                        nextLine = lyricsReader.nextLine();
                    }
                }


//                int match;
//                // this is probably really bad practice but who's gonna stop me
//                // compare the formatted line to the user formatted line, see how much of the line the user provided
//                for (match = 0; match < formatLine.length() && match < uLine.length() && formatLine.charAt(match)==uLine.charAt(match); match++) {
//                }
//                if (formatLine.substring(match).length() > 1) { // if there's any left-over line that the user didn't provide, have trashbot complete the line
//                    nextLine = formatLine.substring(match); // note that this process means that trashbot spits out the scan-formatted line, which makes it look like he's having a stroke
//                } else {
//                    nextLine = lyricsReader.nextLine(); // if the whole line is completed, send the next line
//                }

                channel.sendMessage(nextLine);
            } else { // if there's no next line, print the goodbye message
                channel.sendMessage("i think that's where the song ends. thanks for singing with me.");
                active = false;
                lyricsReader.close();
            }
        }
    }


    /*---------------------------------------Helper Functions-----------------------------------------------*/

    // Method that pauses the bot for 1 second
    private static void botWait() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }

    // removes characters if there are more than 1 in a row
    private static String removeElongation(String line) {
        String out = "";
        char previousChar = ' ';
        for (int i = 0; i < line.length(); i++) {
            char currentChar = line.charAt(i);
            if (currentChar != previousChar) {
                out+=currentChar;
                previousChar = currentChar;
            }
        }
        return out;
    }

    // removes a specific set of characters from a string
    // aids in formatting for scan
    private static String removePunctuation(String line) {
        String out = "";
        for (int i = 0; i < line.length(); i++) {
            char currentChar = line.charAt(i);
            if (Character.isLetter(currentChar) || currentChar=='(' || currentChar==')' || currentChar==' ' || currentChar=='？' || currentChar=='、') {
                out+=currentChar;
            } else if (i == line.length()-1 && (currentChar=='?' || currentChar=='!')) {
                out+=currentChar;
            }
        }
        return out;
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
        }
        return match;
    }
}
