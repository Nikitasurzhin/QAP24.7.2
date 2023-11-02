import os

from dotenv import load_dotenv
load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
auth_key = {"key": "7e9e47dfdec15cb0cde602dbddf654bd2c4914d823d92de3d915a83f"}
invalid_auth_key = {"key": "7645hfd7dfdec15cb0cde602dbddf654bd2c4914d823d92de3d915a83f"}