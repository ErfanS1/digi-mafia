This is going to be a mafia party game app.

so far developed:
    some routes of creating user and authorization with jwt token, only backend side.
    routes of add roles and players to game.
    routes of starting the game and assigning roles to players.

assist to Moderator part is almost Done.

to be developed: actions of the game like nights actions, different logic of the game and rules.

Hope it brings some joy to people !

Setting Up the Environment:
Mac:
1 - first you need to install homebrew. you can get help from here https://www.igeeksblog.com/how-to-install-homebrew-on-mac/ 
it's an open source package manager for mac.
2 - now you need to install postgresql, with or without brew. 
    brew install postgresql@15
3 - you need to install pip3 if you already don't have.
4 - in the folder of the project, set up a virtual env. you can install it with pip.
5 - activate the venv.
    source {venv-name}/bin/activate
6 - install the requirements.
    pip3 install -r requirements.txt
7 - install Docker desktop for mec. https://docs.docker.com/get-docker/
8 - now just use docker-compose command to run the postgres container.
    docker-compose up -d
9 - now start the fastapi main with uvicorn server.
    uvicorn main:app --reload
10 - everything's ready to test now. use the swagger to work with APIs.
    localhost:8000/docs/

Linux:
for linux its kind of the same approach and steps are the same!

feel free to message me if something went wrong and you couldn't figure it out yourself.