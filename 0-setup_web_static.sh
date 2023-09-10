#!/usr/bin/env bash
# setup server for static deployment of static web clone of Airbnb
sudo apt-get update -y
sudo apt-get install nginx -y
sudo mkdir -p /data/web_static/{releases,shared}/
sudo mkdir -p /data/web_static/releases/test/
sudo tee /data/web_static/releases/test/index.html > /dev/null <<EOT
<html>
  <head>
  <head>
  <body>
    Holberton School
  </body>
</html>
EOT
if [ -e /data/web_static/current ] 
then
	sudo rm -rf /data/web_static/current
fi

sudo ln -s /data/web_static/releases/test /data/web_static/current
sudo chown -R "$USER":"$USER" /data
sudo tee /etc/nginx/sites-enabled/default > /dev/null << EOT

server {
	listen 80;
	server_name _;
	root /var/www/html;	
	
	add_header X-Served-By \$HOSTNAME;
	
	location /redirect_me {
		return 301 http://midosolutions.tech/;
	}
	
	error_page 404 /custom_404.html;
	location = /custom_404.html {
		root /usr/share/nginx/html;
		internal;
	}

	
	location / {
		try_files \$uri \$uri/ = 404;
	}


	location /hbnb_static/ {
		alias /data/web_static/current/;
	}
}
EOT
sudo service nginx restart
