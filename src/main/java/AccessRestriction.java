import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

class AccessRestriction {
    private File file;
    private HashMap<String, Set<String>> permissions = new HashMap<>();

    private static final Logger logger = LogManager.getLogger(AccessRestriction.class);

    AccessRestriction(String filename) {
        file = new File(filename);
        loadPermissions();
    }

    void addUser(String userID, String name, String accessLevel) {
        if (permissions.containsKey(accessLevel)) {
            permissions.get(accessLevel).add(userID + "§" + name);
            logger.info("User <@" + userID + "> added to permission " + accessLevel);
        } else {
            Set<String> tempAdd = new HashSet<>();
            tempAdd.add(userID + "§" + name);
            permissions.put(accessLevel, tempAdd);
            logger.info("New keycard color created: " + accessLevel + ", user <@" + userID + "> has been added.");
        }
        save();
    }

    void removeUser(String userID, String accessLevel) {
        boolean found = false;
        for (String userIDAndName : permissions.get(accessLevel)) {
            if (userIDAndName.startsWith(userID)) {
                found = true;
                permissions.get(accessLevel).remove(userIDAndName);
                logger.info("User <@" + userID + "> removed from permission " + accessLevel);
                if (permissions.get(accessLevel).size() == 0) {
                    permissions.remove(accessLevel);
                    logger.info("Permission level " + accessLevel + " is now empty, and has been deleted.");
                }
            }
        }
        if (!found) {
            logger.warn("User <@" + userID + "> does not have that keycard!");
        }
        save();
    }

    Set<String> getUsers(String accessLevel) {
        Set<String> out = new HashSet<>();
        if (permissions.containsKey(accessLevel)) {
            out = permissions.get(accessLevel);
        }
        return out;
    }

    boolean doesUserHaveAccess(String id, String... accessLevels) {
        boolean found = false;
        for (String level : accessLevels) {
            Set<String> users = permissions.get(level);
            for (String userIDAndName : users) {
                if (userIDAndName.startsWith(id)) {
                    found = true;
                }
            }
        }
        return found;
    }

    private void loadPermissions() {
        Scanner in = null;

        Set<String> users;

        try {
            in = new Scanner(file, StandardCharsets.UTF_8).useDelimiter("\n");
        } catch (IOException e) {
            logger.error("File " + file + " not found: ");
        }
        if (in != null && in.hasNextLine()) {
            try {
                String permissionLevel = in.nextLine();

                while (!permissionLevel.equals("***")) {
                    users = new HashSet<>();
                    String user = in.nextLine();

                    do {
                        users.add(user);
                        user = in.nextLine();
                    } while (!user.equals(""));
                    permissions.put(permissionLevel, users);
                    permissionLevel = in.nextLine();
                }
                logger.info("Permissions loaded.");
            } catch (NoSuchElementException e) {
                logger.error("Incorrect formatting in " + this.file.getName() + ", correctly formatted entries have been loaded.");
            }
            in.close();
        }
    }

    private void save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8));
        } catch (FileNotFoundException e) {
            logger.error("File " + file + " not found: ");
        }

        if (out != null) {
            for (Map.Entry<String, Set<String>> permissionLevel : permissions.entrySet()) {
                String level = permissionLevel.getKey();
                Set<String> members = permissionLevel.getValue();
                out.println(level);
                for (String name : members) {
                    out.println(name);
                }
                out.println();
            }
            out.print("***");
            out.close();
        }

        logger.info("New permissions data saved.");
    }
}
