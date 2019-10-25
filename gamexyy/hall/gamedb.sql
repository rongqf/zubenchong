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

 Date: 25/10/2019 09:58:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for attackconfig
-- ----------------------------
DROP TABLE IF EXISTS `attackconfig`;
CREATE TABLE `attackconfig`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attackid` int(11) NULL DEFAULT NULL,
  `attackname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `cost` int(10) NULL DEFAULT NULL,
  `attacktime` int(11) NULL DEFAULT NULL,
  `attackpoint` int(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of attackconfig
-- ----------------------------
INSERT INTO `attackconfig` VALUES (1, 1, '断水', 100, 300, 2);
INSERT INTO `attackconfig` VALUES (2, 2, '断网', 120, 300, 3);
INSERT INTO `attackconfig` VALUES (3, 3, '断电', 200, 300, 4);
INSERT INTO `attackconfig` VALUES (4, 4, '扔垃圾', 150, 300, 5);

-- ----------------------------
-- Table structure for buildingconfig
-- ----------------------------
DROP TABLE IF EXISTS `buildingconfig`;
CREATE TABLE `buildingconfig`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `buildid` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `level` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of buildingconfig
-- ----------------------------
INSERT INTO `buildingconfig` VALUES (1, 1, '学校', NULL);
INSERT INTO `buildingconfig` VALUES (2, 2, '医院', NULL);
INSERT INTO `buildingconfig` VALUES (3, 3, '商店', NULL);
INSERT INTO `buildingconfig` VALUES (4, 4, '游乐场', NULL);
INSERT INTO `buildingconfig` VALUES (5, 5, '酒吧', NULL);

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
  `recycle` decimal(11, 4) NOT NULL DEFAULT 0.0000,
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

-- ----------------------------
-- Table structure for friend
-- ----------------------------
DROP TABLE IF EXISTS `friend`;
CREATE TABLE `friend`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `friendid` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index_userid`(`userid`, `friendid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of friend
-- ----------------------------
INSERT INTO `friend` VALUES (21, 7, 12);
INSERT INTO `friend` VALUES (23, 8, 12);
INSERT INTO `friend` VALUES (25, 9, 12);
INSERT INTO `friend` VALUES (27, 10, 12);
INSERT INTO `friend` VALUES (29, 11, 12);
INSERT INTO `friend` VALUES (22, 12, 7);
INSERT INTO `friend` VALUES (24, 12, 8);
INSERT INTO `friend` VALUES (26, 12, 9);
INSERT INTO `friend` VALUES (28, 12, 10);
INSERT INTO `friend` VALUES (30, 12, 11);
INSERT INTO `friend` VALUES (12, 12, 13);
INSERT INTO `friend` VALUES (14, 12, 15);
INSERT INTO `friend` VALUES (16, 12, 16);
INSERT INTO `friend` VALUES (18, 12, 17);
INSERT INTO `friend` VALUES (11, 13, 12);
INSERT INTO `friend` VALUES (13, 15, 12);
INSERT INTO `friend` VALUES (15, 16, 12);
INSERT INTO `friend` VALUES (20, 17, 12);

-- ----------------------------
-- Table structure for friendreq
-- ----------------------------
DROP TABLE IF EXISTS `friendreq`;
CREATE TABLE `friendreq`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `requid` int(11) NOT NULL,
  `accuid` int(11) NOT NULL,
  `acccode` int(11) NOT NULL DEFAULT 0 COMMENT '0表示请求末处理\r\n1表示接受方接受请求\r\n2表示接受方拒绝请求',
  `valid` tinyint(4) NOT NULL DEFAULT 1,
  `reqtime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_req`(`requid`) USING BTREE,
  INDEX `inde_acc`(`accuid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of friendreq
-- ----------------------------
INSERT INTO `friendreq` VALUES (98, 13, 12, 1, 0, '2019-09-27 15:51:43');
INSERT INTO `friendreq` VALUES (99, 15, 12, 1, 0, '2019-09-27 15:58:31');
INSERT INTO `friendreq` VALUES (100, 16, 12, 1, 0, '2019-09-27 16:04:06');
INSERT INTO `friendreq` VALUES (101, 17, 12, 1, 0, '2019-09-28 15:15:04');
INSERT INTO `friendreq` VALUES (102, 12, 17, 1, 0, '2019-09-28 15:17:53');
INSERT INTO `friendreq` VALUES (103, 7, 12, 1, 0, '2019-09-29 11:35:36');
INSERT INTO `friendreq` VALUES (104, 8, 12, 1, 1, '2019-09-29 10:05:02');
INSERT INTO `friendreq` VALUES (105, 9, 12, 1, 1, '2019-09-29 10:05:03');
INSERT INTO `friendreq` VALUES (106, 10, 12, 1, 1, '2019-09-29 10:05:05');
INSERT INTO `friendreq` VALUES (107, 11, 12, 1, 1, '2019-09-29 10:05:09');

-- ----------------------------
-- Table structure for marquee
-- ----------------------------
DROP TABLE IF EXISTS `marquee`;
CREATE TABLE `marquee`  (
  `id` int(11) NOT NULL,
  `msg` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `msgtype` tinyint(4) NOT NULL,
  `updatetime` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `valid` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of marquee
-- ----------------------------
INSERT INTO `marquee` VALUES (1, 'test1111111111111111', 1, '2019-09-27 12:07:12', 1);

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo`  (
  `userid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `logo` int(10) NOT NULL DEFAULT 1,
  `salt` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `money` int(15) NOT NULL DEFAULT 0,
  `gamepoint` int(15) NOT NULL DEFAULT 0,
  `exp` int(15) NOT NULL DEFAULT 0,
  `mapdata` varchar(16384) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `zbc` decimal(15, 4) NOT NULL DEFAULT 0.0000,
  PRIMARY KEY (`userid`) USING BTREE,
  UNIQUE INDEX `index_username`(`username`) USING BTREE,
  INDEX `index_gamepoint`(`gamepoint`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES (1, '112233', 'rongqf', 1, '12', 0, 88888, 88888, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (2, '112233', 'huanghui', 1, '12', 100000000, 100000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (3, '112233', 'test1', 1, '12', 88888, 1000050, 150, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (4, '123456', 'test2', 1, '12', 88888, 997130, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (5, '112233', 'test3', 1, '12', 88888, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (6, '112233', 'test4', 1, '12', 88888, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (7, '112233', 'test5', 1, '12', 88888, 1011728, 13628, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (8, '112233', 'test6', 1, '12', 88888, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (9, '112233', 'test7', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (10, '112233', 'test8', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (11, '112233', 'test9', 1, '12', 0, 999900, 300, '', 0.0000);
INSERT INTO `userinfo` VALUES (12, '112233', 'test10', 1, '12', 0, 999600, 600, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (13, '112233', 'test11', 1, '12', 0, 999550, 150, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (14, '112233', 'test12', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (15, '112233', 'test13', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (16, '112233', 'test14', 1, '12', 0, 1001200, 1200, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (17, '112233', 'test15', 1, '12', 0, 1011150, 11250, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (18, '112233', 'test16', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (19, '112233', 'test17', 1, '12', 0, 1000460, 1160, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (20, '112233', 'test18', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (21, '112233', 'test19', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (22, '112233', 'test20', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (23, '112233', 'test21', 1, '12', 0, 1000000, 0, NULL, 0.0000);
INSERT INTO `userinfo` VALUES (24, '112233', 'rqf123456', 1, '11', 0, 0, 0, NULL, 0.0000);

-- ----------------------------
-- Table structure for usertitle
-- ----------------------------
DROP TABLE IF EXISTS `usertitle`;
CREATE TABLE `usertitle`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `level` int(11) NOT NULL,
  `exp` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usertitle
-- ----------------------------
INSERT INTO `usertitle` VALUES (1, 1, 1000, '称号1');
INSERT INTO `usertitle` VALUES (2, 2, 4000, '称号2');
INSERT INTO `usertitle` VALUES (3, 3, 10000, '称号3');
INSERT INTO `usertitle` VALUES (4, 4, 20000, '称号4');
INSERT INTO `usertitle` VALUES (5, 5, 50000, '称号5');
INSERT INTO `usertitle` VALUES (6, 6, 80000, '称号6');
INSERT INTO `usertitle` VALUES (7, 7, 100000, '称号7');
INSERT INTO `usertitle` VALUES (8, 8, 500000, '称号8');

-- ----------------------------
-- Procedure structure for AccFriend
-- ----------------------------
DROP PROCEDURE IF EXISTS `AccFriend`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AccFriend`(IN `ruid` int,IN `auid` int, IN `acode` int)
BEGIN
	#Routine body goes here...
	IF EXISTS(SELECT * FROM friendreq WHERE requid = `ruid` AND accuid = `auid`) THEN
		UPDATE friendreq SET acccode = `acode` WHERE requid = `ruid` and accuid = `auid`;
		IF `acode` = 1 THEN
			IF NOT EXISTS(SELECT * FROM friend WHERE userid = ruid AND friendid = auid) THEN
				INSERT INTO friend(userid, friendid) VALUES(`ruid`, `auid`);
				INSERT INTO friend(userid, friendid) VALUES(`auid`, `ruid`);
			END IF;
			SELECT 0 as ret;
		ELSE
			SELECT 0 as ret;
		END IF;
	ELSE
		SELECT 2 as ret;
	END IF;
	
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetFriend
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetFriend`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetFriend`(IN `userid` int)
BEGIN
	#Routine body goes here...
	SELECT f.*, u.username, u.exp FROM friend f JOIN userinfo u on f.friendid = u.userid where f.userid = `userid`;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetFriendAcc
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetFriendAcc`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetFriendAcc`(IN `userid` int)
BEGIN
	#Routine body goes here...
	SELECT f.requid, f.accuid, f.acccode, f.reqtime, u.username 
	FROM friendreq f JOIN userinfo u on f.accuid = u.userid 
	WHERE f.accuid = `userid` and f.acccode = 0 and f.valid = 1;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetFriendReq
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetFriendReq`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetFriendReq`(IN `userid` int)
BEGIN
	#Routine body goes here...
	SELECT f.requid, f.accuid, f.acccode, f.reqtime, u.username 
	FROM friendreq f JOIN userinfo u on f.accuid = u.userid 
	WHERE f.requid = `userid` and f.acccode <> 0 and f.valid = 1;
	
	UPDATE friendreq SET valid = 0 
	WHERE requid = `userid` and acccode <> 0 and valid = 1;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for ReqFriend
-- ----------------------------
DROP PROCEDURE IF EXISTS `ReqFriend`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ReqFriend`(IN `ruid` int,IN `auid` int)
BEGIN
	#Routine body goes here...
	DECLARE uid1 INT DEFAULT 0;
	DECLARE uid2 INT DEFAULT 0;
	DECLARE acode INT DEFAULT 0;
	
	IF NOT EXISTS(SELECT * FROM friend as f WHERE f.userid = `ruid` and f.friendid = `auid`) THEN
	
		SELECT fq.requid,fq.accuid,fq.acccode INTO uid1, uid2, acode
		FROM friendreq fq 
		WHERE fq.requid = `ruid` and fq.accuid = `auid`;
		IF uid1 <> 0 THEN
			IF acode = 2 THEN
				UPDATE friendreq SET acccode = 0, valid = 1, reqtime = NOW() WHERE fq.requid = `requid` and fq.accuid = `accuid`;
				SELECT 0 as ret;
			ELSE
				SELECT 1 as ret;
			END IF;
		ELSE
			INSERT INTO friendreq(requid, accuid, reqtime) VALUES(`ruid`, `auid`, NOW());
			SELECT 0 as ret;
		END IF;
	ELSE
		SELECT 2 as ret;
	END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
