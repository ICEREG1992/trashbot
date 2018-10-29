import org.javacord.api.entity.channel.TextChannel;

import java.util.ArrayList;

public class Speak {

    private ArrayList<String> phrasesList;
    private boolean active;
    private TextChannel speakChannel;
    private int level;

    public Speak(TextChannel channel, ArrayList<String> phrases) {
        this.active = true;
        this.speakChannel = channel;
        this.phrasesList = phrases;
        this.level = 0;

        // print loading
        channel.sendMessage("Loading Speak...");
        helperFunctions.botWait();
        channel.sendMessage("At any time, say \"!quit\" to quit.");
    }

    public void run(String message) {
        String messageToStringLower = message.toLowerCase();
        if (this.active) {
            if (level > 0 && level <= 5) {
                this.speakChannel.sendMessage("<:blank:445505783224991747>");
                if (messageToStringLower.contains("stop")) {
                    level = 6;
                }
            } else if (level > 5 && level <= 10) {
                this.speakChannel.sendMessage("...");
                if (messageToStringLower.contains("stop")) {
                    level = 11;
                }
            } else if (level > 10 && level <= 15) {
                this.speakChannel.sendMessage(message);
                if (messageToStringLower.contains("stop")) {
                    level = 16;
                }
            } else if (level > 15 && level <= 25) {
                this.speakChannel.sendMessage(stringFlip(message));
                if (messageToStringLower.contains("stop")) {
                    level = 26;
                }
            } else if (level > 25 && level <= (25 + phrasesList.size())) {
                this.speakChannel.sendMessage(removeAny(phrasesList));
                if (messageToStringLower.contains("stop")) {
                    level = 26 + phrasesList.size();
                }
            } else if (level == 26 + phrasesList.size()) {
                this.speakChannel.sendMessage("Do you think that all of this will end some day?");
            } else if (level > 27 + phrasesList.size()) {
                this.speakChannel.sendMessage("<:blank:445505783224991747>");
            }

            if (level == 5) {
                this.speakChannel.sendMessage("[                                                  ]");
            } else if (level == 10) {
                this.speakChannel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 15) {
                this.speakChannel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 25) {
                this.speakChannel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 27 + phrasesList.size()) {
                this.speakChannel.sendMessage("[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]\n" +
                        "[                                                  ]");
            } else if (level == 132) {
                this.speakChannel.sendMessage("thanks for playing speak.");
                this.active = false;
            }
            level++;
        }
    }

    public boolean isDead() {
        return !this.active;
    }

    /*
    Helper Functions
     */

    private static String stringFlip(String in) {
        String out = "";
        for (int i = in.length()-1; i >= 0; i--) {
            out += in.charAt(i);
        }
        return out;
    }

    private static String removeAny(ArrayList<String> strings) {
        int rand = ((int) (Math.random() * strings.size()) );
        return strings.remove(rand);
    }
}
