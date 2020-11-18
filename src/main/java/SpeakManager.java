import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.event.message.MessageCreateEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class SpeakManager {

    private Map<String, Speak> speakMap = new HashMap<>();
    private ArrayList<String> phrasesList;
    private File speakFile;
    private static final Logger logger = LogManager.getLogger(SpeakManager.class);

    SpeakManager(String phrasesFilename) {
        // initialize file to filename given in constructor
        this.speakFile = new File(phrasesFilename);
        this.phrasesList = getPhrases();
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        String channelID = channel.getIdAsString();
        Message message = event.getMessage();
        String messageToString = message.getContent();
        String messageToStringLower = message.getContent().toLowerCase();

        if (channel.asPrivateChannel().isPresent() && messageToStringLower.equalsIgnoreCase("!speak")) {
            addSpeak(channel);
            logger.info("Speak game started by " + message.getAuthor().getId());
            channel.sendMessage("Loading Speak...");
            helperFunctions.botWait();
            channel.sendMessage("At any time, say \"!quit\" to quit.");
        } else if (messageToStringLower.equalsIgnoreCase("!speak")) {
            channel.sendMessage("Speak can only be played in direct messages. it go down in the dm! see ya there");
        }

        if (speakMap.containsKey(channelID) && !speakMap.get(channelID).isDead()) {
            sendToSpeak(channelID, messageToString);
        }
    }

    private void addSpeak(TextChannel channel) {
        cleanSpeak();
        if (!speakMap.containsKey(channel.getIdAsString())) {
            Speak newSpeak = new Speak(channel, phrasesList);
            speakMap.put(channel.getIdAsString(), newSpeak);
        }
    }

    private void cleanSpeak() {
        for (String userID : speakMap.keySet()) {
            if (speakMap.get(userID).isDead()) {
                speakMap.remove(userID);
                logger.info("Speak game by " + userID + " ended.");
            }
        }
    }

    private void sendToSpeak(String channelID, String message) {
        speakMap.get(channelID).run(message);
    }

    private ArrayList<String> getPhrases() {
        phrasesList = helperFunctions.readEntriesFromFile(this.speakFile);
        logger.info("Speak phrases loaded.");
        return phrasesList;
    }
}
