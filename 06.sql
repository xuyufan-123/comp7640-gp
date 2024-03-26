/*
 Navicat Premium Data Transfer

 Source Server         : 123456
 Source Server Type    : MySQL
 Source Server Version : 80300
 Source Host           : localhost:3306
 Source Schema         : 06

 Target Server Type    : MySQL
 Target Server Version : 80300
 File Encoding         : 65001

 Date: 26/03/2024 16:50:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for customer
-- ----------------------------
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer`  (
  `id` int(0) NOT NULL COMMENT '客户id',
  `name` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '客户姓名',
  `password` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '登录密码',
  `cust_phone` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '顾客电话',
  `address` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '收货地址',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `customer_phone`(`cust_phone`) USING BTREE,
  INDEX `username`(`name`) USING BTREE,
  INDEX `password`(`password`) USING BTREE,
  INDEX `id`(`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of customer
-- ----------------------------
INSERT INTO `customer` VALUES (1, 'Tsui', '123', '110', 'Kowloon');
INSERT INTO `customer` VALUES (2, 'xu', '123', '111', 'Hong Kong');
INSERT INTO `customer` VALUES (3, 'xu', '123', '113', NULL);
INSERT INTO `customer` VALUES (4, 'xu', '123', '114', NULL);
INSERT INTO `customer` VALUES (5, 'xu', '123', '115', NULL);
INSERT INTO `customer` VALUES (8, 'xu', '123', '118', NULL);
INSERT INTO `customer` VALUES (9, 'xu', '123', '119', NULL);
INSERT INTO `customer` VALUES (10, 'zhang', '123', '181', '');

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order`  (
  `order_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '訂單id',
  `vendor_id` int(0) NOT NULL COMMENT '店铺id',
  `product_id` int(0) NOT NULL COMMENT '产品id',
  `customer_id` int(0) NOT NULL COMMENT '顾客id',
  `status` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '物流状态',
  `date` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '下单时间',
  `order` int(0) DEFAULT NULL,
  `purchase_count` int(0) DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `vender_id`(`vendor_id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  INDEX `customer_id`(`customer_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 42 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order
-- ----------------------------
INSERT INTO `order` VALUES (29, 10, 100, 1, 'Shipped', '2024-03-25 19:22:10', 222, 3);
INSERT INTO `order` VALUES (30, 10, 101, 1, 'Order confirmed', '2024-03-25 19:22:10', 222, 2);
INSERT INTO `order` VALUES (31, 10, 100, 1, 'Order confirmed', '2024-03-25 20:03:31', 223, 1);
INSERT INTO `order` VALUES (32, 10, 100, 1, 'Order confirmed', '2024-03-25 20:21:25', 224, 1);
INSERT INTO `order` VALUES (33, 10, 100, 1, 'Order confirmed', '2024-03-25 20:25:06', 225, 1);
INSERT INTO `order` VALUES (34, 10, 101, 1, 'Order confirmed', '2024-03-25 20:25:06', 225, 1);
INSERT INTO `order` VALUES (35, 10, 100, 1, 'Order confirmed', '2024-03-25 20:36:49', 226, 1);
INSERT INTO `order` VALUES (36, 11, 102, 1, 'Order confirmed', '2024-03-25 20:36:49', 226, 1);
INSERT INTO `order` VALUES (37, 10, 100, 1, 'Order confirmed', '2024-03-25 20:42:14', 227, 1);
INSERT INTO `order` VALUES (38, 10, 100, 1, 'Order confirmed', '2024-03-25 20:49:02', 228, 1);
INSERT INTO `order` VALUES (39, 11, 102, 1, 'Order confirmed', '2024-03-25 20:49:02', 228, 3);
INSERT INTO `order` VALUES (40, 10, 100, 1, 'Order confirmed', '2024-03-25 22:01:51', 229, 1);
INSERT INTO `order` VALUES (41, 11, 102, 1, 'Order confirmed', '2024-03-25 22:01:51', 229, 3);

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product`  (
  `product_id` int(0) NOT NULL COMMENT '产品id',
  `product_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品名字',
  `vendor_id` int(0) NOT NULL COMMENT '卖家id',
  `price_pd` int(0) NOT NULL COMMENT '商品价格',
  `inventory` int(0) NOT NULL COMMENT '产品库存',
  PRIMARY KEY (`product_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of product
-- ----------------------------
INSERT INTO `product` VALUES (100, 'shirt', 10, 139, 150);
INSERT INTO `product` VALUES (101, 'sneaker', 10, 199, 183);
INSERT INTO `product` VALUES (103, 'pants', 10, 399, 300);

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `tagid` int(0) NOT NULL COMMENT '标签id',
  `p_id` int(0) NOT NULL COMMENT '对应的产品id',
  `colour` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `size` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `thickness` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`tagid`) USING BTREE,
  INDEX `product_id`(`p_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (1, 100, 'black', 'small-size', 'thick');
INSERT INTO `tag` VALUES (2, 101, 'blue', 'over-size', 'thin');
INSERT INTO `tag` VALUES (3, 102, 'white', 'small-size', 'thick');

-- ----------------------------
-- Table structure for vendor
-- ----------------------------
DROP TABLE IF EXISTS `vendor`;
CREATE TABLE `vendor`  (
  `score_count` int(0) DEFAULT NULL,
  `vendor_id` int(0) NOT NULL COMMENT '卖家id',
  `vendor_name` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '卖家姓名',
  `score_ave` float(50, 2) DEFAULT NULL COMMENT '顾客评价的平均值',
  `vd_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '商家电话可用于登录',
  `password` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '商家登录密码',
  `geo` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发货地',
  UNIQUE INDEX `vender_phone`(`vd_phone`) USING BTREE,
  INDEX `vendor_id`(`vendor_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vendor
-- ----------------------------
INSERT INTO `vendor` VALUES (1, 12, 'stussy', 0.00, '119', '123', NULL);
INSERT INTO `vendor` VALUES (5, 10, 'Nike', 4.60, '133', '123', 'Kowloon');
INSERT INTO `vendor` VALUES (1, 11, 'adidas', 0.00, '134', '123', 'Hong Kong');
INSERT INTO `vendor` VALUES (1, 13, 'Supreme', 0.00, '190', '123', NULL);

SET FOREIGN_KEY_CHECKS = 1;
