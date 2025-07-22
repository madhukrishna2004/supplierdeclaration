-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: central_db
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `email_logs`
--

DROP TABLE IF EXISTS `email_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `email_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `recipient` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` text,
  `sheet_link` text NOT NULL,
  `sent_time` datetime NOT NULL,
  `form_link` text,
  `pdf_link` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `email_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_logs`
--

LOCK TABLES `email_logs` WRITE;
/*!40000 ALTER TABLE `email_logs` DISABLE KEYS */;
INSERT INTO `email_logs` VALUES (1,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1MgOxvRuoe0e4a45xgcHZr25ClVAo7gEAfaED9-jmgRg','2025-02-17 12:36:39',NULL,NULL),(2,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/15QM9Vd-TJtfwpZuCLl6s7yEOpNAaH0vvnWmatweclEo','2025-02-17 12:36:41',NULL,NULL),(3,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1x8Qvu6Ja8vnQSR2K6McVWYB0hJqIGo1XquNHyZdMGV8','2025-02-17 17:56:47',NULL,NULL),(4,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/199sxDwAgZeQKoZ91iz33mcrzkNF-0iY6CiRkcRG_FQM','2025-02-17 17:56:50',NULL,NULL),(5,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1HXbj9_YKH4k7XTSilagSV44vy9vfrig3K9yIfKHG-n4','2025-02-17 18:10:27',NULL,NULL),(6,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/125_tYUiLtyH3bNDpGrQpxMq9ln6HkJJpAun5mzK6fKI','2025-02-17 18:10:30',NULL,NULL),(7,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1SXvDfsRYE_B5rV7ydFxxbaT9BrfSgApVle8LmoHnKb8','2025-02-17 21:39:32',NULL,NULL),(8,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1B630HE4AufOHj5XFd6NYOHXTZ8zkJE77N8Hk5bKBn5Y','2025-02-17 21:39:37',NULL,NULL),(9,5,'krama7275@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1ZfGiTnnxiqrTnn0ZNeuTU3uQkgzT8o5RkRF042yLdtE','2025-02-17 21:39:42',NULL,NULL),(10,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1xUJ9QCx9W6TIChlOzZhrCaIEP1ffM_GT3I4-a3BK-x0','2025-02-17 23:00:37',NULL,NULL),(11,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/16LnJmqHUubtU3yKR7n5O07OyyQyMXkJkZw8TDoi47IE','2025-02-19 09:19:36',NULL,NULL),(12,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1C9hXDahaQAQRUnj0_QnUOpuKZTPw_KrY9U8mfZSdxH4','2025-02-19 09:19:39',NULL,NULL),(13,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/12fk898nsYmaKpUMlfBvDgy1FC_Q_1aVM2GhLG9L2W2M','2025-02-19 09:26:00',NULL,NULL),(14,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1EcXeuImBq05yRFUvTjjonYtY87RkeH9qy_-xWzQ3n9A','2025-02-19 09:26:04',NULL,NULL),(15,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1cmmXonJjLONyvOsxTWkwY-uXL5Wfq0PAFDS8ARIudPk','2025-02-19 09:33:30',NULL,NULL),(16,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/12oOIPZgb2TW21Llg3QKA_YCjZMa0pNkJdNHX-PQPIow','2025-02-19 09:33:32',NULL,NULL),(17,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1wgQXtXBiRwycaYbE6sgRjL_PXz6si6BZqlonNiBWyNg','2025-02-19 09:40:17',NULL,NULL),(18,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1XVZo5TPtWz20nMuo7Cwoa0ezMnfrU5T0swOmcW8Vj9w','2025-02-19 09:40:20',NULL,NULL),(19,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1fJUwPrr6zq4lD-nDBsxZhvDhARRQBvNV4685_BzSLJU','2025-02-19 10:29:15',NULL,NULL),(20,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1WRUtXFIEKm6088cNPyR_x8tU48239C1Cg6Am148XI8s','2025-02-19 10:29:17',NULL,NULL),(21,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/101shAlNo0Mti9bFe2CS0jLLQDP8xzEELyxk0CDDCTe4','2025-02-19 12:13:14','https://docs.google.com/forms/d/1dOWdzXzw8t1LDKzBiZJyHu3FzK2B-ksYZJmNa_xEbuk/edit',NULL),(22,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1TmSncrPf3pcUkbwwEPTsWi2cPZ7UAF4L0oVE5-M7yz0','2025-02-19 12:13:17','https://docs.google.com/forms/d/1vXhGoVqQnVn61K_Ngz69qywNo7UBUypHInWb3lKJq5c/edit',NULL),(23,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1H40aIl99weS3YJRBA641vfL-cghnDzuYeSjq2zi3TDU','2025-02-19 12:23:47','https://docs.google.com/forms/d/1NecyBMUy_nYKJv-gBttypb7iAtKsE_DzUaIK2VZiJ6g/edit',NULL),(24,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1kO94xFCrJKSN453OagRGrDKkms_gjUagloj0-Qs1JG8','2025-02-19 12:23:50','https://docs.google.com/forms/d/1oyjDTCwT1itiRdi0E8pPh0ZDzKJjffeYBEJBz4yLRG8/edit',NULL),(25,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1isLKrrzpPq1HtKzXyS7GfOPfoiGqVbciPilD9EfWaBQ','2025-02-19 12:52:14','https://docs.google.com/forms/d/1ZO5--Kd-uZTi4CwDNFsBYeK3sbugYbVZ4JVlpJEswb4/edit',NULL),(26,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1Xa4ftDPz36AO337Ij6YzT5vGlY-WZi4tCpEP0CjiC_Y','2025-02-19 12:52:17','https://docs.google.com/forms/d/1anq7Th6I9niNlCU6EOIlqmMS_el0jDmOh2QdfnDyzxE/edit',NULL),(27,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1aSXK2B9oRKMST-xHVBhfJ0lO1eWOL4dp68-Grruy6Y0','2025-02-19 12:56:45','https://docs.google.com/forms/d/1j09We6J0BShZg7as3Y0zST3RlOQ9I6vfqkqK47I0YeE/edit',NULL),(28,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1_EjO-dYKoRYJOibDm72m_0wJMoxwsb7iZyF4MJ1YCuo','2025-02-19 13:20:55','https://docs.google.com/forms/d/1Gv-FcJoEXuyq6auhyILaf1_KEdda-2R3ZlV9cQPhNTI/edit',NULL),(29,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1WQ9eoTNY4tW3gdNRgb1BIkJUe_xw0-k178BaYpDUb0k','2025-02-19 13:20:58','https://docs.google.com/forms/d/1zyU6ETOkJ4nbd7S7bPamN1-0BSgczZRO4shKXW0magU/edit',NULL),(30,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1AJleODfDMudBBeFqDCdTY7WAPnGO8sMFh0M_YI3cW5U','2025-02-19 13:30:32','https://docs.google.com/forms/d/1tpa4NB2EMrekWzCoDrbbOIPwkvb5sQLSL4d1SFKBges/edit',NULL),(31,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1TdBYi1BzZvYUosuQBCJi66ZwwQw37WNhe8J_CrPwVeI','2025-02-19 13:30:35','https://docs.google.com/forms/d/1PISiuUONZEjRAchkW_LRQtSePjc7CkloaH-p7d_FICE/edit',NULL),(32,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1VBow3ZDKb-G1HTVA97cQDiiovWOn_7PvyDxz8Oa3mAQ','2025-02-19 13:45:43','https://docs.google.com/forms/d/1UgIyir0mQBlSUknmoOmjlHZD-WDFV1_fFPxxGiOGtCY/edit',NULL),(33,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1mufyJkkFkyhbtzD-MajyHD0ZBaNJsdfGJgAMLqg4kf0','2025-02-19 13:45:46','https://docs.google.com/forms/d/1RC04Uciy02i7gZOFvfsuLAQ2aXREiGtOWSL052a5n18/edit',NULL),(34,5,'krishnamadhurama@gmail.com','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1O4A22MfzRzwMcV59UfpzaQoDN2aV43hHpt7lp-IJgFk','2025-02-20 15:00:10','https://docs.google.com/forms/d/1VVny03qEu3W66iHO8NSr8CbBvJ_wcID3X2Pe1CvQmWQ/edit',NULL),(35,5,'RKLSGROUPS@GMAIL.COM','Requesting Supplier Declaration','Dear Supplier, please complete the attached form and submit it.','https://docs.google.com/spreadsheets/d/1R48HNqNdGpSw9eulxP815FOEhUKm3-KL2hv5LHO0jXo','2025-02-20 15:00:12','https://docs.google.com/forms/d/1KAW-vEHSxQ5p2CuehKR08gftcH1XR_edaXHWDXpBAhc/edit',NULL),(36,5,'krishnamadhurama@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1ei_QkH3_1qEyq_jlaqZ1rLC6h5g7hteYxzKZu9wXVQ8','2025-02-22 11:04:31','https://docs.google.com/forms/d/1p-R6khgOs4VhhUQBuzwH-F_lnDnZpwp9Q93ECQy0HK0/edit',NULL),(37,5,'RKLSGROUPS@GMAIL.COM','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1dQJ6-kZ6NtpnMpVZ0dIuA-0kqBMu2dshGftgSbzPf6Y','2025-02-22 11:04:39','https://docs.google.com/forms/d/1STBZlFw5QQBWD9mPy4oKTL4De1qRAuG9uWM7w2QB930/edit',NULL),(38,5,'krishnamadhurama@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/15csl6-XkdfNnfkeyhiHbdp9aT72gwIZZlQj2msJ08MA','2025-02-22 13:31:09','https://docs.google.com/forms/d/1jQOXmVMtJYTWPRX985Rdo2XMnDQF2YDhRZGxFbdqFGw/edit',NULL),(39,5,'RKLSGROUPS@GMAIL.COM','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1L7WHWEJagUKhE0i6UoYB-uXDYQU2EzVjv8wETe73JJ0','2025-02-22 13:31:16','https://docs.google.com/forms/d/1wUPJM2XWMVIpPxfv93WyTCfo2KTdweS1PlB03XUw-Cs/edit',NULL),(40,5,'krishnamadhurama@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1zo6XEZzgvTFKem0sLqnm2hWwB_Y4ff3fRJw18GRsBBo','2025-02-22 19:59:28','https://docs.google.com/forms/d/1uZ7T8CkqDJRpELAeqmlQO1cbPZJRKRe2qjUA039fPqo/edit',NULL),(41,5,'RKLSGROUPS@GMAIL.COM','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1abJ8tPxfOfKkVEh_7znOviiY37dCk7R4gAJ04nKXEXo','2025-02-22 19:59:45','https://docs.google.com/forms/d/1nfHL8kRJ8eFWcq_xRsbvqchHiWFe5z9wVtHPC6DUIGM/edit',NULL),(42,5,'krishnamadhurama@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1IjfAABrHj6e5Skqyna1R-Jab4dO19S_65V5_mdO0aQ4','2025-02-22 20:30:52','https://docs.google.com/forms/d/1nCtDvzo3DwZ1V2-3QtzgYdveix7-9wa62B0J6NvKwqE/edit',NULL),(43,5,'RKLSGROUPS@GMAIL.COM','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1_PJrvFjMWI1J1J1UX0wltnDBz2qIdT2EpHxSJXkuP4w','2025-02-22 20:31:11','https://docs.google.com/forms/d/1zlIUJ14CSmhk5ZgZkLY7le1hK7xjI_V_bMzW-WNvnWM/edit',NULL),(44,5,'krishnamadhurama@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1hBoyndK18WbUFct363NfgIXYihfPs9ESv8Y39l5s7ZE','2025-02-22 21:13:23','https://docs.google.com/forms/d/1VKxdP32_72QXQKWiBUgO9ttj2siY0eYcIHHJ752K6b8/edit',NULL),(45,5,'RKLSGROUPS@GMAIL.COM','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1tnbrV1MuggNvIStpM9heJjZybTlTF9XtjEysoeJ0V20','2025-02-22 21:13:43','https://docs.google.com/forms/d/1Nyxud3wp6gxqNbvq_4MmCjsKoxqr86bpWzxETMwx3XQ/edit',NULL),(46,5,'krishnamadhurama@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1o_Kg91lsK-moy5a9SLslXrV3KhQ88I17FDfzMEUjxIM','2025-02-22 21:30:56','https://docs.google.com/forms/d/1nzBbme6Du__210e-v0hpVnXTp19iLktadODqehDhiGY/edit',NULL),(47,5,'RKLSGROUPS@GMAIL.COM','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1saiow9sYs7D319OeqKq7864vh8ihSO5gs4jp26YQdwk','2025-02-22 21:31:19','https://docs.google.com/forms/d/1eIeutnysvS15oAjwGDwFx8k00zGfh9SJqaRmasLQH4U/edit',NULL),(48,5,'bannurusashidhar21@gmail.com','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1EAVHFAFgBHonTJT8aK9C-YkB8031ydyKl0aTpIvstaY','2025-02-22 21:31:45','https://docs.google.com/forms/d/13v1BpdxHGsigTB5_Zw8JilaG6641HT0omrw-0wBSNDk/edit',NULL),(49,5,'21021771@geu.ac.in','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1py0LxM4WVvrBvdNWlIJJz2JOHt996oqAIm5apshD2Xs','2025-03-05 23:42:22','https://docs.google.com/forms/d/1NGHy70Cvt4L6uSWJxn_hCsJxhsiHWaTNknzHdLux__0/edit',NULL),(50,5,'21021771@geu.ac.in','? Official Request: Supplier Declaration Submission',NULL,'https://docs.google.com/spreadsheets/d/1znVf_GbJPbeJemNPkxBO8u6mG5k2JV44TFVjA2Qp_NA','2025-03-05 23:46:34','https://docs.google.com/forms/d/1SfPwUOSynxCk5MPkj-dOgO5Hwefv2HfuAaqt_4fYPP0/edit',NULL);
/*!40000 ALTER TABLE `email_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emails`
--

DROP TABLE IF EXISTS `emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `recipient_email` varchar(255) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `body` text,
  `attachments` json DEFAULT NULL,
  `sent_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails`
