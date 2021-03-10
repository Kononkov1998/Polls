from fabric.api import local


def run(port=8000):
    local(f"python manage.py runserver 0.0.0.0:{port}")


def upgrade():
    local("python -m pip install -U pip")
    local("pip install --upgrade -r requirements.txt")


def migrate():
    local("python manage.py makemigrations")
    local("python manage.py migrate")


def makemigrations():
    local("python manage.py makemigrations")


def test():
    local("python manage.py test")


def startapp(name):
    local(f"python manage.py startapp {name}")


def check():
    local(f"python manage.py check --deploy")


def createsuperuser():
    local(f"python manage.py createsuperuser")
