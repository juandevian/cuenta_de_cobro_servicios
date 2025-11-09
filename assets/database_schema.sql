-- Esquema de base de datos para sistema de facturación Panorama_net
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS Panorama_net;
USE Panorama_net;

-- Definition of oriitemsprogramafact table
CREATE TABLE IF NOT EXISTS `oriitemsprogramafact` (
    `CantidadPeriodos` smallint(6) NOT NULL DEFAULT '0',
    `Consumo` double NOT NULL DEFAULT '0',
    `IdAno` smallint(6) NOT NULL DEFAULT '0',
    `IdCarpeta` smallint(6) NOT NULL DEFAULT '0',
    `IdCentroUtil` smallint(6) NOT NULL DEFAULT '1',
    `IdPredio` char(20) NOT NULL DEFAULT '',
    `IdServicio` smallint(6) NOT NULL DEFAULT '0',
    `IdTerceroCliente` decimal(12,2) NOT NULL DEFAULT '0',
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