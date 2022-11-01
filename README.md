# ict3x03-2022-team32
Data Analytics Website for Employees in Industries of Singapore

To run, For linux:
```
python3 -m venv appvenv
source appvenv/bin/activate
pip install -r requirements.txt
python3 wsgi.py
```

To run, For Windows:
```
For windows:
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python3 wsgi.py
```

To generate "requirements.txt"
```
pip freeze > requirements.txt
```


References:
```
setting up Gunicorn and Nginx: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04
Git command on linux cli: https://www.earthdatascience.org/workshops/intro-version-control-git/basic-git-commands/
Permission problem when creating venv on linux: https://stackoverflow.com/questions/19471972/how-to-avoid-permission-denied-when-using-pip-with-virtualenv
Converting vevn between windows and linux: https://stackoverflow.com/questions/42733542/how-to-use-the-same-python-virtualenv-on-both-windows-and-linux
```
