/*
 Navicat Premium Data Transfer

 Source Server         : localqm
 Source Server Type    : MySQL
 Source Server Version : 50617
 Source Host           : localhost:3306
 Source Schema         : techcms

 Target Server Type    : MySQL
 Target Server Version : 50617
 File Encoding         : 65001

 Date: 04/06/2018 12:27:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ui_log
-- ----------------------------
DROP TABLE IF EXISTS `ui_log`;
CREATE TABLE `ui_log`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` tinyint(4) NOT NULL DEFAULT -1 COMMENT '1:操作日志记录;2:其他记录...',
  `state` tinyint(4) NOT NULL DEFAULT -1 COMMENT '1:新增；2：修改；3：删除',
  `remark` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '备注',
  `author` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '操作人员',
  `create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `project_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT 'ui_project.id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_author`(`author`) USING BTREE,
  INDEX `idx_author_createtime`(`author`, `create_time`) USING BTREE,
  INDEX `idx_createtime`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 260 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'UI日志记录表' ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
