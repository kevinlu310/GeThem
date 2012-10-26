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
  need_title varchar(400) not null,
  need_content varchar(800) not null,
  need_pub_date integer
);

drop table if exists provide;
create table provide (
  provide_id integer primary key auto_increment,
  provide_author_id integer not null,
  provide_title varchar(400) not null,
  provide_content varchar(800) not null,
  provide_pub_date integer
);

drop table if exists matchpost;
create table matchpost (
  need_id integer,
  provide_id integer,
  score float(53,16)
);

drop table if exists needpic;
create table needpic (
  needpic_id integer primary key auto_increment,
  needpic_url varchar(400) not null,
  needpic_user_id integer,
  need_id integer,
  needpic_pub_date integer
);

drop table if exists providepic;
create table providepic (
  providepic_id integer primary key auto_increment,
  providepic_url varchar(400) not null,
  provdepic_user_id integer,
  provide_id integer,
  providepic_pub_date integer
);
