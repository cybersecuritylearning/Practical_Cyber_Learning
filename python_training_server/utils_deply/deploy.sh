#!/bin/bash

rm -r /var/www/server
rm server/main/migrations/0001_initial.py
cp -r server /var/www/
cp settings.py /var/www/server/server/
cd /var/www/server/
chown www-data /var/www/server
python3 manage.py collectstatic
./reinit_database.sh
chown www-data /var/www/server/db.sqlite3
chown www-data /var/www/server/main/migrations/0001_initial.py
service apache2 reload
