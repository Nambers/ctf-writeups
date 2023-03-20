# Employee 427: Compromised

## Description

This is the story of Employee 427

Employee 427 works all day, every day. This is because Employee 427 loves his job

Then one day, something strange happens

Something Employee 427 would never forget

The profits diagram that Employee 427 had put months together suddenly disappeared

Employee 427 was shocked, what could have happened? He thought to himself

Unsure what to do, Employee 427 has reached out to you, yes you, to figure out how his precious diagram could have vanished

The triage data can be found here

## Resources

triage data - data.zip \[provided by challenge\]  
output.txt  

# Steps

There are a lot of data and binary file in the zip file. Therefore, I try to find something interesting by using `grep -aPr` and some keywords.  

1. so I start in `[root]`
2. `grep -Pr "profit" > output.txt` (output in `output.txt`)
3. in these bunch of logs, I found an interesting line: `Users/emplo/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt:rm profits.jpg; #pastebin-dot-com-slash-75Muuu8m`
4. then open `Users/emplo/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt`:
   ```bash
   cd '.\Desktop\IMPORTANT DO NOT DELETE\'
   ls
   rm profits.jpg; #pastebin-dot-com-slash-75Muuu8m
   echo this dude is going to be so screwed at his meeting LOL
   exit
   ```  
5. then after opening the pastebin link `pastebin.com/75Muuu8m`, we got flag
