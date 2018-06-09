import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class EmojiReactions {
    public static Map<ArrayList<String>, String> emojisAndKeywords = new HashMap<>();

    public static File file;

    public EmojiReactions(String filename) {
        file = new File(filename);
    }

    public void run() {

    }

    public static void prepareEmojiReactions() {
        ArrayList<String> keys = new ArrayList<>();
        String isMoreData = "";
        Scanner in = null;
        try {
            in = new Scanner(file);
        } catch (FileNotFoundException e) {
            System.out.println("EmojiReactions was unable to locate the file: " + e);
        }

        do {
            String key = in.nextLine();
            String value = "";
            keys.clear();
            do {
                keys.add(key);
                System.out.println(key);
                key = in.nextLine();
            } while (!key.equals(""));
            value = in.nextLine();

            System.out.println(keys);
            System.out.println(value);
            emojisAndKeywords.put(keys,value);
            isMoreData = in.nextLine();
        } while (!isMoreData.equals("***"));

        System.out.println(emojisAndKeywords);
    }
}
