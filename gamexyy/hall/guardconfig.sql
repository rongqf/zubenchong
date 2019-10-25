/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50711
 Source Host           : localhost:3306
 Source Schema         : gamedb

 Target Server Type    : MySQL
 Target Server Version : 50711
 File Encoding         : 65001

 Date: 25/10/2019 21:08:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for guardconfig
-- ----------------------------
DROP TABLE IF EXISTS `guardconfig`;
CREATE TABLE `guardconfig`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `guardid` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `attackid` int(11) NOT NULL,
  `guardtime` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of guardconfig
-- ----------------------------
INSERT INTO `guardconfig` VALUES (1, '供网', 1, 100, 2, 300);
INSERT INTO `guardconfig` VALUES (2, '供水', 2, 100, 1, 300);
INSERT INTO `guardconfig` VALUES (3, '供电', 3, 100, 3, 300);
INSERT INTO `guardconfig` VALUES (4, '清理垃圾', 4, 100, 4, 300);

SET FOREIGN_KEY_CHECKS = 1;
