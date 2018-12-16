drop schema if exists sastaGoogle;
CREATE SCHEMA sastaGoogle;
USE sastaGoogle;

create table files (
	fileID varchar(32) primary key,
    fileAdd varchar(240),
    category int);
    
create table wordFile (
	fileID varchar(32),
    wordID varchar(32),
    score int,
    primary key (wordID, fileID)
    );

grant all privileges on sastagoogle.* to 'root'@localhost;