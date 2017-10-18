###########################################
Git
###########################################
#First time
	cd to the directory
	#Create local git
	git init
	#Add all things in the current directory to the local git
	git add .
	#Add a remote repository
	git remote add remotename https://Piyapong_4507075@bitbucket.org/Piyapong_4507075/gcgcointegration.git
	#Commit with comments
	git commit -m "first version"
	#Push to a remote repository
	git push remotename master
	#Push local branch to remote branch
	git push remotename dev:dev

#Other time
	cd to the directory
	cd ~/GCP
	#Add all things in the current directory to the local git
	git add .
	#Commit with comments
	git commit -m "Initial version"
	#Push to a remote repository
	git push origin master

#Optional force push to a remote repository
git push -f origin master

#Display current status
git status

###########################################
Setup flask
###########################################

http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/

# install wsgi
apt-get install libapache2-mod-wsgi

# create wsgi file in a root directory

import sys

sys.path.insert(0, '/var/www/public_html/flask')
from flaskapp import app as application

#config apache2
#create flask.conf

sudo nano /etc/apache2/sites-available/flask.conf

<VirtualHost *>
ServerName localhost
WSGIDaemonProcess flaskapp user=piyapong group=piyapong threads=5
 WSGIScriptAlias / /var/www/public_html/flask/app.wsgi
<Directory /var/www/public_html/flask/>
 WSGIProcessGroup flaskapp
 WSGIApplicationGroup %{GLOBAL}
 WSGIScriptReloading On
Require all granted
</Directory>
</VirtualHost>

sudo service apache2 restart 

###########################################
File
###########################################

sqlcert
https://cloud.google.com/sql/docs/mysql/configure-ssl-instance
=====> client-cert.pem, client-key.pem, server-ca.pem ==> certificate to connect sql database
=====> connectsql.sh ==> script to connect sql database


web/flask/file
=====> backup_to_bucket.sh ==> script to backup document to GCP buckets
=====> crontab.txt ==> crontab events set on the server
=====> init_script.sh ==> install all requirements on a new server

web/flask/web
=====> css,img,js ==> web materials used in the web ==> upload to GCP storage and access via a public link

web/flask/
=====> app.wsgi ==> add flask to a system environment and init flask app
=====> bulkload.py ==> bulk load data from oanda and save the data to GCP data storage
=====> calcoint.py ==> test cointegration on the most recent data length and save to a database if it's significantly cointegrated.
=====> callstmstat.py ==> update mu (mean for an entire dataset) for lstm
=====> flaskapp.py ==> first python file that flask point to init the default web
=====> forcast.py ==> take a snapshot of cointegration forecast and save to database

web/flask/src
======> contains all libraries and files called by python files in the web/flask folder
