import psycopg2
# -------------------create test table-----------------
# create table people(
# 	id serial primary key not null,
#     name varchar(15) not null,
#     surname varchar(20) not null,
# 	age integer,
#     job varchar(30)
# );
# 


class DB_PostgreSQL(object):

    def __init__(self, db, usr, passwd, host_adr, port_value):          # подключаемся к бд
        try:
            self.connection = psycopg2.connect(database = db, user = usr, password = passwd, host = host_adr, port = port_value)        # установка соединения
            self.cur = self.connection.cursor()                 # создание курсора - объекта для манипуляций с бд

            print("Successfull connection to database: \"%s\" for user \"%s\"\n"%(db, usr))
        except:
            print("Some errors with connection to database: \"%s\" for user \"%s\"\n- database address: %s\n- port: %s"%(db,usr, host_adr, port_value))
        
    def add_user(self, table, name, surname, age, job = "free"):        # добавление строки в таблицу 
        try:
            self.cur.execute("INSERT INTO %s (name, surname, age, job) VALUES ('%s', '%s', %d, '%s')"%(table, name, surname, age, job))

            self.connection.commit()

            print("Record inserted successfully")
        except:
            print("Some errors with adding person %s %s"%(name, surname))

    def delete_user(self, table, name, surname):                        # удаление строки по условию
        try:
            self.cur.execute("DELETE FROM %s WHERE name = '%s' and surname = '%s'"%(table, name, surname))

            self.connection.commit()
            
            print("Person \"%s %s\" was deleted"%(name, surname))
        except:
            print("Some errors with deleting")
            
    def get_table_rows(self, table):                                    # получения всех строк таблицы
        try:
            self.cur.execute("SELECT * FROM %s"%(table))

            rows = self.cur.fetchall()

            return rows
        except:
            print("Some errors with showing table \"%s\""%(table))
    
    def print_rows(self, rows):                                         # печать двумерного массива
        for row in rows:
            for i in range(len(row)):
                print(row[i], end="\t")
            print("")

    def close_connection(self):
        self.connection.close()
        print("\nConnection close")


if __name__ == "__main__":
    database = "N33481_22"
    username = "postgres"
    password = "1234"
    host = "127.0.0.1"
    port = "5433"

    DB = DB_PostgreSQL(database, username, password, host, port)
    
    # DB.add_user("people", "Python", "Sulimenko", 20,"student")
    # DB.delete_user("people", "Python", "Sulimenko")
    
    rows = DB.get_table_rows("people")
    DB.print_rows(rows)

    DB.close_connection()
    
    # DB.add_user("people", "Python", "Sulimenko", 20,"student")
