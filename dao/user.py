import hashlib
import base64
import hmac
from config import Config
from .model.user import User


class UserDAO:

    def __init__(self, session):
        self.session = session

    def create(self, user_d):
        user = User(**user_d)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()

    def generate_password_digest(self, password):
        return hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=Config.PWD_SALT,
            iterations=Config.PWD_ITERATIONS,
        )

    def get_hash(self, password):
        return base64.b64encode(self.generate_password_digest(password)).decode('utf-8')


    def comprare_passwords(self, hash_password, other_password) -> bool:
        decode_digest = base64.b64decode(hash_password)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode(),
            Config.PWD_SALT,
            Config.PWD_ITERATIONS,
        )
        return hmac.compare_digest(decode_digest, hash_digest)
