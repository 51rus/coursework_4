from dao.model.user import UserSchema
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_email(self, email):
        user = self.dao.get_by_email(email)
        return user

    def create(self, user_d):
        user_password = user_d.get('password')
        if user_password:
            user_d['password'] = self.dao.get_hash(user_password)
        user = self.dao.create(user_d)
        return UserSchema().dump(user)

    def compare_passwords(self, password, other_password):
        hash_pas = self.dao.get_hash(other_password)
        return self.dao.comprare_passwords(password, hash_pas)
