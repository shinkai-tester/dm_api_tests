from db_client.db_client import DBClient


class DmDatabase:
    def __init__(self, user, password, host, database):
        self.db = DBClient(user, password, host, database)

    def get_all_users(self):
        query = 'select * from "public"."Users"'
        dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(self, login: str):
        query = f'''
        select * from "public"."Users"
        where "Users"."Login"='{login}'
        '''
        dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(self, login: str):
        query = f'''
        delete from "public"."Users"
        where "Login"='{login}'
        '''
        dataset = self.db.send_bulk_query(query=query)
        return dataset

    def set_activated_flag_by_login(self, login: str, value: bool = True):
        query = f'''
        update "public"."Users"
        set "Activated" = {value}
        where "Login"='{login}'
        '''
        dataset = self.db.send_bulk_query(query=query)
        return dataset
