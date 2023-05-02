#!/usr/bin/env bash
# A script that sets up your web servers for the deployment of web_static

# Install Nginx if it is not already installed
if [ $(dpkg-query -W -f='${Status}' nginx 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    apt-get -y update
    apt-get -y install nginx
fi

# Create the necessary directories if they don't exist
if [ ! -d /data/web_static/releases/test ];
then
    mkdir -p /data/web_static/releases/test
fi

if [ ! -d /data/web_static/shared ];
then
    mkdir -p /data/web_static/shared
fi

# Create a fake HTML file for testing
echo "<html><head></head><body>ALX School The Best</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link from current to the test release
if [ -L /data/web_static/current ];
then
    rm /data/web_static/current
fi

ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content of /data/web_static/current to hbnb_static
# (ex: https://mydomainname.tech/hbnb_static)
sed -i '/listen 80 default_server;/a location /hbnb_static/ {\n\talias /data/web_static/current/;\n}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
service nginx restart

exit 0
