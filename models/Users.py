import sqlite3
import datetime
from flask import flash

class UserLogin():
    def fromDB(self,user_id: int,db: str):
        self.__user = db.getUser(user_id)
        return self
    
    def create(self,user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user['id'])