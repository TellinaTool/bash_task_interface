""" Create file server-credentials.txt, with MAX_USERS randomly-generated passwords. """
import random

MAX_USERS = 100
password_length = 10
password_chars = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"

passwords = []
with open('server-credentials.txt', 'w') as file:
    for i in range(MAX_USERS):
        # generate password by randomly selecting chars from password_chars
        password =  "".join(random.sample(password_chars, password_length))
        file.write("%s\n" % password)
