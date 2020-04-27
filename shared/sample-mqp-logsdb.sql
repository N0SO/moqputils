-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 25, 2020 at 04:32 PM
-- Server version: 10.3.22-MariaDB
-- PHP Version: 7.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mqptest`
--

-- --------------------------------------------------------

--
-- Table structure for table `LOGHEADER`
--

CREATE TABLE `LOGHEADER` (
  `ID` int(11) NOT NULL,
  `START` varchar(20) DEFAULT NULL,
  `CALLSIGN` varchar(10) DEFAULT NULL,
  `CREATEDBY` varchar(50) DEFAULT NULL,
  `LOCATION` varchar(10) DEFAULT NULL,
  `CONTEST` varchar(30) DEFAULT NULL,
  `NAME` varchar(40) NOT NULL,
  `ADDRESS` varchar(120) NOT NULL,
  `CITY` varchar(40) NOT NULL,
  `STATEPROV` varchar(40) NOT NULL,
  `ZIPCODE` varchar(12) NOT NULL,
  `COUNTRY` varchar(25) NOT NULL,
  `EMAIL` varchar(40) NOT NULL,
  `CATASSISTED` varchar(20) NOT NULL,
  `CATBAND` varchar(10) NOT NULL,
  `CATMODE` varchar(20) NOT NULL,
  `CATOPERATOR` varchar(20) NOT NULL,
  `CATOVERLAY` varchar(20) NOT NULL,
  `CATPOWER` varchar(10) NOT NULL,
  `CATSTATION` varchar(20) NOT NULL,
  `CATXMITTER` varchar(20) NOT NULL,
  `CERTIFICATE` varchar(10) NOT NULL,
  `OPERATORS` varchar(120) NOT NULL,
  `CLAIMEDSCORE` varchar(20) NOT NULL,
  `CLUB` varchar(120) NOT NULL,
  `IOTAISLANDNAME` varchar(40) NOT NULL,
  `OFFTIME` varchar(20) NOT NULL,
  `SOAPBOX` varchar(120) NOT NULL,
  `ENDOFLOG` varchar(20) NOT NULL,
  `MOQPCAT` varchar(60) NOT NULL,
  `STATUS` varchar(20) NOT NULL,
  `CABBONUS` int(11) NOT NULL DEFAULT 100,
  `TIMESTAMP` timestamp(6) NOT NULL DEFAULT current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `MISSOURI`
--

CREATE TABLE `MISSOURI` (
  `ID` int(11) NOT NULL,
  `LOGID` int(11) NOT NULL DEFAULT 0,
  `M` varchar(6) NOT NULL DEFAULT '',
  `I_1` varchar(6) DEFAULT '',
  `S_1` varchar(6) NOT NULL DEFAULT '',
  `S_2` varchar(6) NOT NULL DEFAULT '',
  `O` varchar(6) NOT NULL DEFAULT '',
  `U` varchar(6) NOT NULL DEFAULT '',
  `R` varchar(6) NOT NULL DEFAULT '',
  `I_2` varchar(6) NOT NULL DEFAULT '',
  `WC` varchar(6) NOT NULL DEFAULT '',
  `QUALIFY` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `QSOS`
--

CREATE TABLE `QSOS` (
  `ID` int(11) NOT NULL,
  `LOGID` int(11) NOT NULL,
  `FREQ` varchar(20) NOT NULL,
  `MODE` varchar(20) NOT NULL,
  `DATE` varchar(12) NOT NULL,
  `TIME` varchar(10) NOT NULL,
  `MYCALL` varchar(20) NOT NULL,
  `MYREPORT` varchar(6) NOT NULL,
  `MYQTH` varchar(10) NOT NULL,
  `URCALL` varchar(20) NOT NULL,
  `URREPORT` varchar(6) NOT NULL,
  `URQTH` varchar(10) NOT NULL,
  `VALID` tinyint(1) NOT NULL DEFAULT 0,
  `QSL` int(11) NOT NULL DEFAULT 0,
  `NOLOG` tinyint(1) NOT NULL DEFAULT 0,
  `NOQSOS` tinyint(1) NOT NULL DEFAULT 0,
  `NOTE` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SHOWME`
--

CREATE TABLE `SHOWME` (
  `ID` int(11) NOT NULL,
  `LOGID` int(11) NOT NULL,
  `S` varchar(15) NOT NULL DEFAULT '',
  `H` varchar(15) NOT NULL DEFAULT '',
  `O` varchar(15) NOT NULL DEFAULT '',
  `W` varchar(15) NOT NULL DEFAULT '',
  `M` varchar(15) NOT NULL DEFAULT '',
  `E` varchar(15) NOT NULL DEFAULT '',
  `WC` varchar(6) NOT NULL DEFAULT '',
  `QUALIFY` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SUMMARY`
--

CREATE TABLE `SUMMARY` (
  `ID` int(11) NOT NULL,
  `LOGID` int(11) NOT NULL DEFAULT 0,
  `CWQSO` int(11) NOT NULL DEFAULT 0,
  `PHQSO` int(11) NOT NULL DEFAULT 0,
  `RYQSO` int(11) NOT NULL DEFAULT 0,
  `VHFQSO` int(11) NOT NULL DEFAULT 0,
  `MULTS` int(11) NOT NULL DEFAULT 0,
  `QSOSCORE` int(11) NOT NULL DEFAULT 0,
  `W0MABONUS` int(11) NOT NULL DEFAULT 0,
  `K0GQBONUS` int(11) NOT NULL DEFAULT 0,
  `CABBONUS` int(11) NOT NULL DEFAULT 0,
  `SCORE` int(11) NOT NULL DEFAULT 0,
  `MOQPCAT` varchar(50) NOT NULL,
  `DIGITAL` tinyint(1) NOT NULL DEFAULT 0,
  `VHF` tinyint(1) NOT NULL DEFAULT 0,
  `ROOKIE` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `LOGHEADER`
--
ALTER TABLE `LOGHEADER`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `MISSOURI`
--
ALTER TABLE `MISSOURI`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `QSOS`
--
ALTER TABLE `QSOS`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `SHOWME`
--
ALTER TABLE `SHOWME`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `SUMMARY`
--
ALTER TABLE `SUMMARY`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `LOGHEADER`
--
ALTER TABLE `LOGHEADER`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `MISSOURI`
--
ALTER TABLE `MISSOURI`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `QSOS`
--
ALTER TABLE `QSOS`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `SHOWME`
--
ALTER TABLE `SHOWME`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `SUMMARY`
--
ALTER TABLE `SUMMARY`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
