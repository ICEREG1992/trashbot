import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.server.Server;
import org.javacord.api.util.logging.ExceptionLogger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collection;
import java.util.Scanner;
import java.util.Set;

public class trashbotBoot {
    // The token that the bot uses to communicate with Discord
    // private static String token = "";

    private static String fileSep = System.getProperty("file.separator");

    // Build and initialize modules to files
    private static AccessRestriction permissions = new AccessRestriction("data" + fileSep + "permissions.dat");
    private static BattleManager battleBot = new BattleManager();
    private static instantHumorEquals humorEquals = new instantHumorEquals("data" + fileSep + "instantHumorEqualsPhrases.dat", permissions);
    private static instantHumorContains humorContains = new instantHumorContains("data" + fileSep + "instantHumorContainsPhrases.dat", permissions);
    private static EmojiReactions emojiReactions = new EmojiReactions("data" + fileSep + "emojisReactionData.dat", permissions);
    private static KaraokeManager karaokeBot = new KaraokeManager("data" + fileSep + "lyrics.dat", permissions);
    private static TodoModule todoModule = new TodoModule("data" + fileSep + "todoList.dat");
    private static HelpModule helpModule = new HelpModule("data" + fileSep + "helpList.dat");
    private static SpeakManager speakModule = new SpeakManager("data" + fileSep + "speakList.dat");
    private static UptimeModule uptimeModule = new UptimeModule("data" + fileSep + "recordUptime.dat");

    private static final Logger botLogger = LoggerFactory.getLogger(trashbotBoot.class);

    public static void main(String[] args) {
        // Read data from files
        instantHumorEquals.prepareInstantHumorEqualsKeyPhrases();
        instantHumorContains.prepareInstantHumorContainsKeyPhrases();
        EmojiReactions.prepareEmojiReactions();
        AccessRestriction.loadPermissions();
        TodoModule.loadTodo();
        HelpModule.loadHelp();
        UptimeModule.loadUptime();

        //Prompt for the token

        System.out.println("Token: ");
        Scanner reader = new Scanner(System.in);
        String token = reader.nextLine();

        // Login trashbot, create message listener
        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {
            api.addMessageCreateListener(event -> {
                // Parse message here so you don't have to later
                TextChannel channel = event.getChannel();
                Message message = event.getMessage();
                String messageToString = message.getContent().toLowerCase();
                String userID = event.getMessage().getAuthor().getIdAsString();

                // Send the event to the battleBot object out here because it needs to be able to respond to its own
                // messages, to use the edit function.
                battleBot.run(event);

                // Only attempt to respond to messages if the message doesn't come from the bot
                if (!message.getAuthor().isYourself()) {
                    // Send the event to the humorEquals object
                    humorEquals.run(event);
                    // Send the event to the humorContains object
                    humorContains.run(event);
                    // Send the event and api to the emojiReactions object
                    emojiReactions.run(event, api, permissions);
                    // Send the event to the karaokeBot object
                    karaokeBot.run(event);
                    // Send the event to the todoModule object
                    todoModule.run(event);
                    // Send the event to the helpModule object
                    helpModule.run(event);
                    // Send the event to the speakModule object
                    speakModule.run(event);
                    // Send the event to the uptimeModule object
                    uptimeModule.run(event);

                    // A bunch of non-standardized commands that cannot be contained within modules are here:

                    // Joke ban command
                    if (messageToString.startsWith("!ban ")) {
                        channel.sendMessage(message.getContent().substring(messageToString.indexOf("!ban ") + 4) + " has been banned.");
                    }

                    // !give <color> keycard <user>
                    // Gives a user the specified permission color.
                    if (messageToString.startsWith("!give ")) {
                        if (permissions.doesUserHaveAccess(userID, "blue")) {
                            String keycardColorAndUser = messageToString.substring(6);
                            String keycardColor = keycardColorAndUser.substring(0,keycardColorAndUser.indexOf("keycard ")-1);
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("keycard")+10, keycardColorAndUser.length()-1);
                            if (keycardUser.contains("!")) {
                                keycardUser = keycardUser.substring(1);
                            }
                            // dumb ass workaround
                            final String finalKeycardUser = keycardUser;
                            api.getUserById(keycardUser).thenAccept(user -> {
                                    String log = permissions.addUser(finalKeycardUser, user.getName(), keycardColor);
                                    channel.sendMessage(log);
                                    botLogger.info(log);
                            });
                        }
                    }

                    // !revoke <color> keycard <user>
                    // Removes a user's permission color
                    if (messageToString.startsWith("!revoke ")) {
                        if (permissions.doesUserHaveAccess(userID, "blue")) {
                            // Trim message to obtain <color> and <user>
                            String keycardColorAndUser = messageToString.substring(8);
                            String keycardColor = keycardColorAndUser.substring(0, keycardColorAndUser.indexOf("keycard ")-1);
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("keycard") + 10, keycardColorAndUser.length()-1);
                            if (keycardUser.contains("!")) {
                                keycardUser = keycardUser.substring(1);
                            }
                            // Print result
                            String log = permissions.removeUser(keycardUser,keycardColor);
                            channel.sendMessage(log);
                            botLogger.info(log);
                        }
                    }

                    // prints all users of a given keycard color
                    if (messageToString.startsWith("!keycard ")) {
                        String accessLevel = messageToString.substring(messageToString.indexOf(" ") + 1);
                        Set<String> users = permissions.getUsers(accessLevel);
                        String send = "__Users with permission " + accessLevel + ":__\n";
                        for (String user: users) {
                            send += user + "\n";
                        }
                        channel.sendMessage(send);
                    }

                    if (messageToString.startsWith("!devsendmessage ")) {
                        if (permissions.doesUserHaveAccess(userID, "blue")) {
                            String loudMessage = messageToString.substring(messageToString.indexOf(" ") + 1);
                            Collection<Server> servers = api.getServers();
                            for (Server server : servers) {
                                TextChannel outChannel = helperFunctions.getGeneralChannel(server);
                                outChannel.sendMessage(loudMessage);
                            }
                            botLogger.info("Dev message sent by " + message.getAuthor().getName() + ": " + loudMessage);
                        } else {
                            channel.sendMessage("easy there bud, you need the blue keycard to do that.");
                        }
                    }

                    if (messageToString.equals("!panic") && permissions.doesUserHaveAccess(userID, "blue")) {
                        channel.sendMessage("ow, fuck!");
                        botLogger.info("Panic command triggered by " + message.getAuthor().getName() + "!");
                        api.disconnect();
                    }

                }
            });
            // Add listener for new member joins, to print a welcome message.
            api.addServerMemberJoinListener(event -> {
                TextChannel channel;
                channel = helperFunctions.getGeneralChannel(event.getServer());

                String user = event.getUser().getDisplayName(event.getServer());
                channel.sendMessage(helperFunctions.pickString("Hey hey, " + user + ", welcome to the server.", "whoa hey lol " + user + " just joined",
                        "hey, was that the wind or did I just hear " + user + " come in?", "lol u bitches better watch out, " + user + "'s here and they're ready to fuck shit up aye",
                        "yo sup " + user, "hey what's kickin, " + user + "?"));
            });

            api.addReactionAddListener(event -> {
                if (!event.getUser().isYourself()) {
                    battleBot.run(event);
                }
            });
            // Print boot success
            botLogger.info("Boot success!");
        }).exceptionally(ExceptionLogger.get());
        reader.close();
    }
}