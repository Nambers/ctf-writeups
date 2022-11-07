import java.io.Reader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Scanner;

// 
// Decompiled by Procyon v0.5.36
// 

public class soda
{
    static final int NUM_DRINKS = 12;
    static boolean bystanders;
    static float wallet;
    
    public static void main(final String[] array) {
        final VendingMachine vendingMachine = new VendingMachine();
        final Scanner scanner = new Scanner(System.in);
        System.out.println("\nThe prophecy states that worthy customers receive flags in their cans...");
        while (true) {
            System.out.println(invokedynamic(makeConcatWithConstants:(Lsoda$VendingMachine;)Ljava/lang/String;, vendingMachine));
            System.out.println(String.format("I have $%.02f in my wallet", soda.wallet));
            System.out.print("command> ");
            try {
                final String nextLine = scanner.nextLine();
                if (!nextLine.isEmpty()) {
                    processCommand(vendingMachine, nextLine.split(" "));
                    continue;
                }
            }
            catch (Exception ex) {}
            break;
        }
        System.out.println();
        scanner.close();
    }
    
    private static void processCommand(final VendingMachine vendingMachine, final String[] array) {
        if (array[0].equalsIgnoreCase("help")) {
            System.out.println(">> You're telling me you don't know how to use a vending machine?");
            return;
        }
        if (array[0].equalsIgnoreCase("purchase")) {
            if (array.length > 1) {
                try {
                    final int int1 = Integer.parseInt(array[1]);
                    if (int1 < 1 || int1 > 12) {
                        throw new RuntimeException();
                    }
                    vendingMachine.buy(int1 - 1);
                    return;
                }
                catch (Exception ex) {
                    System.out.println(">> That's not a real choice");
                    return;
                }
            }
            System.out.println(">> Purchase what?");
            return;
        }
        if (array[0].equalsIgnoreCase("punch")) {
            System.out.println(">> That's not a good idea");
            return;
        }
        if (array[0].equalsIgnoreCase("kick")) {
            System.out.println(">> That's a terrible idea");
            return;
        }
        if (array[0].equalsIgnoreCase("shake")) {
            System.out.println(">> That's the worst idea ever");
            return;
        }
        if (array[0].equalsIgnoreCase("shatter")) {
            System.out.println(">> What is wrong with you???");
            return;
        }
        if (array[0].equalsIgnoreCase("reach")) {
            if (soda.bystanders) {
                System.out.println(">> I can't do that with people around!\n>> They'll think I'm stealing!");
                return;
            }
            final int reach = vendingMachine.reach();
            vendingMachine.dropped += reach;
            if (reach > 0) {
                System.out.println(">> Ok, here goes... gonna reach through the door and try to knock it down...");
                pause(3);
                System.out.println(">> !!! I heard something fall!");
            }
            else {
                System.out.println(">> There's nothing to reach for");
            }
        }
        else {
            if (array[0].equalsIgnoreCase("wait")) {
                int int2;
                try {
                    int2 = Integer.parseInt(array[1]);
                }
                catch (Exception ex2) {
                    System.out.println(">> Not sure what you mean");
                    return;
                }
                pause(int2);
                if (int2 >= 10) {
                    soda.bystanders = false;
                    System.out.println(">> ...Looks like nobody's around...");
                }
                else {
                    soda.bystanders = true;
                    System.out.println(">> People are walking down the street.");
                }
                return;
            }
            if (array[0].equalsIgnoreCase("tap")) {
                System.out.println(">> Tapping the glass is harmless, right?");
                pause(1);
                vendingMachine.tap();
                System.out.println(">> Not sure if that helped at all...");
                return;
            }
            if (array[0].equalsIgnoreCase("grab")) {
                if (vendingMachine.dropped > 0) {
                    System.out.println(">> Alright!! Let's see what I got!");
                    vendingMachine.retrieve();
                }
                else {
                    System.out.println(">> There's nothing to grab...");
                }
                return;
            }
            System.out.println(">> Not sure what you mean");
        }
    }
    
