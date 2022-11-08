# Challenge
## description
I definitely made a Git repo, but I somehow broke it. Something about not getting a HEAD of myself.  
## resources
A zip compressed file of git repository: what-you-see-is-what-you-git.zip
# Step
At first, I try to use `git log` to check history, but it fail: `fatal: your current branch 'main' does not have any commits yet`.  
Then, I open `.git/logs/HEAD` to check history manually.  
Result:
```
0000000000000000000000000000000000000000 30b26c2c7e8d48612cc5f6da4a374e262ccf860c NOT Gent Semaj  <jim@bo.hacked> 1667608995 -0400	commit (initial): Initial commit
30b26c2c7e8d48612cc5f6da4a374e262ccf860c 02417f390d6d72ad68082cd243760461aa3bd42a Shannon's Man <peanut@butter.jellytime> 1667609597 -0400	commit: Added Andy Warhol effect to file

7ae8453a76a41d40bdfcc7992175390f70ba9fdf c4681c8d561653cee9ecbea5d5ca5629adfd67a4 Matthew Ayers <matt@matthewayers.com> 1667704926 -0400	commit: Hid the flag
```
Thus, I checkout to the commit before the "hid the flag" commit.  

# Solution
```shell
git reset --hard 7ae8453a76a41d40bdfcc7992175390f70ba9fdf
```
And then, see the content of flag