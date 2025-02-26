/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80041
 Source Host           : 127.0.0.1:3306
 Source Schema         : platfrom

 Target Server Type    : MySQL
 Target Server Version : 80041
 File Encoding         : 65001

 Date: 26/02/2025 23:24:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_api_case
-- ----------------------------
DROP TABLE IF EXISTS `t_api_case`;
CREATE TABLE `t_api_case`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用例编号',
  `api_info_id` int NOT NULL COMMENT '关联接口ID',
  `collection_id` int NOT NULL COMMENT '关联集合ID',
  `run_order` int NOT NULL COMMENT '执行顺序',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_api_collection
-- ----------------------------
DROP TABLE IF EXISTS `t_api_collection`;
CREATE TABLE `t_api_collection`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '集合编号',
  `project_id` int NULL DEFAULT NULL COMMENT '所属项目ID',
  `module_id` int NULL DEFAULT NULL COMMENT '所属模块ID',
  `collection_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '集合名称',
  `collection_desc` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '集合描述',
  `collection_env` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '运行环境数据',
  `collection_params` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '参数化运行',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_api_history
-- ----------------------------
DROP TABLE IF EXISTS `t_api_history`;
CREATE TABLE `t_api_history`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录编号',
  `collection_id` int NULL DEFAULT NULL COMMENT '用例ID',
  `history_desc` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '运行记录简述',
  `history_detail` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '运行详细记录',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `suite_id` int NULL DEFAULT NULL COMMENT '任务创建时间',
  `suite_create_time` datetime NULL DEFAULT NULL COMMENT '任务创建时间',
  `collection_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用例名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 211 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_api_info
-- ----------------------------
DROP TABLE IF EXISTS `t_api_info`;
CREATE TABLE `t_api_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '接口用例编号',
  `project_id` int NOT NULL COMMENT '项目ID',
  `module_id` int NOT NULL COMMENT '模块ID',
  `api_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '接口名称',
  `is_login` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否为登录接口',
  `cookie_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT 'cookiename',
  `request_method` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '请求方法',
  `request_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '请求地址',
  `request_params` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT 'URL参数',
  `request_headers` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '请求头',
  `debug_vars` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '调试参数',
  `request_form_datas` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT 'form-data',
  `request_www_form_datas` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT 'www-form-data',
  `requests_json_data` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT 'json数据',
  `assert_vars` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '执行后断言',
  `extract_vars` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '执行后变量提取',
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_api_module
-- ----------------------------
DROP TABLE IF EXISTS `t_api_module`;
CREATE TABLE `t_api_module`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '模块编号',
  `project_id` int NOT NULL COMMENT '所属项目ID',
  `module_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '模块名称',
  `module_desc` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '模块介绍',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_api_project
-- ----------------------------
DROP TABLE IF EXISTS `t_api_project`;
CREATE TABLE `t_api_project`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '项目编号',
  `project_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '项目名称',
  `project_desc` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '项目描述',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_api_suite
-- ----------------------------
DROP TABLE IF EXISTS `t_api_suite`;
CREATE TABLE `t_api_suite`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '任务编号',
  `suite_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '任务名称',
  `suite_desc` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '任务描述',
  `suite_schedule` int NOT NULL COMMENT '定时任务时间',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_case
-- ----------------------------
DROP TABLE IF EXISTS `t_case`;
CREATE TABLE `t_case`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `api_case_id` int NOT NULL COMMENT '关联用例ID',
  `suite_id` int NOT NULL COMMENT '关联任务ID',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 121 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_excute_suite
-- ----------------------------
DROP TABLE IF EXISTS `t_excute_suite`;
CREATE TABLE `t_excute_suite`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `suite_id` int NULL DEFAULT NULL COMMENT '关联任务ID',
  `excute_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '关联执行任务ID',
  `excute_suite_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '任务名称',
  `excute_status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '任务状态',
  `pass_count` int NULL DEFAULT NULL COMMENT '任务成功数',
  `fail_count` int NULL DEFAULT NULL COMMENT '任务失败数',
  `total_count` int NULL DEFAULT NULL COMMENT '总数',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `excute_time` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '执行时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 126 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `role` smallint NULL DEFAULT NULL COMMENT '0，管理员 ,1 测试人员 ，2 其他类型',
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
