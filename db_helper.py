import sqlite3

class DbHelper:
    def __init__(self):
        self.db_connection = sqlite3.connect('ninetycamera.db')
        self.db_cursor = self.db_connection.cursor()
        self.create_tables()

    # function to create the tables. If tables already exits it will not create the tables. 
    def create_tables(self):
        
        with open("DB/ddl.sql") as file:
            data = file.read().split(';')
            
        for one_statement in data:
            self.db_cursor.execute(one_statement)
        
    # function to add suspect image paths to suspect_ss table.
    def add_intrusion(self,intrusion_id,video_path,image1_path,image2_path,image3_path,date_time):
        statement = "insert into intrusion(intrusion_id,video_path,image1_path,image2_path,image3_path,date_time) values (?,?,?,?,?,?);"
        values = (intrusion_id,video_path,image1_path,image2_path,image3_path,date_time)
        with self.db_connection:
            self.db_cursor.execute(statement,values)
        
            
    # function to add recorded video path to db.  
    def add_record_video(self,video_path,date_time):
        statement = "insert into record(video_path,date_time) values (?,?);"
        values = (video_path,date_time)
        with self.db_connection:
            self.db_connection.execute(statement,values)
        
    # funtion to add user data to db.
    def add_user_data(self,username,email,token,first_name,last_name):
        statement = "insert into user_data(username,email,token,first_name,last_name) values (?,?,?,?,?);"
        values = (username,email,token,first_name,last_name)
        with self.db_connection:
            self.db_cursor.execute(statement,values)
            
    # function to get the token for the user.
    def get_token(self,username):
        statement = "select token from user_data where username = ?;"
        with self.db_connection:
            self.db_cursor.execute(statement,(username,))
        return self.db_cursor.fetchone()
        




