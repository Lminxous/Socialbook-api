import string
import random
from rest_framework_jwt.settings import api_settings

# Creating a random password 

def generate_random_password():
    PASS_CHARS = string.ascii_letters + string.digits
    for i in '0oO1QlLiI':
        PASS_CHARS = PASS_CHARS.replace(i,'')
    return "".join(random.choice(PASS_CHARS) for _ in range(0, 10))

# Creating a new token manually 

''' Return a token to the user immediately after account creation.'''

def get_jwt_with_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # Function to generate the token payload
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER # Function to encode the token
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
