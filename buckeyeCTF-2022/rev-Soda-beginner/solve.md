# Challenge
## Description
Man, I'm parched. I sure hope this vending machine doesn't suck...
```
nc pwn.chall.pwnoh.io 13375
```
## resources
A jar file: Soda
# Steps
## decompile
At first, I find a random jar deompile website(just google "jar deompile online"), and get the decompile java file (`soda.java`).  
## analyze
In order to find where this program print the flag, I search for the text "flag" in java file: I found `printFlag()` function which will print out the flag.  
Then, I check the usage for `printFlag()`: the only usage is in `retrieve()` in `soda.java#L234`.  
Then, I check the conditions in `retrieve()` of calling `printFlag()`: `this.drinks[n].status == Drink.DrinkStatus.DROPPED`.  
Then, I check what is the value of `n`: the `n` is the id of one not empty drink with highest price.  
Then, I check where change the status to dropped (by simpely search the text "Drink.DrinkStatus.DROPPED"): in `reach()` and the conditions are `this.drinks[i].status == Drink.DrinkStatus.STUCK && this.drinks[i].stuck == 0`.  
Then, I check where the status change to stuck: in `buy()`, after you purchased a drink, it's status will be stuck, and the stuck variable is 3 initially.  
Then, I check where stuck variable assign to zero: in `tap()`, after you tab, it's stuck variable will decrease by one.  
Okay, so I got all conditions so far.  
Then I check when this program will call `buy`, `tap`, `retrieve`, and `reach`: the calling condition of first three functions is simple, you need to input `purchase`, `tap`, `grab` to call them.  
But for `reach`, it need you input `reach` and `soda.bystanders` variable equal to false (or zero).  
So that, I check where the `soda.bystanders` assign to zero: In `wait()`, if you wait for more than 10 seconds, the `bystanders` will be zero.  
Alright, so here is the condition to get flag:  
```
connect and reconnect to server until the highest price of all drink is lower than 5
buy the drink with highest drink
wait 11
tap for at least 3 times
reach
grab
```

# Solution
```
The prophecy states that worthy customers receive flags in their cans...

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |  __  |  __  |  __  |
| |  | | |  | | |  | | |  | | |  | | |  | |
| |__| | |__| | |__| | |__| | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $5.00 in my wallet
command> purchase 4
>> [VENDING]
. . . . .
>> ...Wait... IT'S STUCK?? NOOOOOO

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |  __  |  __  |  __  |
| |  | | |  | | |  | | |**| | |  | | |  | |
| |__| | |__| | |__| | |__| | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
command> wait 11
. . . . . . . . . . .
>> ...Looks like nobody's around...

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |  __  |  __  |  __  |
| |  | | |  | | |  | | |**| | |  | | |  | |
| |__| | |__| | |__| | |__| | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
command> tap
>> Tapping the glass is harmless, right?
.
>> Not sure if that helped at all...

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |  __  |  __  |  __  |
| |  | | |  | | |  | | |**| | |  | | |  | |
| |__| | |__| | |__| | |__| | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
command> tap
>> Tapping the glass is harmless, right?
.
>> Not sure if that helped at all...

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |  __  |  __  |  __  |
| |  | | |  | | |  | | |**| | |  | | |  | |
| |__| | |__| | |__| | |__| | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
command> tap
>> Tapping the glass is harmless, right?
.
>> Not sure if that helped at all...

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |  __  |  __  |  __  |
| |  | | |  | | |  | | |**| | |  | | |  | |
| |__| | |__| | |__| | |__| | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
command> reach
>> Ok, here goes... gonna reach through the door and try to knock it down...
. . .
>> !!! I heard something fall!

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
command> grab
>> Alright!! Let's see what I got!
>> WOAH!! There's a flag in here!!
buckeye{w3_c411_7h3_s7uff_"p0p"_h3r3}

-------------------------------------------
| 1    | 2    | 3    | 4    | 5    | 6    |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.71 | 4.30 | 4.53 | 1.59 | 2.79 |
-------------------------------------------
| 7    | 8    | 9    | 10   | 11   | 12   |
|  __  |  __  |  __  |      |  __  |  __  |
| |  | | |  | | |  | |      | |  | | |  | |
| |__| | |__| | |__| |      | |__| | |__| |
|      |      |      |      |      |      |
| 1.55 | 3.10 | 4.41 | 4.80 | 3.77 | 0.46 |
-------------------------------------------

I have $0.47 in my wallet
```
