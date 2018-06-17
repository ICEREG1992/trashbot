import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.*;

import java.util.Scanner;

public class trashbotBoot {
    // The token that the bot uses to communicate with Discord
    private static String token = "";

    private static AccessRestriction permissions = new AccessRestriction("data\\permissions.dat");
    private static BattleBot battleBot = new BattleBot("data\\battle.dat");
    private static instantHumorEquals humorEquals = new instantHumorEquals("data\\instantHumorEqualsPhrases.dat");
    private static instantHumorContains humorContains = new instantHumorContains("data\\instantHumorContainsPhrases.dat");
    private static EmojiReactions emojiReactions = new EmojiReactions("data\\emojisReactionData.dat");

    private static final long selfID = 450507364768940034L;

    public static void main(String[] args) throws FileNotFoundException  {
        // Scanner object for reading system input
        Scanner reader = new Scanner(System.in);

        instantHumorEquals.prepareInstantHumorEqualsKeyPhrases();
        instantHumorContains.prepareInstantHumorContainsKeyPhrases();
        BattleBot.prepareBattleBot();
        EmojiReactions.prepareEmojiReactions();
        AccessRestriction.loadPermissions();

        //Prompts for the token
        System.out.print("Token: ");
        token = reader.nextLine();

        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {
            api.addMessageCreateListener(event -> {
                TextChannel channel = event.getChannel();
                Message message = event.getMessage();
                String messageToString = message.getContent().toLowerCase();

                if (message.getAuthor().getId() != selfID) {
                    // Send the event to the BattleBot object
                    battleBot.battle(event);
                    // Send the event to the humorEquals object
                    humorEquals.run(event);
                    // Send the event to the humorContains object
                    humorContains.run(event);
                    // Send the event and api to the emojiReactions object
                    emojiReactions.run(event, api, permissions);

                    if (messageToString.startsWith("!ban ")) {
                        channel.sendMessage(messageToString.substring(messageToString.indexOf("!ban ") + 4) + " has been banned.");
                    }

                    //!give <color> keycard <user>
                    if (messageToString.startsWith("!give ")) {
                        if (permissions.doesUserHaveAccess((String.valueOf(message.getAuthor().getId())), "blue")) {
                            String keycardColorAndUser = messageToString.substring(6);
                            String keycardColor = keycardColorAndUser.substring(0,keycardColorAndUser.indexOf(" "));
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("k")+10, keycardColorAndUser.length()-1);
                            channel.sendMessage(permissions.addUser(keycardUser, keycardColor));
                        }
                    }

                    if (messageToString.equals("!help")) {
                        channel.sendMessage("**Hi!** I'm Trashbot. I'm a friendly guy and can do many things.\n\nHere are some commands:\n```!help\n!ban <user>\n!add <keyword> <emoji>\n!give <color> keycard <@user>\n!keywords <emoji>\n!karaoke <Song name> / <Artist name>\n!battle\n     !attack\n     !heal\n     !run\n!blue keycard\n!yellow keycard\n!fuck you\n!nah u good\n!buckbumble\n/rule34\n@trashbot\ntrashbot\ngood work, trashbot\nshut the fuck up\nliterally stop\n(literally anything involving money)\nblack```");
                    }

                    if (messageToString.startsWith("!keywords ")) {
                        EmojiReactions.getKeywords(message);
                    }
                }
            });

            // Print boot success
            System.out.println("Boot success!");

        }).exceptionally(ExceptionLogger.get());
    }
}