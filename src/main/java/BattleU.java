import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.Reaction;

class BattleU extends BattleB{

    private int leftHealth = 0;
    private int rightHealth = 0;
    private boolean active = false;
    private boolean turn = false; // false for left's turn, true for right's turn
    private String leftID;
    private String leftEmoji;
    private String rightEmoji;
    private StringBuilder healthBar = new StringBuilder();

    private static String[] attackResponse = {"oh damn he goin in!", "worldstar!!", "worldstar!", "oh get him!", "yea show him the 1-2 mayweather!", "3-4 mcgreggor!!!", "yo beat the shit outta him!", "yooooooooo!!!!!!!", "show him what fer!", "ohh damn!"};
    private static String[] healResponse = {"he chargin up!", "ohkay!", "oh damnn!", "ok bro he finna heal right up then!", "weird flex but ok", "ooh!", "he need some milk!!", "you aint even seen his final form yet!!!"};
    private static String[] runResponse = {"sorta anticlimactic but ok", "coward ass! take this on ur way out!", "fuckin lame-o!", "pussy bitch! take this aye!", "oh so now u finna back down!?", "loser!"};
    private static String[] promptResponse = {"ohkay what next tho!", "brooo hit him back!", "damn bro swing at him!", "HIT HIMMM!!", "AIGHT!", "LES GOOO", "*bruh*!!", "u just gon let him do that!?!", "what u gon do next tho!?"};
    private static String[] startResponse = {"swing first bro, swing first!", "whoa okay guys settle down a lil", "oh he doin it!", "bro someone start recording this gonna be wicked", "broooooooooo"};

    private Message battleMessage = null;

    BattleU(TextChannel textChannel, String userID) {
        super(textChannel, userID);
        this.leftID = userID;
    }

