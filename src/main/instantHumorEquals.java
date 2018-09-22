import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class instantHumorEquals {

    // hashmap to store <prompt phrase, reaction phrase>
    private static Map<String, String> keyPhrases = new HashMap<>();

    private static File file;

    public instantHumorEquals(String filename) {
        file = new File(filename);
    }

    public void run(MessageCreateEvent event) {
        // Parse message here so you don't have to later
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        for (String keyPhrase: keyPhrases.keySet()) {
            if(messageToString.equals(keyPhrase)) {
                if(messageToString.equals("/rule34")) {
                    if ((int) (Math.random() * 4) == 1) {
                        botWaitLong();
                        channel.sendMessage("That's fucked.");
                    }
                } else if (message.getAuthor().getId() == 473760382616600597L && messageToString.equals("shut the fuck up")) {
                    channel.sendMessage("what the fuck is your problem?");
                } else {
                    channel.sendMessage(keyPhrases.get(keyPhrase));
                }
            }
        }
    }

    private static void botWaitLong() {
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }

    public static void prepareInstantHumorEqualsKeyPhrases() {
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

    // Adds a new keyword that Trashbot can respond to. The key is the keyword and the value is Trashbot's response.
    public static void addKeyPhrasePair(String key, String value) {
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

        out.println(key);
        out.println(value);
        out.println("\n***");
        keyPhrases.put(key, value);
        out.close();
    }
}
