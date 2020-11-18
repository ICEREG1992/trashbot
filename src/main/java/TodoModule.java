import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class TodoModule {

    private static File file;
    private static final Logger botLogger = LogManager.getLogger(TodoModule.class);
    private static ArrayList<String> todoList = new ArrayList<>();

    TodoModule(String filename) {
        file = new File(filename);
        loadTodo();
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.startsWith("!todo ")) {
            String todo = messageToString.substring(messageToString.indexOf(" ") + 1);
            todoList.add(todo);
            channel.sendMessage("added to todo list. get to work bud");
            botLogger.info("New item added to todo list: " + todo);
            save();
        } else if (messageToString.startsWith("!todoclear ")) {
            int index = Integer.parseInt(messageToString.substring(messageToString.indexOf(" ") + 1)) - 1;
            if (index >= 0 && index < todoList.size()) {
                String remove = todoList.get(index);
                todoList.remove(index);
                botLogger.info("Item removed from todo list: " + remove);
            }
            save();
            channel.sendMessage("removed from todo list. good job man im proud of ya");
        } else if (messageToString.equals("!todo")) {
            channel.sendMessage("ok here's what needs to be done");
            StringBuilder outString = new StringBuilder();
            for (int i = 0; i < todoList.size(); i++) {
                outString.append(i+1).append(": ").append(todoList.get(i)).append("\n");
            }
            if (todoList.size() == 0) {
                outString.append("uuuhhhhh.... nothing! nice, man. get some sleep.");
            }
            channel.sendMessage(outString.toString());
        }
    }

    private void save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8));
        } catch (FileNotFoundException e) {
            botLogger.error("File " + file + " not found: ");
        }
        if (out != null) {
            for (String objective : todoList) {
                out.println(objective);
            }
            out.close();
            botLogger.info("New todo data saved.");
        }
    }

    private void loadTodo() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(file, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            botLogger.error("File " + file + " not found: ");
        }
        if (fileReader != null) {
            while (fileReader.hasNextLine()) {
                todoList.add(fileReader.nextLine());
            }
            fileReader.close();
            botLogger.info("Todo data loaded.");
        }
    }
}
