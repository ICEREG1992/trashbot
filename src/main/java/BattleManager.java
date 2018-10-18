import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.event.message.reaction.ReactionAddEvent;

import java.util.HashMap;
import java.util.Map;

public class BattleManager {

    private Map<String, Battle> battleMap = new HashMap<>();

    public BattleManager() {
    }

    public void run(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.equals("!battle")) {
            addBattle(message.getAuthor().getIdAsString(), channel);
        } else if (message.getAuthor().isYourself() && messageToString.startsWith("user")) {
            String userID = messageToString.substring(4);
            battleMap.get(userID).initialize(message);
        }
    }

    public void run(ReactionAddEvent event) {
        String userID = event.getUser().getIdAsString();
        if (battleMap.containsKey(userID)) {
            sendToBattle(userID, event.getReaction().get());
        }
    }

    public void addBattle(String userID, TextChannel channel) {
        cleanBattles();
        if (!battleMap.containsKey(userID)) {
            Battle addBattle = new Battle(channel, userID);
            battleMap.put(userID, addBattle);
        }
    }

    public void cleanBattles() {
        for (String userID : battleMap.keySet()) {
            if (battleMap.get(userID).isDead()) {
                battleMap.remove(userID);
            }
        }
    }

    public void sendToBattle(String userID, Reaction reaction) {
        battleMap.get(userID).battle(reaction);
    }
}
