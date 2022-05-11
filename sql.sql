/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.7.31 : Database - credit_cardfraud_detection
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`credit_cardfraud_detection` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `credit_cardfraud_detection`;

/*Table structure for table `bookings` */

DROP TABLE IF EXISTS `bookings`;

CREATE TABLE `bookings` (
  `booking_id` int(100) NOT NULL AUTO_INCREMENT,
  `cart_id` int(100) DEFAULT NULL,
  `amount` int(100) DEFAULT NULL,
  `b_status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=MyISAM AUTO_INCREMENT=123 DEFAULT CHARSET=latin1;

/*Data for the table `bookings` */

insert  into `bookings`(`booking_id`,`cart_id`,`amount`,`b_status`) values 
(119,20,125,'booked'),
(118,19,0,'pending'),
(117,18,0,'pending'),
(116,17,0,'pending'),
(120,21,0,'pending'),
(121,22,0,'pending'),
(122,23,0,'pending');

/*Table structure for table `cart` */

DROP TABLE IF EXISTS `cart`;

CREATE TABLE `cart` (
  `cart_id` int(100) NOT NULL AUTO_INCREMENT,
  `prod_id` int(100) DEFAULT NULL,
  `user_id` int(100) DEFAULT NULL,
  `quantity` int(100) DEFAULT NULL,
  `c_status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`cart_id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

/*Data for the table `cart` */

insert  into `cart`(`cart_id`,`prod_id`,`user_id`,`quantity`,`c_status`) values 
(19,4,6,1,'add to cart'),
(18,3,5,1,'add to cart'),
(17,4,5,1,'add to cart'),
(20,3,6,1,'booked'),
(21,4,9,1,'add to cart'),
(22,3,9,1,'add to cart'),
(23,5,9,1,'add to cart');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `comp_id` int(100) DEFAULT NULL,
  `user_id` int(100) DEFAULT NULL,
  `complaint` varchar(500) DEFAULT NULL,
  `comp_date` date DEFAULT NULL,
  `replay` varchar(500) DEFAULT NULL,
  `rep_date` date DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`comp_id`,`user_id`,`complaint`,`comp_date`,`replay`,`rep_date`) values 
(1,12,'delivery time is too long','2022-03-09','sorry for the late delivery','2022-03-22'),
(NULL,5,'bad','2022-03-25',NULL,NULL),
(NULL,5,'ihg;iodgh','2022-03-25',NULL,NULL),
(NULL,5,'poor ','2022-03-30',NULL,NULL),
(NULL,5,'poor packing','2022-03-30',NULL,NULL),
(NULL,9,'','2022-04-07',NULL,NULL);

/*Table structure for table `credit_card` */

DROP TABLE IF EXISTS `credit_card`;

CREATE TABLE `credit_card` (
  `card_id` int(100) DEFAULT NULL,
  `user_id` int(100) DEFAULT NULL,
  `card_number` int(25) DEFAULT NULL,
  `cvv` varchar(25) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `holder's name` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `credit_card` */

/*Table structure for table `dealer` */

DROP TABLE IF EXISTS `dealer`;

CREATE TABLE `dealer` (
  `login_id` int(100) DEFAULT NULL,
  `dealer_name` varchar(100) DEFAULT NULL,
  `d_place` varchar(100) DEFAULT NULL,
  `d_post` varchar(100) DEFAULT NULL,
  `d_phone` int(100) DEFAULT NULL,
  `d_pin` int(10) DEFAULT NULL,
  `d_email` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `dealer` */

insert  into `dealer`(`login_id`,`dealer_name`,`d_place`,`d_post`,`d_phone`,`d_pin`,`d_email`) values 
(2,'joy','kotkl','crsl',1234,676542,'joy123@gmail.com'),
(3,'Rinsha','mysticfalls','brtn',12354,7452,'rin@gmail.com');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(100) NOT NULL AUTO_INCREMENT,
  `user_id` int(100) DEFAULT NULL,
  `feedback` varchar(500) DEFAULT NULL,
  `feedback_date` date DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`user_id`,`feedback`,`feedback_date`) values 
(1,5,'good','2022-03-25'),
(2,5,'not bad','2022-03-25'),
(3,5,'not bad','2022-03-25'),
(4,5,'good','2022-03-25'),
(5,5,'kdjv','2022-03-25'),
(6,5,'good','2022-03-30'),
(7,9,'','2022-04-07');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'joy123@gmail.com','9386','dealer'),
(3,'rin@gmail.com','3094','dealer'),
(6,'joe@gmail.com','joe123','user'),
(5,'hani@gmail.com','hani123','user'),
(7,'joseph@gmail.com','joseph123','user'),
(8,'thas@gmail.com','thas123','user'),
(9,'sham@gmail.com','sham123','user');

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int(100) NOT NULL AUTO_INCREMENT,
  `prod_name` varchar(150) DEFAULT NULL,
  `prod_quantity` int(100) DEFAULT NULL,
  `price` int(100) DEFAULT NULL,
  `dealer_id` int(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `fresh` varchar(100) DEFAULT NULL,
  `details` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `product` */

insert  into `product`(`product_id`,`prod_name`,`prod_quantity`,`price`,`dealer_id`,`image`,`category`,`fresh`,`details`) values 
(4,'ring',1,239,2,'/static/productimg/220321-202715.jpg','Jwellery','Branded New','stone ring'),
(3,'necklace',1,32060,2,'/static/productimg/220321-202640.jpg','Jwellery','Branded New','gold layered necklace'),
(5,'bangle',1,45030,2,'/static/productimg/220321-202746.jpg','Jwellery','Branded New',''),
(6,'gold bangle ',1,56320,2,'/static/productimg/220321-202826.jpg','Jwellery','Branded New',''),
(7,'lipstick',1,125,2,'/static/productimg/220321-202852.jpg','Cosmetics','Branded New',''),
(8,'lakmi foundation',1,450,2,'/static/productimg/220321-202936.jpg','Cosmetics','Branded New',''),
(9,'eyeliner',1,200,2,'/static/productimg/220321-203004.jpg','Cosmetics','Branded New','colossal eyeliner'),
(10,'eyebrow pencil',1,40,2,'/static/productimg/220321-203040.jpg','Cosmetics','Branded New','');

/*Table structure for table `stock` */

DROP TABLE IF EXISTS `stock`;

CREATE TABLE `stock` (
  `stock_id` int(100) NOT NULL AUTO_INCREMENT,
  `product_id` int(100) DEFAULT NULL,
  `stock_quantity` int(100) DEFAULT NULL,
  PRIMARY KEY (`stock_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `stock` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `login_id` int(200) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `phone` int(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pin` int(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`login_id`,`user_name`,`dob`,`place`,`post`,`phone`,`email`,`pin`) values 
(6,'joe','1994-05-03','orleans','new orleans',12354,'joe@gmail.com',123654),
(5,'hani123','2007-01-15','ktkl','ktkl',1234,'hani@gmail.com',654),
(7,'joseph','1990-06-12','mex','mex',1254,'joseph@gmail.com',54214),
(8,'thas','1998-02-14','orleans','new orleans',1236,'thas@gmail.com',123654),
(9,'sham','1996-05-14','mex','mex',65423,'sham@gmail.com',12345);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
