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

 Date: 01/11/2019 16:46:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for buildinglevelconfig
-- ----------------------------
DROP TABLE IF EXISTS `buildinglevelconfig`;
CREATE TABLE `buildinglevelconfig`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `buildid` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `timeinterval` int(11) NOT NULL,
  `generate` int(11) NOT NULL,
  `upgrade` int(11) NOT NULL,
  `timedisabled` int(11) NOT NULL,
  `doubletime` int(11) NOT NULL DEFAULT 0,
  `doublecost` int(11) NOT NULL DEFAULT 0,
  `recycle` float(11, 4) NOT NULL DEFAULT 0.0000,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of buildinglevelconfig
-- ----------------------------
INSERT INTO `buildinglevelconfig` VALUES (33, 1, 0, 0, 0, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (34, 1, 1, 15, 10, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (35, 1, 2, 15, 20, 200, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (36, 1, 3, 15, 30, 300, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (37, 1, 4, 15, 40, 400, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (38, 1, 5, 15, 50, 400, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (39, 2, 0, 0, 0, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (40, 2, 1, 15, 10, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (41, 2, 2, 15, 20, 200, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (42, 2, 3, 15, 30, 300, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (43, 2, 4, 15, 40, 400, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (44, 2, 5, 15, 50, 500, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (45, 3, 0, 0, 0, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (46, 3, 1, 10, 11, 500, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (47, 3, 2, 10, 22, 600, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (48, 3, 3, 10, 33, 70, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (49, 3, 4, 10, 44, 800, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (50, 3, 5, 15, 50, 900, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (51, 4, 0, 0, 0, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (52, 4, 1, 10, 11, 500, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (53, 4, 2, 10, 22, 600, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (54, 4, 3, 10, 33, 700, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (55, 4, 4, 10, 44, 800, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (56, 4, 5, 15, 50, 900, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (57, 5, 0, 0, 0, 100, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (58, 5, 1, 8, 13, 600, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (59, 5, 2, 8, 24, 700, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (60, 5, 3, 8, 35, 800, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (61, 5, 4, 8, 46, 900, 600, 300, 500, 1000.0000);
INSERT INTO `buildinglevelconfig` VALUES (62, 5, 5, 8, 50, 1000, 600, 300, 500, 1000.0000);

SET FOREIGN_KEY_CHECKS = 1;
