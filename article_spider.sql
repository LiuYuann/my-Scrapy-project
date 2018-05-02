/*
 Navicat MySQL Data Transfer

 Source Server         : t2
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : localhost:3306
 Source Schema         : article_spider

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : 65001

 Date: 02/05/2018 12:19:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article`  (
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `create_date` date NULL DEFAULT NULL,
  `url` varchar(300) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `url_object_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `image_urls` varchar(300) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `image_path` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `comment_nums` int(11) NOT NULL DEFAULT 0,
  `fav_nums` int(11) NOT NULL DEFAULT 0,
  `praise_nums` int(11) NOT NULL DEFAULT 0,
  `tags` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`url_object_id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
