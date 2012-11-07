-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2012 年 11 月 06 日 22:00
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
  `need_content` text NOT NULL,
  `need_pub_date` int(11) DEFAULT NULL,
  PRIMARY KEY (`need_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17 ;

--
-- 转存表中的数据 `need`
--

INSERT INTO `need` (`need_id`, `need_author_id`, `need_title`, `need_content`, `need_pub_date`) VALUES
(1, 1, 'Macbook Pro Retina', 'I need a pro retina, 13in, the latest version...', 1351200909),
(2, 1, 'PDF editor', 'to edit some figures', 1351354060),
(3, 1, 'Upload images', '2 files', 1351354326),
(4, 1, 'Add Image', 'try', 1351354632),
(5, 1, 'Add Image', 'try', 1351354668),
(6, 1, 'Add another image', 'try again', 1351354771),
(7, 1, 'Insert Image', 'db', 1351357077),
(8, 1, 'again', 'db', 1351357116),
(9, 1, 'dddd', 'db', 1351357141),
(10, 1, 'xxxx', 'test', 1351357318),
(11, 1, '555', 'test', 1351357460),
(12, 1, 'yyyy', 'test', 1351357542),
(13, 1, 'too much', 'trials', 1351357771),
(14, 1, 'tre', '223456', 1351365958),
(15, 1, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxtttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt', 'test the super long', 1351885561),
(16, 1, 'test long content', 'ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc', 1351885864);

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

--
-- 转存表中的数据 `need_img`
--

INSERT INTO `need_img` (`id`, `need_post_id`, `uri`) VALUES
(1, 14, '12148ca44c08c50c37c3918b4e58bdd7001f8f5c9c91d6213f88be13.jpg');

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
  PRIMARY KEY (`provide_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

--
-- 转存表中的数据 `provide`
--

INSERT INTO `provide` (`provide_id`, `provide_author_id`, `provide_title`, `provide_content`, `provide_pub_date`) VALUES
(1, 1, 'Bike', 'good one', 1351362571),
(2, 1, 'fsfadsfd', 'good one', 1351362636),
(3, 2, 'Car', 'good', 1351365245),
(4, 1, 'A lot of things', 'fjsldkjflkdsjlf', 1351365443),
(5, 1, 'new offer', 'test', 1351365562),
(6, 1, 'fsdfsd', '534534523', 1351365721),
(7, 1, 'yyy', 'ttt', 1351365973),
(8, 1, 'uuu', 'uuuuu', 1351366029),
(9, 1, 'tt', 'xx', 1351366078),
(10, 1, 'useful', 'work', 1351366158),
(11, 1, 'cup', 'a good cup', 1351366378),
(12, 1, 'rrr', 'qqqq', 1351366444),
(13, 1, 'urutyu', 'poiopui', 1351366685),
(14, 2, 'I have another book', 'story', 1351366811),
(15, 1, '777gdfgdf', 'gdfgsdfgdfsg', 1351366918),
(16, 1, 't', 'ds', 1351367034),
(17, 1, 'use', 'fjsdjflk', 1351367094),
(18, 2, 'jflksjflkdsjaflksajdlfjdslfjsdlkjfl;sajfkjflksjflkdsjaflksajdlfjdslfjs', '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111119999999999999999999999999999999999999999999999999999999999999999999999999991111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111999999999999999999999999999999999999999999999999999999999999999999999999999', 1351887491);

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

--
-- 转存表中的数据 `provide_img`
--

INSERT INTO `provide_img` (`id`, `provide_post_id`, `uri`) VALUES
(1, 17, '7bb343d964e4598e262756655c5be6991ecc3eb9d4455bd2fb18a2d9.jpg'),
(2, 17, 'dde772e2429936283d97b04ed4105ce2b4f0c3079041f6e694fed557.pdf');

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

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`user_id`, `username`, `email`, `pw_hash`) VALUES
(1, 'jliao2', 'jliao2@utk.edu', 'sha1$GfYG4RbH$fed245ef0b8b11531dde3ea0f7c0c48be1224afc'),
(2, 'mushroom', 'phoenix.yanjinlee@gmail.com', 'sha1$Bg2HwleT$3a2a44c0bc99cab3b69d183b4dcc4df247e3e539');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
