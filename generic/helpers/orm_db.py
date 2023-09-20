import allure
from typing import List
from sqlalchemy import select, delete, update
from generic.helpers.orm_models import User
from orm_client.orm_client import OrmClient


class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        with allure.step("Get all users from DB"):
            query = select(User)
            dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(self, login: str) -> List[User]:
        with allure.step(f"Get user with login {login} from DB"):
            query = (
                select(User)
                .where(User.Login == login)
            )
            dataset = self.db.send_query(query=query)
        return dataset

    def get_users_by_login_pattern(self, pattern: str) -> List[User]:
        with allure.step(f"Get all users data from DB with login which contains substring '{pattern}'"):
            query = (
                select(User)
                .where(User.Login.like(pattern))
            )
            dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(self, login: str):
        with allure.step(f"Delete user from DB using login '{login}' in where clause"):
            query = (
                delete(User)
                .where(User.Login == login)
            )
            dataset = self.db.send_bulk_query(query=query)
        return dataset

    def delete_users_by_login_pattern(self, pattern: str):
        with allure.step(f"Delete all users from DB by login substring '{pattern}' in where clause"):
            query = (
                delete(User)
                .where(User.Login.like(pattern))
            )
            dataset = self.db.send_bulk_query(query=query)
        return dataset

    def set_activated_flag_by_login(self, login: str, value: bool = True):
        with allure.step("User activation flag in DB"):
            query = (
                update(User)
                .where(User.Login == login)
                .values(Activated=value)
            )
            dataset = self.db.send_bulk_query(query=query)
        return dataset
