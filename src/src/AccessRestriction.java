import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.*;

public class AccessRestriction {
    private static File file;

    private static HashMap<String, Set<String>> permissions = new HashMap<>();

    public AccessRestriction(String filename) {
        file = new File(filename);
    }

    public static String addUser(String userID, String accessLevel) {
        permissions.get(accessLevel).add(userID);
        save();
        return "User <@" + userID + "> added to permission " + accessLevel;
    }

    public static String removeUser(String userID, String accessLevel) {
        permissions.get(accessLevel).remove(userID);
        save();
        return "User <@" + userID + "> removed from permission " + accessLevel;
    }

    public static boolean doesUserHaveAccess(String id, String accessLevel) {
        Set<String> users = permissions.get(accessLevel);

        return users.contains(id);
    }

    public static void loadPermissions() {
        Scanner in = null;

        Set<String> users;

        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + " not found: ");
        }
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
