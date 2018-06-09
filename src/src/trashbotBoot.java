import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.util.logging.ExceptionLogger;
import sun.plugin2.message.Message;

import java.io.*;

import java.util.ArrayList;
import java.util.Map;
import java.util.Scanner;

public class trashbotBoot {

    // Dictionary with Emoji Names as the key and an array of the keywords to trigger that emoji as the value
    //public static Map<String, ArrayList<String>> emojisAndKeywords = new HashMap<>();
    public static ArrayList<String> keywords= new ArrayList<>();

    // The token that the bot uses to communicate with Discord
    private static String token = "";

    private static BattleBot battleBot = new BattleBot("data\\battle.dat");
    private static StupidInstantHumor stupidInstantHumor = new StupidInstantHumor("data\\stupidInstantHumorKeyPhrases.dat");
    private static EmojiReactions emojiReactions = new EmojiReactions("data\\emojisReactionData.dat");

    public static void main(String[] args) throws FileNotFoundException  {
        // Scanner object for reading system input
        Scanner reader = new Scanner(System.in);

        stupidInstantHumor.prepareStupidInstantHumorKeyPhrases();
        battleBot.prepareBattleBot();
        System.out.println("\n\nBefore\n\n");
        emojiReactions.prepareEmojiReactions();
        System.out.println("\n\nAfter\n\n");

        //Prompts for the token
        //System.out.print("Token: ");
        //token = reader.nextLine();

        // Creates the file that stores the keywords that the bot responds to with a mrkrabs emoji
        File keywordsDat = new File("keywords.dat");
        Scanner keywordsReader = new Scanner(keywordsDat);
        while (keywordsReader.hasNextLine()) {
            keywords.add(keywordsReader.nextLine());
        }

        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {

            api.addMessageCreateListener(event -> {
                TextChannel channel = event.getChannel();
                org.javacord.api.entity.message.Message message = event.getMessage();
                String messageToString = message.getContent().toLowerCase();

                // Send the event to the BattleBot object
                battleBot.battle(event);
                stupidInstantHumor.run(event);

                for(String keyword: keywords) {
                    if (messageToString.contains(keyword)) {
                        event.getMessage().addReaction(api.getCustomEmojiById("451793501470982155").get());
                    }
                }


                if (messageToString.startsWith("!ban ")) {
                    channel.sendMessage(event.getMessage().getContent().substring(event.getMessage().getContent().indexOf("!ban ") + 4) + " has been banned.");
                }

                if (messageToString.startsWith("!add ")) {

                    String id = event.getMessage().getAuthor().getIdAsString();
                    if (id.equals("132374584086364160") || id.equals("283785595728429057") || id.equals("392731013496700928")) {
                        String newKeyword = event.getMessage().getContent().toLowerCase().substring(5);
                        keywords.add(newKeyword);
                        refreshKeywordsDat();
                        channel.sendMessage("``" + newKeyword + "`` added as new keyword.");
                    } else {
                        channel.sendMessage("sorry pal, you need the blue keycard to use this command.");
                    }
                }

                if (messageToString.startsWith("!remove ")) {
                    String id = message.getAuthor().getIdAsString();
                    if (id.equals("132374584086364160") || id.equals("283785595728429057") || id.equals("392731013496700928")) {
                        String removeKeyword = messageToString.substring(8);
                        keywords.remove(removeKeyword);
                        refreshKeywordsDat();
                        channel.sendMessage("``" + removeKeyword + "`` has been removed from the keywords list.");
                    } else {
                        channel.sendMessage("sorry pal, you need the blue keycard to use this command.");
                    }
                }

                if (messageToString.equals("!keywords")) {
                    String out = "";
                    for (String keyword: keywords) {
                        out += keyword + " // ";
                    }
                    channel.sendMessage(out);
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