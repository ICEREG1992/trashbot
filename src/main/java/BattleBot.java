import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.event.message.reaction.ReactionAddEvent;

// IMPORTANT

// THIS FILE IS DEPRECIATED. CURRENTLY HELD IN THE FILE DIRECTORY JUST IN CASE SOMETHING GOES HORRIBLY WRONG
// AND WE LOSE SOMETHING

public class BattleBot {

    public BattleBot() {
    }

    private int health = 0;
    private int botHealth = 0;
    private int choice = 0;
    private String userEmoji = "";
    private String healthBar = "";

    private Message startMessage = null;

    private static final long selfID = 450507364768940034L;
    private static final long willID = 132374584086364160L;
    private static final String BLANK = "<:blank:445505783224991747>";
    private static final String GREEN = "<:green:482986420668071937>";
    private static final String HALFGREEN = "<:halfgreen:482986735073230848>";
    private static final String PURPLE = "<:purple:482986438195937291>";
    private static final String HALFPURPLE = "<:halfpurple:482986748926885908>";


    private Message battleMessage = null;

    public void battle(MessageCreateEvent event) {
        TextChannel channel = event.getChannel();
        Message message = event.getMessage();
        String messageToString = message.getContent().toLowerCase();

        if (messageToString.equals("!battle") && message.getAuthor().getId()!=selfID) {
            channel.sendMessage("§§§");

            startMessage = message;
        }

        if (messageToString.equals("§§§") && message.getAuthor().getId()==selfID) {
            battleMessage = message;
            battleMessage.addReaction("⚔");
            battleMessage.addReaction("\uD83D\uDC8A");
            battleMessage.addReaction("\uD83C\uDFC3");
            if (choice != -1) {
                battleMessage.edit(helperFunctions.pickString("Let's fuckin fight then boi", "aight bet!!!", "fuckin come get me mf!",
                        "let's go! start swingin bro!", "oh you really wanna go? u really wanna go!?"));
                botWait();
                userEmoji = "";
                if (startMessage.getAuthor().getId() == willID) {
                    userEmoji = "<:william:457350683927117826>";
                } else {
                userEmoji = helperFunctions.pickString("\uD83D\uDE20", "\uD83D\uDE2C", "\uD83E\uDD2A", "\uD83E\uDD14");
                }
                health = ((int) (Math.random() * 10) * 2) + 10;
                botHealth = ((int) (Math.random() * 10) * 2) + 10;
                choice = -1;

                System.out.println("Battle started!");
                healthBar = healthString(health, botHealth);
                battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\nWhat do you do? >!attack >!heal >!run");
            } else {
                channel.sendMessage(helperFunctions.pickString("Whoa there, buddy. I'm already fighting someone.", "easy there frosh chill a sec lemme finish fighting someone else",
                        "Ok lol chill out", "ok i'm already fighting someone rn chill a little"));
            }
        }
    }

    public void battle(ReactionAddEvent event) {
        Reaction messageReaction = null;
        if (event.getReaction().isPresent()) {
            messageReaction = event.getReaction().get();
        }
        if (messageReaction.getEmoji().isUnicodeEmoji()) {
            if (messageReaction.getEmoji().asUnicodeEmoji().get().equals("⚔")) {
                int[] update = attack(health, botHealth, choice, userEmoji, healthBar, battleMessage);
                health = update[0];
                botHealth = update[1];
                choice = update[2];
            }
            else if (messageReaction.getEmoji().asUnicodeEmoji().get().equals("\uD83D\uDC8A")) {
                int[] update = heal(health, botHealth, choice, userEmoji, healthBar, battleMessage);
                health = update[0];
                botHealth = update[1];
                choice = update[2];
            }
            else if (messageReaction.getEmoji().asUnicodeEmoji().get().equals("\uD83C\uDFC3")) {
                int[] update = run(health, botHealth, choice, userEmoji, healthBar, battleMessage);
                health = update[0];
                botHealth = update[1];
                choice = update[2];
            }
        }
    }

