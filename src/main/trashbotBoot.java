import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;
import org.javacord.api.util.logging.ExceptionLogger;
import java.lang.management.RuntimeMXBean;
import java.lang.management.ManagementFactory;
import java.io.*;
import java.util.Scanner;
import java.util.Set;

public class trashbotBoot {
    // The token that the bot uses to communicate with Discord
    private static String token = "";

    // Build and initialize modules to files
    private static AccessRestriction permissions = new AccessRestriction("data/permissions.dat");
    private static BattleBot battleBot = new BattleBot();
    private static instantHumorEquals humorEquals = new instantHumorEquals("data/instantHumorEqualsPhrases.dat");
    private static instantHumorContains humorContains = new instantHumorContains("data/instantHumorContainsPhrases.dat");
    private static EmojiReactions emojiReactions = new EmojiReactions("data/emojisReactionData.dat");
    private static KaraokeBot karaokeBot = new KaraokeBot("data/lyrics.dat", permissions);
    private static TodoModule todoModule = new TodoModule("data/todoList.dat");
    private static HelpModule helpModule = new HelpModule("data/helpList.dat");
    private static SpeakModule speakModule = new SpeakModule("data/speakList.dat");

    // Trashbot's user ID; this should be changed if this library is being used for a different bot.
    private static final long selfID = 450507364768940034L;

    public static void main(String[] args) throws FileNotFoundException  {
        // Scanner object for reading system input
        Scanner reader = new Scanner(System.in);
        // RuntimeMXBean object for reporting system uptime
        RuntimeMXBean runtime = ManagementFactory.getRuntimeMXBean();

        // Read data from files
        instantHumorEquals.prepareInstantHumorEqualsKeyPhrases();
        instantHumorContains.prepareInstantHumorContainsKeyPhrases();
        EmojiReactions.prepareEmojiReactions();
        AccessRestriction.loadPermissions();
        TodoModule.loadTodo();
        HelpModule.loadHelp();
        SpeakModule.loadMessages();

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

                // Send the event to the battleBot object out here because it needs to be able to respond to its own
                // messages, to use the edit function.
                battleBot.battle(event);

                // Only attempt to respond to messages if the message doesn't come from the bot
                if (message.getAuthor().getId() != selfID) {
                    // Send the event to the humorEquals object
                    humorEquals.run(event);
                    // Send the event to the humorContains object
                    humorContains.run(event);
                    // Send the event and api to the emojiReactions object
                    emojiReactions.run(event, api, permissions);
                    // Send the event to the karaokeBot object
                    karaokeBot.karaoke(event);
                    // Send the event to the todoModule object
                    todoModule.run(event);
                    // Send the event to the helpModule object
                    helpModule.run(event);
                    // Send the event to the speakModule object
                    speakModule.run(event);

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
                            String keycardColor = keycardColorAndUser.substring(0,keycardColorAndUser.indexOf("keycard ")-1);
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("keycard")+10, keycardColorAndUser.length()-1);
                            if (keycardUser.contains("!")) {
                                keycardUser = keycardUser.substring(1);
                            }
                            // dumb ass workaround
                            final String finalKeycardUser = keycardUser;
                            api.getUserById(keycardUser).thenAccept(user ->
                                    channel.sendMessage(permissions.addUser(finalKeycardUser, user.getName(), keycardColor)));
                        }
                    }

                    // !revoke <color> keycard <user>
                    // Removes a user's permission color
                    if (messageToString.startsWith("!revoke ")) {
                        if (permissions.doesUserHaveAccess((String.valueOf(message.getAuthor().getId())), "blue")) {
                            // Trim message to obtain <color> and <user>
                            String keycardColorAndUser = messageToString.substring(8);
                            String keycardColor = keycardColorAndUser.substring(0, keycardColorAndUser.indexOf("keycard ")-1);
                            String keycardUser = keycardColorAndUser.substring(keycardColorAndUser.indexOf("keycard") + 10, keycardColorAndUser.length()-1);
                            if (keycardUser.contains("!")) {
                                keycardUser = keycardUser.substring(1);
                            }
                            // Print result
                            channel.sendMessage(permissions.removeUser(keycardUser,keycardColor));
                        }
                    }

                    // I'm not actually sure if this is necessary.
                    if (messageToString.startsWith("!keywords ")) {
                        EmojiReactions.getKeywords(message);
                    }

                    // uptime command
                    if (messageToString.equalsIgnoreCase("!uptime")) {
                        double uptime = runtime.getUptime();
                        String unit = "milliseconds";
                        if (uptime > 1000) {
                            uptime /= 1000;
                            unit = "seconds";
                            if (uptime > 60) {
                                uptime /= 60;
                                unit = "minutes";
                                if (uptime > 60) {
                                    uptime /= 60;
                                    unit = "hours";
                                    if (uptime > 24) {
                                        uptime /= 24;
                                        unit = "days";
                                    }
                                }
                            }
                        }
                        String value = String.format("%.3f", uptime);
                        channel.sendMessage("Trashbot has been up for " + value + " " + unit + ". wow!");
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
                channel.sendMessage(pickString("Hey hey, " + user + ", welcome to the server.", "whoa hey lol " + user + " just joined",
                        "hey, was that the wind or did I just hear " + user + " come in?", "lol u bitches better watch out, " + user + "'s here and they're ready to fuck shit up aye",
                        "yo sup " + user, "hey what's kickin, " + user + "?"));
            });

            api.addUserStartTypingListener(event -> {
               if ((int) (Math.random() * 1000) == 1) {
                   System.out.println("");
                   event.getChannel().sendMessage("get ready for the dopest fuckin message you're about to ever read in your entire life");
               }
            });

            api.addReactionAddListener(event -> {
                if (event.getUser().getId() != selfID) {
                    Reaction messageReaction = null;
                    if (event.getReaction().isPresent()) {
                        messageReaction = event.getReaction().get();
                    }
//                    if (messageReaction.getEmoji().isUnicodeEmoji()) {
//                        if (messageReaction.getEmoji().asUnicodeEmoji().get().equals("\uD83D\uDE44")) {
//                            if ((int) (Math.random() * 3) == 1) {
//                                event.getChannel().sendMessage("fuck off you sarcastic piece of shit eye roll motherfucker grow the fuck up nobody likes you");
//                                System.out.println("dice!");
//                            } else {
//                                System.out.println("no dice on the eye roll clapback");
//                            }
//                        }
//                    }
                    battleBot.battle(event);
                }
            });
            // Print boot success
            System.out.println("Boot success!");
        }).exceptionally(ExceptionLogger.get());


    }

    private static String pickString(String... set) {
        int rand = (int)(Math.random()*(set.length-1));
        return set[rand];
    }
}