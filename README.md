Live at https://forwardfeed.github.io/ER-nextdex/static/

## What is it
A web application about the Elite Redux pokemon game, acts as a documentation. ER is made thanks to pret-pokeemerald hence all other games based on this work may reuse a significan part of this project.

## tldr; How to make all work
requires npm and nodejs
This will initialize the project
``` 
npm install
npm run build
npm run run 
```

then `nextdex_config.json` should appear and you need to edit the field project_root
`project_root` is the path of your Elite Redux folder.

```
# this will pull the latest into Alphatest
npm run run -- -sv 2 -rd -o Alphatest
```


## How it works more in details
There is two part in this project:

### 1. The data fetcher/aggregator/parser
from the source files of the game.

It requires TSC or any typescript compiler (transpiler) but more critically a nodeJS environnement.
No dependecies are used in this games.

Commands:
- build: just a shortcut to tsc
- run: will execute the program, see below for specification, if nothing is specified it will output in out/gameData.json with the path specified in nextdex_config.json using structure version 0

Run Arguments:
    - -o --output     : name of the output to gamedata{arg}.json
    - -ip --input-path: override the path of the root folder in nextdex_config.json
    - -sv --structure-version: indicate which version of the parsing alg to use, since the codebase evolves with the version, it may be necessary, it always be an integer so in the code you can do: if(version > 3 && version < 5) { read this way } else {read this way}
    - -so --sprites-only: Do not parse for gamedata.json and only outputs all the sprites of pokemon found in out/sprites, i advice to use the python script sprites_utils.py after used that.
    - -rd -redirect-data: Do not redirect gameData.json to /out/ but directly to the UI folder at /static/js/data/ 

Quick tip, if you use git on your pokemon project you can get back to a previous version with these bash commands
`git log  --all --grep='V0.0.1'` where `V0.0.1` is the message of a commit marking the version of the game. Copy the commit sha1 hash and then you can do
`git checkout 'the sha1 you got'`. Then now you can fetch the data with this software to then `git switch -` to get back to where you where originally.

By default the data is outputed to out/, you can change that with the variable OUTPUT in src/main.ts

### 2. The UI that uses this data
It requires an HTTP server since it uses JS modules. If you code with VSC for example you may uselive-server add-on.

Aside this it is just a static html web app

## Project Structure

### nextdex_config.json
It is created upon launching the data fetcher
Fields:
    - "project_root": absolute path of your game files, YOU MUST ADAPT THIS FIELD
    - "verified": automatic, will set itself to true if you fed a right project_root.

### src/ 
holds the gamefile parsing and compactify into a data called gameData.js, outputed to out/
Althougt it shouldn't, most of the parameters are inside the code and not as environnement variable or configuration files
You run it with npm or tsc

### target/
Build of the src/ application

### out/
Output dir by default of some files.

### static/
a simple vanilla js + jquery + css + HTML Web application, this is what is live and should be interacted with as a end user.


## Notes about images
The script I have in python in postbuild don't really work, I actually use the one I made https://github.com/ForwardFeed/taillow
there.

## Docker & DevDex
There's an experimental devDex and docker
the dev dex is a program that will use a webhook from a github repository to get informations on new pushes
on push, the nextdext reparse the file and output a new gameData. on a server that will be hosted only (would be great if it was password locked)

Handle the github token, in order to have the program to work with private repository a github token is needed.
the token is passed with the whole file configuration using docker secret files
--secret id=FILENAME,src=LOCAL_FILENAME