import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.*;

import java.util.Scanner;

public class trashbotBoot {

    public static void main(String[] args) throws FileNotFoundException  {
        Scanner reader = new Scanner(System.in);
        File battleDat = new File("battle.dat");
        PrintWriter battleOut = new PrintWriter("battle.dat");
        battleOut.print("0\n0\n0");
        battleOut.close();
        System.out.print("Token: ");
        String token = reader.nextLine();

        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {

            api.addMessageCreateListener(event -> {
                if (event.getMessage().getContent().equalsIgnoreCase("!fuck you")) {
                    event.getChannel().sendMessage("I'm sorry!");
                }

                if (event.getMessage().getContent().toLowerCase().contains("money") || event.getMessage().getContent().toLowerCase().contains("cash")
                        || event.getMessage().getContent().toLowerCase().contains("$") || event.getMessage().getContent().toLowerCase().contains("dollars")
                        || event.getMessage().getContent().toLowerCase().contains("pay") || event.getMessage().getContent().toLowerCase().contains("currency")
                        || event.getMessage().getContent().toLowerCase().contains("cheddar") || event.getMessage().getContent().toLowerCase().contains("dough")
                        || event.getMessage().getContent().toLowerCase().contains("moolah") || event.getMessage().getContent().toLowerCase().contains("€")) {
                    event.getMessage().addReaction("<:mrkrabs:451793501470982155>");
                    event.getChannel().sendMessage("<:mrkrabs:451793501470982155>");
                }

                if (event.getMessage().getContent().equals("!battle")) {
                    event.getChannel().sendMessage("Let's fuckin fight then boi");
                    botWait();
                    int health = ((int)(Math.random() * 10) * 2) + 10;
                    int botHealth = ((int)(Math.random() * 10) * 2) + 10;
                    int choice = -1;
                    PrintWriter battleOutBattle = null;
                    try {
                        battleOutBattle = new PrintWriter("battle.dat");
                    } catch (FileNotFoundException e) {
                        System.out.println("Something went wrong.");
                        choice = 0;
                    }
                    battleOutBattle.print(health + "\n" + botHealth + "\n" + choice);
                    battleOutBattle.close();

                    System.out.println("battle info should be printed to battle.dat");
                    System.out.println(health);
                    System.out.println(botHealth);
                    System.out.println(choice);
                    if (choice != 0) {
                        event.getChannel().sendMessage("You have " + health + " health.");
                        botWait();
                        event.getChannel().sendMessage("What do you do?\n > attack\n > heal\n > run");
                    }
                }

                if (event.getMessage().getContent().toLowerCase().contains("!attack")) {
                    int damage = ((int)(Math.random() * 5) + 5);
                    Scanner battleData = null;
                    try {
                        battleData = new Scanner(battleDat);
                    } catch (FileNotFoundException e) {
                        System.out.println("file not here, aye");
                    }
                    int health = Integer.parseInt(battleData.nextLine());
                    int botHealth = Integer.parseInt(battleData.nextLine());
                    int choice = Integer.parseInt(battleData.nextLine());
                    if (choice != 0) {
                        event.getChannel().sendMessage("You attack for " + damage + " damage!");
                        botHealth -= damage;
                        damage = ((int)(Math.random() * 5) + 5);
                        health -= damage;
                        botWait();
                        event.getChannel().sendMessage("You were hit for " + damage + " damage, now at " + health + " health!");
                        botWait();
                        event.getChannel().sendMessage("What do you do?\n > attack\n > heal\n > run");
                    } else {
                        event.getChannel().sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
                    }
                    PrintWriter battleOutAttack = null;
                    try {
                        battleOutAttack = new PrintWriter("battle.dat");
                    } catch (FileNotFoundException e) {
                        System.out.println("Something went wrong.");
                    }
                    battleOutAttack.print(health + "\n" + botHealth + "\n" + choice);
                    battleOutAttack.close();
                }

                if (event.getMessage().getContent().toLowerCase().contains("!heal")) {
                    int damage = ((int)(Math.random() * 5) + 5);
                    Scanner battleData = null;
                    try {
                        battleData = new Scanner(battleDat);
                    } catch (FileNotFoundException e) {
                        System.out.println("file not here, aye");
                    }
                    int health = Integer.parseInt(battleData.nextLine());
                    int botHealth = Integer.parseInt(battleData.nextLine());
                    int choice = Integer.parseInt(battleData.nextLine());
                    if (choice != 0) {
                        health -= damage;
                        event.getChannel().sendMessage("You were hit for " + damage + " damage, now at " + health + " health!");
                        int heal = ((int)(Math.random() * 10) + 7);
                        health += heal;
                        botWait();
                        event.getChannel().sendMessage("You heal yourself for " + heal + " health, now at " + health + " health!");
                        botWait();
                        event.getChannel().sendMessage("What do you do?\n > attack\n > heal\n > run");
                    } else {
                        event.getChannel().sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
                    }
                    PrintWriter battleOutHeal = null;
                    try {
                        battleOutHeal = new PrintWriter("battle.dat");
                    } catch (FileNotFoundException e) {
                        System.out.println("Something went wrong.");
                    }
                    battleOutHeal.print(health + "\n" + botHealth + "\n" + choice);
                    battleOutHeal.close();
                }

                if (event.getMessage().getContent().toLowerCase().contains("!run")) {
                    int damage = ((int)(Math.random() * 5) + 5);
                    Scanner battleData = null;
                    try {
                        battleData = new Scanner(battleDat);
                    } catch (FileNotFoundException e) {
                        System.out.println("file not here, aye");
                    }
                    int health = Integer.parseInt(battleData.nextLine());
                    int botHealth = Integer.parseInt(battleData.nextLine());
                    int choice = Integer.parseInt(battleData.nextLine());
                    if (choice != 0) {
                        health -= damage;
                        event.getChannel().sendMessage("On your way out, you were hit for " + damage + " damage, leaving you at " + health + " health.");
                        choice = 0;
                        botWait();
                        event.getChannel().sendMessage("Next time you come round here you better up your game, pussy bitch. <:restinpepperoni:412754423257890827>");
                    } else {
                        event.getChannel().sendMessage("A battle is not going on right now. Type ``!battle`` to start one!");
                    }
                    PrintWriter battleOutRun = null;
                    try {
                        battleOutRun = new PrintWriter("battle.dat");
                    } catch (FileNotFoundException e) {
                        System.out.println("Something went wrong.");
                    }
                    battleOutRun.print(health + "\n" + botHealth + "\n" + choice);
                    battleOutRun.close();
                }

                if (event.getMessage().getContent().equalsIgnoreCase("/rule34")) {
                    if ((int) (Math.random() * 10) == 1) {
                        botWaitLong();
                        event.getChannel().sendMessage("That's fucked.");
                    }
                }
            });

            // Print the invite url of your bot
            System.out.println("You can invite the bot by using the following url: " + api.createBotInvite());

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
            Thread.sleep(2500);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
    }
}