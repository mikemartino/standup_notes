![](images/standup-notes.png)

A simple way to capture notes for your daily standup meetings.

https://mikemartino.github.io/standup_notes/

## Installation
### From source

```
python3 -m pip install pipenv 
python3 setup.py install --user
```
### From PyPi

```
pip3 install standup-notes
```

## Run
 ```
standup-notes --l
standup-notes --list
 ``` 
 will list commands that can be run by the script

 ```
standup-notes --r
standup-notes --read
 ``` 
will print out the stand up note based on the date flag passed

```
standup-notes --read
standup-notes --copy
standup-notes --edit
```
#####Delete Notes
```
standup-notes --delete
```
Deletes all notes that are older then the date inputted



# Why? Why not?

__Tired__ of opening `nano` on your own?

__Forget__ if you like headings or italics for your standup section titles?

__Stuck__ in that weird `VISUAL MODE` in `vim` where you can't right-click copy and paste your notes into chat? Looking like a tool, because you aren't using the right ones.


***

_**Well, no more.**_

`standup-notes` to the rescue.

***

## Brag hard about your $EDITOR selection
 
Set your `$EDITOR` environment variable (in your __.bashrc__) to tell `standup-notes` and your friends, 

> "Yo playa', I use __X__ to edit my files. Like a boss!" 

## Only chumps right-click to _Copy and Paste_

You heard me. And I know you're no chump. Use `standup-notes` to seamlessly `--copy-today`'s notes and by ready for that meeting on the fly. So fly.

## I have kids. I don't sleep. My brain is basically just scrambled eggs. I use templates.

Get to the point. I can't remember what I like (italics vs. headings). I just do what my template tells me. 

Don't waste time with that cookie cutter garbagio. Get straight to the content. Leave the boilerplate to the tool. 
