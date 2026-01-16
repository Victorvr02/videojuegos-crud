CREATE TABLE IF NOT EXISTS videojuegos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    plataforma TEXT NOT NULL
);
