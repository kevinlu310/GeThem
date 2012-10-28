-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2012 年 10 月 27 日 22:11
-- 服务器版本: 5.5.24
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
-- 表的结构 `matchpost`
--

DROP TABLE IF EXISTS `matchpost`;
CREATE TABLE IF NOT EXISTS `matchpost` (
  `need_id` int(11) DEFAULT NULL,
  `provide_id` int(11) DEFAULT NULL,
  `score` float(53,16) DEFAULT NULL
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
  `need_content` varchar(800) NOT NULL,
  `need_pub_date` int(11) DEFAULT NULL,
  PRIMARY KEY (`need_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

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
-- 表的结构 `provide`
--

DROP TABLE IF EXISTS `provide`;
CREATE TABLE IF NOT EXISTS `provide` (
  `provide_id` int(11) NOT NULL AUTO_INCREMENT,
  `provide_author_id` int(11) NOT NULL,
  `provide_title` varchar(400) NOT NULL,
  `provide_content` varchar(800) NOT NULL,
  `provide_pub_date` int(11) DEFAULT NULL,
  PRIMARY KEY (`provide_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

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