    private static int[] attack(int health, int botHealth, int choice, String userEmoji, String healthBar, Message battleMessage) {
        int damage = ((int)(Math.random() * 5) + 5);
        if (choice != 0) {
            battleMessage.removeAllReactions();
            // SHOW bot punch (don't change health yet)
            healthBar = healthString(health, botHealth);
            battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83D\uDCA5\n" + helperFunctions.pickString("ow fuck!", "ow jeez dude!", "oof!", "ouchie!", "fuck jeez ow!"));
            // decrease bot health for next show
            botHealth -= damage;
            botWait();
            // set user emoji to punch for next show
            userEmoji = "\uD83D\uDCA5";
            // SHOW user punch (bot health has changed
            healthBar = healthString(health, botHealth);
            battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("take that!", "take this frosh!", "get a taste of my knuckle sandwich!", "take that bro!", "ok take this aye!"));
            // decrease user health for next show
            damage = ((int)(Math.random() * 5) + 5);
            health -= damage;
            botWait();
            if (botHealth<=0) {

                userEmoji = helperFunctions.pickString("\uD83D\uDE01", "☺️", "\uD83D\uDE24");
                // SHOW battle end
                healthBar = healthString(health, botHealth);
                battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nOh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                battleMessage.removeAllReactions();
                choice = 0;
                System.out.println("Battle ended!");
            } else if (health<=0) {
                // set user emoji to skull, ghost, or upside down face
                userEmoji = helperFunctions.pickString("\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43");
                // SHOW battle end
                healthBar = healthString(health, botHealth);
                battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                battleMessage.removeAllReactions();
                choice = 0;
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
        int[] out = {health, botHealth, choice};
        return out;
    }

    private static int[] heal(int health, int botHealth, int choice, String userEmoji, String healthBar, Message battleMessage) {
        int damage = ((int)(Math.random() * 5) + 5);
        if (choice != 0) {
            battleMessage.removeAllReactions();

            // set user emoji to punch
            userEmoji = "\uD83D\uDCA5";
            // SHOW user punch
            healthBar = healthString(health, botHealth);
            battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("take that!", "take this frosh!", "this boutta do so much damage", "take that bro!", "ok take this aye!"));
            botWait();
            health -= damage;
            // set user emoji to hurt
            userEmoji = helperFunctions.pickString("\uD83D\uDE23", "\uD83D\uDE1F", "\uD83D\uDE22", "\uD83E\uDD12", "\uD83E\uDD15", "\uD83E\uDD22");
            // SHOW new health
            healthBar = healthString(health, botHealth);
            battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("yeet", "lol haha", "esketit bro", "aight frosh"));
            botWait();
            int heal = ((int)(Math.random() * 10) + 7);
            health += heal;
            if (health > 30) {
                health = 30;
            }
            // set user emoji to hospital
            userEmoji = "\uD83D\uDE91";
            healthBar = healthString(health, botHealth);
            battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("o", "oh ok", "thats sorta unfair but ok", "oh", "oh no"));
            botWait();
            if (botHealth<=0) {
                userEmoji = helperFunctions.pickString("\uD83D\uDE01", "☺️", "\uD83D\uDE24");
                // SHOW battle end
                healthBar = healthString(health, botHealth);
                battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nOh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                battleMessage.removeAllReactions();
                choice = 0;
                System.out.println("Battle ended!");
            } else if (health<=0) {
                // set user emoji to skull, ghost, or upside down face
                userEmoji = helperFunctions.pickString("\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43");
                // SHOW battle end
                healthBar = healthString(health, botHealth);
                battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                battleMessage.removeAllReactions();
                choice = 0;
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
        int[] out = {health, botHealth, choice};
        return out;
    }

    private static int[] run(int health, int botHealth, int choice, String userEmoji, String healthBar, Message battleMessage) {
        int damage = ((int)(Math.random() * 5) + 5);
        if (choice != 0) {
            battleMessage.removeAllReactions();
            health -= damage;
            userEmoji = "\uD83D\uDCA5";
            // SHOW user punch (bot health has changed
            healthBar = healthString(health, botHealth);
            battleMessage.edit (userEmoji + ":" + healthBar + ":\uD83E\uDD16\n" + helperFunctions.pickString("coward ass! take this on ur way out!", "fuckin lame-o!", "pussy bitch! take this aye!", "oh so now u finna back down!?", "loser!"));
            if (health<=0) {
                // set user emoji to skull, ghost, or upside down face
                userEmoji = helperFunctions.pickString("\uD83D\uDC80", "\uD83D\uDC7B", "\uD83D\uDE43");
                // SHOW battle end
                healthBar = healthString(health, botHealth);
                battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                choice = 0;
                System.out.println("Battle ended!");
            }
            choice = 0;
            System.out.println("Battle ended!");
            botWait();
            // set user emoji to running
            userEmoji = "\uD83C\uDFC3";
            health = 0;
            healthBar = healthString(health, botHealth);
            battleMessage.edit(userEmoji + ":" + healthBar + ":\uD83E\uDD16\nNext time you come round here you better up your game, pussy bitch. <:restinpepperoni:412754423257890827>");
        }
        int[] out = {health, botHealth, choice};
        return out;
    }
    /*---------------------------------------Helper Functions-----------------------------------------------*/

    // Method that pauses the bot for 1 second
    private static void botWait() {
        try {
            Thread.sleep(1500);
        } catch (InterruptedException e) {
            System.out.println("bot's broke, boss");
        }
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
