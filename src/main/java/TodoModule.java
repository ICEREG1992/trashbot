import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class TodoModule {

    private static File file;
    private static final Logger botLogger = LoggerFactory.getLogger(TodoModule.class);
    private static ArrayList<String> todoList = new ArrayList<>();

    public TodoModule(String filename) {
        file = new File(filename);
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.startsWith("!todo ")) {
            String todo = messageToString.substring(messageToString.indexOf(" ") + 1);
            todoList.add(todo);
            save();
            channel.sendMessage("added to todo list. get to work bud");
            botLogger.info("New item added to todo list: " + todo);
        } else if (messageToString.startsWith("!todoclear ")) {
            int index = Integer.parseInt(messageToString.substring(messageToString.indexOf(" ") + 1)) - 1;
            if (index >= 0 && index < todoList.size()) {
                botLogger.info("Item removed from todo list: " + todoList.get(index));
                todoList.remove(index);
            }
            save();
            channel.sendMessage("removed from todo list. good job man im proud of ya");
        } else if (messageToString.equals("!todo")) {
            channel.sendMessage("ok here's what needs to be done");
            String out = "";
            for (int i = 0; i < todoList.size(); i++) {
                out+= i+1 + ": " + todoList.get(i) + "\n";
            }
            channel.sendMessage(out);
        }
    }

    public static String save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8));
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        for (String objective : todoList) {
            out.println(objective);
        }

        out.close();
        botLogger.info("New todo data saved.");
        return "New todo data saved.";
    }

    public static void loadTodo() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(file, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            System.out.println("File " + file + " not found: ");
        }
        while (fileReader.hasNextLine()) {
            todoList.add(fileReader.nextLine());
        }
        botLogger.debug("Todo data loaded successfully.");
    }
}
