rm db.sqlite3
rm main/migrations/001*
./manage.py makemigrations
./manage.py migrate
./manage.py runscript update_models_db --dir-policy each