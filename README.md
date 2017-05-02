# discordbot
This is a bot for Discord written in Python 3. (Tested on Python 3.6)
It uses an SQL database for user permissions and such
and a web based Admin UI made using Flask.

## Available commands
| command | function                       |
----------|---------------------------------
| test    | testing command                |
| help    | list available commands        |
| users   | list all users in the database |
| files   | list all the files uploaded    |
| getfile | fetch a file from the server   |

## Usage
Requires uWSGI and Nginx
```
# mkdir /var/www/discordbot
# chown www-data:www-data /var/www/discordbot
# mkdir /srv/discordbot
# chown www-data:www-data /srv/discordbot
# sudo -u www-data uwsgi -s /tmp/discordbot.sock --manage-script-name --mount /=app:app --enable-threads
```
This makes the webapp run on the root level of your webserver.

If you didn't install uWSGI thru pip, add `plugin --python3` to the last command.

Now uWSGI is running in an unix socket. You'll want to use Nginx to server your app via HTTP on an actual socket.
Something like this in `/etc/nginx/sites-available/discordbot` should do the trick on Debian:
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / { try_files $uri @discordbot; }
        location @discordbot {
            include uwsgi_params;
            uwsgi_pass unix:/tmp/discordbot.sock;
        }
}
```
Now symlink the file to sites-enabled:
```
# ln -s /etc/nginx/sites-available/discordbot /etc/nginx/sites-enabled/discordbot
```
You may have to restart Nginx at this point.
