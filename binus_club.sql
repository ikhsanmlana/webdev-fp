-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 05, 2020 at 04:50 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `binus_club`
--

-- --------------------------------------------------------

--
-- Table structure for table `clubs`
--

CREATE TABLE `clubs` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `members` int(11) NOT NULL,
  `image` varchar(20) NOT NULL DEFAULT 'default.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clubs`
--

INSERT INTO `clubs` (`id`, `name`, `contact`, `email`, `members`, `image`) VALUES
(1, 'Club 1 ', '081317621542', 'club1@gmail.com', 3, 'default.jpg'),
(2, 'Club 2', NULL, 'club2@gmail.com', 2, 'default.jpg'),
(3, 'Binary', NULL, NULL, 15, 'binary.png');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` varchar(10) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL,
  `role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_id`, `first_name`, `last_name`, `email`, `password`, `gender`, `batch`, `role`) VALUES
('2201794231', 'John', 'Doe', 'johnd@gmail.com', '$2b$12$t.CZrAXSs1RqCdH0kqs7MecFkM4c8iy5h7c917/leZ3yDOYx13za2', 'M', 22, NULL),
('2201794232', 'Test', 'Testtt', 'testt@gmail.com', '$2b$12$1I2C3FrwAkOiqVFMm5foBuIPQHXNdUAFKEkb6gZ8P4QcGPK.yqk.i', 'M', 22, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clubs`
--
ALTER TABLE `clubs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
