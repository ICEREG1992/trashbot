import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class HelpModule {
    private static final String helpMessage = "**Hi!** I'm Trashbot. I'm a friendly guy and can do many things.\n\n" +
            "Here are some commands (you can use \"!help <command>\" for more information):\n" +
            "```!help\n" +
            "!ban <user>\n" +
            "!add <keyword> <emoji>\n" +
            "!remove <keyword> <emoji>\n" +
            "!printall\n" +
            "!give <color> keycard <@user>\n" +
            "!revoke <color> keycard <@user>\n" +
            "!keycard <color>\n" +
            "!keywords <emoji>\n" +
            "!containsadd <keyword> § <response>\n" +
            "!containsremove <keyword>\n" +
            "!equalsadd <keyword> § <response>\n" +
            "!equalsremove <keyword>\n" +
            "!karaoke\n" +
                "\t!givelyrics <lyrics>\n" +
                "\t!exit\n" +
            "!battle\n" +
            "!todo <suggestion>\n" +
            "!todoclear <entry number>\n" +
            "!speak\n" +
                "\t!quit\n" +
            "!uptime\n" +
            "!recorduptime\n" +
            "!devsendmessage <message>\n" +
            "!fuck you\n" +
            "nah u good\n" +
            "!buckbumble\n" +
            "/rule34\n" +
            "@trashbot\n" +
            "trashbot\n" +
            "good work, trashbot\n" +
            "shut the fuck up\n" +
            "literally stop\n" +
            "(literally anything involving money)\n" +
            "black```";

    private static File file;

    private static Map<String, String> helpList = new HashMap<>();

    public HelpModule(String filename) {
        file = new File(filename);
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.startsWith("!help ")) {
            String uCommand = messageToString.substring(messageToString.indexOf(" ") + 1);
            if (helpList.containsKey(uCommand)) {
                String description = helpList.get(uCommand);
                channel.sendMessage(description);
            } else {
                channel.sendMessage("that command doesn't seem to exist. try adding an ! or check spelling?");
            }
        } else if (messageToString.equalsIgnoreCase("!help")) {
            channel.sendMessage(helpMessage);
        }
    }

    public static String save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        for (String key : helpList.keySet()) {
            out.println(key);
            out.println(helpList.get(key));
            out.println();
        }

        out.close();
        return "New todo data saved.";
    }

    public static void loadHelp() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        while (fileReader.hasNextLine()) {
            helpList.put(fileReader.nextLine(), fileReader.nextLine());
            if (fileReader.hasNextLine()) {
                fileReader.nextLine();
            }
        }
    }
}
