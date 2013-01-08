-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2013 年 01 月 08 日 16:04
-- 服务器版本: 5.5.28
-- PHP 版本: 5.3.10-1ubuntu3.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `gethemdb`
--
CREATE DATABASE `gethemdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `gethemdb`;

-- --------------------------------------------------------

--
-- 表的结构 `follower`
--

DROP TABLE IF EXISTS `follower`;
CREATE TABLE IF NOT EXISTS `follower` (
  `who_id` int(11) DEFAULT NULL,
  `whom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `need`
--

DROP TABLE IF EXISTS `need`;
CREATE TABLE IF NOT EXISTS `need` (
  `need_id` int(11) NOT NULL AUTO_INCREMENT,
  `need_author_id` int(11) NOT NULL,
  `need_title` varchar(400) NOT NULL,
  `need_content` text NOT NULL,
  `need_pub_date` int(11) DEFAULT NULL,
  `tag` varchar(256) NOT NULL,
  PRIMARY KEY (`need_id`),
  KEY `tag` (`tag`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

-- --------------------------------------------------------

--
-- 表的结构 `need_img`
--

DROP TABLE IF EXISTS `need_img`;
CREATE TABLE IF NOT EXISTS `need_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `need_post_id` int(11) NOT NULL,
  `uri` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `need_match`
--

DROP TABLE IF EXISTS `need_match`;
CREATE TABLE IF NOT EXISTS `need_match` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `need_id` int(11) NOT NULL,
  `provide_id` int(11) NOT NULL,
  `score` double NOT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `provide_id` (`provide_id`),
  KEY `need_id` (`need_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=339 ;

-- --------------------------------------------------------

--
-- 表的结构 `need_topic`
--

DROP TABLE IF EXISTS `need_topic`;
CREATE TABLE IF NOT EXISTS `need_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `need_id` int(11) NOT NULL,
  `tag` varchar(256) NOT NULL,
  `topic_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `need_id` (`need_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `provide`
--

DROP TABLE IF EXISTS `provide`;
CREATE TABLE IF NOT EXISTS `provide` (
  `provide_id` int(11) NOT NULL AUTO_INCREMENT,
  `provide_author_id` int(11) NOT NULL,
  `provide_title` varchar(400) NOT NULL,
  `provide_content` text NOT NULL,
  `provide_pub_date` int(11) DEFAULT NULL,
  `tag` varchar(256) NOT NULL,
  PRIMARY KEY (`provide_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=21 ;

-- --------------------------------------------------------

--
-- 表的结构 `provide_img`
--

DROP TABLE IF EXISTS `provide_img`;
CREATE TABLE IF NOT EXISTS `provide_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provide_post_id` int(11) NOT NULL,
  `uri` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- 表的结构 `provide_match`
--

DROP TABLE IF EXISTS `provide_match`;
CREATE TABLE IF NOT EXISTS `provide_match` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provide_id` int(11) NOT NULL,
  `need_id` int(11) NOT NULL,
  `score` double NOT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `need_id` (`need_id`),
  KEY `provide_id` (`provide_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=339 ;

-- --------------------------------------------------------

--
-- 表的结构 `provide_topic`
--

DROP TABLE IF EXISTS `provide_topic`;
CREATE TABLE IF NOT EXISTS `provide_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provide_id` int(11) NOT NULL,
  `tag` varchar(256) NOT NULL,
  `topic_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `provide_id` (`provide_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pw_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
