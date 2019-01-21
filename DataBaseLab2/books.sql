-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: books
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add user',7,'add_admin'),(26,'Can change user',7,'change_admin'),(27,'Can delete user',7,'delete_admin'),(28,'Can view user',7,'view_admin'),(29,'Can add book',8,'add_book'),(30,'Can change book',8,'change_book'),(31,'Can delete book',8,'delete_book'),(32,'Can view book',8,'view_book'),(33,'Can add car',9,'add_car'),(34,'Can change car',9,'change_car'),(35,'Can delete car',9,'delete_car'),(36,'Can view car',9,'view_car'),(37,'Can add correct',10,'add_correct'),(38,'Can change correct',10,'change_correct'),(39,'Can delete correct',10,'delete_correct'),(40,'Can view correct',10,'view_correct'),(41,'Can add user',11,'add_normal'),(42,'Can change user',11,'change_normal'),(43,'Can delete user',11,'delete_normal'),(44,'Can view user',11,'view_normal'),(45,'Can add order',12,'add_order'),(46,'Can change order',12,'change_order'),(47,'Can delete order',12,'delete_order'),(48,'Can view order',12,'view_order'),(49,'Can add report',13,'add_report'),(50,'Can change report',13,'change_report'),(51,'Can delete report',13,'delete_report'),(52,'Can view report',13,'view_report'),(53,'Can add user',14,'add_retailer'),(54,'Can change user',14,'change_retailer'),(55,'Can delete user',14,'delete_retailer'),(56,'Can view user',14,'view_retailer'),(57,'Can add rlist',15,'add_rlist'),(58,'Can change rlist',15,'change_rlist'),(59,'Can delete rlist',15,'delete_rlist'),(60,'Can view rlist',15,'view_rlist');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$R8bbnRyQu67M$XXijYoaKlskF4JJg3fyIUEX6oBQiv4+5KWhXmh/XhRs=','2018-12-11 10:57:53.203329',0,'normal1','n','','',0,1,'2018-12-10 02:28:21.249121'),(2,'pbkdf2_sha256$120000$1c7KMi8Li7fi$wt2bXQGFHpIzAHP9i0DmHrvjQqJBMe5v9rQ4nywZjzE=','2018-12-11 13:22:30.531043',0,'3','g','','',0,1,'2018-12-10 02:38:20.292935'),(3,'pbkdf2_sha256$120000$gIjEGJm8PyWI$++CLbg8q7MUkkGyrlt3DsKdcoP6DpjgNUYn3kFi5AoQ=','2018-12-11 11:00:11.734770',0,'2','a','','',0,1,'2018-12-10 02:51:30.155645'),(4,'pbkdf2_sha256$120000$WFAuboLPdHEn$+UxQFc07E6u2+T7uFUbVbzPUtqb02X5mtyZOg+IsX9M=','2018-12-11 13:21:03.490128',0,'sdy','n','','',0,1,'2018-12-11 12:12:59.649066'),(5,'pbkdf2_sha256$120000$7AzqJ275t1Ax$tz5hx9kD4F+U3aIKNDmtFseHOdQd+H9ogpAkdgmpMJE=','2018-12-11 13:22:57.433269',0,'bxy','n','','',0,1,'2018-12-11 12:25:42.235106');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_admin`
--

DROP TABLE IF EXISTS `bookdeal_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_admin` (
  `user_ptr_id` int(11) NOT NULL,
  `info` varchar(50) NOT NULL,
  PRIMARY KEY (`user_ptr_id`),
  CONSTRAINT `bookdeal_admin_user_ptr_id_41829f65_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_admin`
--

LOCK TABLES `bookdeal_admin` WRITE;
/*!40000 ALTER TABLE `bookdeal_admin` DISABLE KEYS */;
INSERT INTO `bookdeal_admin` VALUES (2,'');
/*!40000 ALTER TABLE `bookdeal_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_book`
--

DROP TABLE IF EXISTS `bookdeal_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `cover` varchar(100) NOT NULL,
  `info` varchar(500) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `isDelete` tinyint(1) NOT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookdeal_book_owner_id_282a6794_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `bookdeal_book_owner_id_282a6794_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_book`
--

