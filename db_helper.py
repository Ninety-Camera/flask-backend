import sqlite3

db_connection = sqlite3.connect('ninetycamera.db')
db_cursor = db_connection.cursor()

# function to create the tables 
def create_tables(cur):
    with open("DB/ddl.sql") as file:
        data = file.read().split(';')
        
    for one_statement in data:
        cur.execute(one_statement)
    
# function to add suspect image paths to suspect_ss table
def add_intrusion(intrusion_id,video_path,image1_path,image2_path,image3_path,date_time):
    statement = "insert into intrusion(intrusion_id,video_path,image1_path,image2_path,image3_path,date_time) values (?,?,?,?,?,?);"
    values = (intrusion_id,video_path,image1_path,image2_path,image3_path,date_time)
    with db_connection:
        db_cursor.execute(statement,values)
    
        
# function to add recorded video path to db      
def add_record_video(video_path,date_time):
    statement = "insert into record(video_path,date_time) values (?,?);"
    values = (video_path,date_time)
    with db_connection:
        db_cursor.execute(statement,values)
    
    
create_tables(db_cursor)



