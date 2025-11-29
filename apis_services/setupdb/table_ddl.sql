-- MySQL dump 10.13  Distrib 8.0.18, for linux-glibc2.12 (x86_64)
--
-- Host: localhost    Database: weather
-- ------------------------------------------------------
-- Server version       8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `wh1080data`
--

DROP TABLE IF EXISTS `wh1080data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wh1080data` (
  `time` text COLLATE utf8mb4_general_ci,
  `battery_ok` bigint(20) DEFAULT NULL,
  `humidity_in` double DEFAULT NULL,
  `temp_c_in` double DEFAULT NULL,
  `humidity` double DEFAULT NULL,
  `temperature_C` double DEFAULT NULL,
  `press_rel` double DEFAULT NULL,
  `rain_mm` double DEFAULT NULL,
  `wind_dir_deg` double DEFAULT NULL,
  `wind_avg_km_h` double DEFAULT NULL,
  `wind_max_km_h` double DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `rainchg` double DEFAULT NULL,
  `apressure` double DEFAULT NULL,
  `model` text COLLATE utf8mb4_general_ci,
  `id` double DEFAULT NULL,
  `mic` text COLLATE utf8mb4_general_ci,
  `subtype` double DEFAULT NULL,
  `year` text COLLATE utf8mb4_general_ci,
  `month` text COLLATE utf8mb4_general_ci,
  `day` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-29 21:44:02
