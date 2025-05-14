-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 14, 2025 at 08:19 AM
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
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `food_item` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `order_id`, `food_item`, `quantity`) VALUES
(1, 4, 'burger', 1),
(2, 5, 'pizza', 1),
(3, 6, 'coffee', 2),
(4, 7, 'fry fish', 1),
(5, 8, 'biryani', 3),
(6, 9, 'biryani', 3),
(7, 14, 'burger', 1),
(8, 17, 'burger', 16),
(9, 18, 'burger', 16),
(10, 21, 'pizza', 1);

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `feedback_text` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedback_id`, `user_id`, `feedback_text`, `timestamp`) VALUES
(2, 4, 'slow', '2025-05-06 02:24:25'),
(3, 4, 'service was slow', '2025-05-06 02:25:19'),
(4, 4, 'service was slow', '2025-05-06 02:29:29');

-- --------------------------------------------------------

--
-- Table structure for table `menu_categories`
--

CREATE TABLE `menu_categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `display_order` int(11) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_categories`
--

INSERT INTO `menu_categories` (`category_id`, `name`, `description`, `image_url`, `display_order`, `is_active`) VALUES
(1, 'Starters', 'Begin your culinary journey', NULL, 1, 1),
(2, 'Main Course', 'Hearty and satisfying dishes', NULL, 2, 1),
(3, 'Desserts', 'Sweet endings to your meal', NULL, 3, 1),
(4, 'Beverages', 'Refreshing drinks', NULL, 4, 1),
(5, 'Seasonal Items', 'Seasonal flavors and dishes.', NULL, 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `item_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `preparation_time` int(11) DEFAULT NULL COMMENT 'In minutes',
  `calories` int(11) DEFAULT NULL,
  `is_vegetarian` tinyint(1) DEFAULT 0,
  `is_spicy` tinyint(1) DEFAULT 0,
  `is_available` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`item_id`, `category_id`, `name`, `description`, `price`, `image_url`, `preparation_time`, `calories`, `is_vegetarian`, `is_spicy`, `is_available`, `created_at`, `updated_at`) VALUES
