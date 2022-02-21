-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema private-wall
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `private-wall` ;

-- -----------------------------------------------------
-- Schema private-wall
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `private-wall` DEFAULT CHARACTER SET utf8 ;
USE `private-wall` ;

-- -----------------------------------------------------
-- Table `private-wall`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `private-wall`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `private-wall`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `private-wall`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `message` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `private-wall`.`shared_messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `private-wall`.`shared_messages` (
  `sender_id` INT NOT NULL,
  `recipient_id` INT NOT NULL,
  PRIMARY KEY (`sender_id`, `recipient_id`),
  INDEX `fk_messages_has_users_users1_idx` (`recipient_id` ASC) VISIBLE,
  INDEX `fk_messages_has_users_messages_idx` (`sender_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_has_users_messages`
    FOREIGN KEY (`sender_id`)
    REFERENCES `private-wall`.`messages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_has_users_users1`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `private-wall`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