--

LOCK TABLES `emails` WRITE;
/*!40000 ALTER TABLE `emails` DISABLE KEYS */;
/*!40000 ALTER TABLE `emails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `google_form_link` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploads`
--

DROP TABLE IF EXISTS `uploads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `file_type` varchar(50) DEFAULT NULL,
  `upload_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `file_path` varchar(500) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploads`
--

LOCK TABLES `uploads` WRITE;
/*!40000 ALTER TABLE `uploads` DISABLE KEYS */;
/*!40000 ALTER TABLE `uploads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `organization` varchar(255) NOT NULL,
  `company_email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'krishnamadhurama@gmail.com','scrypt:32768:8:1$IpkVVHaEudkeTdHI$1afddd231c21088819b07b08759754af847470b6ca7ef538612df2d5babc45ebb034673b7e82da3541807c0b76d26ab6e3bff12992484acdc23a52305dc02cbf','','',''),(5,'RKLSGROUPS@GMAIL.COM','$2b$12$VptL1BnMD.zHnXJcIS8PsewX20piEo554UyWqIu8y7P43JmR49jgi','','',''),(6,'madhu@999','$2b$12$ItiX56a/FawL4IEWtpgjleuNeJt29bFniZkBYzNhFLKSWZqe2ukDy','','',''),(7,'madhu@krishna','$2b$12$Wm2C90dtoefQLrCwuPkHjOT16F9I2sGJRG7UJ.a4cdlB7KmwX7ph.','madhu krishna','RKLS Groups','RKLSGROUPS@GMAIL.COM'),(8,'lakshmi@9100','$2b$12$kldv3cGdUiwnoZ.5KUuN/OAK1dMQN/xNKhag16.NMTmbWY0rlvzZi','Madhu Krishna','rkls',NULL),(9,'madhu@8074','$2b$12$JDmLPv5zdI7xXvRFmk4veO.H6auxHniSeFiHAopzqTR4Im3TDTF0m','Madhu Krishna','sreeis rkls',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-07 14:01:21