    private static void printFlag() {
        try {
            final BufferedReader bufferedReader = new BufferedReader(new FileReader("flag.txt"));
            System.out.println(">> WOAH!! There's a flag in here!!");
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                System.out.println(line);
            }
        }
        catch (Exception ex) {
            System.out.println(">> You find a piece of paper in the can! It reads:");
            System.out.println("\n\t\"You are not worthy\"\n");
        }
    }
    
    private static void pause(final int n) {
        try {
            for (int i = 0; i < n; ++i) {
                System.out.print(". ");
                Thread.sleep(1000L);
            }
        }
        catch (Exception ex) {}
        System.out.println();
    }
    
    static {
        soda.bystanders = true;
        soda.wallet = 5.0f;
    }
    
    static class VendingMachine
    {
        Drink[] drinks;
        public int dropped;
        
        public VendingMachine() {
            this.drinks = new Drink[12];
            this.dropped = 0;
            for (int i = 0; i < 12; ++i) {
                this.drinks[i] = new Drink();
            }
        }
        
        public boolean hasDroppedDrinks() {
            for (int i = 0; i < 12; ++i) {
                if (this.drinks[i].status == Drink.DrinkStatus.DROPPED) {
                    return true;
                }
            }
            return false;
        }
        
        public void buy(final int n) {
            if (this.drinks[n].status != Drink.DrinkStatus.READY) {
                System.out.println(">> [OUT OF STOCK]");
                return;
            }
            if (soda.wallet > this.drinks[n].cost) {
                System.out.println(">> [VENDING]");
                soda.pause(5);
                System.out.println(">> ...Wait... IT'S STUCK?? NOOOOOO");
                this.drinks[n].status = Drink.DrinkStatus.STUCK;
                soda.wallet -= this.drinks[n].cost;
                return;
            }
            System.out.println(">> I don't have enough money :(");
        }
        
        public void tap() {
            for (int i = 0; i < 12; ++i) {
                if (this.drinks[i].status == Drink.DrinkStatus.STUCK && this.drinks[i].stuck > 0) {
                    final Drink drink = this.drinks[i];
                    --drink.stuck;
                }
            }
        }
        
        public int reach() {
            int n = 0;
            for (int i = 0; i < 12; ++i) {
                if (this.drinks[i].status == Drink.DrinkStatus.STUCK && this.drinks[i].stuck == 0) {
                    this.drinks[i].status = Drink.DrinkStatus.DROPPED;
                    ++n;
                }
            }
            return n;
        }
        
        public void retrieve() {
            int n = -1;
            float cost = -1.0f;
            for (int i = 0; i < 12; ++i) {
                if (this.drinks[i].status != Drink.DrinkStatus.EMPTY && this.drinks[i].cost > cost) {
                    n = i;
                    cost = this.drinks[i].cost;
                }
            }
            if (this.drinks[n].status == Drink.DrinkStatus.DROPPED) {
                soda.printFlag();
            }
            else {
                System.out.println(">> No flags in here... was the prophecy a lie...?");
            }
        }
        
        @Override
        public String toString() {
            String s = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, "-------".repeat(6));
            for (int i = 0; i < 6; ++i) {
                for (int j = 0; j < 6; ++j) {
                    s = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s, this.drinks[j].asText(j + 1)[i]);
                }
                s = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, s);
            }
            String s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s, "-------".repeat(6));
            for (int k = 0; k < 6; ++k) {
                for (int l = 6; l < 12; ++l) {
                    s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s2, this.drinks[l].asText(l + 1)[k]);
                }
                s2 = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, s2);
            }
            return invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s2, "-------".repeat(6));
        }
    }
    
    static class Drink
    {
        float cost;
        DrinkStatus status;
        int stuck;
        
        public Drink() {
            this.cost = (float)(Math.random() * 6.0);
            this.status = ((Math.random() > 0.75) ? DrinkStatus.EMPTY : DrinkStatus.READY);
            this.stuck = 3;
        }
        
        public String getCostLabel() {
            return String.format("%1.02f", this.cost);
        }
        
        public String[] asText(final int n) {
            final String[] array = { invokedynamic(makeConcatWithConstants:(ILjava/lang/String;)Ljava/lang/String;, n, (n < 10) ? "    " : "   "), "|      ", "|      ", "|      ", "|      ", invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, this.getCostLabel()) };
            if (this.status != DrinkStatus.EMPTY && this.status != DrinkStatus.DROPPED) {
                return new String[] { invokedynamic(makeConcatWithConstants:(ILjava/lang/String;)Ljava/lang/String;, n, (n < 10) ? "    " : "   "), "|  __  ", (this.status == DrinkStatus.STUCK) ? "| |**| " : "| |  | ", "| |__| ", "|      ", invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, this.getCostLabel()) };
            }
            return array;
        }
        
        enum DrinkStatus
        {
            EMPTY, 
            READY, 
            STUCK, 
            DROPPED;
        }
    }
}