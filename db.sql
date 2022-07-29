/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - bacteria_identification
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`bacteria_identification` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `bacteria_identification`;

/*Table structure for table `bacteria` */

DROP TABLE IF EXISTS `bacteria`;

CREATE TABLE `bacteria` (
  `bacteria_id` int(11) NOT NULL AUTO_INCREMENT,
  `bname` varchar(200) DEFAULT NULL,
  `btype` varchar(200) DEFAULT NULL,
  `image1` varchar(200) DEFAULT NULL,
  `image2` varchar(200) DEFAULT NULL,
  `details` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`bacteria_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `bacteria` */

insert  into `bacteria`(`bacteria_id`,`bname`,`btype`,`image1`,`image2`,`details`) values 
(1,'C. diptheriae','cocus','/static/bacteria_pics/imag120201023-215257.jpg','/static/bacteria_pics/imag220201023-215257.jpg','one of the bacteria type of cocus');

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `complaint` varchar(200) DEFAULT NULL,
  `c_date` date DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `r_date` date DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`cid`,`complaint`,`c_date`,`reply`,`r_date`,`login_id`) values 
(1,'Datas are seems to be invalid','2020-10-23','Your problems will be correct it as soon as possible. Sorry for the consequences.','2020-10-23',11),
(2,'very poor clarity','2020-10-23','pending','0000-00-00',11),
(3,'ppp\r\n','2022-05-25','pending','2022-05-25',11);

/*Table structure for table `history` */

DROP TABLE IF EXISTS `history`;

CREATE TABLE `history` (
  `hid` int(11) NOT NULL AUTO_INCREMENT,
  `in_image` varchar(200) DEFAULT NULL,
  `result` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `history` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`user_type`) values 
(1,'admin','admin','admin'),
(11,'anannyatv@gmail.com','123','user'),
(12,'sarankp@gmail.com','s1234','user');

/*Table structure for table `pesticides` */

DROP TABLE IF EXISTS `pesticides`;

CREATE TABLE `pesticides` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `bacteria` varchar(56) DEFAULT NULL,
  `pesticide` text,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `pesticides` */

insert  into `pesticides`(`pid`,`bacteria`,`pesticide`) values 
(2,'Lactobacillus_delbrueckii','kpio'),
(3,'Staphylococcus_aureus','lklkl');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `r_id` int(11) NOT NULL AUTO_INCREMENT,
  `r_value` varchar(200) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`r_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`r_id`,`r_value`,`login_id`) values 
(1,'2',11),
(2,'4',12),
(3,'2',11);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `place` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`user_id`,`name`,`age`,`place`,`email`,`phone`,`login_id`) values 
(1,'Anannya T V','22','Thalassery','anannyatv@gmail.com','9867521341',11),
(2,'Saran K P','25','Kannur','sarankp@gmail.com','9867521343',12);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
