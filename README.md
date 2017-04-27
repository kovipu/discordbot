# discordbot

This is a bot for Discord written in Python 3.
It uses an SQL database for user permissions and such
and a web based Admin UI made using Flask.

## Usage

Make required changes to `config.py.EXAMPLE` and rename it to `config.py`.
Now run `bot.py`:
```
$ python3 bot.py
```

## Available commands:
| command | function                       |
----------|---------------------------------
| test    | testing command                |
| help    | list available commands        |
| users   | list all users in the database |
