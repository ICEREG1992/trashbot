import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.*;

import java.util.ArrayList;
import java.util.Scanner;

public class trashbotBoot {

    public static ArrayList<String> keywords = new ArrayList<String>();

    public static void main(String[] args) throws FileNotFoundException  {
        Scanner reader = new Scanner(System.in);
        PrintWriter battleOut = new PrintWriter("battle.dat");
        battleOut.print("0\n0\n0");
        battleOut.close();
        System.out.print("Token: ");
        String token = reader.nextLine();

        File keywordsDat = new File("keywords.dat");
        Scanner keywordsReader = new Scanner(keywordsDat);
        while (keywordsReader.hasNextLine()) {
            keywords.add(keywordsReader.nextLine());
        }

        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {

            api.addMessageCreateListener(event -> {
                if (event.getMessage().getContent().equalsIgnoreCase("!fuck you")) {
                    event.getChannel().sendMessage("I'm sorry!");
                }

                boolean contains = false;
                for(String keyword: keywords) {
                    if (event.getMessage().getContent().toLowerCase().contains(keyword)) {
                        event.getMessage().addReaction(api.getCustomEmojiById("451793501470982155").get());
                    }
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

                if (event.getMessage().getContent().toLowerCase().startsWith("!ban ")) {
                    event.getChannel().sendMessage(event.getMessage().getContent().substring(event.getMessage().getContent().indexOf("!ban ") + 4) + " has been banned.");
                }

                if (event.getMessage().getContent().toLowerCase().startsWith("!add ")) {
                    String id = event.getMessage().getAuthor().getIdAsString();
                    if (id.equals("132374584086364160") || id.equals("283785595728429057") || id.equals("392731013496700928")) {
                        String newKeyword = event.getMessage().getContent().toLowerCase().substring(5);
                        keywords.add(newKeyword);
                        refreshKeywordsDat();
                        event.getChannel().sendMessage("``" + newKeyword + "`` added as new keyword.");
                    } else {
                        event.getChannel().sendMessage("sorry pal, you need the blue keycard to use this command.");
                    }
                }

                if (event.getMessage().getContent().toLowerCase().startsWith("!remove ")) {
                    String id = event.getMessage().getAuthor().getIdAsString();
                    if (id.equals("132374584086364160") || id.equals("283785595728429057") || id.equals("392731013496700928")) {
                        String removeKeyword = event.getMessage().getContent().toLowerCase().substring(8);
                        keywords.remove(removeKeyword);
                        refreshKeywordsDat();
                        event.getChannel().sendMessage("``" + removeKeyword + "`` has been removed from the keywords list.");
                    } else {
                        event.getChannel().sendMessage("sorry pal, you need the blue keycard to use this command.");
                    }
                }

                if (event.getMessage().getContent().equalsIgnoreCase("!keywords")) {
                    String out = "";
                    for (String keyword: keywords) {
                        out += keyword + " // ";
                    }
                    event.getChannel().sendMessage(out);
                }

                if (event.getMessage().getContent().contains("<@450507364768940034>") || event.getMessage().getContent().toLowerCase().contains("trashbot")) {
                    event.getChannel().sendMessage("you called?");
                }

                if (event.getMessage().getContent().equalsIgnoreCase("shut the fuck up")) {
                    event.getChannel().sendMessage("sorry.");
                }

                if (event.getMessage().getContent().equalsIgnoreCase("!blue keycard")) {
                    event.getChannel().sendMessage("look, you don't have permission to use that command either, but I can give you the yellow keycard.");
                }

                if (event.getMessage().getContent().equalsIgnoreCase("!yellow keycard")) {
                    event.getChannel().sendMessage("here ya go, pal, you now have the yellow keycard. go wild.");
                }

                if (event.getMessage().getContent().equals("look, man, i know sometimes it seems like i don't love you as much as i say i do, but i promise you, you're like a child to me. and i love and respect you so much. keep your chin up, man, alright? i appreciate you."))
                    event.getChannel().sendMessage("hey look, it's alright, i get it. you do what you gotta do, i'll just be here. thanks for being my friend.");
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

    private static void refreshKeywordsDat() {
        PrintWriter out = null;
        try {
            out = new PrintWriter("keywords.dat");
        } catch (FileNotFoundException e) {
            System.out.println("Something went wrong.");
        }
        for (String oldKeyword: keywords) {
            out.println(oldKeyword);
        }
        out.close();
    }
}