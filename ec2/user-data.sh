#!/bin/bash
yum update -y
yum install httpd -y
echo "Hola TALENTOTECH" > /var/www/html/index.html
service httpd restart
