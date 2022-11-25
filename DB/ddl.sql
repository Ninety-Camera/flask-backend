create table if not exists Record(
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_path text(200),
    date_time timestamp
);

create table if not exists Intrusion(
    intrusion_id varchar(200) primary key,
    video_path text(200),
    image1_path text(200),
    image2_path text(200),
    image3_path text(200),
    date_time timestamp
);


create table if not exists User_data(
    email varchar(30) primary key,
    user_id varchar(200),
    role varchar(30),
    token text(500),
    first_name varchar(20),
    last_name varchar(20)
);

create table if not exists Camera(
    camera_id varchar(20) primary key,
    camera_name varchar(20),
    is_ip_camera Number(1),
    camera_link varchar(40)
);

create table if not exists System(
    system_id varchar(200) primary key
);