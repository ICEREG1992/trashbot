import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.w3c.dom.Text;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.util.ArrayList;
import java.util.Scanner;

public class GoModule {

    // RuntimeMXBean object for reporting system uptime
    private RuntimeMXBean runtime = ManagementFactory.getRuntimeMXBean();
    private static final Logger logger = LogManager.getLogger(GoModule.class);
    private ArrayList<ArrayList<String>> board;
    private boolean gameStarted = false;
    private static final char[] letters = {'a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
    private int size;

    GoModule() {
        this.board = buildGoBoard(13);
        size = 13;
        logger.info("Go board loaded.");
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.startsWith("!go ")) {
            if (!this.gameStarted) {
                this.gameStarted = true;
            }
            // first OOB, get coordinate
            String coordinate = messageToString.substring(messageToString.indexOf(' ') + 1);
            char letter = coordinate.charAt(0);
            int number = Integer.parseInt(coordinate.substring(1));
            int number2 = letterToNumber(letter);
            this.board.get(number).set(number2, "P");
            helperFunctions.botWait();
            botPlaceTile(channel);

        } else if (messageToString.equalsIgnoreCase("!go")) {
            if (!this.gameStarted) {
                this.gameStarted = true;
                channel.sendMessage("sure! i'll go first. we're playing on a " + size + "x" + size + " board rn.");
                helperFunctions.botWait();
                int number = helperFunctions.randomNumber(1, this.size);
                int number2 = helperFunctions.randomNumber(1, this.size);
                while (!spotIsOpen(number, number2)) {
                    number = helperFunctions.randomNumber(1, this.size);
                    number2 = helperFunctions.randomNumber(1, this.size);
                }
                this.board.get(number).set(number2, "B");
                botPlaceTile(channel);
            }
        }

        else if (messageToString.startsWith("!resetgo")) {
            String number = messageToString.substring(messageToString.indexOf(' ') + 1);
            int size = 0;
            try {
                size = Integer.parseInt(number);
            } catch (NumberFormatException e) {
                if (number.length() == 0) {
                    channel.sendMessage("give me a board size and i'll reset the game for ya!");
                } else {
                    channel.sendMessage("hey man, that's not even a number. pls try again.");
                }
            }
            if (size > 25) {
                channel.sendMessage("lol that'd be funny as shit but no pls");
            } else if (size > 0) {
                board = buildGoBoard(size);
                this.size = size;
                this.gameStarted = false;
                channel.sendMessage("okay! go board reset for " + size + "x" + size + " game!");
                logger.info("Go board reset to size " + size + ".");
            }
        }
    }

     private static ArrayList<ArrayList<String>> buildGoBoard(int size) {
        ArrayList<ArrayList<String>> board = new ArrayList<>();
        ArrayList<String> row = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            row.add(String.valueOf(i));
        }
        for (int i = 0; i < size; i++) {
            board.add(row);
        }
        return board;
     }

     private void botPlaceTile(TextChannel channel) {
         int number = helperFunctions.randomNumber(1, this.size);
         int number2 = helperFunctions.randomNumber(1, this.size);
         while (!spotIsOpen(number, number2)) {
             number = helperFunctions.randomNumber(1, this.size);
             number2 = helperFunctions.randomNumber(1, this.size);
         }
         this.board.get(number).set(number2, "B");
         channel.sendMessage("" + numberToLetter(number) + number2);
     }

     private static int letterToNumber(char letter) {
        int out = -1;
         for (int i = 0; i < letters.length; i++) {
             if (letter == letters[i]) {
                 out = i;
             }
         }
         return out;
     }

     private static char numberToLetter(int number) {
        return letters[number];
     }

     private boolean spotIsOpen(int number, int number2) {
        boolean out = true;
        String spot = this.board.get(number).get(number2);
        if (spot.equals("B") || spot.equals("P")) {
            out = false;
        }
        return out;
     }
}
