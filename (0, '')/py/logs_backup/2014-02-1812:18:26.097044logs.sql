-- MySQL dump 10.13  Distrib 5.5.31, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: fs2
-- ------------------------------------------------------
-- Server version	5.5.31-0+wheezy1

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
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `sno` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tstamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `type` varchar(40) DEFAULT NULL,
  `msg` longtext NOT NULL,
  `log_src` varchar(40) DEFAULT NULL,
  `more_info` longtext,
  PRIMARY KEY (`sno`),
  UNIQUE KEY `sno` (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'2014-02-18 06:22:26','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(2,'2014-02-18 06:24:30','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(3,'2014-02-18 06:25:01','INFO','Snapshot [SNP000NAS-nas_disk] removed successfully','SCRIPT','snap shot  delete_snapshot function'),(4,'2014-02-18 06:25:01','INFO','snapshot SNP000NAS-nas_disk created Successfully','SCRIPT','snap shot create_snapshot  function'),(5,'2014-02-18 06:25:01','INFO','INFO: snapshot disk successfully created for disk NAS-nas_disk','SCRIPT','snapshotschedule module rotate function'),(6,'2014-02-18 06:25:30','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(7,'2014-02-18 06:27:09','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(8,'2014-02-18 06:30:01','INFO','Snapshot [SNP001NAS-nas_disk] removed successfully','SCRIPT','snap shot  delete_snapshot function'),(9,'2014-02-18 06:30:01','INFO','snapshot SNP001NAS-nas_disk created Successfully','SCRIPT','snap shot create_snapshot  function'),(10,'2014-02-18 06:30:01','INFO','INFO: snapshot disk successfully created for disk NAS-nas_disk','SCRIPT','snapshotschedule module rotate function'),(11,'2014-02-18 06:36:13','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(12,'2014-02-18 06:38:48','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(13,'2014-02-18 06:40:01','INFO','Snapshot [SNP003NAS-nas_disk] removed successfully','SCRIPT','snap shot  delete_snapshot function'),(14,'2014-02-18 06:40:02','INFO','snapshot SNP003NAS-nas_disk created Successfully','SCRIPT','snap shot create_snapshot  function'),(15,'2014-02-18 06:40:02','INFO','INFO: snapshot disk successfully created for disk NAS-nas_disk','SCRIPT','snapshotschedule module rotate function'),(16,'2014-02-18 06:40:05','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(17,'2014-02-18 06:41:08','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(18,'2014-02-18 06:41:44','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(19,'2014-02-18 06:43:40','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(20,'2014-02-18 06:44:02','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(21,'2014-02-18 06:45:01','INFO','Snapshot [SNP000NAS-nas_disk] removed successfully','SCRIPT','snap shot  delete_snapshot function'),(22,'2014-02-18 06:45:01','INFO','snapshot SNP000NAS-nas_disk created Successfully','SCRIPT','snap shot create_snapshot  function'),(23,'2014-02-18 06:45:01','INFO','INFO: snapshot disk successfully created for disk NAS-nas_disk','SCRIPT','snapshotschedule module rotate function'),(24,'2014-02-18 06:45:49','ERROR','check if string is present in \"/tmp/.sessions/sessions.txt\" or not','SCRIPT','tools module \"get_string_from_file\" '),(25,'2014-02-18 06:46:05','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(26,'2014-02-18 06:47:00','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(27,'2014-02-18 06:48:07','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function'),(28,'2014-02-18 06:48:25','ERROR','INFO: All share informations fetched successfully.','SCRIPT','tools module create_share function');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-18 12:18:26
