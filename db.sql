CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre_producto VARCHAR(100),
    precio DECIMAL(10,2),
    categoria VARCHAR(50),
    stock INT,
    descripcion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre_cliente VARCHAR(100),
    dni VARCHAR(20),
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_cliente INT NOT NULL,
    fecha DATE,
    estado VARCHAR(20), -- 'pendiente', 'pagado', 'vencido'
    monto_total DECIMAL(10,2),
    observaciones TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);