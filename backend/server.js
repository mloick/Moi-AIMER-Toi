const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const multer = require('multer');
const path = require('path');
const db = require('./database');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

// Setup multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, path.join(__dirname, 'uploads'));
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});
const upload = multer({ storage });

// ==================== COUPLE DATA ENDPOINTS ====================

// Get couple data
app.get('/api/couple-data', (req, res) => {
    db.get('SELECT * FROM couple_data LIMIT 1', (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(row || {});
    });
});

// Update start date
app.put('/api/couple-data/start-date', (req, res) => {
    const { start_date } = req.body;
    if (!start_date) {
        res.status(400).json({ error: 'start_date is required' });
        return;
    }
    
    db.run('UPDATE couple_data SET start_date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1',
        [start_date],
        (err) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ success: true, message: 'Start date updated' });
        }
    );
});

// Update home message
app.put('/api/couple-data/home-message', (req, res) => {
    const { home_message } = req.body;
    
    db.run('UPDATE couple_data SET home_message = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1',
        [home_message],
        (err) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ success: true, message: 'Home message updated' });
        }
    );
});

// Update intro text
app.put('/api/couple-data/intro', (req, res) => {
    const { intro_text } = req.body;
    
    db.run('UPDATE couple_data SET intro_text = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1',
        [intro_text],
        (err) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ success: true, message: 'Intro text updated' });
        }
    );
});

// ==================== MEMORIES ENDPOINTS ====================

// Get all memories
app.get('/api/memories', (req, res) => {
    db.all('SELECT * FROM memories ORDER BY created_at DESC', (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows || []);
    });
});

// Get single memory
app.get('/api/memories/:id', (req, res) => {
    db.get('SELECT * FROM memories WHERE id = ?', [req.params.id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        if (!row) {
            res.status(404).json({ error: 'Memory not found' });
            return;
        }
        res.json(row);
    });
});

// Create new memory
app.post('/api/memories', (req, res) => {
    const { title, description, photo_base64 } = req.body;
    
    if (!title || !description) {
        res.status(400).json({ error: 'Title and description are required' });
        return;
    }
    
    db.run('INSERT INTO memories (title, description, photo_base64) VALUES (?, ?, ?)',
        [title, description, photo_base64 || null],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.status(201).json({ 
                id: this.lastID, 
                title, 
                description, 
                photo_base64,
                created_at: new Date()
            });
        }
    );
});

// Update memory
app.put('/api/memories/:id', (req, res) => {
    const { title, description, photo_base64 } = req.body;
    
    db.run('UPDATE memories SET title = ?, description = ?, photo_base64 = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        [title, description, photo_base64, req.params.id],
        (err) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ success: true, message: 'Memory updated' });
        }
    );
});

// Delete memory
app.delete('/api/memories/:id', (req, res) => {
    db.run('DELETE FROM memories WHERE id = ?', [req.params.id], (err) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ success: true, message: 'Memory deleted' });
    });
});

// ==================== PERSPECTIVES ENDPOINTS ====================

// Get all perspectives
app.get('/api/perspectives', (req, res) => {
    db.all('SELECT * FROM perspectives ORDER BY perspective_number', (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows || []);
    });
});

// Get single perspective
app.get('/api/perspectives/:number', (req, res) => {
    db.get('SELECT * FROM perspectives WHERE perspective_number = ?', [req.params.number], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(row || { perspective_number: req.params.number, content: '' });
    });
});

// Create or update perspective
app.post('/api/perspectives', (req, res) => {
    const { perspective_number, content } = req.body;
    
    if (!perspective_number || !content) {
        res.status(400).json({ error: 'perspective_number and content are required' });
        return;
    }
    
    db.get('SELECT * FROM perspectives WHERE perspective_number = ?', [perspective_number], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        
        if (row) {
            // Update
            db.run('UPDATE perspectives SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE perspective_number = ?',
                [content, perspective_number],
                (err) => {
                    if (err) {
                        res.status(500).json({ error: err.message });
                        return;
                    }
                    res.json({ success: true, message: 'Perspective updated' });
                }
            );
        } else {
            // Insert
            db.run('INSERT INTO perspectives (perspective_number, content) VALUES (?, ?)',
                [perspective_number, content],
                (err) => {
                    if (err) {
                        res.status(500).json({ error: err.message });
                        return;
                    }
                    res.status(201).json({ success: true, message: 'Perspective created' });
                }
            );
        }
    });
});

// Update perspective
app.put('/api/perspectives/:number', (req, res) => {
    const { content } = req.body;
    
    db.run('UPDATE perspectives SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE perspective_number = ?',
        [content, req.params.number],
        (err) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ success: true, message: 'Perspective updated' });
        }
    );
});

// ==================== HEALTH CHECK ====================

app.get('/api/health', (req, res) => {
    res.json({ status: 'Backend is running!', timestamp: new Date() });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Server is running on http://localhost:${PORT}`);
    console.log(`📡 API Documentation:`);
    console.log(`   GET  /api/health - Check server status`);
    console.log(`   GET  /api/couple-data - Get couple data`);
    console.log(`   GET  /api/memories - Get all memories`);
    console.log(`   POST /api/memories - Create new memory`);
    console.log(`   GET  /api/perspectives - Get all perspectives`);
});
