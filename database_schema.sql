-- Esquema de base de datos para sistema de facturación Panorama_net
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS Panorama_net;
USE Panorama_net;

-- Definition of oriitemsprogramafact table
-- TODO: Elimina el DROP TABLE en producción 
-- DROP TABLE IF EXISTS `oriitemsprogramafact`;
CREATE TABLE IF NOT EXISTS `oriitemsprogramafact` (
    `CantidadPeriodos` smallint(6) NOT NULL DEFAULT '0',
    `Consumo` double NOT NULL DEFAULT '0',
    `IdAno` smallint(6) NOT NULL DEFAULT '0',
    `IdTerceroCliente` decimal(12,2) NOT NULL DEFAULT '0',
    `IdCarpeta` smallint(6) NOT NULL DEFAULT '0',
    `IdCentroUtil` smallint(6) NOT NULL DEFAULT '1',
    `IdPredio` char(20) NOT NULL DEFAULT '',
    `IdServicio` smallint(6) NOT NULL DEFAULT '0',
    `LecturaActual` decimal(12,2) NOT NULL DEFAULT '0',
    `LecturaAnterior` decimal(12,2) NOT NULL DEFAULT '0',
    `Ordinal` int(11) NOT NULL DEFAULT '0',
    `Origen` tinyint(4) NOT NULL DEFAULT '2' COMMENT '0:Ninguno 1:Aplicacion 2:Usuario',
    `PeriodoInicioFact` char(6) NOT NULL DEFAULT '*',
    `Saldo` decimal(12,2) NOT NULL DEFAULT '0.00',
    `ValorPeriodo` decimal(12,2) NOT NULL DEFAULT '0.00',
    `ValorUnitario` decimal(12,2) NOT NULL DEFAULT '0.00',
    PRIMARY KEY (`IdCarpeta`,`IdCentroUtil`,`Ordinal`),
    KEY `Predios` (`IdCarpeta`,`IdCentroUtil`,`IdPredio`,`IdAno`,`IdServicio`),
    KEY `Clientes` (`IdCarpeta`,`IdCentroUtil`,`IdTerceroCliente`,`IdServicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 
-- Dumping data for table oriitemsprogramafact 
-- Insertar datos de ejemplo
/*
INSERT INTO `oriitemsprogramafact`(`CantidadPeriodos`,`Consumo`,`IdAno`,`IdTerceroCliente`,`IdCarpeta`,`IdCentroUtil`,`IdPredio`,`IdServicio`,`LecturaActual`,`LecturaAnterior`,`Ordinal`,`Origen`,`PeriodoInicioFact`,`Saldo`,`ValorPeriodo`,`ValorUnitario`) VALUES
(1,25,0,0,1,1,'APTO 0501 A',2,120,95,0,3,'202401',0.00,345500.00,7250.00),
(1,1911,0,0,1,1,'APTO 0402 B',2,25460,23549,1,3,'202401',0.00,479500.00,7250.00),
(1,3,0,0,1,1,'APTO 0501 B',2,50,47,2,3,'202401',0.00,278400.00,7250.00),
(1,51,0,0,1,1,'APTO 0802 A',2,1250,1199,3,3,'202401',0.00,328500.00,7250.00),
(1,65,0,0,1,1,'APTO 1201 A',2,13560,13495,4,3,'202401',0.00,382300.00,7250.00),
(1,170,0,0,1,1,'APTO 0602 B',2,9120,8950,5,3,'202401',0.00,412500.00,7250.00),
(1,167,0,0,1,1,'APTO 0701 A',2,1122,955,6,3,'202401',0.00,295400.00,7250.00),
(1,107,0,0,1,1,'APTO 1202 A',2,1202,1095,7,3,'202401',0.00,365200.00,7250.00),
(1,161,0,0,1,1,'APTO 0301 B',2,10020,9859,8,3,'202401',0.00,405600.00,7250.00),
(1,185,0,0,1,1,'APTO 0302 B',2,3120,2935,9,3,'202401',0.00,450300.00,7250.00),
(1,19,0,0,1,1,'APTO 0301 A',2,5910,5895,10,3,'202401',0.00,289700.00,7250.00),
(1,125,0,0,1,1,'APTO 0302 A',2,3120,2995,11,3,'202401',0.00,375800.00,7250.00);
*/