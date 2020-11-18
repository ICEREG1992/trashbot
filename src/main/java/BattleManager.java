import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.event.message.reaction.ReactionAddEvent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class BattleManager {

    private Map<String, Battle> battleMap;
    private static final Logger logger = LogManager.getLogger(BattleManager.class);

    BattleManager() {
        battleMap = new HashMap<>();
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.equals("!battle")) {
            addBotBattle(message.getAuthor().getIdAsString(), channel);
        } else if (messageToString.startsWith("!battle <@")) {
            addUserBattle(message.getAuthor().getIdAsString(), "" + helperFunctions.getFirstMentionID(message), channel);
        } else if (message.getAuthor().isYourself() && messageToString.startsWith("battle")) {
            String userID = messageToString.substring(6);
            battleMap.get(userID).initialize(message);
        }
    }

    public void run(ReactionAddEvent event) {
        String userID = event.getUser().getIdAsString();
        if (battleMap.containsKey(userID)) {
            event.getReaction().ifPresent(reaction -> sendToBattle(userID, reaction));
        }
    }

    private void addBotBattle(String userID, TextChannel channel) {
        cleanBattles();
        if (!battleMap.containsKey(userID)) {
            Battle addBattle = new BattleB(channel, userID);
            battleMap.put(userID, addBattle);
            logger.info("Bot battle started for " + userID + ".");
        } else {
            channel.sendMessage("yo chill you're already fighting me bro");
        }
    }

    private void addUserBattle(String userID, String enemyID, TextChannel channel) {
        cleanBattles();
        if (!battleMap.containsKey(userID)) {
            Battle addBattle = new BattleU(channel, userID);
            battleMap.put(userID, addBattle);
            battleMap.put(enemyID, addBattle);
            logger.info("User battle started for " + userID + " against " + enemyID + ".");
        } else {
            channel.sendMessage("calm down one guy at a time dude");
        }
    }

    private void cleanBattles() {
        ArrayList<String> cleanStrings = new ArrayList<>();
        for (String userID : battleMap.keySet()) {
            if (battleMap.get(userID).isDead()) {
                cleanStrings.add(userID);
            }
        }
        for (String clean : cleanStrings) {
            battleMap.remove(clean);
            logger.info("Battle ended for " + clean + ".");
        }
    }

    private void sendToBattle(String userID, Reaction reaction) {
        battleMap.get(userID).battle(userID, reaction);
    }
}
