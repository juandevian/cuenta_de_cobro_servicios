-- Esquema de base de datos para sistema de facturación Panorama_net
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS panorama_net;
USE panorama_net;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS oriclientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_cliente VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(500),
    telefono VARCHAR(20),
    email VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_codigo_cliente (codigo_cliente)
);

-- Tabla principal de facturas
CREATE TABLE IF NOT EXISTS orifacturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura VARCHAR(50) NOT NULL UNIQUE,
    id_cliente INT NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    lectura_anterior DECIMAL(10,2),
    lectura_actual DECIMAL(10,2),
    consumo DECIMAL(10,2),
    valor_unitario DECIMAL(10,2),
    subtotal DECIMAL(12,2),
    iva DECIMAL(12,2),
    total DECIMAL(12,2),
    estado ENUM('pendiente', 'pagada', 'vencida', 'cancelada') DEFAULT 'pendiente',
    fecha_pago DATE NULL,
    metodo_pago VARCHAR(50),
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE,
    INDEX idx_numero_factura (numero_factura),
    INDEX idx_fecha_emision (fecha_emision),
    INDEX idx_estado (estado),
    INDEX idx_id_cliente (id_cliente)
);

-- Tabla de historial de pagos
CREATE TABLE IF NOT EXISTS pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT NOT NULL,
    monto_pagado DECIMAL(12,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    metodo_pago VARCHAR(50),
    referencia VARCHAR(100),
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_factura) REFERENCES facturas(id) ON DELETE CASCADE,
    INDEX idx_id_factura (id_factura),
    INDEX idx_fecha_pago (fecha_pago)
);

-- Insertar datos de ejemplo
INSERT INTO clientes (codigo_cliente, nombre, direccion, telefono, email) VALUES
('CLI001', 'Cliente Ejemplo 1', 'Calle 123 #45-67', '3001234567', 'cliente1@example.com'),
('CLI002', 'Cliente Ejemplo 2', 'Carrera 89 #12-34', '3007654321', 'cliente2@example.com');

-- Insertar facturas de ejemplo
INSERT INTO facturas (numero_factura, id_cliente, fecha_emision, fecha_vencimiento, lectura_anterior, lectura_actual, consumo, valor_unitario, subtotal, iva, total, estado) VALUES
('FAC001', 1, '2024-01-15', '2024-02-15', 1000.50, 1150.75, 150.25, 850.00, 127712.50, 24265.38, 151977.88, 'pagada'),
('FAC002', 2, '2024-01-20', '2024-02-20', 2500.00, 2750.25, 250.25, 920.00, 230230.00, 43743.70, 273973.70, 'pendiente');