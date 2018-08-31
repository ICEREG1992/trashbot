import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.*;

public class AccessRestriction {
    private static File file;

    private static HashMap<String, Set<String>> permissions = new HashMap<>();

    public AccessRestriction(String filename) {
        file = new File(filename);
    }

    public static String addUser(String userID, String name, String accessLevel) {
        String out = "";
        if (permissions.containsKey(accessLevel)) {
            permissions.get(accessLevel).add(userID + "§" + name);
            out = "User <@" + userID + "> added to permission " + accessLevel;
        } else {
            Set<String> tempAdd = new HashSet<>();
            tempAdd.add(userID + "§" + name);
            permissions.put(accessLevel, tempAdd);
            out = "New keycard color created: " + accessLevel + ", user <@" + userID + "> has been added.";
        }
        save();
        return out;
    }

    public static String removeUser(String userID, String accessLevel) {
        String out = "";
        boolean found = false;
        for (String userIDAndName : permissions.get(accessLevel)) {
            if (userIDAndName.startsWith(userID)) {
                found = true;
                permissions.get(accessLevel).remove(userIDAndName);
                out = "User <@" + userID + "> removed from permission " + accessLevel;
                if (permissions.get(accessLevel).size() == 0) {
                    permissions.remove(accessLevel);
                    out+=". " + accessLevel + " is now empty, and has been deleted.";
                }
            }
        }
        if (!found) {
            out = "User <@" + userID + "> does not have that keycard!";
        }
        save();
        return out;
    }

    public static Set<String> getUsers(String accessLevel) {
        Set<String> out = new HashSet<>();
        if (permissions.containsKey(accessLevel)) {
            out = permissions.get(accessLevel);
        }
        return out;
    }

    public static boolean doesUserHaveAccess(String id, String... accessLevels) {
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

    public static void loadPermissions() {
        Scanner in = null;

        Set<String> users;

        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
        if (in.hasNextLine()) {
            String permissionLevel = in.nextLine();

            while(!permissionLevel.equals("***")) {
                users = new HashSet<>();
                String user = in.nextLine();

                do {
                    users.add(user);
                    user = in.nextLine();
                } while (!user.equals(""));
                permissions.put(permissionLevel,users);
                permissionLevel = in.nextLine();
            }
        }


        System.out.println("Permissions successfully loaded.");
    }

    // TODO: Finish save() method
    public static String save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }

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
        return "New permissions data successfully saved.";
    }
}
