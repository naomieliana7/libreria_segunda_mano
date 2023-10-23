import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*[a-z].*[a-z].*[a-z])(?=.*\d.*\d.*\d.*\d)(?=.*[!@#$%^&*]).{10,}$')
TELEFONO_PY_REGEX = re.compile(r'^595[0-9]{9}$')
ALLOWED_EXTENSIONS = re.compile(r'\.(png|jpg|jpeg|gif)$')
