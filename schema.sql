drop database if exists gethemdb;
create database gethemdb;
use gethemdb;

drop table if exists user;
create table user (
  user_id integer primary key AUTO_INCREMENT,
  username varchar(80) not null,
  email varchar(100) not null,
  pw_hash varchar(100) not null
);

drop table if exists follower;
create table follower (
  who_id integer,
  whom_id integer
);

drop table if exists need;
create table need (
  need_id integer primary key auto_increment,
  need_author_id integer not null,
  need_text varchar(400) not null,
  need_pub_date integer
);

drop table if exists provide;
create table provide (
  provide_id integer primary key auto_increment,
  provide_author_id integer not null,
  provide_text varchar(400) not null,
  provide_pub_date integer
);

drop table if exists matchpost;
create table matchpost (
  need_id integer,
  provide_id integer,
  score float(53,16)
);
