import sqlite3

class DbHelper:
    def __init__(self):
        self.db_connection = sqlite3.connect('ninetycamera.db',check_same_thread=False)
        self.db_cursor = self.db_connection.cursor()
        self.__create_tables()
        
    

    # function to create the tables. If tables already exits it will not create the tables. 
    # this will be private function since only calling in the init.
    def __create_tables(self):
        
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
    def add_user_data(self,email,id,role,token,first_name,last_name):
        statement = "insert into user_data(email,user_id,role,token,first_name,last_name) values (?,?,?,?,?,?);"
        values = (email,id,role,token,first_name,last_name)
        with self.db_connection:
            self.db_cursor.execute(statement,values)
            
    # function to get the token for the user.
    def get_token(self):
        statement = "select token from user_data;"
        with self.db_connection:
            self.db_cursor.execute(statement)
        return self.db_cursor.fetchone()[0]
        
    # function to get the intrusion video and images when the intrusion id given.
    def get_one_intrusion_data(self,intrusion_id):
        statement = "select * from intrusion where intrusion_id=?;"
        with self.db_connection:
            self.db_cursor.execute(statement,(intrusion_id,))
        return self.db_cursor.fetchone()
    
    # function to get the all intrusion details.
    def get_all_intrusion_data(self):
        statement = "select * from intrusion;"
        with self.db_connection:
            self.db_cursor.execute(statement)
        return self.db_cursor.fetchall()
    
    # function to add the camera.
    def add_camera(self,camera_id,camera_name,is_ip_camera,camera_link):
        statement = 'insert into camera(camera_id,camera_name,is_ip_camera,camera_link) values (?,?,?,?);'
        with self.db_connection:
            self.db_cursor.execute(statement,(camera_id,camera_name,is_ip_camera,camera_link))
    
    # function to get the camera details.
    def get_camera_details(self):
        statement = "select * from camera;"
        with self.db_connection:
            self.db_cursor.execute(statement)
        return self.db_cursor.fetchall()
    
    # function to get user details
    def get_user_details(self):
        statement = "select * from user_data;"
        with self.db_connection:
            self.db_cursor.execute(statement)

        return self.db_cursor.fetchone()
    
    # function to delete the user data table
    def delete_userdata(self):
        with self.db_connection:
            self.db_cursor.execute('delete from user_data;')
        

    