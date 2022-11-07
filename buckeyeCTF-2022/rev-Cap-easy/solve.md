# Challenge
## Description
Someone got rid of my macros and now my program won't compile fr fr
## Resource
A C file: Cap.c
# Step
We need to guess all the macro in the C file, let's start!  
At first, because each line end with `fr`, it is safe to say `fr` is `;`.  
Then we can assume that there are 4 functions in file, `brutus`, `kinda`, `wilin` and `main`.  
Thus, obviously the `finna` is `{`, `tho` is `}`, `af` is `)` and `ongod` is `(`.  
Then, I look forward to block (which mean code surrounded by `{}`), and I found some blocks starts with `boutta`, `poppin`, `tryna` or `respectfully`. 
Normally, the start of block in C could be `for`, `while`, `do-while`, `if` or `else`.
- For `poppin`, we can see in it's `()`, there are three variable and one int. So that, we can assume it is `for`, because the usual form of for is `for(int i = 0; i < 10; i ++){}`.  
- For `boutta`, we can see one variable and one value, thus we can assume it is `while` or `if`. But in the `cap.c#L86`, it appear after `}`, thus, it cannot be `if`.  
- For `tryna`, we can see one variable followed by one value. So that, we can assume `tryna` is `if`.  
- For `respectfully`, the only usage is with `while`. Thus, it must be `do`.  

Then, look back to function, I notice that `legit` and `lit` are two kinds of function return types. In addition, in last block of function `brutus`, the only code line start with a variable. Thus there isn't a `return` in `brutus`. So that, it is safe to say that `legit` is `void`.  
Then, I check for `lit`. Because `legit` is `void`, `lit` cannot be `void`. In codes of main, the last line of codes is `deadass cap;`. So that, I assume `deadass` is `return`, and `lit` is type of `cap`. Normally, the return of `main` is `void` or `int`. Thus, I assume `lit` is `int` and `cap` is 0.  
Back to `brutus` function, in the L42, it is safe to say that it is a assignment code. So that, `clean` is a type and `lookin` is `=`. Because `cap` is int, `clean` could be `int`.  
Now look to `main` function, because `flag` equal to a string, I guess `clean` is `char` and `yeet rn` equal to `[ ]` (because people use `char[]` or `char*` to save a string in C).  
Back to `brutus`, in the second line of `brutus`, because `poppin` is `for`, I guess `lowkey` is `<` and `playin` is `++` (because i start from 0 to 11).  
In the L50 `mf ongod x dub bussin af lookin val fr fr`, `mf` is still totally unknown for me, and I guess `dub` is calculation operator and `bussin` is a number value.  
In the L60, I guess `wack` and `lackin` also is a calculation operator.  
In L92, it is obviously that `downbad` is `--` (because `downbad` only can be `++` or `--`).  
In L120, we can see that program print a string, thus, I guess `sheeeesh` is `printf`.  
In L145 to L147, we can see the program pass the address of `flag` `dub` a number value. Thus, I guess `dub` is `+` because it isn't reasonable to pass a start address of an array `-`, `*` or `/` another value.  
Thus, in L92, because `dub` is `+` and `boutta`, it is reasonable for `bussin` equal to `1`.  
For `no`, the usage is L130, and it is obviously that `no` is `!`.  
For `be`, according to L72, I assume `be` is `==`.  
For `like`, according to L92, I assume `like` is `||` (because i cannot equal to 5 and 6).  
For `highkey`, according to L86 and `lowkey` is `<`, I assume `highkey` is `>`.  
For `chill`, in L73, because it in `for`, I assume `chill` is `break` or `continue`. But it is not meaningful if `chill` is `break`, because there are codes for i == 8 under, and i will not be 8 if `chill` is `break`. 
For `yikes`, I search whole program, it is not a usage of it. So it is safe to comment it.   

Here is hard part:
It is diffcult to determine `mf` and the codes from L133 and L138.  
After thinking for a while (maybe >10 mins), I realize that the codes between L133 and L138 is ternary operator (`(condition)?statement1:statement2;`).  
Thus, `drip` is `:` and `sus` is `?`.  
And the only possible value for `mf` is `*`, because after a type and variable name, the only possible text is `*` (pointer type).  

Also, `wack` also is hard to determine, I decide to try all the calculation operator except `+` and `-`. So, I start with `/` and it works.  

# Solution
```C
#define cap 0
#define lit int
#define bussin 1
#define no !
#define sus ?
#define fr ;
#define legit void
#define finna {
#define be ==
#define boutta while
#define bruh ,
#define deadass return
// #define yikes ??? no used
#define ongod (
#define clean char
#define yeet [
#define mf *
#define tryna if
#define tho }
#define respectfully do
#define like ||
#define lackin -
#define poppin for
#define drip :
#define rn ]
#define chill continue
#define af )
#define lowkey <
#define sheeeesh printf
#define lookin =
#define downbad --
#define playin ++
#define wack /
#define dub +
#define highkey >
```