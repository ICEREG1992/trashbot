import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;

class BattleB implements Battle {

    private String leftID;
    private boolean active;
    private String leftEmoji;
    private String rightEmoji;
    private int leftHealth;
    private int rightHealth;
    private Message battleMessage;
    private StringBuilder healthBar;

    BattleB(TextChannel textChannel, String userID) {
        textChannel.sendMessage("user" + userID);
        this.leftID = userID;
    }

    public void initialize(Message message) {
        this.battleMessage = message;
        this.battleMessage.addReaction(ATTACK_EMOJI);
        this.battleMessage.addReaction(HEAL_EMOJI);
        this.battleMessage.addReaction(RUN_EMOJI);
        this.battleMessage.edit(helperFunctions.pickString("Let's fuckin fight then boi", "aight bet!!!", "fuckin come get me mf!",
                "let's go! start swingin bro!", "oh you really wanna go? u really wanna go!?"));
        helperFunctions.botWait();
        this.leftEmoji = helperFunctions.pickString(NORMAL_EMOJIS);
        this.rightEmoji = helperFunctions.pickString(ROBOT_EMOJI);
        this.leftHealth = ((int) (Math.random() * 10) * 2) + 10;
        this.rightHealth = ((int) (Math.random() * 10) * 2) + 10;
        this.active = true;
        this.healthBar = new StringBuilder();

        updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
        this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + helperFunctions.pickString("Pick a button bro lets go!", "What do you do frosh? Click a button let's fight bro!"));
    }

    public void battle(String userID, Reaction reaction) {
        if (userID.equals(this.leftID)) {
            if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals(ATTACK_EMOJI)) {
                attack();
            }
            else if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals(HEAL_EMOJI)) {
                heal();
            }
            else if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals(RUN_EMOJI)) {
                run();
            }
        }
    }

    protected void attack() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            // SHOW bot punch (don't change leftHealth yet)
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + PUNCH_EMOJI + "\n" + helperFunctions.pickString("ow fuck!", "ow jeez dude!", "oof!", "ouchie!", "fuck jeez ow!"));
            // decrease bot leftHealth for next show
            this.rightHealth -= damage;
            helperFunctions.botWait();
            // set user emoji to punch for next show
            this.leftEmoji = PUNCH_EMOJI;
            // SHOW user punch (bot leftHealth has changed
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\n" + helperFunctions.pickString("take that!", "take this frosh!", "get a taste of my knuckle sandwich!", "take that bro!", "ok take this aye!"));
            // decrease user leftHealth for next show
            damage = ((int)(Math.random() * 5) + 5);
            this.leftHealth -= damage;
            helperFunctions.botWait();
            if (this.rightHealth <=0) {
                this.leftEmoji = helperFunctions.pickString(WIN_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\nOh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                this.battleMessage.removeAllReactions();
                this.active = false;
            } else if (leftHealth <=0) {
                // set user emoji to skull, ghost, or upside down face
                leftEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                battleMessage.edit(leftEmoji + ":" + healthBar + ":" + ROBOT_EMOJI + "\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                battleMessage.removeAllReactions();
                active = false;
            } else {
                // set user emoji to hurt
                leftEmoji = helperFunctions.pickString(HURT_EMOJIS);
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                battleMessage.edit (leftEmoji + ":" + healthBar + ":" + ROBOT_EMOJI + "\nWhat do you do? >!attack >!heal >!run");
            }
        }
    }

    protected void heal() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            // set user emoji to punch
            this.leftEmoji = PUNCH_EMOJI;
            // SHOW user punch
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\n" + helperFunctions.pickString("take that!", "take this frosh!", "this boutta do so much damage", "take that bro!", "ok take this aye!"));
            helperFunctions.botWait();
            this.leftHealth -= damage;
            // set user emoji to hurt
            this.leftEmoji = helperFunctions.pickString(HURT_EMOJIS);
            // SHOW new leftHealth
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\n" + helperFunctions.pickString("yeet", "lol haha", "esketit bro", "aight frosh"));
            helperFunctions.botWait();
            int heal = ((int)(Math.random() * 10) + 7);
            this.leftHealth += heal;
            if (this.leftHealth > 30) {
                this.leftHealth = 30;
            }
            // set user emoji to hospital
            this.leftEmoji = HOSPITAL;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\n" + helperFunctions.pickString("o", "oh ok", "thats sorta unfair but ok", "oh", "oh no"));
            helperFunctions.botWait();
            if (this.rightHealth <=0) {
                this.leftEmoji = helperFunctions.pickString(WIN_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\nOh shit, fuck, ow. You whooped my ass pretty hard. gg <:oof:418944392124956682>");
                this.active = false;
            } else if (this.leftHealth <=0) {
                // set user emoji to skull, ghost, or upside down face
                this.leftEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                this.active = false;
            } else {
                // set user emoji to hurt
                this.leftEmoji = helperFunctions.pickString(HURT_EMOJIS);
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\nWhat do you do? >!attack >!heal >!run");
            }
        }
    }

    protected void run() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            this.leftHealth -= damage;
            this.leftEmoji = PUNCH_EMOJI;
            // SHOW user punch (bot leftHealth has changed
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\n" + helperFunctions.pickString("coward ass! take this on ur way out!", "fuckin lame-o!", "pussy bitch! take this aye!", "oh so now u finna back down!?", "loser!"));
            if (leftHealth <=0) {
                // set user emoji to skull, ghost, or upside down face
                this.leftEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\nYou fall to your bitch ass and die. Fuckin rest in pepperonis bro <:restinpepperoni:412754423257890827>");
                this.active = false;
            }
            this.active = false;
            helperFunctions.botWait();
            // set user emoji to running
            this.leftEmoji = RUN_EMOJI;
            this.leftHealth = 0;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + ROBOT_EMOJI + "\nNext time you come round here you better up your game, pussy bitch. <:restinpepperoni:412754423257890827>");
        }
    }

    static void updateHealthBar(int leftHealth, int rightHealth, StringBuilder healthBar) {
        if (healthBar.length() != 0 ) {
            healthBar.delete(0,healthBar.length());
        }

        if (leftHealth < 0) {
            leftHealth = 0;
        }
        if (rightHealth < 0) {
            rightHealth = 0;
        }
        int blank = (30-leftHealth) + (30-rightHealth);
        while (leftHealth > 1) {
            healthBar.append(GREEN);
            leftHealth -= 2;
        }
        if (leftHealth == 1) {
            healthBar.append(HALFGREEN);
            blank--;
        }
        while (blank > 1) {
            healthBar.append(BLANK);
            blank -= 2;
        }
        if (rightHealth%2 != 0) {
            healthBar.append(HALFPURPLE);
            rightHealth -= 1;
        }
        while (rightHealth > 0) {
            healthBar.append(PURPLE);
            rightHealth -= 2;
        }
    }

    public boolean isDead() {
        boolean out = false;
        if (!this.active) {
            out = true;
        }
        return out;
    }

}
