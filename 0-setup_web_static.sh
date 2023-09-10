#!/usr/bin/env bash
# bash script that sets up webstatic

sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "<html>
  <head>
  <head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
content=$(cat << 'END HEREDOC'
	location /hbnb_static {
		alias /data/web_static/current/;
	}
END HEREDOC
)
echo -e "$content" >> text.txt
sudo sed -i '/server_name _;/r text.txt' /etc/nginx/sites-available/default
sudo rm text.txt
sudo service nginx restart
