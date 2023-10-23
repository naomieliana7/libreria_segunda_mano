-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bd_libreria
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `bd_libreria` ;

-- -----------------------------------------------------
-- Schema bd_libreria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bd_libreria` DEFAULT CHARACTER SET utf8 ;
USE `bd_libreria` ;

-- -----------------------------------------------------
-- Table `bd_libreria`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_libreria`.`usuarios` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(245) NOT NULL,
  `apellido` VARCHAR(245) NOT NULL,
  `correo` VARCHAR(245) NOT NULL,
  `contraseña` VARCHAR(245) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`correo` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_libreria`.`libros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_libreria`.`libros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `título` VARCHAR(245) NOT NULL,
  `autor` VARCHAR(245) NOT NULL,
  `categoría` VARCHAR(245) NOT NULL,
  `precio` INT NOT NULL,
  `descripción` TEXT NOT NULL,
  `portada` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `usuario_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_libros_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_libros_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `bd_libreria`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
