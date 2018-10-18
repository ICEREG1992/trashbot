import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;

public class Battle {

    private int health = 0;
    private int botHealth = 0;
    private int active = 0;
    private String userEmoji = "";
    private String healthBar = "";

    private Message startMessage = null;
    private Message battleMessage = null;
    private TextChannel messageChannel;

    private static final String willID = "132374584086364160";
    private static final String BLANK = "<:blank:445505783224991747>";
    private static final String GREEN = "<:green:482986420668071937>";
    private static final String HALFGREEN = "<:halfgreen:482986735073230848>";
    private static final String PURPLE = "<:purple:482986438195937291>";
    private static final String HALFPURPLE = "<:halfpurple:482986748926885908>";

    public Battle(TextChannel textChannel, String userID) {
        this.messageChannel = textChannel;
        messageChannel.sendMessage("user" + userID);
    }

    public void initialize(Message message) {
        this.battleMessage = message;
        this.battleMessage.addReaction("⚔");
        this.battleMessage.addReaction("\uD83D\uDC8A");
        this.battleMessage.addReaction("\uD83C\uDFC3");
        if (this.active == 0) {
            this.battleMessage.edit(helperFunctions.pickString("Let's fuckin fight then boi", "aight bet!!!", "fuckin come get me mf!",
                    "let's go! start swingin bro!", "oh you really wanna go? u really wanna go!?"));
            helperFunctions.botWait();
            this.userEmoji = helperFunctions.pickString("\uD83D\uDE20", "\uD83D\uDE2C", "\uD83E\uDD2A", "\uD83E\uDD14");
            this.health = ((int) (Math.random() * 10) * 2) + 10;
            this.botHealth = ((int) (Math.random() * 10) * 2) + 10;
            this.active = 1;

            System.out.println("Battle started!");
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("Pick a button bro lets go!", "What do you do frosh? Click a button let's fight bro!"));
        } else {
            this.messageChannel.sendMessage(helperFunctions.pickString("Whoa there, buddy. I'm already fighting someone.", "easy there frosh chill a sec lemme finish fighting someone else",
                    "Ok lol chill out", "ok i'm already fighting someone rn chill a little"));
            // this should not be reached?
        }
    }

    public void battle(Reaction reaction) {
        if (reaction.getEmoji().isUnicodeEmoji()) {
            if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals("⚔")) {
                attack();
            }
            else if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals("\uD83D\uDC8A")) {
                heal();
            }
            else if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals("\uD83C\uDFC3")) {
                run();
            }
        }
    }

    private void attack() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active == 1) {
            this.battleMessage.removeAllReactions();
            // SHOW bot punch (don't change health yet)
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83D\uDCA5\n" + helperFunctions.pickString("ow fuck!", "ow jeez dude!", "oof!", "ouchie!", "fuck jeez ow!"));
            // decrease bot health for next show
            this.botHealth -= damage;
            helperFunctions.botWait();
            // set user emoji to punch for next show
            this.userEmoji = "\uD83D\uDCA5";
            // SHOW user punch (bot health has changed
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("take that!", "take this frosh!", "get a taste of my knuckle sandwich!", "take that bro!", "ok take this aye!"));
            // decrease user health for next show
            damage = ((int)(Math.random() * 5) + 5);
            this.health -= damage;
            helperFunctions.botWait();
            if (this.botHealth<=0) {
                this.userEmoji = helperFunctions.pickString("\uD83D\uDE01", "☺️", "\uD83D\uDE24");
                // SHOW battle end
                this.healthBar = healthString(this.health, this.botHealth);
                this.battleMessage.edit(this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\nOh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                this.battleMessage.removeAllReactions();
                this.active = 0;
                System.out.println("Battle ended!");
            } else if (health<=0) {
                // set user emoji to skull, ghost, or upside down face
                userEmoji = helperFunctions.pickString("\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43");
                // SHOW battle end
                healthBar = healthString(health, botHealth);
                battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                battleMessage.removeAllReactions();
                active = 0;
                System.out.println("Battle ended!");
            } else {
                // set user emoji to hurt
                userEmoji = helperFunctions.pickString("\uD83D\uDE23", "\uD83D\uDE1F", "\uD83D\uDE22", "\uD83E\uDD12", "\uD83E\uDD15", "\uD83E\uDD22");
                healthBar = healthString(health, botHealth);
                battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\nWhat do you do? >!attack >!heal >!run");
                battleMessage.addReaction("⚔");
                battleMessage.addReaction("\uD83D\uDC8A");
                battleMessage.addReaction("\uD83C\uDFC3");
            }
        }
    }

    private void heal() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active == 1) {
            this.battleMessage.removeAllReactions();

            // set user emoji to punch
            this.userEmoji = "\uD83D\uDCA5";
            // SHOW user punch
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("take that!", "take this frosh!", "this boutta do so much damage", "take that bro!", "ok take this aye!"));
            helperFunctions.botWait();
            this.health -= damage;
            // set user emoji to hurt
            this.userEmoji = helperFunctions.pickString("\uD83D\uDE23", "\uD83D\uDE1F", "\uD83D\uDE22", "\uD83E\uDD12", "\uD83E\uDD15", "\uD83E\uDD22");
            // SHOW new health
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("yeet", "lol haha", "esketit bro", "aight frosh"));
            helperFunctions.botWait();
            int heal = ((int)(Math.random() * 10) + 7);
            this.health += heal;
            if (this.health > 30) {
                this.health = 30;
            }
            // set user emoji to hospital
            this.userEmoji = "\uD83D\uDE91";
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("o", "oh ok", "thats sorta unfair but ok", "oh", "oh no"));
            helperFunctions.botWait();
            if (this.botHealth<=0) {
                this.userEmoji = helperFunctions.pickString("\uD83D\uDE01", "☺️", "\uD83D\uDE24");
                // SHOW battle end
                this.healthBar = healthString(this.health, this.botHealth);
                this.battleMessage.edit(this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\nOh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                this.battleMessage.removeAllReactions();
                this.active = 0;
                System.out.println("Battle ended!");
            } else if (this.health<=0) {
                // set user emoji to skull, ghost, or upside down face
                this.userEmoji = helperFunctions.pickString("\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43");
                // SHOW battle end
                this.healthBar = healthString(this.health, this.botHealth);
                this.battleMessage.edit(this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                this.battleMessage.removeAllReactions();
                this.active = 0;
                System.out.println("Battle ended!");
            } else {
                // set user emoji to hurt
                this.userEmoji = helperFunctions.pickString("\uD83D\uDE23", "\uD83D\uDE1F", "\uD83D\uDE22", "\uD83E\uDD12", "\uD83E\uDD15", "\uD83E\uDD22");
                this.healthBar = healthString(this.health, this.botHealth);
                this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\nWhat do you do? >!attack >!heal >!run");
                this.battleMessage.addReaction("⚔");
                this.battleMessage.addReaction("\uD83D\uDC8A");
                this.battleMessage.addReaction("\uD83C\uDFC3");
            }
        }
    }

    private void run() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active == 1) {
            this.battleMessage.removeAllReactions();
            this.health -= damage;
            this.userEmoji = "\uD83D\uDCA5";
            // SHOW user punch (bot health has changed
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit (this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("coward ass! take this on ur way out!", "fuckin lame-o!", "pussy bitch! take this aye!", "oh so now u finna back down!?", "loser!"));
            if (health<=0) {
                // set user emoji to skull, ghost, or upside down face
                this.userEmoji = helperFunctions.pickString("\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43");
                // SHOW battle end
                this.healthBar = healthString(this.health, this.botHealth);
                this.battleMessage.edit(this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                this.active = 0;
                System.out.println("Battle ended!");
            }
            this.active = 0;
            System.out.println("Battle ended!");
            helperFunctions.botWait();
            // set user emoji to running
            this.userEmoji = "\uD83C\uDFC3";
            this.health = 0;
            this.healthBar = healthString(this.health, this.botHealth);
            this.battleMessage.edit(this.userEmoji + ":" + this.healthBar + ":\uD83E\uDD16\nNext time you come round here you better up your game, pussy bitch. <:restinpepperoni:412754423257890827>");
        }
    }

    public boolean isDead() {
        boolean out = false;
        if (this.active == 0) {
            out = true;
        }
        return out;
    }

    private static String healthString(int uHealth, int botHealth) {
        String out = "";
        if (uHealth < 0) {
            uHealth = 0;
        }
        if (botHealth < 0) {
            botHealth = 0;
        }
        int blank = (30-uHealth) + (30-botHealth);
        while (uHealth > 1) {
            out += GREEN;
            uHealth -= 2;
        }
        if (uHealth == 1) {
            out += HALFGREEN;
            blank--;
        }
        while (blank > 1) {
            out += BLANK;
            blank -= 2;
        }
        if (botHealth%2 != 0) {
            out += HALFPURPLE;
            botHealth -= 1;
        }
        while (botHealth > 0) {
            out += PURPLE;
            botHealth -= 2;
        }
        return out;
    }
}
