import com.fasterxml.jackson.annotation.JsonProperty;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.event.message.reaction.ReactionAddEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.*;

public class KaraokeManager {

    private Map<String, Karaoke> karaokeMap = new HashMap<>();
    private static AccessRestriction permissions = null;
    private File lyricsFile;

    public KaraokeManager(String lyricsFilename, AccessRestriction perms) {
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
        } else if (karaokeMap.containsKey(channelID) && !karaokeMap.get(channelID).isDead()) {
            sendToKaraoke(channelID, message.getContent());
        } else if (messageToString.startsWith("!givelyrics ")) {
            String userID = event.getMessage().getAuthor().getIdAsString();
            if (permissions.doesUserHaveAccess(userID, "blue")) {
                String lyrics = message.getContent().substring(messageToString.indexOf(" ") + 1);
                printToFile(lyrics);
                channel.sendMessage("New lyrics loaded!");
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
        for (String userID : karaokeMap.keySet()) {
            if (karaokeMap.get(userID).isDead()) {
                karaokeMap.remove(userID);
            }
        }
    }

    private void sendToKaraoke(String channelID, String message) {
        karaokeMap.get(channelID).run(message);
    }

    private void printToFile(String lyrics) {
        PrintWriter out = null;
        try {
            out = new PrintWriter(this.lyricsFile);
        } catch (FileNotFoundException e) {
            System.out.println("File " + this.lyricsFile + " not found during save.");
        }
        out.println(lyrics);
        out.close();
        System.out.println("New lyrics data saved.");
    }

    private Queue<String> getLyrics() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(lyricsFile);
        } catch (FileNotFoundException e) {
            System.out.println("File " + this.lyricsFile + " not found during load.");
        }
        Queue<String> lyricsQueue = new LinkedList<>();
        while (fileReader.hasNextLine()) {
            lyricsQueue.add(fileReader.nextLine());
        }
        fileReader.close();
        return lyricsQueue;
    }
}
