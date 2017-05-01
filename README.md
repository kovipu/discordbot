# discordbot
This is a bot for Discord written in Python 3. (Tested on Python 3.6)
It uses an SQL database for user permissions and such
and a web based Admin UI made using Flask.

## Usage
Make required changes to `config.py.EXAMPLE` and rename it to `config.py`.
Now run `app.py`:
```
$ python3 app.py
```

## uWSGI & Nginx
```
# mkdir /var/www/discordbot
# chown www-data:www-data /var/www/discordbot
# mkdir /srv/discordbot
# chown www-data:www-data /srv/discordbot
# sudo -u www-data uwsgi -s /tmp/discordbot.sock --manage-script-name --mount /=app:app --enable threads
```
If you didn't install uWSGI thru pip, add `plugin --python3` to the last command.

## Available commands:
| command | function                       |
----------|---------------------------------
| test    | testing command                |
| help    | list available commands        |
| users   | list all users in the database |
| files   | list all the files uploaded    |
| getfile | fetch a file from the server   |
