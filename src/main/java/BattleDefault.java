import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;

abstract class BattleDefault implements Battle {

    private String leftID;
    private boolean active;
    private String leftEmoji;
    private String rightEmoji;
    private int leftHealth;
    private int rightHealth;
    private Message battleMessage;
    private StringBuilder healthBar;

    BattleDefault(TextChannel textChannel, String userID) {

    }





    protected abstract void attack();
    protected abstract void heal();
    protected abstract void run();




}