    public void initialize(Message message) {
        this.battleMessage = message;
        this.battleMessage.addReaction(ATTACK_EMOJI);
        this.battleMessage.addReaction(HEAL_EMOJI);
        this.battleMessage.addReaction(RUN_EMOJI);
        this.battleMessage.edit(helperFunctions.pickString(startResponse));
        helperFunctions.botWait();
        this.leftEmoji = helperFunctions.pickString(NORMAL_EMOJIS);
        this.rightEmoji = helperFunctions.pickString(NORMAL_EMOJIS);
        this.leftHealth = ((int) (Math.random() * 10) * 2) + 10;
        this.rightHealth = ((int) (Math.random() * 10) * 2) + 10;
        this.active = true;
        this.healthBar = new StringBuilder();

        updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
        this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + helperFunctions.pickString("Pick a button bro lets go!", "Aight frosh pick a button!"));
    }

    public void battle(String userID, Reaction reaction) {
        if (reaction.getEmoji().isUnicodeEmoji()) {
            if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals(ATTACK_EMOJI)) {
                if (userID.equals(leftID) && !turn) {
                    attack();
                }
                if (!userID.equals(leftID) && turn){
                    rightAttack();
                }
            }
            else if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals(HEAL_EMOJI)) {
                if (userID.equals(leftID) && !turn) {
                    heal();
                }
                if (!userID.equals(leftID) && turn){
                    rightHeal();
                }
            }
            else if (reaction.getEmoji().asUnicodeEmoji().isPresent() && reaction.getEmoji().asUnicodeEmoji().get().equals(RUN_EMOJI)) {
                if (userID.equals(leftID) && !turn) {
                    run();
                }
                if (!userID.equals(leftID) && turn){
                    rightRun();
                }
            }
        }
    }

    //left attack on right side
    protected void attack() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            this.rightEmoji = PUNCH_EMOJI;
            // SHOW right as boom emoji (don't change right health yet)
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(attackResponse));
            // decrease right health for next show
            this.rightHealth -= damage;
            this.rightEmoji = helperFunctions.pickString(HURT_EMOJIS);
            helperFunctions.botWait();
            // SHOW right as hurt, health has been lowered
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(promptResponse));

            if (this.rightHealth <=0) {
                // set left emoji to proud face
                this.leftEmoji = helperFunctions.pickString(WIN_EMOJI);
                // set right emoji to skull, ghost, or upside down face
                this.rightEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\nAnd <@" + this.leftID + "> wins!!!");
                this.battleMessage.removeAllReactions();
                this.active = false;
            }
            this.turn = !this.turn;
        }
    }

    private void rightAttack() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            // SHOW left as boom emoji (don't change right health yet)
            this.leftEmoji = ATTACK_EMOJI;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(attackResponse));
            // decrease right health for next show
            this.leftHealth -= damage;
            this.leftEmoji = helperFunctions.pickString(HURT_EMOJIS);
            helperFunctions.botWait();
            // SHOW right as hurt, health has been lowered
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(promptResponse));

            if (leftHealth <=0) {
                // set right emoji to proud face
                this.rightEmoji = helperFunctions.pickString(WIN_EMOJI);
                // set left emoji to skull, ghost, or upside down face
                this.leftEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\nLOL! <@" + this.leftID + "> you got your ass kicked bro!");
                this.battleMessage.removeAllReactions();
                this.active = false;
            }
            this.turn = !this.turn;
        }
    }

    protected void heal() {
        if (this.active) {
            // set left emoji to hospital, health has not been raised
            this.leftEmoji = HOSPITAL;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar); // this is probably not necessary
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(healResponse));
            helperFunctions.botWait();
            int heal = ((int)(Math.random() * 12) + 4);
            this.leftHealth += heal;
            if (this.leftHealth > 30) {
                this.leftHealth = 30;
            }
            // set user emoji back to regular, health has been raised
            this.leftEmoji = helperFunctions.pickString(NORMAL_EMOJIS);
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(promptResponse));
            // nobody can die during this turn because nobody loses health, so no need for if statement here.
            this.turn = !this.turn;
        }
    }

    private void rightHeal() {
        if (this.active) {
            // set right emoji to hospital, health has not been raised
            this.rightEmoji = HOSPITAL;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar); // this is probably not necessary
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(healResponse));
            helperFunctions.botWait();
            int heal = ((int)(Math.random() * 12) + 4);
            this.rightHealth += heal;
            if (this.rightHealth > 30) {
                this.rightHealth = 30;
            }
            // set right emoji back to regular, health has been raised
            this.rightEmoji = helperFunctions.pickString(NORMAL_EMOJIS);
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(promptResponse));
            // nobody can die during this turn because nobody loses health, so no need for if statement here.
            this.turn = !this.turn;
        }
    }

    protected void run() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            this.battleMessage.removeAllReactions();
            this.leftHealth -= damage;
            this.leftEmoji = PUNCH_EMOJI;
            // SHOW user punch (leftHealth has changed)
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit (this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(runResponse));
            if (leftHealth <=0) {
                // set user emoji to skull, ghost, or upside down face
                this.leftEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\nLOL! <@" + this.leftID + "> you got your ass kicked bro!");
            }
            this.active = false;
            helperFunctions.botWait();
            // set user emoji to running
            this.leftEmoji = RUN_EMOJI;
            this.leftHealth = 0;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\nNext time you come round here you better up your game, pussy bitch.");
        }
    }

    private void rightRun() {
        int damage = ((int)(Math.random() * 5) + 5);
        if (this.active) {
            this.battleMessage.removeAllReactions();
            this.rightHealth -= damage;
            this.rightEmoji = PUNCH_EMOJI;
            // SHOW right punch (rightHealth has changed)
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit((this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\n" + helperFunctions.pickString(runResponse)));
            if (rightHealth <= 0) {
                // set right emoji to skull, ghost, or upside down face
                this.rightEmoji = helperFunctions.pickString(DEAD_EMOJI);
                // SHOW battle end
                updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
                this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\nAnd <@" + this.leftID + "> wins!!!");
            }
            this.active = false;
            helperFunctions.botWait();
            // set right emoji to running
            this.rightEmoji = RUN_EMOJI;
            this.rightHealth = 0;
            updateHealthBar(this.leftHealth, this.rightHealth, this.healthBar);
            this.battleMessage.edit(this.leftEmoji + ":" + this.healthBar + ":" + this.rightEmoji + "\nNext time you come round here you better up your game, pussy bitch.");
        }
    }
}
