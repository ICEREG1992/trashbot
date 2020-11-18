import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class instantHumorContains {

    // hashmap to store <prompt phrase, reaction phrase>
    private Map<String, ArrayList<String>> keyPhrases = new HashMap<>();
    private AccessRestriction permissions;
    private File file;
    private static final Logger logger = LogManager.getLogger(instantHumorContains.class);


    instantHumorContains(String filename, AccessRestriction permissions) {
        this.permissions = permissions;
        this.file = new File(filename);
        prepareInstantHumorContainsKeyPhrases();
    }

    public void run(MessageCreateEvent event) {
        // Parse message here so you don't have to later
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();
        String userID = event.getMessage().getAuthor().getIdAsString();

        for (String keyPhrase: keyPhrases.keySet()) {
            if(messageToString.contains(keyPhrase)) {
                channel.sendMessage(helperFunctions.pickString(keyPhrases.get(keyPhrase)));
            }
        }
        if (messageToString.contains("black")) {
            if (message.getServer().isPresent() && message.getServer().get().getId() == 141643881723723777L) {
                if ((int) (Math.random() * 5) == 1) {
                    logger.info("In The Witness server: \"race thing\" message triggered.");
                    channel.sendMessage("why you gotta make it a race thing");
                } else {
                    logger.info("In The Witness server: \"race thing\" message not triggered.");
                }
            } else {
                logger.info("In " + message.getServer().get().getName() + ": \"race thing\" message triggered.");
                channel.sendMessage("why you gotta make it a race thing");
            }
        }
        if (messageToString.startsWith("!containsadd ") && permissions.doesUserHaveAccess(userID, "blue")) {
            String keyword = messageToString.substring(messageToString.indexOf(" ") + 1, messageToString.indexOf("§") - 1);
            String response = message.getContent().substring(messageToString.indexOf("§") + 2);
            if (keyPhrases.containsKey(keyword)) {
                keyPhrases.get(keyword).add(response);
                logger.info("New contains response for \"" + keyword + "\" added: \"" + response + "\"");
            } else {
                ArrayList<String> addList = new ArrayList<>();
                addList.add(response);
                keyPhrases.put(keyword, addList);
                logger.info("New contains keyword added: \"" + keyword + "\" with response \"" + response + "\"");
            }
            save();
        } else if (messageToString.startsWith("!containsremove ") && permissions.doesUserHaveAccess(userID, "blue")) {
            String keyword = messageToString.substring(messageToString.indexOf(" ") + 1);
            keyPhrases.remove(keyword);
            logger.info("Contains responses for \"" + keyword + "\" has been removed.");
            save();
        }
    }

    private void prepareInstantHumorContainsKeyPhrases() {
        // This boolean is to keep track of whether the content in the destination file contains any information.
        boolean hasAnyContent = true;
        Scanner in = null;

        // Creates a new scanner item to read from the file
        try {
            in = new Scanner(file, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            logger.error("File not found error: " + e);
        }

        if (in != null) {
            try {
                // Reads in only the first line of the file
                String key = in.nextLine();

                // If the first line is empty or contains the escape sequence (***) then there is no content in the file.
                if(key.equals("***") || key.equals("")) {
                    hasAnyContent = false;
                }

                if (hasAnyContent) {
                    while (!key.equals("***")) {
                        ArrayList<String> addList = new ArrayList<>();
                        String value = in.nextLine();
                        while (!value.equals("")) {
                            addList.add(value);
                            value = in.nextLine();
                        }
                        this.keyPhrases.put(key, addList);
                        key = in.nextLine();

                    }
                }
                logger.info("Contains phrases loaded.");
            } catch (NoSuchElementException e) {
                logger.error("Incorrect formatting in " + this.file.getName() + ", correctly formatted entries have been loaded.");
            }
            in.close();
        }
    }

    // Saves the current data in keyPhrases to file.
    private void save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8));
        } catch (FileNotFoundException e) {
            logger.error("Error creating filewriter: " + e);
        }

        if (out != null) {
            for (String oldKey : keyPhrases.keySet()) {
                out.println(oldKey);
                for (String response : keyPhrases.get(oldKey)) {
                    out.println(response);
                }
                out.println();
            }
            out.println("***");
            out.close();
        }
    }
}
