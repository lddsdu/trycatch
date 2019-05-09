-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: trycatch
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `steaf`
--

DROP TABLE IF EXISTS `steaf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `steaf` (
  `name` varchar(100) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `sex` char(1) DEFAULT NULL,
  `image_path` varchar(200) DEFAULT NULL,
  `serialize_file` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `steaf`
--

LOCK TABLES `steaf` WRITE;
/*!40000 ALTER TABLE `steaf` DISABLE KEYS */;
INSERT INTO `steaf` VALUES ('lidongdong',0,'m','/home/jack/Desktop/target/lidongdong.jpg','/home/jack/Desktop/ser/lidongdong.ser'),('weiran',0,'m','/home/jack/Desktop/target/weiran.jpg','/home/jack/Desktop/ser/weiran.ser'),('obama',0,'m','/home/jack/Desktop/target/obama.jpg','/home/jack/Desktop/ser/obama.ser'),('ab',0,'m','/home/jack/Desktop/target/ab.jpg','/home/jack/Desktop/ser/ab.ser'),('biden',0,'m','/home/jack/Desktop/target/biden.jpg','/home/jack/Desktop/ser/biden.ser'),('jiangzeming',0,'m','/home/jack/Desktop/target/jiangzeming.jpg','/home/jack/Desktop/ser/jiangzeming.ser');
/*!40000 ALTER TABLE `steaf` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-17 16:19:14
