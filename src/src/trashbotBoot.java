import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.*;

import java.util.Scanner;

public class trashbotBoot {

    public static void main(String[] args) throws FileNotFoundException  {
        Scanner reader = new Scanner(System.in);
        PrintWriter battleOut = new PrintWriter("battle.dat");
        battleOut.print("0\n0\n0");
        battleOut.close();
        System.out.print("Token: ");
        String token = reader.nextLine();
        final String[] keywords = {"money", "cash", "$", "dollar", "pay", "currency", "cheddar", "dough", "moolah", "€",
        "cent", "bank"};

        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {

            api.addMessageCreateListener(event -> {
                if (event.getMessage().getContent().equalsIgnoreCase("!fuck you")) {
                    event.getChannel().sendMessage("I'm sorry!");
                }

                boolean contains = false;
                for (int i = 0; i < keywords.length && !contains; i++) {
                    if (event.getMessage().getContent().toLowerCase().contains(keywords[i])) {
                        contains = true;
                    }
                }
                if (contains) {
                    // this line needs tweaking to fix, i would rather have reaction than message
                    event.getMessage().addReaction(api.getCustomEmojiById("451793501470982155").get());
                    // this line works
                    // event.getChannel().sendMessage("<:mrkrabs:451793501470982155>");
                }

                if (event.getMessage().getContent().equals("!battle")) {
                    event.getChannel().sendMessage("Let's fuckin fight then boi");
                    botWait();
                    int health = ((int)(Math.random() * 10) * 2) + 10;
                    int botHealth = ((int)(Math.random() * 10) * 2) + 10;
                    int choice = -1;
                    writeToBattleDat(health, botHealth, choice);

                    System.out.println("Battle started!");
                    if (choice != 0) {
                        event.getChannel().sendMessage("You have " + health + " health.");
                        botWait();
                        event.getChannel().sendMessage("I'm at " + botHealth + " health. What do you do?\n > attack\n > heal\n > run");
                    }
                }

                if (event.getMessage().getContent().toLowerCase().contains("!attack")) {
                    int damage = ((int)(Math.random() * 5) + 5);
                    int[] stats = readFromBattleDat();
                    int health = stats[0];
                    int botHealth = stats[1];
                    int choice = stats[2];
                    if (choice != 0) {
                        event.getChannel().sendMessage("You attack for " + damage + " damage!");
                        botHealth -= damage;
                        damage = ((int)(Math.random() * 5) + 5);
                        health -= damage;
                        botWait();
                        event.getChannel().sendMessage("You were hit for " + damage + " damage, now at " + health + " health!");
                        botWait();
                        event.getChannel().sendMessage("I'm at " + botHealth + " health. What do you do?\n > attack\n > heal\n > run");
                    } else {
                        event.getChannel().sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
                    }
                    writeToBattleDat(health, botHealth, choice);
                }

                if (event.getMessage().getContent().toLowerCase().contains("!heal")) {
                    int damage = ((int)(Math.random() * 5) + 5);
                    int[] stats = readFromBattleDat();
                    int health = stats[0];
                    int botHealth = stats[1];
                    int choice = stats[2];
                    if (choice != 0) {
                        health -= damage;
                        event.getChannel().sendMessage("You were hit for " + damage + " damage, now at " + health + " health!");
                        int heal = ((int)(Math.random() * 10) + 7);
                        health += heal;
                        botWait();
                        event.getChannel().sendMessage("You heal yourself for " + heal + " health, now at " + health + " health!");
                        botWait();
                        event.getChannel().sendMessage("I'm at " + botHealth + " health. What do you do?\n > attack\n > heal\n > run");
                    } else {
                        event.getChannel().sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
                    }
                    writeToBattleDat(health, botHealth, choice);
                }

                if (event.getMessage().getContent().toLowerCase().contains("!run")) {
                    int damage = ((int)(Math.random() * 5) + 5);
                    int[] stats = readFromBattleDat();
                    int health = stats[0];
                    int botHealth = stats[1];
                    int choice = stats[2];
                    if (choice != 0) {
                        health -= damage;
                        event.getChannel().sendMessage("On your way out, you were hit for " + damage + " damage, leaving you at " + health + " health.");
                        choice = 0;
                        System.out.println("Battle ended!");
                        botWait();
                        event.getChannel().sendMessage("I'm at " + botHealth + " health.");
                        botWait();
                        event.getChannel().sendMessage("Next time you come round here you better up your game, pussy bitch. <:restinpepperoni:412754423257890827>");
                    } else {
                        event.getChannel().sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
                    }
                    writeToBattleDat(health, botHealth, choice);
                }

                if (event.getMessage().getContent().equalsIgnoreCase("/rule34")) {
                    if ((int) (Math.random() * 4) == 1) {
                        botWaitLong();
                        event.getChannel().sendMessage("That's fucked.");
                    }
                }

                if (event.getMessage().getContent().toLowerCase().contains("!ban")) {
                    event.getChannel().sendMessage(event.getMessage().getContent().substring(event.getMessage().getContent().indexOf("!ban") + 4) + " has been banned.");
                }

            });

            // Print the invite url of your bot
            System.out.println("Boot success!");


        }).exceptionally(ExceptionLogger.get());
    }

    private static void botWait() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }

    private static void botWaitLong() {
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }

    private static void writeToBattleDat(int health, int botHealth, int choice) {
        PrintWriter out = null;
        try {
            out = new PrintWriter("battle.dat");
        } catch (FileNotFoundException e) {
            System.out.println("Something went wrong.");
        }
        out.print(health + "\n" + botHealth + "\n" + choice);
        out.close();
    }

    private static int[] readFromBattleDat() {
        File battleDat = new File("battle.dat");
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
        return outArray;
    }
}