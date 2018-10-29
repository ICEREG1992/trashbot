import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class SpeakManager {

    private Map<String, Speak> speakMap = new HashMap<>();
    private ArrayList<String> phrasesList;
    private File speakFile;

    public SpeakManager(String phrasesFilename) {
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
            }
        }
    }

    private void sendToSpeak(String channelID, String message) {
        speakMap.get(channelID).run(message);
    }

    private ArrayList<String> getPhrases() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(this.speakFile, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            System.out.println("File " + this.speakFile + " not found during load.");
        }
        ArrayList<String> phrasesList = new ArrayList<>();
        if (fileReader != null) {
            while (fileReader.hasNextLine()) {
                phrasesList.add(fileReader.nextLine());
            }
            fileReader.close();
        }

        return phrasesList;
    }
}
