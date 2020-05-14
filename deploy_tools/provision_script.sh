#! /bin/sh
#requires to be inside deploy_tools folder
if [ "$1" == ""]; then
	exit 1
fi

# first arg
domain = $1
#second arg
user = $2

cat nginx.template.conf \
| sed "s/DOMAIN/$domain/g" \
| sed "s/USER/$user/g" \
| sudo tee /etc/nginx/sites-available/$domain

sudo ln -s /etc/nginx/sites-available/$domain \
    /etc/nginx/sites-enabled/$domain

cat  gunicorn-systemd.template.service \
| sed "s/DOMAIN/$domain/g" \
| sed "s/USER/$user/g" \
| sudo tee /etc/systemd/system/gunicorn-$domain.service

sudo systemctl daemon-reload
sudo systemctl reload nginx
sudo systemctl enable gunicorn-$domain
sudo systemctl restart gunicorn-$domain

echo 'Provisioning Successfully Completed!'
exit 0