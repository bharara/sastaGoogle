drop schema if exists sastagoogle;
CREATE SCHEMA sastagoogle;
USE sastagoogle;

create table files (
	fileID varchar(32) primary key,
    fileAdd varchar(240),
    category int);

create table wordFile (
    word varchar(32),
	fileID varchar(32),
    score int,
    index (word, fileID)
    );

grant all privileges on sastagoogle.* to 'root'@localhost;