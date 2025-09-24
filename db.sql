-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS distribuidora_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE distribuidora_db;

-- Tabla de usuarios
CREATE TABLE usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  contraseña VARCHAR(255) NOT NULL,
  rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
  activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabla de clientes
CREATE TABLE clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  DNI VARCHAR(20) NOT NULL UNIQUE,
  direccion VARCHAR(150),
  telefono VARCHAR(20),
  usuario_id INT,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

-- Tabla de productos
CREATE TABLE productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  tipo ENUM('carne', 'embutido', 'queso') NOT NULL,
  precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
  stock INT NOT NULL CHECK (stock >= 0)
);

-- Tabla de ventas
CREATE TABLE ventas (
  id_venta INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATE NOT NULL,
  cliente_id INT NOT NULL,
  usuario_id INT NOT NULL,
  total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
  FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Tabla intermedia: detalle de venta
CREATE TABLE detalle_venta (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  venta_id INT NOT NULL,
  producto_id INT NOT NULL,
  cantidad INT NOT NULL CHECK (cantidad > 0),
  precio_unit DECIMAL(10,2) NOT NULL CHECK (precio_unit >= 0),
  FOREIGN KEY (venta_id) REFERENCES ventas(id_venta)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES productos(id_producto)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Tabla de pagos
CREATE TABLE pagos (
  id_pago INT AUTO_INCREMENT PRIMARY KEY,
  venta_id INT NOT NULL,
  fecha_pago DATE NOT NULL,
  monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
  estado ENUM('pendiente', 'parcial', 'completo') NOT NULL DEFAULT 'pendiente',
  cuota_nro INT DEFAULT NULL,
  FOREIGN KEY (venta_id) REFERENCES ventas(id_venta)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);