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

 Date: 23/03/2024 17:29:08
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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

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
  `date` datetime(0) NOT NULL COMMENT '下单时间',
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `vender_id`(`vendor_id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  INDEX `customer_id`(`customer_id`) USING BTREE,
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

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
INSERT INTO `product` VALUES (100, 't-shirt', 10, 99, 200);
INSERT INTO `product` VALUES (101, 'sneaker', 10, 199, 200);

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `tagid` int(0) NOT NULL COMMENT '标签id',
  `p_id` int(0) NOT NULL COMMENT '对应的产品id',
  `ctlog` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类别',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标签名',
  PRIMARY KEY (`tagid`) USING BTREE,
  INDEX `product_id`(`p_id`) USING BTREE,
  CONSTRAINT `productid` FOREIGN KEY (`p_id`) REFERENCES `product` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for vendor
-- ----------------------------
DROP TABLE IF EXISTS `vendor`;
CREATE TABLE `vendor`  (
  `vendor_id` int(0) NOT NULL COMMENT '卖家id',
  `vendor_name` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '卖家姓名',
  `score_ave` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '顾客评价的平均值',
  `vd_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '商家电话可用于登录',
  `password` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '商家登录密码',
  `geo` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发货地',
  UNIQUE INDEX `vender_phone`(`vd_phone`) USING BTREE,
  INDEX `vendor_id`(`vendor_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vendor
-- ----------------------------
INSERT INTO `vendor` VALUES (12, 'stussy', '0', '119', '123', NULL);
INSERT INTO `vendor` VALUES (10, 'Nike', '0', '133', '123', 'Kowloon');
INSERT INTO `vendor` VALUES (11, 'adidas', '0', '134', '123', 'Hong Kong');

SET FOREIGN_KEY_CHECKS = 1;
