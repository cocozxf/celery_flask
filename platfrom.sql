/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50744
 Source Host           : localhost:3306
 Source Schema         : platfrom

 Target Server Type    : MySQL
 Target Server Version : 50744
 File Encoding         : 65001

 Date: 16/06/2024 15:58:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_api_case
-- ----------------------------
DROP TABLE IF EXISTS `t_api_case`;
CREATE TABLE `t_api_case`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用例编号',
  `api_info_id` int(11) NOT NULL COMMENT '关联接口ID',
  `collection_id` int(11) NOT NULL COMMENT '关联集合ID',
  `run_order` int(11) NOT NULL COMMENT '执行顺序',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_api_case
-- ----------------------------
INSERT INTO `t_api_case` VALUES (1, 1, 1, 1, '2024-05-25 03:57:25');
INSERT INTO `t_api_case` VALUES (3, 1, 1, 3, '2024-05-27 23:18:38');
INSERT INTO `t_api_case` VALUES (4, 1, 1, 2, '2024-05-27 23:18:39');
INSERT INTO `t_api_case` VALUES (5, 1, 1, 4, '2024-05-27 23:18:53');

-- ----------------------------
-- Table structure for t_api_collection
-- ----------------------------
DROP TABLE IF EXISTS `t_api_collection`;
CREATE TABLE `t_api_collection`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '集合编号',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '所属项目ID',
  `collection_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '集合名称',
  `collection_desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '集合描述',
  `collection_env` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '运行环境数据',
  `collection_params` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '参数化运行',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_api_collection
-- ----------------------------
INSERT INTO `t_api_collection` VALUES (1, 11, 'sss', 'sss', '', '[{\"name\":\"tony\",\"pwd\":\"xxxx\",\"desc\":\"参数描述\"},{\"name\":\"jack\",\"pwd\":\"xxxx\",\"desc\":\"参数描述\"}]', '2024-05-25 03:57:20');

-- ----------------------------
-- Table structure for t_api_history
-- ----------------------------
DROP TABLE IF EXISTS `t_api_history`;
CREATE TABLE `t_api_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录编号',
  `collection_id` int(11) NULL DEFAULT NULL COMMENT '用例ID',
  `history_desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '运行记录简述',
  `history_detail` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '运行详细记录',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `suite_id` int(11) NULL DEFAULT NULL COMMENT '任务创建时间',
  `suite_create_time` datetime NULL DEFAULT NULL COMMENT '任务创建时间',
  `collection_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用例名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 128 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_api_history
-- ----------------------------

-- ----------------------------
-- Table structure for t_api_info
-- ----------------------------
DROP TABLE IF EXISTS `t_api_info`;
CREATE TABLE `t_api_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '接口用例编号',
  `project_id` int(11) NOT NULL COMMENT '项目ID',
  `module_id` int(11) NOT NULL COMMENT '模块ID',
  `api_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接口名称',
  `is_login` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '是否为登录接口',
  `cookie_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'cookiename',
  `request_method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '请求方法',
  `request_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '请求地址',
  `request_params` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'URL参数',
  `request_headers` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '请求头',
  `debug_vars` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '调试参数',
  `request_form_datas` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'form-data',
  `request_www_form_datas` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'www-form-data',
  `requests_json_data` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'json数据',
  `assert_vars` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '执行后断言',
  `extract_vars` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '执行后变量提取',
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_api_info
-- ----------------------------


-- ----------------------------
-- Table structure for t_api_module
-- ----------------------------
DROP TABLE IF EXISTS `t_api_module`;
CREATE TABLE `t_api_module`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '模块编号',
  `project_id` int(11) NOT NULL COMMENT '所属项目ID',
  `module_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '模块名称',
  `module_desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '模块介绍',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_api_module
-- ----------------------------
INSERT INTO `t_api_module` VALUES (1, 11, 'test01', 'aaaa', '2024-05-25 01:59:54');
INSERT INTO `t_api_module` VALUES (2, 12, 'aaaa', 'asda', '2024-05-25 02:25:54');

-- ----------------------------
-- Table structure for t_api_project
-- ----------------------------
DROP TABLE IF EXISTS `t_api_project`;
CREATE TABLE `t_api_project`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '项目编号',
  `project_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '项目名称',
  `project_desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '项目描述',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_api_project
-- ----------------------------
INSERT INTO `t_api_project` VALUES (11, 'test01', 'tesstat', '2024-05-25 02:24:56');
INSERT INTO `t_api_project` VALUES (12, 'test02', 'aaaaa', '2024-05-25 02:25:16');

