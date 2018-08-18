import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

public class HelpModule {
    private static File file;

    private static ArrayList<String> helpList = new ArrayList<>();

    public HelpModule(String filename) {
        file = new File(filename);
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.startsWith("!help ")) {
            String todo = messageToString.substring(messageToString.indexOf(" ") + 1);
            helpList.add(todo);
            save();
            channel.sendMessage("added to todo list. get to work bud");
        } else if (messageToString.startsWith("!todoclear ")) {
            int index = Integer.parseInt(messageToString.substring(messageToString.indexOf(" ") + 1)) - 1;
            if (index >= 0 && index < helpList.size()) {
                helpList.remove(index);
            }
            save();
            channel.sendMessage("removed from todo list. good job man im proud of ya");
        } else if (messageToString.equals("!todo")) {
            channel.sendMessage("ok here's what needs to be done");
            String out = "";
            for (int i = 0; i < helpList.size(); i++) {
                out+= i+1 + ": " + helpList.get(i) + "\n";
            }
            channel.sendMessage(out);
        }
    }

    // TODO: Finish save() method
    public static String save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        for (String objective : helpList) {
            out.println(objective);
        }

        out.close();
        return "New todo data saved.";
    }

    public static void loadTodo() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        while (fileReader.hasNextLine()) {
            helpList.add(fileReader.nextLine());
        }
    }
}