LOCK TABLES `bookdeal_book` WRITE;
/*!40000 ALTER TABLE `bookdeal_book` DISABLE KEYS */;
INSERT INTO `bookdeal_book` VALUES (1,'概率统计 第二版','covers/屏幕快照_2018-12-10_上午10.43.25.png','浙大四版 概率论与数理统计 第四版 浙大概率论 盛骤 高等教育出版社 概率论与数理统计(第4版)(配防伪标)浙江大学研究生考研教材',26.80,0,1),(2,'11','covers/屏幕快照_2018-12-10_上午10.28.30.png','11e3rwegtrhyt',11.00,0,1),(3,'数据库系统原理','covers/屏幕快照_2018-12-10_上午10.54.10.png','数据库系统概论(第5版十二五普通高等教育本科规划教材) 计算机程序设计教程教材书籍数据结构编程入门计算机书籍',39.90,0,3),(4,'doc','covers/屏幕快照_2018-12-11_下午8.28.51_2fEngt4.png','wqdefvrbgthnytbgrvfewdwcefv',11.10,1,5),(5,'汉子','covers/屏幕快照_2018-12-11_下午8.28.51_v6dTn2b.png','wdewdefrgbtwdefrr',11.10,1,5),(6,'计算机组成','covers/屏幕快照_2018-12-11_下午8.28.51_HGQtsSG.png','计算机组成与设计硬件软件接口(原书第5版) 帕特森 亨尼斯 计算机教材 计算机专用书籍 王党辉 计算机网络 机械工业出版社',81.90,0,5),(7,'概率统计','covers/屏幕快照_2018-12-11_下午8.58.04.png','概率论浙大四版 概率论与数理统计 浙大第四版 教材+习题全解指南 盛骤 高等教育出版社 浙江大学概率论与数理统计(第4版)考研书籍',43.80,0,5),(8,'离散数学','covers/屏幕快照_2018-12-11_下午9.01.12.png','产品名称：离散数学及其应用 原书第7...ISBN编号: 9787111453826书名: 离散数学及其应用 原书第7版作者: Kenneth H. Rosen出版时间: 2015-01-01定价: 129.00元书名: 离散数学及其应用 原书第7版是否是套装: 否',92.90,0,5),(9,'数据结构与算法','covers/屏幕快照_2018-12-11_下午9.05.17.png','Python语言实现 python编程入门基础教程指南 计算机程序设计实践图书籍 基于Python3标准讲解数据结构与算法分析',76.00,0,5),(10,'数学建模','covers/屏幕快照_2018-12-11_下午9.06.36.png','数学建模方法与分析 原书第4版 数学译丛数学 数学分析 数学建模竞赛 大学数学专业书籍 数学建模竞赛的人员参考图书籍',39.90,0,5),(11,'数据结构','covers/屏幕快照_2018-12-11_下午9.08.18.png','数据结构题集 c语言版 严蔚敏 数据结构c语言版 数据结构题集 数据结构和算法习题 c语言数据结构 清华大学',21.50,0,5),(12,'基础物理','covers/屏幕快照_2018-12-11_下午9.09.26.png','科学 现代宇宙学 现代物理基础丛书 [美]Scott Dodelson 宇宙学研究前沿 理论物理 研究生教材 天文学 科研 科学出版社',98.90,0,5),(13,'基础物理实验','covers/屏幕快照_2018-12-11_下午9.10.52.png','【正版现货】基础物理实验（修订版）（十一五）/李朝荣　等编著',12.90,0,5),(14,'数据库系统原理','covers/屏幕快照_2018-12-11_下午9.12.05.png','正版现货 数据库系统概论第五版 王珊 萨师煊 计算机数据库基本原理 第5版 高等教育出版社 大学本科教材辅导用书A034',12.10,0,5),(15,'编译技术','covers/屏幕快照_2018-12-11_下午9.13.38.png','编译技术 张莉 高等教育出版社9787040463170基于系统能力培养的计算机专业课程建设研究 本科计算机类专业编译技术课程教材图书籍',12.60,0,5),(16,'高等数学','covers/屏幕快照_2018-12-11_下午9.15.28.png','复旦大学 数学分析第二版上下册教材 陈纪修+数学分析习题全解指南上下册 四本 高等教育出版 复旦数学分析全程辅导及习题精解',98.10,0,5),(17,'数学分析','covers/屏幕快照_2018-12-11_下午9.16.40.png','数学分析学习指导书 第四版第4版 上下册 华师大数学分析 数学分析.下册(第四版)辅导书 高等教育出版社 华东师范大学',9.50,0,5),(18,'高等代数','covers/屏幕快照_2018-12-11_下午9.17.32.png','王萼芳 高等代数 第四版第4版 北大四版 教材+辅导与习题解答 高等教育出版社 北京大学高等代数教程辅导与习题解答北大',11.20,0,5),(19,'C语言程序设计','covers/屏幕快照_2018-12-11_下午9.25.43.png','克尼汉正版 C程序设计语言 第二版 教材教辅+习题解答 共两本The C Programming Language 计算机科学丛书C语言书籍',22.10,0,5),(20,'英语','covers/屏幕快照_2018-12-11_下午9.27.01.png','现货速发English Grammar in Use全英文原版 英语在用剑桥初级中级高级英语语法 全套3册 实用大学英语语法大全手册自学教材书籍',32.50,0,5);
/*!40000 ALTER TABLE `bookdeal_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_car`
--

DROP TABLE IF EXISTS `bookdeal_car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_car` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookdeal_car_user_id_4176a9d0_fk_bookdeal_normal_user_ptr_id` (`user_id`),
  CONSTRAINT `bookdeal_car_user_id_4176a9d0_fk_bookdeal_normal_user_ptr_id` FOREIGN KEY (`user_id`) REFERENCES `bookdeal_normal` (`user_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_car`
--

LOCK TABLES `bookdeal_car` WRITE;
/*!40000 ALTER TABLE `bookdeal_car` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookdeal_car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_correct`
--

DROP TABLE IF EXISTS `bookdeal_correct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_correct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` varchar(1000) NOT NULL,
  `isFinish` tinyint(1) NOT NULL,
  `corrector_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookdeal_correct_corrector_id_76610026_fk_auth_user_id` (`corrector_id`),
  CONSTRAINT `bookdeal_correct_corrector_id_76610026_fk_auth_user_id` FOREIGN KEY (`corrector_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_correct`
--

LOCK TABLES `bookdeal_correct` WRITE;
/*!40000 ALTER TABLE `bookdeal_correct` DISABLE KEYS */;
INSERT INTO `bookdeal_correct` VALUES (1,'缺少概率统计',1,1);
/*!40000 ALTER TABLE `bookdeal_correct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_normal`
--

DROP TABLE IF EXISTS `bookdeal_normal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_normal` (
  `user_ptr_id` int(11) NOT NULL,
  `credit` decimal(2,1) NOT NULL,
  `info` varchar(50) NOT NULL,
  `isDelete` tinyint(1) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `grade` int(11) NOT NULL,
  `sale` int(11) NOT NULL,
  PRIMARY KEY (`user_ptr_id`),
  CONSTRAINT `bookdeal_normal_user_ptr_id_599a9a7c_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_normal`
--

LOCK TABLES `bookdeal_normal` WRITE;
/*!40000 ALTER TABLE `bookdeal_normal` DISABLE KEYS */;
INSERT INTO `bookdeal_normal` VALUES (1,5.0,'',0,'BUAA6',3,0),(4,5.0,'',0,'buaa6',2,0),(5,5.0,'',0,'BUAA6',2,0);
/*!40000 ALTER TABLE `bookdeal_normal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_order`
--

DROP TABLE IF EXISTS `bookdeal_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `buyer` varchar(20) NOT NULL,
  `brate` decimal(2,1) NOT NULL,
  `srate` decimal(2,1) NOT NULL,
  `date` datetime(6) NOT NULL,
  `isFinish` tinyint(1) NOT NULL,
  `book_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookdeal_order_book_id_id_c7d9231c_fk_bookdeal_book_id` (`book_id_id`),
  CONSTRAINT `bookdeal_order_book_id_id_c7d9231c_fk_bookdeal_book_id` FOREIGN KEY (`book_id_id`) REFERENCES `bookdeal_book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_order`
--

LOCK TABLES `bookdeal_order` WRITE;
/*!40000 ALTER TABLE `bookdeal_order` DISABLE KEYS */;
INSERT INTO `bookdeal_order` VALUES (1,'normal1',4.0,4.0,'2018-12-10 03:19:01.992250',1,3),(2,'normal1',4.0,0.0,'2018-12-11 10:41:51.089331',1,3),(3,'normal1',0.0,4.0,'2018-12-11 10:54:16.756047',1,3);
/*!40000 ALTER TABLE `bookdeal_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_report`
--

DROP TABLE IF EXISTS `bookdeal_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` varchar(1000) NOT NULL,
  `isFinish` tinyint(1) NOT NULL,
  `reporter_id` int(11) NOT NULL,
  `trans_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookdeal_report_reporter_id_f5062702_fk_auth_user_id` (`reporter_id`),
  KEY `bookdeal_report_trans_id_e1d87a05_fk_bookdeal_order_id` (`trans_id`),
  CONSTRAINT `bookdeal_report_reporter_id_f5062702_fk_auth_user_id` FOREIGN KEY (`reporter_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `bookdeal_report_trans_id_e1d87a05_fk_bookdeal_order_id` FOREIGN KEY (`trans_id`) REFERENCES `bookdeal_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_report`
--

LOCK TABLES `bookdeal_report` WRITE;
/*!40000 ALTER TABLE `bookdeal_report` DISABLE KEYS */;
INSERT INTO `bookdeal_report` VALUES (1,'商品存在质量问题，以盗版顶替二手',1,1,1);
/*!40000 ALTER TABLE `bookdeal_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_retailer`
--

DROP TABLE IF EXISTS `bookdeal_retailer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_retailer` (
  `user_ptr_id` int(11) NOT NULL,
  `credit` decimal(2,1) NOT NULL,
  `info` varchar(50) NOT NULL,
  `isDelete` tinyint(1) NOT NULL,
  `sale` int(11) NOT NULL,
  PRIMARY KEY (`user_ptr_id`),
  CONSTRAINT `bookdeal_retailer_user_ptr_id_68a63374_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_retailer`
--

LOCK TABLES `bookdeal_retailer` WRITE;
/*!40000 ALTER TABLE `bookdeal_retailer` DISABLE KEYS */;
INSERT INTO `bookdeal_retailer` VALUES (3,5.0,'',0,0);
/*!40000 ALTER TABLE `bookdeal_retailer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookdeal_rlist`
--

DROP TABLE IF EXISTS `bookdeal_rlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bookdeal_rlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `names` varchar(500) NOT NULL,
  `dept` varchar(50) NOT NULL,
  `grade` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookdeal_rlist`
--

LOCK TABLES `bookdeal_rlist` WRITE;
/*!40000 ALTER TABLE `bookdeal_rlist` DISABLE KEYS */;
INSERT INTO `bookdeal_rlist` VALUES (1,'数据库系统原理,编译技术,机器学习','BUAA6',3),(2,'计算机组成,概率统计,离散数学,算法设计与分析,数学建模,数据结构,基础物理,基础物理实验','BUAA6',2),(3,'数学分析,高等代数,C语言,英语','BUAA6',1);
/*!40000 ALTER TABLE `bookdeal_rlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'bookdeal','admin'),(8,'bookdeal','book'),(9,'bookdeal','car'),(10,'bookdeal','correct'),(11,'bookdeal','normal'),(12,'bookdeal','order'),(13,'bookdeal','report'),(14,'bookdeal','retailer'),(15,'bookdeal','rlist'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-12-10 02:25:24.078847'),(2,'auth','0001_initial','2018-12-10 02:25:24.350440'),(3,'admin','0001_initial','2018-12-10 02:25:24.435458'),(4,'admin','0002_logentry_remove_auto_add','2018-12-10 02:25:24.445844'),(5,'admin','0003_logentry_add_action_flag_choices','2018-12-10 02:25:24.455711'),(6,'contenttypes','0002_remove_content_type_name','2018-12-10 02:25:24.523829'),(7,'auth','0002_alter_permission_name_max_length','2018-12-10 02:25:24.559910'),(8,'auth','0003_alter_user_email_max_length','2018-12-10 02:25:24.600267'),(9,'auth','0004_alter_user_username_opts','2018-12-10 02:25:24.610913'),(10,'auth','0005_alter_user_last_login_null','2018-12-10 02:25:24.657453'),(11,'auth','0006_require_contenttypes_0002','2018-12-10 02:25:24.660471'),(12,'auth','0007_alter_validators_add_error_messages','2018-12-10 02:25:24.670073'),(13,'auth','0008_alter_user_username_max_length','2018-12-10 02:25:24.717683'),(14,'auth','0009_alter_user_last_name_max_length','2018-12-10 02:25:24.773510'),(15,'bookdeal','0001_initial','2018-12-10 02:25:25.256307'),(16,'sessions','0001_initial','2018-12-10 02:25:25.279173');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('l3wfbazhj9ni1u0y0vslp8rwv4mi0d4d','MjQ4NTA0NmRlNjVkZDYwOTk4NGIwZjIwM2RlM2UyZDMyZWE4Y2U3YTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiX2F1dGhfdXNlcl9pZCI6IjUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjkyNDhjOTBjYzcyZmU5YjFhOGEzMDQwZmIwZGM2MzkyOWRlN2QwNjgifQ==','2018-12-25 13:22:57.435806'),('s4f6e89cl42yl05asxxeipivugn0m3vr','ZGE4ODJhZTcwNzFlMmVkYzYyYTg3NjY3ZTk2OWY4MmI0MmIxZjU5Mzp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM4MWMzNWU5MWRjNGE0ZjQ1ZDUzNjU4YzAxNjZmY2VjYzRiOThhMDUifQ==','2018-12-24 03:27:43.143472');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-11 21:40:27
