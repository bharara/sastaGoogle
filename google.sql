CREATE SCHEMA sastaGoogle;
USE sastaGoogle;


create table files (
	fileID varchar(32) primary key,
    fileAdd varchar(100));
    
create table wordFile (
	fileID varchar(32),
    wordID varchar(32),
    score int,
    primary key (fileID, wordID),
    foreign key (fileID) references files(fileID));
