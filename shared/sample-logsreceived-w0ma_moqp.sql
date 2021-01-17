-- phpMyAdmin SQL Dump
-- version 4.9.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 25, 2020 at 01:52 PM
-- Server version: 10.3.22-MariaDB
-- PHP Version: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `w0ma_moqp_2020`
--

-- --------------------------------------------------------

--
-- Table structure for table `logs_received`
--

CREATE TABLE `logs_received` (
  `ID` int(10) UNSIGNED NOT NULL COMMENT 'Table index',
  `STA_CALL` text NOT NULL COMMENT 'Callsign used during event',
  `CATEGORY` enum('Expedition Single Op','Fixed Single Op','Fixed Multi-Op','Mobile Single-Op','Mobile Multi-Op','Mobile Unlimited','Expedition Multi-Op') DEFAULT NULL,
  `POWER` enum('QRP','LP','HP') DEFAULT NULL,
  `MODE` enum('CW','PH','DIGITAL','MIXED') DEFAULT NULL,
  `OP_NAME` text NOT NULL COMMENT 'Name of the op holding the callsign used',
  `MY_CALL` text DEFAULT NULL COMMENT 'Real call of the CALLSIGN (if different than CALL',
  `RECEIVED_BY` enum('EMAIL','WEB','OTHER') DEFAULT NULL COMMENT 'Submitted by e-mail, web, other?',
  `LOCATION` text DEFAULT NULL COMMENT 'QTH during contest',
  `EMAIL` text DEFAULT NULL COMMENT 'Email address',
  `ADDRESS_1` text DEFAULT NULL,
  `ADDRESS_2` text DEFAULT NULL,
  `ADDRESS_3` text DEFAULT NULL,
  `SOAPBOX` text DEFAULT NULL,
  `FILENAME` text DEFAULT NULL COMMENT 'Path to logfile',
  `DATE_REC` datetime DEFAULT NULL COMMENT 'Date of entry or update',
  `EMAILSUBJ` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='For recording station submitting logs';

-- --------------------------------------------------------

--
-- Table structure for table `mocounties`
--

CREATE TABLE `mocounties` (
  `ID` int(10) UNSIGNED NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `code` varchar(3) DEFAULT NULL,
  `coords` varchar(15) NOT NULL DEFAULT '248,301,22'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE `routes` (
  `ID` int(10) UNSIGNED NOT NULL COMMENT 'Record ID',
  `STATION_ID` int(10) UNSIGNED NOT NULL COMMENT 'Record ID of station from stations_registered table owning this route',
  `EVENT_DAY` enum('SAT','SUN') NOT NULL DEFAULT 'SAT' COMMENT 'Day this route is for',
  `COMMENTS` text DEFAULT NULL COMMENT 'Comments',
  `DATE` datetime NOT NULL COMMENT 'Date route is created'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `route_entries`
--

CREATE TABLE `route_entries` (
  `ID` int(10) UNSIGNED NOT NULL COMMENT 'Table index',
  `ROUTE_ID` int(10) UNSIGNED NOT NULL COMMENT 'ID from routes table',
  `STATION_ID` int(10) UNSIGNED NOT NULL COMMENT 'IID from stations table',
  `ROUTE_SEQ` int(10) NOT NULL COMMENT 'Order sequence for this route',
  `COUNTY_ID` int(10) UNSIGNED NOT NULL COMMENT 'ID from mocounties table',
  `DATE` datetime NOT NULL COMMENT 'Date this element entered.'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `stations_registered`
--

CREATE TABLE `stations_registered` (
  `ID` int(10) UNSIGNED NOT NULL,
  `CALLSIGN` varchar(15) DEFAULT NULL COMMENT 'Call used in event',
  `NAME` text DEFAULT NULL COMMENT 'Call used custodian',
  `CLUB` text DEFAULT NULL COMMENT 'Club name or additional Operators call(s)',
  `EMAIL` text DEFAULT NULL,
  `MODE` enum('CW','PHONE','MIXED','CW+DIGITAL','PHONE+DIGITAL','MIXED+DIGITAL') DEFAULT 'MIXED',
  `POWER` enum('QRP','LOW','HIGH') DEFAULT NULL,
  `CATEGORY` enum('FIXED SINGLE OP','FIXED MULTI OP','MOBILE SINGLE OP','MOBILE MULTI OP','MOBILE UNLIMITED','EXPEDITION') DEFAULT NULL,
  `VHF` enum('NO','YES') DEFAULT 'NO',
  `SAT_ROUTE` int(10) UNSIGNED DEFAULT 0 COMMENT 'Index to Saturday county / route',
  `SUN_ROUTE` int(10) UNSIGNED DEFAULT 0 COMMENT 'Index to Sunday county / route',
  `DATE` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'Date / time registered',
  `COMMENTS` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `logs_received`
--
ALTER TABLE `logs_received`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `mocounties`
--
ALTER TABLE `mocounties`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `routes`
--
ALTER TABLE `routes`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `route_entries`
--
ALTER TABLE `route_entries`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `stations_registered`
--
ALTER TABLE `stations_registered`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `logs_received`
--
ALTER TABLE `logs_received`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Table index';

--
-- AUTO_INCREMENT for table `mocounties`
--
ALTER TABLE `mocounties`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `routes`
--
ALTER TABLE `routes`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Record ID';

--
-- AUTO_INCREMENT for table `route_entries`
--
ALTER TABLE `route_entries`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Table index';

--
-- AUTO_INCREMENT for table `stations_registered`
--
ALTER TABLE `stations_registered`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
