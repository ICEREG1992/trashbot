import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.*;

import java.util.ArrayList;
import java.util.Scanner;

public class trashbotBoot {
    // The token that the bot uses to communicate with Discord
    private static String token = "";

    private static AccessRestriction permissions = new AccessRestriction("permissions.dat");
    private static BattleBot battleBot = new BattleBot("data\\battle.dat");
    private static StupidInstantHumor stupidInstantHumor = new StupidInstantHumor("data\\stupidInstantHumorKeyPhrases.dat");
    private static EmojiReactions emojiReactions = new EmojiReactions("data\\emojisReactionData.dat");

    public static void main(String[] args) throws FileNotFoundException  {
        // Scanner object for reading system input
        Scanner reader = new Scanner(System.in);

        stupidInstantHumor.prepareStupidInstantHumorKeyPhrases();
        battleBot.prepareBattleBot();
        emojiReactions.prepareEmojiReactions();

        //Prompts for the token
        System.out.print("Token: ");
        token = reader.nextLine();

        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {
            api.addMessageCreateListener(event -> {
                TextChannel channel = event.getChannel();
                org.javacord.api.entity.message.Message message = event.getMessage();
                String messageToString = message.getContent().toLowerCase();

                // Send the event to the BattleBot object
                battleBot.battle(event);
                // Send the event to the stupidInstantHumorBot object
                stupidInstantHumor.run(event);
                // Send the event and api to the emojiReactions object
                emojiReactions.run(event, api, permissions);

                if (messageToString.startsWith("!ban ")) {
                    channel.sendMessage(messageToString.substring(messageToString.indexOf("!ban ") + 4) + " has been banned.");
                }

                if (messageToString.equals("!blue keycard")) {
                    channel.sendMessage("look, you don't have permission to use that command either, but I can give you the yellow keycard.");
                }

                if (messageToString.equals("!yellow keycard")) {
                    channel.sendMessage("here ya go, pal, you now have the yellow keycard. go wild.");
                }
            });

            // Print the invite url of your bot
            System.out.println("Boot success!");


        }).exceptionally(ExceptionLogger.get());
    }
}