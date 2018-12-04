import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.server.Server;
import org.javacord.api.util.logging.ExceptionLogger;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Collection;
import java.util.Scanner;
import java.util.Set;

public class trashbotBoot {

    private static final Logger botLogger = LogManager.getLogger(trashbotBoot.class);
    static { botLogger.info("Booting Trashbot v0.12 -");}

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

    public static void main(String[] args) {
        String token;
        if (args.length > 0 && !args[0].equals("")) {
            token = args[0];
        } else {
            botLogger.error("Missing argument!");
            throw new IllegalArgumentException("Missing token argument in boot command.");
        }

        File attemptFile = new File(token);
        try {
            Scanner fileReader = new Scanner(attemptFile);
            if (fileReader.hasNext()) {
                token = fileReader.nextLine();
            }
            fileReader.close();
            botLogger.info("Argument identified as token file location, continuing.");
        } catch (FileNotFoundException e) {
            botLogger.info("Argument identified as plaintext token, continuing.");
            // reset token to args[0] for safety
            token = args[0];
        }

        // Login trashbot, create message listener
        new DiscordApiBuilder().setToken(token).login().thenAccept(api -> {
            botLogger.info("Token success!");
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
                    emojiReactions.run(event, api);
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

                    if (messageToString.contains("thoonk")) {
                        channel.sendMessage("<:thoonk:491141744445095947>");
                    }

                    // !give <color> keycard <user>
                    // Gives a user the specified permission color.
                    if (messageToString.startsWith("!give ")) {
                        if (permissions.doesUserHaveAccess(userID, "blue")) {
                            String keycardColorAndUser = messageToString.substring(6);
                            String keycardColor = keycardColorAndUser.substring(0,keycardColorAndUser.indexOf("keycard ")-1);
                            String keycardUser = "" + helperFunctions.getFirstMentionID(message);
                            // dumb ass workaround
                            final String finalKeycardUser = keycardUser;
                            api.getUserById(keycardUser).thenAccept(user -> {
                                    permissions.addUser(finalKeycardUser, user.getName(), keycardColor);
                                    String log = "User <@" + userID + "> added to permission " + keycardColor;
                                    channel.sendMessage(log);
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
                            String keycardUser = "" + helperFunctions.getFirstMentionID(message);
                            // Print result
                            permissions.removeUser(keycardUser,keycardColor);
                            String log = "User <@" + userID + "> removed from permission " + keycardColor;
                            channel.sendMessage(log);
                        }
                    }

                    // prints all users of a given keycard color
                    if (messageToString.startsWith("!keycard ")) {
                        String accessLevel = messageToString.substring(messageToString.indexOf(" ") + 1);
                        Set<String> users = permissions.getUsers(accessLevel);
                        StringBuilder outString = new StringBuilder();
                        outString.append("__Users with permission ").append(accessLevel).append(":__\n");
                        for (String user: users) {
                            outString.append(user).append("\n");
                        }
                        channel.sendMessage(outString.toString());
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
                        main(args);
                    }

                    if (messageToString.equals("!shutdown") && permissions.doesUserHaveAccess(userID, "blue")) {
                        channel.sendMessage(helperFunctions.pickString("night, night.", "\uD83D\uDECC\uD83D\uDCA4", "ok bye, guys"));
                        botLogger.info("Shutdown command triggered by " + message.getAuthor().getName() + "!");
                        api.disconnect();
                    }

                } else {
                    if (messageToString.equals("<:thoonk:491141744445095947>")) {
                        helperFunctions.botWaitShort();
                        message.edit("<:thoonkroll1:518144565538979870>");
                        helperFunctions.botWaitShort();
                        message.edit("<:thoonkroll2:518144615459848207>");
                        helperFunctions.botWaitShort();
                        message.edit("<:thoonkroll3:518144629825208341>");
                        helperFunctions.botWaitShort();
                        message.edit("<:thoonk:491141744445095947>");
                        helperFunctions.botWaitShort();
                        message.delete();
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
                        "yo sup " + user, "hey what's kickin, " + user + "?", "yo yo it's " + user, "beep boop beep " + user + "'s here"));
            });

            api.addReactionAddListener(event -> {
                if (!event.getUser().isYourself()) {
                    battleBot.run(event);
                }
            });
            // Print boot success
        }).exceptionally(ExceptionLogger.get());
    }
}