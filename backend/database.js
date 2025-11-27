const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, 'moi_aimer_toi.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error opening database:', err);
    } else {
        console.log('Connected to SQLite database at', dbPath);
    }
});

// Initialize database tables
db.serialize(() => {
    // Couple Data Table
    db.run(`CREATE TABLE IF NOT EXISTS couple_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_date TEXT NOT NULL,
        home_message TEXT,
        intro_text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Memories Table
    db.run(`CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        photo_filename TEXT,
        photo_base64 LONGTEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Perspectives Table
    db.run(`CREATE TABLE IF NOT EXISTS perspectives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perspective_number INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(perspective_number)
    )`);

    // Initialize default couple data if empty
    db.get('SELECT COUNT(*) as count FROM couple_data', (err, row) => {
        if (row && row.count === 0) {
            db.run(`INSERT INTO couple_data (start_date, home_message, intro_text) VALUES (?, ?, ?)`,
                ['2023-11-10', 'Default home message', 'Default intro text']
            );
        }
    });
});

module.exports = db;
