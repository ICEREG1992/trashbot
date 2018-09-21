import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Set;

public class SpeakModule {

    private static File file;

    private static ArrayList<String> uniqueStrings = new ArrayList<>();

    private static boolean active = false;
    private static TextChannel speakChannel = null;
    private static int level = 0;

    public SpeakModule(String filename) {
        file = new File(filename);
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();
        String messageToStringLower = message.getContent().toLowerCase();
        if (channel.asPrivateChannel().isPresent() && messageToStringLower.equalsIgnoreCase("!speak")) {
            loadMessages();
            active = true;
            speakChannel = channel;
            channel.sendMessage("Loading Speak...");
            botWait();
            channel.sendMessage("At any time, say \"!quit\" to quit.");
        } else if (messageToStringLower.equalsIgnoreCase("!speak")) {
            channel.sendMessage("Speak can only be played in direct messages. it go down in the dm! see ya there");
        } else if (messageToStringLower.equalsIgnoreCase("!quit") && channel.asPrivateChannel().isPresent()) {
            if (active) {
                channel.sendMessage("ok cool sorry for bein weird on ya");
                active = false;
                level = 0;
            } else {
                channel.sendMessage("you aren't currently playing Speak. if you'd like to, please say \"!speak\"");
            }
        }

        if (active && channel.equals(speakChannel)) {
            if (level == 0) {
                // do nothing
            } else if (level > 0 && level <= 5) {
                channel.sendMessage("<:blank:445505783224991747>");
                if (messageToStringLower.contains("stop")) {
                    level = 6;
                }
            } else if (level > 5 && level <= 10) {
                channel.sendMessage("...");
                if (messageToStringLower.contains("stop")) {
                    level = 11;
                }
            } else if (level > 10 && level <= 15) {
                channel.sendMessage(messageToString);
                if (messageToStringLower.contains("stop")) {
                    level = 16;
                }
            } else if (level > 15 && level <= 25) {
                channel.sendMessage(stringFlip(messageToString));
                if (messageToStringLower.contains("stop")) {
                    level = 26;
                }
            } else if (level > 25 && level <= (25+uniqueStrings.size())) {
                channel.sendMessage(removeAny(uniqueStrings));
                if (messageToStringLower.contains("stop")) {
                    level = 26 + uniqueStrings.size();
                }
            } else if (level == 26 + uniqueStrings.size()) {
                channel.sendMessage("Do you think that all of this will end some day?");
            } else if (level > 27 + uniqueStrings.size()) {
                channel.sendMessage("<:blank:445505783224991747>");
            }

            if (level == 5) {
                channel.sendMessage("[                                                  ]");
            } else if (level == 10) {
                channel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 15) {
                channel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 25) {
                channel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 27+uniqueStrings.size()) {
                channel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 140) {
                channel.sendMessage("(the game's over, man)");
            } else if (level == 145) {
                channel.sendMessage("(say \"!exit\" to exit)");
            }
            level++;
        }
    }

    public static void loadMessages() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        while (fileReader.hasNextLine()) {
            uniqueStrings.add(fileReader.nextLine());
        }
    }

    // Method that pauses the bot for 1 second
    private static void botWait() {
        try {
            Thread.sleep(1500);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }

    private static String stringFlip(String in) {
        String out = "";
        for (int i = in.length()-1; i >= 0; i--) {
            out += in.charAt(i);
        }
        return out;
    }

    private static String removeAny(ArrayList<String> strings) {
        int rand = ((int) Math.random()*strings.size());
        return strings.remove(rand);
    }
}
