import sqlite3
import datetime
from flask import flash

class Coins:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()
        
    def addUser(self,username: str,email: str,isAdmin: bool,hpsw: str,balance: str) -> bool:
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                flash("Пользователь с таким email уже существует")
                return False
                
            dt = datetime.datetime.now()
            self.__cur.execute("INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?,?)",(dt, username,balance ,email,isAdmin, hpsw,'None','None'))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка добавления пользователя в БД {str(e)}')
            return False
            
        return True 

    def swap_pass(self,password,user_id):
        try:
            self.__cur.execute(f"UPDATE users SET password = {password} WHERE id = {user_id}")
            return true
        except:
            flash("Ошибка смены пароля, свяжитесь с админом сайта")
            return false

    def getUser(self,user_id: int):
        try:
            query = f"SELECT * FROM users WHERE id = {user_id} LIMIT 1"
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if not res:
                flash('Пользователь не найден')
                return False
            return res
        except sqlite3.Error as e:
            print("1Ошибка получения данных из БД "+str(e))
        
        return False
    
    def getUserId(self,email: str):
        query = f"SELECT id FROM users WHERE email = '{email}' LIMIT 1"
        self.__cur.execute(query)
        res = self.__cur.fetchone()
        if not res:
            print("User not found")
            return False
        return res[0]

    def getUserByEmail(self,email: str) -> sqlite3.Row:
        try:
            query = f"SELECT * FROM users WHERE email = '{email}' LIMIT 1"
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if not res:
                flash("Пользователь не найден")
                return False
            
            return res
        except sqlite3.Error as e:
            print("2Ошибка получения данных из БД "+str(e))
        return False
    
    def getUserCount(self):
        query = f"SELECT * FROM users"
        self.__cur.execute(query)
        res = self.__cur.fetchone()
        if not res:
            flash("Пользователь не найден")
            return False
        return res

    def getCoin(self) -> sqlite3.Row:
        query = """SELECT * from BUSD"""
        self.__cur.execute(query)
        records = self.__cur.fetchall()
        return(records)

    def getUsers(self) -> sqlite3.Row:
        query = """SELECT * from users"""
        self.__cur.execute(query)
        records = self.__cur.fetchall()
        return(records)
