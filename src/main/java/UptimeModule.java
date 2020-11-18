import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.util.Scanner;

public class UptimeModule {

    private File file;
    private double recordUptime;

    // RuntimeMXBean object for reporting system uptime
    private RuntimeMXBean runtime = ManagementFactory.getRuntimeMXBean();
    private static final Logger logger = LogManager.getLogger(UptimeModule.class);

    UptimeModule(String filename) {
        file = new File(filename);
        loadUptime();
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        org.javacord.api.entity.message.Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.equalsIgnoreCase("!uptime")) {
            double currentUptime = runtime.getUptime();
            boolean record = false;
            if (currentUptime > recordUptime) {
                record = true;
                recordUptime = currentUptime;
                save();
                logger.info("New uptime record! " + millisToString(recordUptime));
            }
            String uptimeOut = millisToString(currentUptime);
            channel.sendMessage(helperFunctions.pickString("Trashbot has been up for " + uptimeOut + ". wow!",
                    "ya boi's been going for " + uptimeOut + " aye!", "choo choo! this train's been goin for like " + uptimeOut + " or smth!",
                    "uh probably like " + uptimeOut + " or something idk", "thanks for asking! i've been up for " + uptimeOut + "."));
            if (record) {
                channel.sendMessage(helperFunctions.pickString("hey, that's a new record!", "whoa, i've never been up that long before!",
                        "ding ding! thas a record!"));
            }
        } else if (messageToString.equalsIgnoreCase("!recorduptime")) {
            String recordOut = millisToString(recordUptime);
            channel.sendMessage(helperFunctions.pickString("the longest i've been up is " + recordOut + "!",
                    "my current record for staying awake is " + recordOut + "!", "my longest uptime is " + recordOut + ", but i bet i could do better!"));
        }
    }

    private void save() {
        PrintWriter out = null;
        try {
            out = new PrintWriter(file);
        } catch (FileNotFoundException e) {
            logger.error("File " + file + " not found: ");
        }
        if (out != null) {
            out.println(recordUptime);
            out.close();
        }
    }

    private void loadUptime() {
        Scanner fileReader = null;
        try {
            fileReader = new Scanner(file);
        } catch (FileNotFoundException e) {
            logger.error("File " + file + " not found: ");
        }
        if (fileReader != null && fileReader.hasNextLine()) {
            recordUptime = fileReader.nextDouble();
            fileReader.close();
        }
        logger.info("Uptime data loaded.");
    }

    private static String millisToString(double millis) {
        String unit = "milliseconds";
        if (millis > 1000) {
            millis /= 1000;
            unit = "seconds";
            if (millis > 60) {
                millis /= 60;
                unit = "minutes";
                if (millis > 60) {
                    millis /= 60;
                    unit = "hours";
                    if (millis > 24) {
                        millis /= 24;
                        unit = "days";
                    }
                }
            }
        }
        return String.format("%.3f " + unit, millis);
    }
}
