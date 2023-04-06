#!/usr/bin/env bash

# Install Nginx if not already installed
if [ ! -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/{releases,test,shared}

# Create fake HTML file
sudo touch /data/web_static/releases/test/index.html
echo "Test page" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/listen 80 default_server;/a \\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