-- ----------------------------
-- Table structure for t_api_suite
-- ----------------------------
DROP TABLE IF EXISTS `t_api_suite`;
CREATE TABLE `t_api_suite`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '任务编号',
  `suite_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务名称',
  `suite_desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务描述',
  `suite_schedule` int(11) NOT NULL COMMENT '定时任务时间',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_api_suite
-- ----------------------------
INSERT INTO `t_api_suite` VALUES (59, 'werwe', '瓦尔二部', 0, '2024-06-08 18:21:56');
INSERT INTO `t_api_suite` VALUES (60, 'testr任务02', 'testr任务02', 0, '2024-06-16 15:53:08');

-- ----------------------------
-- Table structure for t_case
-- ----------------------------
DROP TABLE IF EXISTS `t_case`;
CREATE TABLE `t_case`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `api_case_id` int(11) NOT NULL COMMENT '关联用例ID',
  `suite_id` int(11) NOT NULL COMMENT '关联任务ID',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 110 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_case
-- ----------------------------
INSERT INTO `t_case` VALUES (90, 1, 58, '2024-06-08 18:20:14');
INSERT INTO `t_case` VALUES (91, 1, 58, '2024-06-08 18:20:17');
INSERT INTO `t_case` VALUES (92, 1, 59, '2024-06-08 18:22:06');
INSERT INTO `t_case` VALUES (93, 1, 59, '2024-06-08 18:22:06');
INSERT INTO `t_case` VALUES (94, 1, 59, '2024-06-16 13:03:08');
INSERT INTO `t_case` VALUES (95, 1, 59, '2024-06-16 13:03:08');
INSERT INTO `t_case` VALUES (96, 1, 59, '2024-06-16 13:03:09');
INSERT INTO `t_case` VALUES (97, 1, 59, '2024-06-16 13:03:09');
INSERT INTO `t_case` VALUES (98, 1, 59, '2024-06-16 13:03:10');
INSERT INTO `t_case` VALUES (99, 1, 59, '2024-06-16 13:03:10');
INSERT INTO `t_case` VALUES (100, 1, 59, '2024-06-16 13:03:11');
INSERT INTO `t_case` VALUES (101, 1, 59, '2024-06-16 13:03:11');
INSERT INTO `t_case` VALUES (106, 1, 60, '2024-06-16 15:53:12');
INSERT INTO `t_case` VALUES (107, 1, 60, '2024-06-16 15:53:13');
INSERT INTO `t_case` VALUES (108, 1, 60, '2024-06-16 15:53:13');
INSERT INTO `t_case` VALUES (109, 1, 60, '2024-06-16 15:53:14');

-- ----------------------------
-- Table structure for t_excute_suite
-- ----------------------------
DROP TABLE IF EXISTS `t_excute_suite`;
CREATE TABLE `t_excute_suite`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `suite_id` int(11) NULL DEFAULT NULL COMMENT '关联任务ID',
  `excute_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '关联执行任务ID',
  `excute_suite_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务名称',
  `excute_status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务状态',
  `pass_count` int(11) NULL DEFAULT NULL COMMENT '任务成功数',
  `fail_count` int(11) NULL DEFAULT NULL COMMENT '任务失败数',
  `total_count` int(11) NULL DEFAULT NULL COMMENT '总数',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `excute_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '执行时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 118 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_excute_suite
-- ----------------------------
INSERT INTO `t_excute_suite` VALUES (115, 59, 'dcba49f0-8c9e-4f77-bfa1-5cc83d345d0a', 'werwe', 'COMPLETE', 14, 0, 14, '2024-06-16 15:46:18', '41.16s');
INSERT INTO `t_excute_suite` VALUES (116, 59, '6a7dde89-ebd2-4e37-bcb8-0812b6c5bb02', 'werwe', 'COMPLETE', 10, 0, 10, '2024-06-16 15:51:01', '28.94s');
INSERT INTO `t_excute_suite` VALUES (117, 60, '93735397-fb6b-42bf-93ac-c7ed47570cff', 'testr任务02', 'COMPLETE', 4, 0, 4, '2024-06-16 15:53:41', '11.41s');

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `role` smallint(1) NULL DEFAULT NULL COMMENT '0，管理员 ,1 测试人员 ，2 其他类型',
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES (1, 'admin', 'admin', 0, '2024-04-13 10:45:02');

SET FOREIGN_KEY_CHECKS = 1;
