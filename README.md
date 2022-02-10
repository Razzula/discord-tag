# discord-tag

A Discord bot for hosting a game of tag. If the person who is 'It' mentions another user,  their role will pass on to the taggee. With a leaderboard that keeps track of how long each person has been it. A bot running this code will  be able to host the game on multiple servers, however the leaderboard will  only work for a single game on a single server, and so using this bot on multiple servers is not advised.

## Getting Started

### Prerequisites

This project was written for Python 3.10
- [discord.py](https://github.com/Rapptz/discord.py) will be required

The bot will require several permissions to function:

- Server Members Intent
- Manage Roles
- Read Messages/View Channels
- Send Messages
- Add Reactions

### Installing

Download the repository, and enter your bot's token into `token.txt`

### Using

To run the bot, run the `main.py` file.

To begin the game simply message `$setup` to a channel. 

The bot will create any required server roles that are missing. Assign the roles `PlayingTag` to all players, and `It` to one (the timer will not start until after the first tag). After the first tag the game will begin.

The leaderboard can be viewed using `$le` and reset using `$re`.

## License

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)