(1, 1, 'Crispy Spring Rolls', 'Vegetable filled crispy rolls served with sweet chili sauce', 8.99, NULL, 15, NULL, 1, 0, 1, '2025-04-27 12:46:30', NULL),
(2, 2, 'Grilled Salmon', 'Fresh salmon fillet with herbs and lemon butter sauce', 24.99, NULL, 25, NULL, 0, 0, 1, '2025-04-27 12:46:30', NULL),
(3, 3, 'Chocolate Lava Cake', 'Warm chocolate cake with molten center', 7.99, NULL, 20, NULL, 1, 0, 1, '2025-04-27 12:46:30', NULL),
(37, 5, 'Pumpkin Spice Latte', 'A classic fall drink with espresso, steamed milk, and pumpkin flavoring, topped with whipped cream.', 4.99, NULL, 5, 250, 0, 0, 1, '2025-05-11 12:22:17', NULL),
(38, 5, 'Caramel Apple Cider', 'Warm apple cider with caramel syrup, topped with whipped cream and a cinnamon stick.', 3.99, NULL, 10, 180, 0, 0, 1, '2025-05-11 12:22:17', NULL),
(39, 5, 'Apple Cinnamon Muffins', 'Soft muffins with apple chunks, cinnamon, and a crumble topping.', 2.99, NULL, 20, 300, 0, 0, 1, '2025-05-11 12:22:17', NULL),
(40, 5, 'Butternut Squash Soup', 'Creamy soup made with roasted butternut squash, onions, and garlic.', 5.99, NULL, 30, 150, 1, 0, 1, '2025-05-11 12:22:17', NULL),
(41, 5, 'Pecan Pie', 'Rich dessert made with pecans, syrup, sugar, and butter in a flaky crust.', 6.99, NULL, 60, 400, 0, 0, 1, '2025-05-11 12:22:17', NULL),
(42, 5, 'Hot Chocolate with Marshmallows', 'Rich hot chocolate topped with fluffy marshmallows.', 3.49, NULL, 5, 290, 0, 0, 1, '2025-05-11 12:22:48', NULL),
(43, 5, 'Gingerbread Cookies', 'Classic gingerbread cookies with a spiced flavor and decorative icing.', 2.49, NULL, 15, 200, 1, 0, 1, '2025-05-11 12:22:48', NULL),
(44, 5, 'Eggnog Latte', 'A festive espresso drink made with eggnog and topped with cinnamon.', 4.49, NULL, 5, 300, 0, 0, 1, '2025-05-11 12:22:48', NULL),
(45, 5, 'Cranberry Sauce', 'Tangy cranberry sauce with a hint of orange zest, perfect for holiday meals.', 2.99, NULL, 10, 120, 1, 0, 1, '2025-05-11 12:22:48', NULL),
(46, 5, 'Chestnut Soup', 'A creamy and nutty soup made with roasted chestnuts, onions, and garlic.', 6.49, NULL, 30, 180, 1, 0, 1, '2025-05-11 12:22:48', NULL),
(47, 5, 'Pepperoni Pizza', 'Classic pizza topped with pepperoni slices, mozzarella cheese, and marinara sauce.', 8.99, NULL, 15, 350, 0, 1, 1, '2025-05-11 12:23:50', NULL),
(48, 5, 'Veggie Pizza', 'A delicious pizza loaded with bell peppers, onions, mushrooms, and olives.', 7.99, NULL, 15, 300, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(49, 5, 'Cheeseburger', 'Juicy beef patty with melted cheddar cheese, lettuce, tomato, and pickles on a toasted bun.', 6.49, NULL, 10, 500, 0, 0, 1, '2025-05-11 12:23:50', NULL),
(50, 5, 'Chicken Burger', 'Grilled chicken breast with lettuce, tomato, and mayonnaise on a soft bun.', 5.99, NULL, 10, 450, 0, 0, 1, '2025-05-11 12:23:50', NULL),
(51, 5, 'BBQ Chicken Sandwich', 'Grilled chicken topped with smoky BBQ sauce, onions, and pickles on a toasted bun.', 6.29, NULL, 10, 480, 0, 0, 1, '2025-05-11 12:23:50', NULL),
(52, 5, 'Classic French Fries', 'Crispy golden fries served with your choice of dipping sauce.', 2.49, NULL, 5, 300, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(53, 5, 'Cheese Fries', 'Crispy fries smothered in melted cheddar cheese and topped with green onions.', 3.49, NULL, 5, 400, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(54, 5, 'Coca-Cola', 'Refreshing carbonated soft drink.', 1.49, NULL, 0, 150, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(55, 5, 'Iced Tea', 'Chilled tea served with a slice of lemon and a touch of sweetness.', 1.99, NULL, 0, 100, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(56, 5, 'Chicken Biryani', 'Aromatic rice dish with tender chicken, spices, and herbs.', 9.99, NULL, 40, 600, 0, 1, 1, '2025-05-11 12:23:50', NULL),
(57, 5, 'Vegetable Biryani', 'Fragrant rice dish cooked with mixed vegetables and aromatic spices.', 8.49, NULL, 40, 550, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(58, 5, 'Espresso', 'Strong and rich coffee made by forcing hot water through finely-ground coffee beans.', 2.99, NULL, 5, 80, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(59, 5, 'Latte', 'Espresso mixed with steamed milk and topped with a small amount of foam.', 3.99, NULL, 5, 200, 1, 0, 1, '2025-05-11 12:23:50', NULL),
(60, 5, 'Cappuccino', 'Espresso topped with steamed milk and foam, offering a creamy texture and rich flavor.', 3.99, NULL, 5, 190, 1, 0, 1, '2025-05-11 12:23:50', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `order_status` varchar(50) DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `order_status`, `created_at`) VALUES
(1, 1, 'Pending', '2025-05-05 15:17:55'),
(2, 1, 'Pending', '2025-05-05 15:35:26'),
(4, NULL, 'Pending', '2025-05-05 16:03:25'),
(5, NULL, 'Pending', '2025-05-06 02:10:23'),
(6, NULL, 'Pending', '2025-05-06 02:10:50'),
(7, NULL, 'Pending', '2025-05-06 02:12:22'),
(8, NULL, 'Pending', '2025-05-06 02:13:06'),
(9, NULL, 'Pending', '2025-05-06 02:13:30'),
(10, 2, 'Pending', '2025-05-06 02:14:19'),
(11, 3, 'Pending', '2025-05-07 15:06:30'),
(12, 3, 'Pending', '2025-05-07 15:17:16'),
(13, 1, 'Pending', '2025-05-07 16:56:38'),
(14, NULL, 'Pending', '2025-05-08 02:04:18'),
(15, 1, 'Pending', '2025-05-10 04:05:44'),
(16, 17, 'Pending', '2025-05-10 04:12:00'),
(17, NULL, 'Pending', '2025-05-10 13:04:44'),
(18, NULL, 'Pending', '2025-05-10 13:12:46'),
(19, 1, 'Pending', '2025-05-11 16:18:59'),
(21, NULL, 'Pending', '2025-05-11 16:47:24'),
(22, 1, 'Pending', '2025-05-12 14:25:10'),
(25, 1, 'Pending', '2025-05-12 14:29:23'),
(26, 1, 'Pending', '2025-05-12 14:29:53');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `food_item` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`item_id`, `order_id`, `food_item`, `quantity`) VALUES
(1, 1, 'chicken karahi', 1),
(2, 2, 'coffee', 1),
(3, 10, 'biryani', 2),
(4, 11, 'chapatis', 3),
(5, 12, 'chapatis', 3),
(6, 13, 'biryani', 1),
(7, 19, 'coffee', 1),
(8, 22, 'biryani', 1),
(9, 25, 'chicken tikka', 1),
(10, 26, 'chicken tikka', 1);

-- --------------------------------------------------------

--
-- Table structure for table `order_tracking`
--

CREATE TABLE `order_tracking` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `food_item` varchar(255) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `status` varchar(255) DEFAULT 'Pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_tracking`
--

INSERT INTO `order_tracking` (`order_id`, `user_id`, `food_item`, `quantity`, `status`, `order_date`) VALUES
(1, 1, 'Pizza', 2, 'Pending', '2025-05-05 15:32:57');

-- --------------------------------------------------------

--
-- Table structure for table `otp_resets`
--

CREATE TABLE `otp_resets` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `otp` int(11) NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `otp_resets`
--

INSERT INTO `otp_resets` (`id`, `user_id`, `otp`, `expires_at`, `used`) VALUES
(1, 6, 631069, '2025-04-28 13:39:28', 0),
(2, 6, 869573, '2025-04-28 13:39:34', 1);

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `otp` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password_resets`
--

INSERT INTO `password_resets` (`id`, `user_id`, `token`, `expires_at`, `used`, `created_at`, `otp`) VALUES
(4, 5, 'MhkuttvRj2GO0JzvIxva1ZdVmsxVz5EMAxuBvCEbzR8', '2025-04-27 21:54:50', 0, '2025-04-27 15:54:50', '');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `id` int(11) NOT NULL,
  `person` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `guests` int(11) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`id`, `person`, `phone`, `guests`, `date_time`) VALUES
(2, 'Hafsa', '03001234567', 2, '2025-05-07 14:00:00'),
(3, 'Hafsa', '03001234567', 2, '2025-05-07 14:00:00'),
(4, 'hafsa', '0300123456', 2, '2025-05-30 18:00:00'),
(5, 'hafsa', '0300123456', 2, '2025-05-30 14:00:00'),
(6, 'hania', '0300286523', 2, '2025-05-30 19:00:00'),
(7, 'Hadia', '03004532173', 2, '2025-05-08 18:00:00'),
(8, 'Aliya', '03054244597', 2, '2025-06-26 17:00:00'),
(9, 'Asiya rehman', '0334627364', 2, '2026-05-07 15:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `role` enum('customer','admin','staff') DEFAULT 'customer',
  `status` enum('active','inactive','banned') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL
) ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password_hash`, `phone`, `role`, `status`, `created_at`, `last_login`) VALUES
(1, 'ali123', 'ali@example.com', 'testhash1', '03001234567', 'customer', 'active', '2025-04-27 13:14:57', NULL),
(2, 'sara456', 'sara@example.com', 'testhash2', '03007654321', 'customer', 'active', '2025-04-27 13:14:57', NULL),
(3, 'ahmed789', 'ahmed@example.com', 'testhash3', '03009876543', 'customer', 'active', '2025-04-27 13:14:57', NULL),
(4, 'fatima321', 'fatima@example.com', 'testhash4', '03001112222', 'customer', 'active', '2025-04-27 13:14:57', NULL),
(5, 'Hafsa', 'hrranger555@gmail.com', '$2b$12$hNLouuoztSjQeeu8/MbOWeVIk/ufxVjfZnLd2qirnnrIch3NdFt8G', NULL, 'admin', 'active', '2025-04-27 13:44:25', NULL),
(6, 'Hafsa', 'bc210414048hja@vu.edu.pk', '$2b$12$1OKXBT7eR4Jz.BLxSNetwevcadt5oLeYCaKmbJoWnoEpQjT7wUK42', NULL, 'customer', 'active', '2025-04-28 07:52:51', NULL),
(7, 'hania', 'afshar123@gmail.com', '$2b$12$ijUXTl1HmUdvZdPRpuXg0e7k0nrDKJ3FRvKV6DMbgzFuMeHno1ncO', NULL, 'customer', 'active', '2025-04-28 08:34:15', NULL),
(8, 'Laiba', 'hani4444@gmail.com', '$2b$12$dFhyRsSbtCcOdtkXrUxzUuPkhiLW2W/oaYJFwuUAGtY/WZjEe8.CK', NULL, 'customer', 'active', '2025-04-29 07:55:07', NULL),
(11, 'Madiha Mehdi', 'madihajinjua14@gmail.com', '$2b$12$f63FZBLNWczpU1J0oeKlVuGz05/agGvRy81NPhDn7dX7OrjrRvwhC', NULL, 'admin', 'active', '2025-04-30 11:46:27', NULL),
(12, 'Hadia', 'hadiarabi45@gmail.com', '$2b$12$BlELkpNuO4bCIc6hvShDW.XrKM4V.TNiZhcR1nYYu81e9r8UJV7sW', NULL, 'customer', 'active', '2025-05-04 07:59:36', NULL),
(13, 'Hadia', 'hadiarabi454@gmail.com', '$2b$12$9CkAu6AFbc3i.Tv3IiXmiuzg5rvf8N7OKd31MqVn78w1Pe5Xtxsse', NULL, 'customer', 'active', '2025-05-05 18:52:58', NULL),
(14, 'Hafsa', 'hafsa@example.com', 'hashedpasswordhere', NULL, 'customer', 'active', '2025-05-06 14:38:01', NULL),
(15, 'Ali', 'ali123@example.com', '$2b$12$bEnMwdWmyXCSx31pc8.yxuoGma1Iy4.ypZ2IKqZG1105YEomi6ZeS', NULL, 'customer', 'active', '2025-05-06 15:01:51', NULL),
(16, 'aliya', 'aliya123@gmail.com', '$2b$12$TMDbQijCbS6ZoyOgH.j97.jU7CJi/gaFI04fY8fYgXWiHdIxxr4gu', NULL, 'customer', 'active', '2025-05-06 15:02:54', NULL),
(17, 'Eman', 'hafsaraja600@gmail.com', 'eman@123', NULL, 'customer', 'active', '2025-05-10 04:09:58', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD KEY `fk_cart_order` (`order_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `menu_categories`
--
ALTER TABLE `menu_categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `fk_menu_category` (`category_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `fk_orders_user` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `fk_order_items_order` (`order_id`);

--
-- Indexes for table `order_tracking`
--
ALTER TABLE `order_tracking`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `otp_resets`
--
ALTER TABLE `otp_resets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id`);

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
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `feedback_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `menu_categories`
--
ALTER TABLE `menu_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `order_tracking`
--
ALTER TABLE `order_tracking`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `otp_resets`
--
ALTER TABLE `otp_resets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `password_resets`
--
ALTER TABLE `password_resets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `fk_cart_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`);

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD CONSTRAINT `fk_menu_category` FOREIGN KEY (`category_id`) REFERENCES `menu_categories` (`category_id`),
  ADD CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `menu_categories` (`category_id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`);

--
-- Constraints for table `order_tracking`
--
ALTER TABLE `order_tracking`
  ADD CONSTRAINT `order_tracking_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `otp_resets`
--
ALTER TABLE `otp_resets`
  ADD CONSTRAINT `otp_resets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD CONSTRAINT `password_resets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
