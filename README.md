# AIASL

## Local development

```sh
$ ./venv-setup.sh
$ source pyenv/bin/activate
(pyenv)$ pip install -r requirements.txt
```

1. Setup local `.env` file for development with following vars:
```sh
DATABASE_URL=sqlite:////home/ajay/git/aiasl/db.sqlite3
PORT=5000
```
2. `heroku local -f Procfile.test`
3. For running migrations, do:
```sh
$ heroku local:run ./pyenv/bin/python manage.py migrate
```

## Production deployment
1. `$ git push heroku main`
2. Go to https://aiasl.herokuapp.com
3. For running migrations do:
```sh
$ heroku run python manage.py migrate
```
