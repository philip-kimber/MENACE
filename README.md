
# MENACE

## What is MENACE?
*You may want to read the [Wikipedia article](https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_and_Crosses_Engine) or watch [this video](https://www.youtube.com/watch?v=R9c-_neaxeU), both of which explain it better than I can*

**MENACE** is essentially one of the first, and simplest, examples of machine learning. Being just a set of 304 matchboxes with coloured beads inside, over enough time it can learn to beat (mostly just draw with) even the strongest human opponents.

It stands for `Matchbox Educable Noughts And Crosses Engine`.

The premise is quite simple: the beads represent spaces on the board where MENACE can go, and each box represents one of the 304 unique positions the system can find itself, depending on where the player moves.

We pick a random bead to decide where MENACE moves. But it's not completely random because if MENACE wins, we increase the number of that colour bead in the box, making it *more likely* to move in that winning square. Conversely, when the system loses, we take away those beads, reducing the chance of it making that 'mistake' again!

MENACE learns from its successes and mistakes, and so over time learns a good strategy. It just requires quite a lot of work to operate the beads and the boxes and everything, so we use a computer program to help and keep track of how it is going.

## How does MENACE work?
Just thinking about the physical boxes (and not the computer at this stage), the process works as follows:
- MENACE moves first. Take the initial box and take out a random bead. This corresponds by the colour map (see below) to positions on the board, where it moves at places an `X` (MENACE is always `X` and the player is `O` to avoid confusion)
- Now it is the player's go. Let them place an `O` in any free space, as normal
- For MENACE's second go we need to find the correct box for the current game position. This is a bit tricky because the system treats all rotations and reflections of a board as the same, so it might take a bit of rotating to find the right one. But there are only 12 second-move boxes to choose from!
- Take out a random bead from this box, and (NB: rotating the colour map if the box was rotated) MENACE moves where the colour corresponds to. Keep these boxes out; don't put them back straight away
- Now it is the player's go again. We repeat the process of having a player move and then finding the right box, making MENACE's move. This goes on until someone has won or the game is a draw
- (If it gets to MENACE having a fifth move, there are of course no boxes, and it just goes in the only empty square)
- When the game is lost or won (or drawn), we look back at the boxes MENACE used and the beads chosen:
 - If MENACE won, we want to *reward* it for good moves, so we *add* 3 more beads of the colour it chose.
 - If MENACE lost, we want to *reduce the chance* that it makes bad moves again, so we *remove* 1 bead of that colour.
 - If the game was a draw, this is still better than losing, so we *reward* MENACE with 1 more bead of the chosen colour.

### The colour map
The rough colours of the beads are there, as are the single-letter descriptors of them that we will use in the program for logging and data entry purposes. They are e.g `red = 'r'` etc: the main surprises are `purple = 'u'` (because `p` is for pink) and `black = 'l'` (because `b` is for blue).

 - ![#b73e3a](https://via.placeholder.com/15/b73e3a/000000?text=+)
![#ce5223](https://via.placeholder.com/15/ce5223/000000?text=+)
![#dcc137](https://via.placeholder.com/15/dcc137/000000?text=+) `r o y`

 - ![#009273](https://via.placeholder.com/15/009273/000000?text=+)
![#104897](https://via.placeholder.com/15/104897/000000?text=+)
![#734b7d](https://via.placeholder.com/15/734b7d/000000?text=+) `g b u`

 - ![#FEC1F5](https://via.placeholder.com/15/FEC1F5/000000?text=+)
![#FFFFFF](https://via.placeholder.com/15/FFFFFF/000000?text=+)
![#000000](https://via.placeholder.com/15/000000/000000?text=+) `p w l`

 - `D` to denote a resignation by MENACE (more on this later)

## How we play a game, using the computer system
The reason we have the computer program running, logging and simulating every move is to avoid losing track of what's going on, and to make finding the right box a lot easier. This also provides us with a helpful tracker of how well MENACE is doing at learning the strategy.

Once on the main section of the program (see below for setup and configs etc.), you are provided with a prompt for a 'command':
```
Setup completed. Enter commands or try 'help' to see list
MENACE>
```
If you enter `game` (or `g` for short) as the command, the following happens:
```
MENACE>game

Find box #0
MENACE turn: Enter initial of bead colour:
```
The system helpfully tells you which box to choose a move from, and then asks you to input the 1-letter initial of the picked bead (as demonstrated on the colour map, e.g `b` or `r`):
```
Find box #0
MENACE turn: Enter initial of bead colour: b
MENACE moves in square 'b'
Player turn: Enter initial of move colour:
```
Everything that is going on is narrated in a helpful fashion. We enter the player's move (also as a colour), and then the system works out the next box needed. NB: when it comes to MENACE's move, the *colour bead picked might not be the square it moves in* and the system will show this - this happens if the board is rotated.
```
MENACE>game

Find box #0
MENACE turn: Enter initial of bead colour: b
MENACE moves in square 'b'
Player turn: Enter initial of move colour: l
Player moves in square 'l'
Find box #11
MENACE turn: Enter initial of bead colour: u
MENACE moves in square 'g'
Player turn: Enter initial of move colour: y
Player moves in square 'y'
Find box #120
MENACE turn: Enter initial of bead colour: w
MENACE moves in square 'u'
Game: MENACE wins
Beads: box #0, do +3 of 'b' coloured bead
Beads: box #11, do +3 of 'u' coloured bead
Beads: box #120, do +3 of 'w' coloured bead

MENACE>
```
This is the transcript of a whole game. At the end, the computer also spells out for us the bead changes we need to make for each box. This should be fairly self-explanatory.

### MENACE can die?
There is a little technicality when it comes to the bead changes surrounding what happens if a box becomes empty (due to MENACE losing too often). In this case, for most boxes (e.g fourth move boxes where the game is basically lost already), we say that MENACE *'resigns'* and let the player win.

If MENACE resigns, we type in - instead of the initial of the bead colour - just `D` (has to be capital) to signify resignation.

But if the very first box becomes empty - the one MENACE always starts with - we have a problem, because MENACE will never play again and has learnt that the best way to play Noughts and Crosses is just to give up before even getting started! Smart. But no good.

Instead, we say that if you are about to remove the last bead from the first box (this only applies to the first box), you leave it in regardless. The box can never be emptied. The computer program shows this as the following:
```
Beads: box #0, do -1 of 'r' coloured bead
Beads REVIVAL: leave 1 'r' coloured bead in box #0, to avoid MENACE dying
```

## Other functions of the MENACE program
There are some other functions of the program. It logs every game into an auto-generated `.json` log file, and can load from logs, as well as several other commands.
The `help` menu gives a brief overview:
```
MENACE>help
List of commands:

    exit: leave the program
    config: view the current configurations and change them
    game (also aliased as 'g'): run and log a game between the physical MENACE and a real opponent
    log: load a log file, playing the games in it
    simulate: simulate game(s) between the simulated MENACE and a simulated opponent
    results: print the list of game results, in order of when they were played (crude list print)
    beads: print the list of number of beads in first box as the games went on
```
We could explain what each of these does, but in the interests of brevity, it's just worth pointing out that the error handling of the inputs is not great. For example, something might ask:
```
Do you want to change these configs (1=yes, 0=no):
```
Don't put `yes` or `no` or something else; this will (at least until we get round to doing better input handling) cause an error.

## Getting started with the program
I recommend running it in the command line, rather than the Python IDLE. Save all the code `.py` files into one folder and open a `cmd` there:
```
python main.py
```
should do the trick.

It takes some time to get started - and first asks you to confirm the configurations - but eventually we make it to the main program loop:
```
Setup completed. Enter commands or try 'help' to see list
MENACE>
```
Where you can enter commands and begin to use the scripts to assist in running the MENACE system playing against human opponents.

---

```
philip-kimber
scorbett123

September 2021
```
