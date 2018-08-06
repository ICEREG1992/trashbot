import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.*;
import java.util.Scanner;

public class BattleBot {
    public static String filename;

    public BattleBot() {
    }

    private int health = 0;
    private int botHealth = 0;
    private int choice = 0;
    public void battle(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.equals("!battle")) {
            if (choice != -1) {
                channel.sendMessage("Let's fuckin fight then boi");
                botWait();
                health = ((int) (Math.random() * 10) * 2) + 10;
                botHealth = ((int) (Math.random() * 10) * 2) + 10;
                choice = -1;

                System.out.println("Battle started!");
                channel.sendMessage("You have " + health + " health.");
                botWait();
                channel.sendMessage("I'm at " + botHealth + " health. What do you do?\n > attack\n > heal\n > run");
            } else {
                channel.sendMessage("Whoa there, buddy. I'm already fighting someone.");
            }
        }

        if (messageToString.contains("!attack")) {
            int damage = ((int)(Math.random() * 5) + 5);
            if (choice != 0) {
                channel.sendMessage("You attack for " + damage + " damage!");
                botHealth -= damage;
                damage = ((int)(Math.random() * 5) + 5);
                health -= damage;
                botWait();
                channel.sendMessage("You were hit for " + damage + " damage, now at " + health + " health!");
                botWait();
                if (health<=0) {
                    channel.sendMessage("You fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                    choice = 0;
                    System.out.println("Battle ended!");
                } else if (botHealth<=0) {
                    channel.sendMessage("Oh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                    choice = 0;
                    System.out.println("Battle ended!");
                } else {
                    channel.sendMessage("I'm at " + botHealth + " health. What do you do?\n > attack\n > heal\n > run");
                }
            } else {
                channel.sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
            }
        }

        if (messageToString.contains("!heal")) {
            int damage = ((int)(Math.random() * 5) + 5);
            if (choice != 0) {
                health -= damage;
                channel.sendMessage("You were hit for " + damage + " damage, now at " + health + " health!");
                int heal = ((int)(Math.random() * 10) + 7);
                health += heal;
                botWait();
                channel.sendMessage("You heal yourself for " + heal + " health, now at " + health + " health!");
                botWait();
                if (health<=0) {
                    channel.sendMessage("You fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                    choice = 0;
                    System.out.println("Battle ended!");
                } else if (botHealth<=0) {
                    channel.sendMessage("Oh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                    choice = 0;
                    System.out.println("Battle ended!");
                } else {
                    channel.sendMessage("I'm at " + botHealth + " health. What do you do?\n > attack\n > heal\n > run");
                }
            } else {
                channel.sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
            }
        }

        if (messageToString.contains("!run")) {
            int damage = ((int)(Math.random() * 5) + 5);
            if (choice != 0) {
                health -= damage;
                channel.sendMessage("On your way out, you were hit for " + damage + " damage, leaving you at " + health + " health.");
                if (health<=0) {
                    channel.sendMessage("You fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                }
                choice = 0;
                System.out.println("Battle ended!");
                botWait();
                channel.sendMessage("I'm at " + botHealth + " health.");
                botWait();
                channel.sendMessage("Next time you come round here you better up your game, pussy bitch. <:restinpepperoni:412754423257890827>");
            } else {
                channel.sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
            }
        }
    }


    /*---------------------------------------Helper Functions-----------------------------------------------*/

    // Method that pauses the bot for 1 second
    private static void botWait() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }

    // Method that writes to the battle data file
    private static void writeToBattleDat(int health, int botHealth, int choice) {
        PrintWriter out = null;
        try {
            out = new PrintWriter(filename);
        } catch (FileNotFoundException e) {
            System.out.println("Something went wrong.");
        }
        out.print(health + "\n" + botHealth + "\n" + choice);
        out.close();
    }

    // Method that reads from the battle data file
    private static int[] readFromBattleDat() {
        File battleDat = new File(filename);
        Scanner battleData = null;
        try {
            battleData = new Scanner(battleDat);
        } catch (FileNotFoundException e) {
            System.out.println("file not here, aye");
        }
        int health = Integer.parseInt(battleData.nextLine());
        int botHealth = Integer.parseInt(battleData.nextLine());
        int choice = Integer.parseInt(battleData.nextLine());
        int[] outArray = {health, botHealth, choice};
        battleData.close();
        return outArray;
    }

    // Method that initializes the battle data file
    public static void prepareBattleBot() {
        File file = new File(filename);
        PrintWriter battleOut = null;
        try {
            battleOut = new PrintWriter(file);
        } catch (IOException e) {
            System.out.println("ERROR: Unable to create battle data file: " + e);
        }
        battleOut.println("0\n0\n0");
        battleOut.close();
    }
}
