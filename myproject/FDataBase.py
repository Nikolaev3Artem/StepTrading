import sqlite3
import datetime
class FDataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()
        
    def addUser(self,username,email,isAdmin,hpsw,balance):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
                
            dt = datetime.datetime.now()
            self.__cur.execute("INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?,?)",(dt, username,balance ,email,isAdmin, hpsw,'None','None'))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД'+str(e))
            return False
            
        return True 


    def getUser(self,user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        
        return False
    
    def getUserByEmail(self,email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if not res:
                print("Пользователь не найден")
                return False
            
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    
    def getCoin(self):
        cursor = self.__db.cursor()
        sql_select_query = """SELECT * from coin_info"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        coin_list = []
        
        for row in records:
            coin_list.append(row)
        return(coin_list)

    def getUsers(self):
        cursor = self.__db.cursor()
        sql_select_query = """SELECT * from users"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        users_list = []
        
        for row in records:
            users_list.append(row)
        return(users_list)
