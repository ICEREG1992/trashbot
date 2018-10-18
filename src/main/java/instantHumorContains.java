import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class instantHumorContains {

    // hashmap to store <prompt phrase, reaction phrase>
    private static Map<String, String> keyPhrases = new HashMap<>();
    private static AccessRestriction permissions = null;
    private static File file;

    public instantHumorContains(String filename, AccessRestriction permissions) {
        this.permissions = permissions;
        this.file = new File(filename);
    }

    public void run(MessageCreateEvent event) {
        // Parse message here so you don't have to later
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();
        String userID = event.getMessage().getAuthor().getIdAsString();

        for (String keyPhrase: keyPhrases.keySet()) {
            if(messageToString.contains(keyPhrase)) {
                if (messageToString.contains("good work, trashbot")) {
                    channel.sendMessage(helperFunctions.pickString("thx man", "i appreciate it", "np", "no problem aye", "thx man", "thx man"));
                } else if (messageToString.contains("<@450507364768940034>")) {
                    channel.sendMessage(helperFunctions.pickString("you called?", "that's me!", "what's up", "you called?", "you called?"));
                } else {
                    channel.sendMessage(keyPhrases.get(keyPhrase));
                }
            }
        }
        if (messageToString.contains("black")) {
            if (message.getServer().get().getId() == 141643881723723777L) {
                if ((int) (Math.random() * 4) == 1) {
                    System.out.println("In The Witness server: \"race thing\" message triggered.");
                    channel.sendMessage("why you gotta make it a race thing");
                } else {
                    System.out.println("In The Witness server: \"race thing\" message not triggered.");
                }
            } else {
                System.out.println("In " + message.getServer().get().getName() + ": \"race thing\" message triggered.");
                channel.sendMessage("why you gotta make it a race thing");
            }
        }
        if (messageToString.startsWith("!containsadd ") && AccessRestriction.doesUserHaveAccess(userID, "blue")) {
            String keyword = messageToString.substring(messageToString.indexOf(" ") + 1, messageToString.indexOf("§") - 1);
            String response = message.getContent().substring(messageToString.indexOf("§") + 2);
            keyPhrases.put(keyword, response);
            save();
        } else if (messageToString.startsWith("!containsremove ") && AccessRestriction.doesUserHaveAccess(userID, "blue")) {
            String keyword = messageToString.substring(messageToString.indexOf(" ") + 1);
            keyPhrases.remove(keyword);
            save();
        }
    }

    public static void prepareInstantHumorContainsKeyPhrases() {
        // This boolean is to keep track of whether the content in the destination file contains any information.
        boolean hasAnyContent = true;
        Scanner in = null;

        // Creates a new scanner item to read from the file
        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File not found error: " + e);
        }

        // Reads in only the first line of the file
        String key = in.nextLine();
        String value = "";

        // If the first line is empty or contains the escape sequence (***) then there is no content in the file.
        if(key.equals("***") || key.equals("")) {
            hasAnyContent = false;
        }

        // Loops until it reaches the escape sequence
        while(hasAnyContent && !key.equals("***")) {
            value = in.nextLine();
            in.nextLine();
            keyPhrases.put(key, value);
            key = in.nextLine();
        }
        in.close();
    }

    // Saves the current data in keyPhrases to file.
    public static void save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(file);
        } catch (FileNotFoundException e) {
            System.out.println("Error creating filewriter: " + e);
        }

        for (String oldKey: keyPhrases.keySet()) {
            out.println(oldKey);
            out.println(keyPhrases.get(oldKey) + "\n");
        }

        out.println("\n***");

        out.close();
    }
}
