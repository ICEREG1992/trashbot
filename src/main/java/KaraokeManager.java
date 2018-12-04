import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.event.message.MessageCreateEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class KaraokeManager {

    private Map<String, Karaoke> karaokeMap = new HashMap<>();
    private static AccessRestriction permissions = null;
    private File lyricsFile;
    private static final Logger logger = LogManager.getLogger(KaraokeManager.class);

    KaraokeManager(String lyricsFilename, AccessRestriction perms) {
        // initialize file to filename given in constructor
        this.lyricsFile = new File(lyricsFilename);
        // set permissions
        permissions = perms;
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        String channelID = channel.getIdAsString();
        Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.equals("!karaoke")) {
            addKaraoke(channel);
            if (event.getServer().isPresent()) {
                logger.info("Karaoke added in " + event.getServer().get().getId());
            }

        } else if (karaokeMap.containsKey(channelID) && !karaokeMap.get(channelID).isDead()) {
            sendToKaraoke(channelID, message.getContent());
            if (messageToString.equals("!exit")) {
                cleanKaraoke();
            }
        } else if (messageToString.startsWith("!givelyrics ")) {
            String userID = event.getMessage().getAuthor().getIdAsString();
            if (permissions.doesUserHaveAccess(userID, "blue")) {
                String lyrics = message.getContent().substring(messageToString.indexOf(" ") + 1);
                printToFile(lyrics);
                channel.sendMessage("New lyrics loaded!");
                logger.info("New lyrics added by " + message.getAuthor().getName() + ": \"" + lyrics.substring(0, lyrics.indexOf("\n")) + "\"...");
            } else {
                channel.sendMessage("Sorry, you need to have the blue keycard to use that command.");
            }
        }
    }

    private void addKaraoke(TextChannel channel) {
        cleanKaraoke();
        if (!karaokeMap.containsKey(channel.getIdAsString())) {
            Karaoke newKaraoke = new Karaoke(channel, getLyrics());
            karaokeMap.put(channel.getIdAsString(), newKaraoke);
        }
    }

    private void cleanKaraoke() {
        for (String channelID : karaokeMap.keySet()) {
            if (karaokeMap.get(channelID).isDead()) {
                karaokeMap.remove(channelID);
                logger.info("Karaoke ended in " + channelID);
            }
        }
    }

    private void sendToKaraoke(String channelID, String message) {
        karaokeMap.get(channelID).run(message);
    }

    private void printToFile(String lyrics) {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(this.lyricsFile), StandardCharsets.UTF_8));
        } catch (FileNotFoundException e) {
            logger.error("File " + this.lyricsFile + " not found during save.");
        }
        if (out != null) {
            out.println(lyrics);
            out.close();
        }
    }

    private Queue<String> getLyrics() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(lyricsFile, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            logger.error("File " + this.lyricsFile + " not found during load.");
        }
        Queue<String> lyricsQueue = new LinkedList<>();
        if (fileReader != null) {
            while (fileReader.hasNextLine()) {
                lyricsQueue.add(fileReader.nextLine());
            }
            fileReader.close();
        }
        logger.info("Lyrics successfully loaded for Karaoke.");
        return lyricsQueue;
    }
}
