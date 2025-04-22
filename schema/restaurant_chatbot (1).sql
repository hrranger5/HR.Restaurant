-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 22, 2025 at 06:52 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant_chatbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `password`) VALUES
(1, 'SuperAdmin', 'admin@example.com', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `chat_sessions`
--

CREATE TABLE `chat_sessions` (
  `session_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_message` text NOT NULL,
  `chatbot_response` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_sessions`
--

INSERT INTO `chat_sessions` (`session_id`, `user_id`, `user_message`, `chatbot_response`, `timestamp`) VALUES
(1, 1, 'Hello, I want to place an order.', 'Sure! What would you like to order?', '2025-03-11 04:33:17'),
(2, 2, 'Can I book a table for 2 at 8 PM?', 'Yes, I can book that for you. Please confirm.', '2025-03-11 04:33:17');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `comments` text NOT NULL,
  `rating` int(11) DEFAULT NULL CHECK (`rating` between 1 and 5),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedback_id`, `user_id`, `comments`, `rating`, `created_at`) VALUES
(1, 1, 'Great service and delicious food!', 5, '2025-03-11 04:33:17'),
(2, 2, 'The pizza was amazing but delivery was slow.', 4, '2025-03-11 04:33:17'),
(3, 1, 'Great service!', 5, '2025-03-14 16:29:28');

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `item_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` enum('starter','main_course','dessert','beverage') NOT NULL,
  `availability` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`item_id`, `name`, `description`, `price`, `category`, `availability`) VALUES
(2, 'Margherita Pizza', 'Classic Italian pizza with fresh basil', 1200.00, 'main_course', 1),
(3, 'Chocolate Cake', 'Rich and moist chocolate cake', 750.00, 'dessert', 1),
(4, 'Cappuccino', 'Freshly brewed cappuccino coffee', 350.00, 'beverage', 1),
(5, 'Burger', NULL, 350.00, 'starter', 1),
(6, 'Pizza', 'Cheese Burst Pizza', 750.00, 'main_course', 1),
(7, 'Pizza', 'Cheese Burst Pizza', 750.00, 'main_course', 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `order_status` enum('pending','preparing','completed','cancelled') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `total_price`, `order_status`, `created_at`) VALUES
(1, 1, 1800.00, 'pending', '2025-03-11 04:33:17'),
(2, 2, 750.00, 'completed', '2025-03-11 04:33:17'),
(3, 1, 0.00, 'pending', '2025-03-17 12:34:08');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `item_id`, `quantity`, `price`) VALUES
(2, 1, 2, 1, 1200.00),
(3, 2, 3, 1, 750.00),
(4, 3, 2, 1, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `reservation_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `num_guests` int(11) NOT NULL,
  `reservation_time` datetime NOT NULL,
  `status` enum('pending','confirmed','cancelled') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`reservation_id`, `user_id`, `num_guests`, `reservation_time`, `status`, `created_at`) VALUES
(1, 1, 4, '2025-03-15 19:00:00', 'confirmed', '2025-03-11 04:33:17'),
(2, 2, 2, '2025-03-16 20:30:00', 'pending', '2025-03-11 04:33:17'),
(3, 1, 4, '2025-03-15 18:30:00', 'pending', '2025-03-14 16:27:29');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` enum('customer','admin') DEFAULT 'customer',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password_hash`, `phone`, `role`, `created_at`) VALUES
(1, 'Ali Khan', 'ali@example.com', 'hashed_password_1', '03001234567', 'customer', '2025-03-11 04:33:17'),
(2, 'Sara Ahmed', 'sara@example.com', 'hashed_password_2', '03111234567', 'customer', '2025-03-11 04:33:17'),
(3, 'Admin User', 'admin@example.com', 'hashed_password_admin', '03221234567', 'admin', '2025-03-11 04:33:17'),
(6, 'testuser', 'testuser@example.com', '$2b$12$QRUcJQWY.nRedRxddhfxFuHmuy5cONloQz8CMpm3vFjfQXR1kDVoe', NULL, 'customer', '2025-03-15 09:34:05'),
(7, 'testuser', '', '$2b$12$N9ahaUu7KxW8vSTuISdJn.tOuw0SektACuv7L9PRGjzDSde8kgyZu', NULL, 'customer', '2025-03-16 12:01:00'),
(9, 'testuser2', 'test2@example.com', '$2b$12$594NBYblSnkKhDAhD5oNoebdaXGtOlwZHMn52vhA3MEnGa5zORGeq', NULL, 'customer', '2025-03-16 12:22:45'),
(10, 'Hafsa', 'hrranger555@gmail.com', '$2b$12$ZAtLrp0HkAjTvvp1iAFdA.wCJdMqPRx6wEC5PMisqA7vEF.FBizji', NULL, 'customer', '2025-03-18 12:46:57'),
(11, 'Hafsa', 'bc210414048hja@vu.edu.pk', '$2b$12$JLZVu4hCn1W/k2Fc3fqHSugEiPkIdgkv9is98815AHnCV54zPvgmC', NULL, 'admin', '2025-03-18 12:50:17'),
(12, 'Rohan Ahmad', 'rohan@modernint.sa', '$2b$12$YkDtuWOJTXgIV.P6kTar6OqIEPMdgR6VFvNcAQasfBb4VFiRQT3cu', NULL, 'customer', '2025-03-20 05:25:57'),
(13, 'Rohan Ahmad', 'ma.mra913@gmail.com', '$2b$12$L.UKkbg409MsW5Ro.jVpEO2.CwZuThDkTljR4ARanXd5cBFuIlS1q', NULL, 'customer', '2025-04-11 12:13:33'),
(14, 'Hafsa Javed', 'hrranger11@gmail.com', '$2b$12$wc35RdVmckKaI4O1Gz3tkuDebycYtHti7/lcc1GxsJjVivhb8Cl96', NULL, 'customer', '2025-04-17 15:01:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `chat_sessions`
--
ALTER TABLE `chat_sessions`
  ADD PRIMARY KEY (`session_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`item_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`reservation_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `chat_sessions`
--
ALTER TABLE `chat_sessions`
  MODIFY `session_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `feedback_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `reservation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat_sessions`
--
ALTER TABLE `chat_sessions`
  ADD CONSTRAINT `chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `menu_items` (`item_id`) ON DELETE CASCADE;

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
