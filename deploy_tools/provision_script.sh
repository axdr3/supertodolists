#! /bin/sh
#requires to be inside deploy_tools folder
# if [ "$1" == "" ]; then
# 	exit 1
# fi

# first arg
# domain = "$1"
#second arg
# user = "$2"

echo `pwd`

cat ./deploy_tools/nginx.template.conf \
| sed "s/DOMAIN/$1/g" \
| sed "s/USER/$2/g" \
| sudo tee /etc/nginx/sites-available/$1

sudo ln -s /etc/nginx/sites-available/$1 \
    /etc/nginx/sites-enabled/$1

cat  ./deploy_tools/gunicorn-systemd.template.service \
| sed "s/DOMAIN/$1/g" \
| sed "s/USER/$2/g" \
| sudo tee /etc/systemd/system/gunicorn-$1.service

# sudo systemctl daemon-reload
# # sudo systemctl reload nginx
# sudo systemctl enable gunicorn-$1
# sudo systemctl restart gunicorn-$1

echo 'Provisioning Successfully Completed!'
exit 0