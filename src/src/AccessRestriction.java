import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class AccessRestriction {
    private static File file;

    private static HashMap<String, Set<String>> permissions = new HashMap<>();

    public AccessRestriction(String filename) {
        file = new File(filename);
    }

    public static String addUser(String userID, String accessLevel) {
        permissions.get(accessLevel).add(userID);
        return "User " + userID + " added to permission " + accessLevel;
    }

    public static boolean doesUserHaveAccess(String id, String accessLevel) {
        Set<String> users = permissions.get(accessLevel);

        return users.contains(id);
    }

    public static void loadPermissions() {
        Scanner in = null;

        Set<String> users = new HashSet<>();

        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("File " + file + "not found: ");
        }

        String permissionLevel = in.nextLine();

        while(!permissionLevel.equals("***")) {
            String user = in.nextLine();

            do {
                users.clear();
                users.add(user);
                user = in.nextLine();
            } while (!user.equals(""));
            permissions.put(permissionLevel,users);
        }

        System.out.println("Permissions successfully loaded.");
    }

    // TODO: Finish save() method
    public static String save() {

        return "New permissions data successfully saved.";
    }
}
