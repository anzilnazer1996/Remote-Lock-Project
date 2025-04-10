import random

import string

from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.conf import settings

def get_password():

    password = ''.join(random.choices(string.ascii_letters+string.digits+string.punctuation,k=20))

    return password

def password_encrypting(password):

    while True:
        try:
            key = DES3.adjust_key_parity(get_random_bytes(24))
            break
        except ValueError:
            pass

    cipher = DES3.new(key, DES3.MODE_EAX)

    nonce = cipher.nonce

    ciphertext = cipher.encrypt(password.encode('ascii'))

    return key,nonce, ciphertext    
    
def password_decrypting(key,nonce,password):

    cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(password)

    return plaintext.decode('ascii')

    
def key_from_binary_to_hex(key):

    return key.hex()

def key_from_hex_to_binary(key):

    return bytes.fromhex(key)  


def send_email(subject,recepient,template,context):

    email_obj = EmailMultiAlternatives(subject,from_email=settings.EMAIL_HOST_USER,to=[recepient])

    content = render_to_string(template,context)

    email_obj.attach_alternative(content, "text/html")

    email_obj.send()