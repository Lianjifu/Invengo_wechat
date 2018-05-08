CREATE SCHEMA 'ywgsh_wx' DEFAULT CHARACTER SET  utf8 COALESCE utf8_general_ci;

CREATE TABLE `ywgsh_wx`.`wx_openid_rfid` (
  `wx_user_id` INT NOT NULL AUTO_INCREMENT,
  `wx_openid` VARCHAR(100) NOT NULL,
  `wx_rfid` VARCHAR(100) NOT NULL,
  `wx_create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `wx_update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`wx_user_id`),
  UNIQUE INDEX `wx_rfid_UNIQUE` (`wx_rfid` ASC));
