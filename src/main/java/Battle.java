import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;

interface Battle {

    String BLANK = "<:blank:445505783224991747>";
    String GREEN = "<:green:482986420668071937>";
    String HALFGREEN = "<:halfgreen:482986735073230848>";
    String PURPLE = "<:purple:482986438195937291>";
    String HALFPURPLE = "<:halfpurple:482986748926885908>";
    String ATTACK_EMOJI = "⚔";
    String HEAL_EMOJI = "\uD83D\uDC8A";
    String RUN_EMOJI = "\uD83C\uDFC3";
    String PUNCH_EMOJI = "\uD83D\uDCA5";
    String ROBOT_EMOJI = "\uD83E\uDD16";
    String HOSPITAL = "\uD83D\uDE91";
    String[] DEAD_EMOJI = {"\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43"};
    String[] WIN_EMOJI = {"\uD83D\uDE01", "☺️", "\uD83D\uDE24"};
    String[] NORMAL_EMOJIS = {"\uD83D\uDE20", "\uD83D\uDE2C", "\uD83E\uDD2A", "\uD83E\uDD14"};
    String[] HURT_EMOJIS = {"\uD83D\uDE23", "\uD83D\uDE1F", "\uD83D\uDE22", "\uD83E\uDD12", "\uD83E\uDD15", "\uD83E\uDD22"};

    void initialize(Message message);

    void battle(String userID, Reaction reaction);

    boolean isDead();
}
