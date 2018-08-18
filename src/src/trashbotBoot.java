import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.emoji.CustomEmoji;
import org.javacord.api.entity.emoji.Emoji;
import org.javacord.api.entity.message.Message;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.*;

import java.util.Scanner;

public class trashbotBoot {
    // The token that the bot uses to communicate with Discord
    private static String token = "";

    // Build and initialize modules to files
    private static AccessRestriction permissions = new AccessRestriction("data\\permissions.dat");
    private static BattleBot battleBot = new BattleBot();
    private static instantHumorEquals humorEquals = new instantHumorEquals("data\\instantHumorEqualsPhrases.dat");
    private static instantHumorContains humorContains = new instantHumorContains("data\\instantHumorContainsPhrases.dat");
    private static EmojiReactions emojiReactions = new EmojiReactions("data\\emojisReactionData.dat");
    private static KaraokeBot karaokeBot = new KaraokeBot("data\\lyrics.dat", permissions);
    private static TodoModule todoModule = new TodoModule("data\\todoList.dat");

    // Trashbot's user ID; this should be changed
    private static final long selfID = 450507364768940034L;

    public static void main(String[] args) throws FileNotFoundException  {
        // Scanner object for reading system input
        Scanner reader = new Scanner(System.in);

        // Read data from files
        instantHumorEquals.prepareInstantHumorEqualsKeyPhrases();
        instantHumorContains.prepareInstantHumorContainsKeyPhrases();
        EmojiReactions.prepareEmojiReactions();
        AccessRestriction.loadPermissions();
        TodoModule.loadTodo();

        //Prompts for the token
        System.out.print("Token: ");
        token = reader.nextLine();

        // Login trashbot, create message listener
        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {
            api.addMessageCreateListener(event -> {
                // Parse message here so you don't have to later
                TextChannel channel = event.getChannel();
                Message message = event.getMessage();
                String messageToString = message.getContent().toLowerCase();

                // Only attempt to respond to messages if the message doesn't come from the bot
                if (message.getAuthor().getId() != selfID) {
                    // Send the event to the battleBot object
                    battleBot.battle(event);
                    // Send the event to the humorEquals object
                    humorEquals.run(event);
                    // Send the event to the humorContains object
                    humorContains.run(event);
                    // Send the event and api to the emojiReactions object
                    emojiReactions.run(event, api, permissions);
                    // Send the event to the karaokeBot object
                    karaokeBot.karaoke(event);
                    // Send the event to the todoList object
                    todoModule.run(event);

                    // A bunch of non-standardized commands that cannot be contained within modules are here:

                    // Joke ban command
                    if (messageToString.startsWith("!ban ")) {
                        channel.sendMessage(message.getContent().substring(messageToString.indexOf("!ban ") + 4) + " has been banned.");
                    }

                    // !give <color> keycard <user>
                    // Gives a user the specified permission color.
                    if (messageToString.startsWith("!give ")) {
                        if (permissions.doesUserHaveAccess((String.valueOf(message.getAuthor().getId())), "blue")) {
                            String keycardColorAndUser = messageToString.substring(6);
                            String keycardColor = keycardColorAndUser.substring(0,keycardColorAndUser.indexOf(" "));
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("keycard")+10, keycardColorAndUser.length()-1);
                            channel.sendMessage(permissions.addUser(keycardUser, keycardColor));
                        }
                    }

                    // !revoke <color> keycard <user>
                    // Removes a user's permission color
                    if (messageToString.startsWith("!revoke ")) {
                        if (permissions.doesUserHaveAccess((String.valueOf(message.getAuthor().getId())), "blue")) {
                            // Trim message to obtain <color> and <user>
                            String keycardColorAndUser = messageToString.substring(8);
                            String keycardColor = keycardColorAndUser.substring(0, keycardColorAndUser.indexOf(" "));
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("keycard") + 10, keycardColorAndUser.length()-1);
                            // Print result
                            channel.sendMessage(permissions.removeUser(keycardUser,keycardColor));
                        }
                    }

                    // Help command, prints most commands to the channel where called.
                    if (messageToString.equals("!help")) {
                        channel.sendMessage("**Hi!** I'm Trashbot. I'm a friendly guy and can do many things.\n\nHere are some commands:\n```!help\n!ban <user>\n!add <keyword> <emoji>\n!give <color> keycard <@user>\n!revoke <color> keycard <@user>\n!keywords <emoji>\n!karaoke <Song name> / <Artist name>\n!battle\n     !attack\n     !heal\n     !run\n!fuck you\nnah u good\n!buckbumble\n/rule34\n@trashbot\ntrashbot\ngood work, trashbot\nshut the fuck up\nliterally stop\n(literally anything involving money)\nblack```");
                    }

                    // I'm not actually sure if this is necessary.
                    if (messageToString.startsWith("!keywords ")) {
                        EmojiReactions.getKeywords(message);
                    }
                }
            });
            // Add listener for new member joins, to print a welcome message.
            api.addServerMemberJoinListener(event -> {
                TextChannel channel;
                // Get a channel to send the welcome message to
                if (event.getServer().getSystemChannel().isPresent()) {
                    channel = event.getServer().getSystemChannel().get();
                } else if (event.getServer().getTextChannelsByNameIgnoreCase("general").size() > 0) { // if there's no default channel for welcome messages, choose a "general" channel
                    channel = event.getServer().getTextChannelsByNameIgnoreCase("general").get(0);
                } else if (event.getServer().getTextChannelsByNameIgnoreCase("off-topic").size() > 0) {
                    channel = event.getServer().getTextChannelsByNameIgnoreCase("off-topic").get(0);
                } else if (event.getServer().getTextChannelsByNameIgnoreCase("casual").size() > 0) {
                    channel = event.getServer().getTextChannelsByNameIgnoreCase("casual").get(0);
                } else {
                    channel = null;
                    System.out.println("A user tried to join " + event.getServer().getName() + " but no suitable channel was found.");
                }

                String user = event.getUser().getDisplayName(event.getServer());
                String[] welcomeMessages = {"Hey hey, " + user + ", welcome to the server.", "whoa hey lol " + user + " just joined",
                "hey, was that the wind or did I just hear " + user + " come in?", "lol u bitches better watch out, " + user + "'s here and they're ready to fuck shit up aye",
                "yo sup " + user, "hey what's kickin, " + user + "?"};
                channel.sendMessage(pickString(welcomeMessages));
            });
        }).exceptionally(ExceptionLogger.get());

        // Print boot success
        System.out.println("Boot success!");
        // It's funny, this line prints even if the token doesn't go through and the whole program crashes on startup.
    }

    private static String pickString(String[] set) {
        int rand = (int)(Math.random()*(set.length-1));
        return set[rand];
    }
}