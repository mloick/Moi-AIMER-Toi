# Moi AIMER Toi - Complete Documentation 📖

**Language / Langue:**
- [English](#english) 🇬🇧
- [Français](#français) 🇫🇷

---

## English

### Overview

**Moi AIMER Toi** is a romantic, personalized web application designed for couples to store, share, and celebrate their memories, milestones, and future dreams together. The site features:

- 💝 **Countdown timer** showing years, months, days, and hours together
- 📸 **Memory gallery** with photo storage and descriptions
- ✍️ **Couple data management** (start date, home message, intro story)
- 🌟 **Perspectives section** for sharing personal dreams and hopes for the future
- 🔐 **Authentication** with JWT tokens and API key fallback for development
- 💾 **Persistent storage** using SQLite and filesystem for photos

### Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Frontend](#frontend)
4. [Backend](#backend)
5. [API Reference](#api-reference)
6. [Usage Examples](#usage-examples)
7. [Security](#security)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps & Enhancements](#next-steps--enhancements)

---

### Quick Start

#### Prerequisites

- Python 3.7+ with pip
- A modern web browser (Chrome, Firefox, Safari, Edge)
- About 5 minutes

#### Installation & Running

**Step 1: Install Backend Dependencies**

```bash
cd backend
pip3 install -r requirements.txt
```

Expected output:
```
Successfully installed Flask Flask-CORS PyJWT
```

**Step 2: Start the Backend Server**

```bash
# From backend/ directory
python3 app.py
```

You should see:
```
🚀 Initializing database...
✅ Database initialized
🚀 Starting Moi AIMER Toi Backend Server...
📡 Server running on http://localhost:3001
```

**Step 3: Start the Frontend Server (in a new terminal)**

```bash
# From project root
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on :: port 8000 ...
```

**Step 4: Open in Browser**

Navigate to: **http://localhost:8000**

**Step 5: Log In**

- Click the **Login** button in the top-right corner
- Username: `admin`
- Password: `password`
- (These are defaults; see [Security](#security) for configuration)

---

### Project Structure

```
Moi-AIMER-Toi/
├── index.html                    # Frontend single-page app
├── DOCUMENTATION.md              # This file
├── README.md                      # Quick overview
├── BACKEND_QUICKSTART.md         # Backend setup guide
├── INTEGRATION_GUIDE.md          # API integration details
│
└── backend/
    ├── app.py                    # Flask API server (main)
    ├── requirements.txt          # Python dependencies
    ├── .env                      # Environment variables
    ├── Dockerfile                # Docker container config
    ├── Procfile                  # Heroku deployment config
    ├── moi_aimer_toi.db          # SQLite database (auto-created)
    ├── uploads/                  # Photo storage directory
    └── README.md                 # Backend-specific docs
```

---

### Frontend

The frontend is a **single-page application (SPA)** built with vanilla HTML, CSS, and JavaScript.

#### Key Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful UI**: Gradient backgrounds, animations, glassmorphic cards
- **Real-time Updates**: Reflects data changes immediately
- **File Upload Support**: Click photos to upload memories
- **Authentication**: Login/Logout button in top navigation

#### How It Works

1. On page load, the app fetches initial data from the backend (`/api/couple-data`, `/api/memories`, `/api/perspectives`)
2. User can navigate between 4 sections: Accueil (Home), Notre Rencontre (Our Story), 2023-2025 (Memories), Notre Avenir (Future)
3. For protected actions (create/edit/delete), the app sends an `Authorization: Bearer <token>` header if logged in, or `X-API-KEY: dev-key` if not
4. File uploads are sent as multipart/form-data to the backend

#### Authentication in Frontend

```javascript
// Helper: Get auth headers (token > API key fallback)
function getAuthHeaders() {
    const token = localStorage.getItem('auth_token');
    if (token) return { 'Authorization': 'Bearer ' + token };
    if (API_KEY) return { 'X-API-KEY': API_KEY };
    return {};
}

// All API calls merge these headers
async function apiFetch(path, opts = {}) {
    opts.headers = Object.assign({}, getAuthHeaders(), opts.headers || {});
    const res = await fetch(API_BASE + path, opts);
    if (!res.ok) throw new Error(`API ${path} error: ${res.status}`);
    return res.json();
}
```

---

### Backend

The backend is a **Flask REST API** that handles data persistence, file uploads, and authentication.

#### Tech Stack

- **Framework**: Flask
- **Database**: SQLite3
- **Authentication**: JWT (PyJWT)
- **CORS**: Flask-CORS (allows frontend to call from different port)
- **File Storage**: Local filesystem (`backend/uploads/`)

#### Database Schema

**Table: couple_data**
```
id (INTEGER PRIMARY KEY)
start_date (TEXT, e.g., "2023-11-10")
home_message (TEXT)
intro_text (TEXT)
```

**Table: memories**
```
id (INTEGER PRIMARY KEY AUTOINCREMENT)
title (TEXT)
description (TEXT)
photo_url (TEXT, path like "/uploads/filename.jpg")
created_at (TIMESTAMP)
```

**Table: perspectives**
```
id (INTEGER PRIMARY KEY AUTOINCREMENT)
perspective_number (INTEGER, 1 or 2)
content (TEXT)
updated_at (TIMESTAMP)
```

#### Authentication Flow

1. Frontend sends POST to `/api/auth/login` with `{ username, password }`
2. Backend validates credentials (default: admin/password)
3. Backend returns `{ token: "<JWT>" }`
4. Frontend stores token in localStorage
5. Frontend sends token in `Authorization: Bearer <token>` header on subsequent requests
6. Backend validates JWT signature; if invalid, falls back to checking `X-API-KEY` header

#### CORS & Development

The backend includes `Flask-CORS` to allow requests from `http://localhost:8000` (frontend) to `http://localhost:3001` (backend).

---

### API Reference

#### Base URL
```
http://localhost:3001
```

#### Authentication

All endpoints marked **[Protected]** require ONE of:
- `Authorization: Bearer <JWT>` header (obtained from `/api/auth/login`)
- `X-API-KEY: dev-key` header

---

#### Endpoints

##### **Auth**

**POST /api/auth/login**
- **Description**: Authenticate and obtain a JWT token
- **Body**: `{ "username": "admin", "password": "password" }`
- **Response**: `{ "token": "eyJ0eXAi..." }`
- **Example**:
  ```bash
  curl -X POST http://localhost:3001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"password"}'
  ```

**GET /api/health**
- **Description**: Health check endpoint
- **Response**: `{ "status": "ok" }`
- **Example**:
  ```bash
  curl http://localhost:3001/api/health
  ```

---

##### **Couple Data**

**GET /api/couple-data**
- **Description**: Fetch couple data (start date, messages, intro)
- **Response**:
  ```json
  {
    "id": 1,
    "start_date": "2023-11-10",
    "home_message": "Our beautiful message",
    "intro_text": "Our story..."
  }
  ```
- **Example**:
  ```bash
  curl http://localhost:3001/api/couple-data
  ```

**PUT /api/couple-data/start-date** [Protected]
- **Description**: Update the relationship start date
- **Body**: `{ "start_date": "2023-11-10" }`
- **Response**: Updated couple data object
- **Example**:
  ```bash
  curl -X PUT http://localhost:3001/api/couple-data/start-date \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"start_date":"2024-01-15"}'
  ```

**PUT /api/couple-data/home-message** [Protected]
- **Description**: Update the home page message
- **Body**: `{ "home_message": "Your message here" }`
- **Response**: Updated couple data object

**PUT /api/couple-data/intro** [Protected]
- **Description**: Update the introduction/story text
- **Body**: `{ "intro_text": "Your story text" }`
- **Response**: Updated couple data object

---

##### **Memories**

**GET /api/memories**
- **Description**: Fetch all memories
- **Response**: Array of memory objects
  ```json
  [
    {
      "id": 1,
      "title": "Our First Date",
      "description": "An amazing evening...",
      "photo_url": "/uploads/photo_001.jpg",
      "created_at": "2025-01-01T12:00:00"
    }
  ]
  ```
- **Example**:
  ```bash
  curl http://localhost:3001/api/memories
  ```

**GET /api/memories/:id**
- **Description**: Fetch a single memory by ID
- **Response**: Single memory object
- **Example**:
  ```bash
  curl http://localhost:3001/api/memories/1
  ```

**POST /api/memories** [Protected]
- **Description**: Create a new memory
- **Body (JSON)**:
  ```json
  {
    "title": "Summer Vacation",
    "description": "A wonderful week together..."
  }
  ```
- **Response**: Created memory object with auto-generated id
- **Example**:
  ```bash
  curl -X POST http://localhost:3001/api/memories \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title":"New Memory","description":"Details..."}'
  ```

**PUT /api/memories/:id** [Protected]
- **Description**: Update a memory (text and/or photo)
- **Supports two content types**:
  
  **a) JSON update (text only)**:
  ```bash
  curl -X PUT http://localhost:3001/api/memories/1 \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title":"Updated Title","description":"Updated description"}'
  ```

  **b) Multipart form-data (with photo)**:
  ```bash
  curl -X PUT http://localhost:3001/api/memories/1 \
    -H "Authorization: Bearer $TOKEN" \
    -F "photo=@/path/to/photo.jpg" \
    -F "title=Updated Title" \
    -F "description=Updated description"
  ```

**DELETE /api/memories/:id** [Protected]
- **Description**: Delete a memory (removes DB row and photo file)
- **Response**: `{ "message": "Memory deleted" }`
- **Example**:
  ```bash
  curl -X DELETE http://localhost:3001/api/memories/1 \
    -H "Authorization: Bearer $TOKEN"
  ```

---

##### **Perspectives**

**GET /api/perspectives**
- **Description**: Fetch all perspectives (future dreams)
- **Response**: Array of perspective objects
  ```json
  [
    {
      "id": 1,
      "perspective_number": 1,
      "content": "My dreams for us...",
      "updated_at": "2025-01-01T10:00:00"
    }
  ]
  ```
- **Example**:
  ```bash
  curl http://localhost:3001/api/perspectives
  ```

**GET /api/perspectives/:number**
- **Description**: Fetch a specific perspective by number (1 or 2)
- **Response**: Single perspective object
- **Example**:
  ```bash
  curl http://localhost:3001/api/perspectives/1
  ```

**POST /api/perspectives** [Protected]
- **Description**: Create or update a perspective
- **Body**:
  ```json
  {
    "perspective_number": 1,
    "content": "My dreams and hopes for us..."
  }
  ```
- **Response**: Created or updated perspective object
- **Example**:
  ```bash
  curl -X POST http://localhost:3001/api/perspectives \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"perspective_number":1,"content":"Our future together..."}'
  ```

**PUT /api/perspectives/:number** [Protected]
- **Description**: Update a perspective by number
- **Body**: `{ "content": "Updated content" }`
- **Response**: Updated perspective object
- **Example**:
  ```bash
  curl -X PUT http://localhost:3001/api/perspectives/1 \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"content":"Updated perspective"}'
  ```

---

##### **File Serving**

**GET /uploads/:filename**
- **Description**: Serve uploaded image files
- **Example**:
  ```bash
  curl http://localhost:3001/uploads/photo_001.jpg > photo.jpg
  ```
- In HTML/frontend, use directly:
  ```html
  <img src="http://localhost:3001/uploads/photo_001.jpg" alt="Memory">
  ```

---

### Usage Examples

#### Example 1: Complete Workflow (BASH + curl)

```bash
#!/bin/bash

# 1. Login
TOKEN=$(curl -s -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' | jq -r '.token')

echo "Token: $TOKEN"

# 2. Get current couple data
curl -s http://localhost:3001/api/couple-data | jq '.'

# 3. Create a memory
MEMORY=$(curl -s -X POST http://localhost:3001/api/memories \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Beach Day","description":"Sunny and romantic"}')

MEMORY_ID=$(echo $MEMORY | jq -r '.id')
echo "Created memory ID: $MEMORY_ID"

# 4. Upload a photo to that memory
curl -X PUT http://localhost:3001/api/memories/$MEMORY_ID \
  -H "Authorization: Bearer $TOKEN" \
  -F "photo=@/path/to/your/photo.jpg" \
  -F "title=Beach Day" \
  -F "description=Sunny and romantic"

# 5. Fetch all memories
curl -s http://localhost:3001/api/memories | jq '.'

# 6. Update a perspective
curl -s -X POST http://localhost:3001/api/perspectives \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"perspective_number":1,"content":"I hope we travel together forever"}'

# 7. Delete a memory
curl -X DELETE http://localhost:3001/api/memories/$MEMORY_ID \
  -H "Authorization: Bearer $TOKEN"
```

#### Example 2: JavaScript Fetch (Browser)

```javascript
const API_BASE = 'http://localhost:3001';
const TOKEN = localStorage.getItem('auth_token');

// Helper function
async function apiCall(method, path, body = null) {
    const opts = {
        method,
        headers: {
            'Authorization': `Bearer ${TOKEN}`,
            'Content-Type': 'application/json'
        }
    };
    if (body) opts.body = JSON.stringify(body);
    
    const res = await fetch(API_BASE + path, opts);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
}

// Create a memory
const memory = await apiCall('POST', '/api/memories', {
    title: 'Sunset',
    description: 'Beautiful evening together'
});
console.log('Created:', memory);

// Upload a photo
const formData = new FormData();
formData.append('photo', fileInputElement.files[0]);
formData.append('title', 'Sunset');
formData.append('description', 'Beautiful evening together');

const res = await fetch(`${API_BASE}/api/memories/${memory.id}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${TOKEN}` },
    body: formData
});
const updated = await res.json();
console.log('Updated with photo:', updated);

// Update perspective
const perspective = await apiCall('POST', '/api/perspectives', {
    perspective_number: 1,
    content: 'We will travel the world together'
});
console.log('Perspective:', perspective);

// Delete a memory
await apiCall('DELETE', `/api/memories/${memory.id}`);
console.log('Deleted');
```

#### Example 3: Python Requests

```python
import requests
import json

API_BASE = 'http://localhost:3001'

# Login
login_res = requests.post(f'{API_BASE}/api/auth/login', json={
    'username': 'admin',
    'password': 'password'
})
token = login_res.json()['token']
headers = {'Authorization': f'Bearer {token}'}

# Create memory
memory_res = requests.post(f'{API_BASE}/api/memories', 
    headers=headers,
    json={
        'title': 'Mountain Hike',
        'description': 'Amazing views and time together'
    }
)
memory = memory_res.json()
print(f"Created memory: {memory['id']}")

# Upload photo
with open('/path/to/photo.jpg', 'rb') as f:
    files = {'photo': f}
    data = {'title': 'Mountain Hike', 'description': 'Amazing views...'}
    upload_res = requests.put(
        f'{API_BASE}/api/memories/{memory["id"]}',
        headers=headers,
        files=files,
        data=data
    )
    print(upload_res.json())

# Get all memories
memories = requests.get(f'{API_BASE}/api/memories').json()
print(f"Total memories: {len(memories)}")

# Delete
requests.delete(f'{API_BASE}/api/memories/{memory["id"]}', headers=headers)
```

---

### Security

#### Current Setup (Development)

- **JWT Secret**: `dev-jwt-secret` (change in production!)
- **Default Admin**: username `admin`, password `password`
- **API Key Fallback**: `dev-key`
- **Storage**: Local filesystem (not encrypted)

#### Production Recommendations

1. **Set Environment Variables** (before running `python3 app.py`):
   ```bash
   export BACKEND_API_KEY="your-strong-random-key"
   export BACKEND_JWT_SECRET="your-long-random-secret"
   export BACKEND_ADMIN_USER="your-username"
   export BACKEND_ADMIN_PASS="your-strong-password"
   ```

2. **Remove API Key Fallback**: Edit `backend/app.py` and remove the `X-API-KEY` header check to force JWT-only auth

3. **Enable HTTPS**: Use a reverse proxy (nginx) or deploy to a platform that auto-enables SSL (Heroku, Render, etc.)

4. **Use HTTP-Only Cookies**: Instead of localStorage for JWT tokens, use HTTP-only cookies to prevent XSS attacks

5. **Password Hashing**: Add `werkzeug.security` to hash passwords:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

6. **Rate Limiting**: Add `Flask-Limiter` to prevent brute-force attacks

7. **Input Validation**: Validate and sanitize all user inputs

8. **HTTPS Redirect**: Auto-redirect HTTP to HTTPS in production

9. **Cloud Storage**: Move photos to S3, Cloudinary, or similar (avoid storing on local filesystem in production)

10. **Regular Backups**: Back up the SQLite database frequently

#### File Upload Security

- Uploaded files are stored in `backend/uploads/` with their original filenames
- For production, consider:
  - Renaming files with UUIDs to prevent enumeration
  - Validating file types (check magic bytes, not just extension)
  - Scanning for malware
  - Compressing/resizing images to save space

---

### Troubleshooting

#### Problem: Backend won't start (`python3 app.py`)

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
cd backend
pip3 install -r requirements.txt
```

---

#### Problem: Can't connect to backend (`curl: Failed to connect`)

**Possible causes**:
1. Backend not running
2. Wrong port
3. Firewall blocking

**Debug**:
```bash
# Check if port 3001 is in use
lsof -i :3001

# Check if Flask is running
ps aux | grep python3

# Try accessing from the backend directory
cd backend
curl -s http://localhost:3001/api/health | python3 -m json.tool
```

---

#### Problem: CORS error in browser console

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
- Ensure backend is running (CORS headers are set by Flask-CORS)
- Check that frontend is calling `http://localhost:3001` (not another host)
- Verify backend includes:
  ```python
  from flask_cors import CORS
  CORS(app)
  ```

---

#### Problem: Photo upload fails

**Error**: `Upload failed` or `413 Payload Too Large`

**Solutions**:
1. Check file size (Flask default limit is 16MB)
2. To increase: add to `backend/app.py`:
   ```python
   app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
   ```
3. Ensure `backend/uploads/` directory exists and is writable:
   ```bash
   mkdir -p backend/uploads
   chmod 755 backend/uploads
   ```

---

#### Problem: Database errors

**Error**: `database is locked` or `no such table`

**Solution**:
- Delete the DB and let it auto-initialize:
  ```bash
  rm backend/moi_aimer_toi.db
  python3 backend/app.py  # This will recreate it
  ```

---

#### Problem: Login not working

**Error**: Credentials rejected or token invalid

**Debug**:
```bash
# Test login directly
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Check if JWT_SECRET is set correctly
echo $BACKEND_JWT_SECRET
```

---

### Next Steps & Enhancements

#### 1. **UI/UX Improvements**
- [ ] Replace browser prompts with a beautiful modal login form
- [ ] Add image preview before upload
- [ ] Add drag-and-drop for photo uploads
- [ ] Add confirmation dialogs before deletions
- [ ] Smooth animations for new memories appearing

#### 2. **Enhanced Authentication**
- [ ] Add password hashing (werkzeug.security)
- [ ] Implement JWT token refresh mechanism
- [ ] Add "Remember me" functionality
- [ ] Support multiple user accounts (not just admin)
- [ ] Add password reset via email
- [ ] Two-factor authentication (2FA)

#### 3. **Image Optimization**
- [ ] Compress images on upload (PIL/Pillow)
- [ ] Generate thumbnail previews
- [ ] Support multiple resolutions for responsive loading
- [ ] Move storage to AWS S3, Google Cloud Storage, or Cloudinary

#### 4. **Data Management**
- [ ] Export memories as PDF/album
- [ ] Automatic backup system
- [ ] Data import from JSON/CSV
- [ ] Timeline view (sort memories by date)
- [ ] Search functionality for memories

#### 5. **Social Features**
- [ ] Share selected memories via link
- [ ] Add comments/reactions to memories
- [ ] Timeline view with events
- [ ] Daily/weekly memory reminders

#### 6. **Performance & Reliability**
- [ ] Add database connection pooling
- [ ] Implement caching (Redis)
- [ ] Add database migrations (Alembic)
- [ ] Unit and integration tests
- [ ] API rate limiting
- [ ] Request logging and monitoring

#### 7. **Deployment**
- [ ] Docker containerization (Dockerfile already created)
- [ ] Deploy to Heroku, Render, or Railway
- [ ] Use environment variables for configuration
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Add automated tests on push

#### 8. **Analytics & Monitoring**
- [ ] Track most viewed memories
- [ ] Monitor API response times
- [ ] Log errors and alerts
- [ ] Dashboard for stats

#### 9. **Mobile & PWA**
- [ ] Add PWA support (service workers, manifest)
- [ ] Offline data caching
- [ ] Install as app on phone
- [ ] Push notifications

#### 10. **Additional Features**
- [ ] Couple's to-do list
- [ ] Budget tracker for shared expenses
- [ ] Calendar for important dates
- [ ] Video uploads (not just photos)
- [ ] Voice notes/video messages
- [ ] Dark mode toggle

---

## Français

### Aperçu

**Moi AIMER Toi** est une application web personnalisée conçue pour les couples afin de stocker, partager et célébrer leurs souvenirs, jalons et rêves d'avenir ensemble. Le site propose :

- 💝 **Compte à rebours** montrant les années, mois, jours et heures ensemble
- 📸 **Galerie de souvenirs** avec stockage de photos et descriptions
- ✍️ **Gestion des données du couple** (date de début, message d'accueil, histoire d'introduction)
- 🌟 **Section perspectives** pour partager des rêves et espoirs personnels pour l'avenir
- 🔐 **Authentification** avec tokens JWT et fallback clé API pour le développement
- 💾 **Stockage persistant** utilisant SQLite et système de fichiers pour les photos

### Table des Matières

1. [Démarrage Rapide](#démarrage-rapide)
2. [Structure du Projet](#structure-du-projet)
3. [Frontend](#frontend-1)
4. [Backend](#backend-1)
5. [Référence API](#référence-api)
6. [Exemples d'Utilisation](#exemples-dutilisation)
7. [Sécurité](#sécurité)
8. [Dépannage](#dépannage)
9. [Prochaines Étapes & Améliorations](#prochaines-étapes--améliorations)

---

### Démarrage Rapide

#### Prérequis

- Python 3.7+ avec pip
- Un navigateur web moderne (Chrome, Firefox, Safari, Edge)
- Environ 5 minutes

#### Installation et Démarrage

**Étape 1: Installer les Dépendances du Backend**

```bash
cd backend
pip3 install -r requirements.txt
```

Sortie attendue:
```
Successfully installed Flask Flask-CORS PyJWT
```

**Étape 2: Démarrer le Serveur Backend**

```bash
# Depuis le répertoire backend/
python3 app.py
```

Vous devriez voir:
```
🚀 Initializing database...
✅ Database initialized
🚀 Starting Moi AIMER Toi Backend Server...
📡 Server running on http://localhost:3001
```

**Étape 3: Démarrer le Serveur Frontend (dans un nouveau terminal)**

```bash
# Depuis la racine du projet
python3 -m http.server 8000
```

Vous devriez voir:
```
Serving HTTP on :: port 8000 ...
```

**Étape 4: Ouvrir dans le Navigateur**

Allez à: **http://localhost:8000**

**Étape 5: Se Connecter**

- Cliquez sur le bouton **Login** en haut à droite
- Nom d'utilisateur: `admin`
- Mot de passe: `password`
- (Ce sont les paramètres par défaut; voir [Sécurité](#sécurité) pour la configuration)

---

### Structure du Projet

```
Moi-AIMER-Toi/
├── index.html                    # Application web monopage
├── DOCUMENTATION.md              # Ce fichier
├── README.md                      # Aperçu rapide
├── BACKEND_QUICKSTART.md         # Guide de configuration du backend
├── INTEGRATION_GUIDE.md          # Détails d'intégration de l'API
│
└── backend/
    ├── app.py                    # Serveur API Flask (principal)
    ├── requirements.txt          # Dépendances Python
    ├── .env                      # Variables d'environnement
    ├── Dockerfile                # Configuration du conteneur Docker
    ├── Procfile                  # Configuration du déploiement Heroku
    ├── moi_aimer_toi.db          # Base de données SQLite (auto-créée)
    ├── uploads/                  # Répertoire de stockage des photos
    └── README.md                 # Documentation spécifique au backend
```

---

### Frontend

Le frontend est une **application web monopage (SPA)** construite avec HTML, CSS et JavaScript vanilla.

#### Fonctionnalités Clés

- **Design Réactif**: Fonctionne sur ordinateur de bureau, tablette et mobile
- **Interface Magnifique**: Arrière-plans dégradés, animations, cartes translucides
- **Mises à Jour en Temps Réel**: Reflète immédiatement les modifications de données
- **Support du Téléchargement de Fichiers**: Cliquez sur les photos pour télécharger des souvenirs
- **Authentification**: Bouton Login/Logout dans la navigation supérieure

#### Comment Ça Fonctionne

1. Au chargement de la page, l'application récupère les données initiales du backend (`/api/couple-data`, `/api/memories`, `/api/perspectives`)
2. L'utilisateur peut naviguer entre 4 sections: Accueil, Notre Rencontre, 2023-2025, Notre Avenir
3. Pour les actions protégées (créer/modifier/supprimer), l'application envoie un en-tête `Authorization: Bearer <token>` si connectée, ou `X-API-KEY: dev-key` sinon
4. Les téléchargements de fichiers sont envoyés au backend en tant que multipart/form-data

#### Authentification dans le Frontend

```javascript
// Aide: Obtenir les en-têtes d'authentification (token > fallback clé API)
function getAuthHeaders() {
    const token = localStorage.getItem('auth_token');
    if (token) return { 'Authorization': 'Bearer ' + token };
    if (API_KEY) return { 'X-API-KEY': API_KEY };
    return {};
}

// Tous les appels API fusionnent ces en-têtes
async function apiFetch(path, opts = {}) {
    opts.headers = Object.assign({}, getAuthHeaders(), opts.headers || {});
    const res = await fetch(API_BASE + path, opts);
    if (!res.ok) throw new Error(`API ${path} error: ${res.status}`);
    return res.json();
}
```

---

### Backend

Le backend est une **API REST Flask** qui gère la persistance des données, le téléchargement de fichiers et l'authentification.

#### Pile Technologique

- **Framework**: Flask
- **Base de Données**: SQLite3
- **Authentification**: JWT (PyJWT)
- **CORS**: Flask-CORS (permet au frontend d'appeler depuis un port différent)
- **Stockage de Fichiers**: Système de fichiers local (`backend/uploads/`)

#### Schéma de la Base de Données

**Tableau: couple_data**
```
id (INTEGER PRIMARY KEY)
start_date (TEXT, ex: "2023-11-10")
home_message (TEXT)
intro_text (TEXT)
```

**Tableau: memories**
```
id (INTEGER PRIMARY KEY AUTOINCREMENT)
title (TEXT)
description (TEXT)
photo_url (TEXT, chemin comme "/uploads/filename.jpg")
created_at (TIMESTAMP)
```

**Tableau: perspectives**
```
id (INTEGER PRIMARY KEY AUTOINCREMENT)
perspective_number (INTEGER, 1 ou 2)
content (TEXT)
updated_at (TIMESTAMP)
```

#### Flux d'Authentification

1. Le frontend envoie POST à `/api/auth/login` avec `{ username, password }`
2. Le backend valide les identifiants (défaut: admin/password)
3. Le backend retourne `{ token: "<JWT>" }`
4. Le frontend stocke le token dans localStorage
5. Le frontend envoie le token dans l'en-tête `Authorization: Bearer <token>` sur les requêtes suivantes
6. Le backend valide la signature JWT ; si invalide, il bascule vers la vérification de l'en-tête `X-API-KEY`

#### CORS et Développement

Le backend comprend `Flask-CORS` pour permettre les requêtes de `http://localhost:8000` (frontend) à `http://localhost:3001` (backend).

---

### Référence API

#### URL de Base
```
http://localhost:3001
```

#### Authentification

Tous les points de terminaison marqués **[Protégé]** nécessitent L'UN des éléments suivants :
- En-tête `Authorization: Bearer <JWT>` (obtenu via `/api/auth/login`)
- En-tête `X-API-KEY: dev-key`

---

#### Points de Terminaison

##### **Authentification**

**POST /api/auth/login**
- **Description**: S'authentifier et obtenir un token JWT
- **Corps**: `{ "username": "admin", "password": "password" }`
- **Réponse**: `{ "token": "eyJ0eXAi..." }`
- **Exemple**:
  ```bash
  curl -X POST http://localhost:3001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"password"}'
  ```

**GET /api/health**
- **Description**: Point de terminaison de vérification de la santé
- **Réponse**: `{ "status": "ok" }`
- **Exemple**:
  ```bash
  curl http://localhost:3001/api/health
  ```

---

##### **Données du Couple**

**GET /api/couple-data**
- **Description**: Récupérer les données du couple (date de début, messages, introduction)
- **Réponse**:
  ```json
  {
    "id": 1,
    "start_date": "2023-11-10",
    "home_message": "Notre beau message",
    "intro_text": "Notre histoire..."
  }
  ```
- **Exemple**:
  ```bash
  curl http://localhost:3001/api/couple-data
  ```

**PUT /api/couple-data/start-date** [Protégé]
- **Description**: Mettre à jour la date de début de la relation
- **Corps**: `{ "start_date": "2023-11-10" }`
- **Réponse**: Objet couple_data mis à jour
- **Exemple**:
  ```bash
  curl -X PUT http://localhost:3001/api/couple-data/start-date \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"start_date":"2024-01-15"}'
  ```

**PUT /api/couple-data/home-message** [Protégé]
- **Description**: Mettre à jour le message de la page d'accueil
- **Corps**: `{ "home_message": "Votre message ici" }`
- **Réponse**: Objet couple_data mis à jour

**PUT /api/couple-data/intro** [Protégé]
- **Description**: Mettre à jour le texte d'introduction/histoire
- **Corps**: `{ "intro_text": "Votre texte d'histoire" }`
- **Réponse**: Objet couple_data mis à jour

---

##### **Souvenirs**

**GET /api/memories**
- **Description**: Récupérer tous les souvenirs
- **Réponse**: Tableau d'objets souvenir
  ```json
  [
    {
      "id": 1,
      "title": "Notre Première Sortie",
      "description": "Une soirée merveilleuse...",
      "photo_url": "/uploads/photo_001.jpg",
      "created_at": "2025-01-01T12:00:00"
    }
  ]
  ```
- **Exemple**:
  ```bash
  curl http://localhost:3001/api/memories
  ```

**GET /api/memories/:id**
- **Description**: Récupérer un seul souvenir par ID
- **Réponse**: Objet souvenir unique
- **Exemple**:
  ```bash
  curl http://localhost:3001/api/memories/1
  ```

**POST /api/memories** [Protégé]
- **Description**: Créer un nouveau souvenir
- **Corps (JSON)**:
  ```json
  {
    "title": "Vacances d'Été",
    "description": "Une semaine merveilleuse ensemble..."
  }
  ```
- **Réponse**: Objet souvenir créé avec id auto-généré
- **Exemple**:
  ```bash
  curl -X POST http://localhost:3001/api/memories \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title":"Nouveau Souvenir","description":"Détails..."}'
  ```

**PUT /api/memories/:id** [Protégé]
- **Description**: Mettre à jour un souvenir (texte et/ou photo)
- **Supporte deux types de contenu**:
  
  **a) Mise à jour JSON (texte seulement)**:
  ```bash
  curl -X PUT http://localhost:3001/api/memories/1 \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title":"Titre Mis à Jour","description":"Description mise à jour"}'
  ```

  **b) Multipart form-data (avec photo)**:
  ```bash
  curl -X PUT http://localhost:3001/api/memories/1 \
    -H "Authorization: Bearer $TOKEN" \
    -F "photo=@/chemin/vers/photo.jpg" \
    -F "title=Titre Mis à Jour" \
    -F "description=Description mise à jour"
  ```

**DELETE /api/memories/:id** [Protégé]
- **Description**: Supprimer un souvenir (supprime la ligne de la BD et le fichier photo)
- **Réponse**: `{ "message": "Memory deleted" }`
- **Exemple**:
  ```bash
  curl -X DELETE http://localhost:3001/api/memories/1 \
    -H "Authorization: Bearer $TOKEN"
  ```

---

##### **Perspectives**

**GET /api/perspectives**
- **Description**: Récupérer toutes les perspectives (rêves d'avenir)
- **Réponse**: Tableau d'objets perspective
  ```json
  [
    {
      "id": 1,
      "perspective_number": 1,
      "content": "Mes rêves pour nous...",
      "updated_at": "2025-01-01T10:00:00"
    }
  ]
  ```
- **Exemple**:
  ```bash
  curl http://localhost:3001/api/perspectives
  ```

**GET /api/perspectives/:number**
- **Description**: Récupérer une perspective spécifique par numéro (1 ou 2)
- **Réponse**: Objet perspective unique
- **Exemple**:
  ```bash
  curl http://localhost:3001/api/perspectives/1
  ```

**POST /api/perspectives** [Protégé]
- **Description**: Créer ou mettre à jour une perspective
- **Corps**:
  ```json
  {
    "perspective_number": 1,
    "content": "Mes rêves et espoirs pour nous..."
  }
  ```
- **Réponse**: Objet perspective créé ou mis à jour
- **Exemple**:
  ```bash
  curl -X POST http://localhost:3001/api/perspectives \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"perspective_number":1,"content":"Notre avenir ensemble..."}'
  ```

**PUT /api/perspectives/:number** [Protégé]
- **Description**: Mettre à jour une perspective par numéro
- **Corps**: `{ "content": "Contenu mis à jour" }`
- **Réponse**: Objet perspective mis à jour
- **Exemple**:
  ```bash
  curl -X PUT http://localhost:3001/api/perspectives/1 \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"content":"Perspective mise à jour"}'
  ```

---

##### **Serveur de Fichiers**

**GET /uploads/:filename**
- **Description**: Servir les fichiers d'images téléchargés
- **Exemple**:
  ```bash
  curl http://localhost:3001/uploads/photo_001.jpg > photo.jpg
  ```
- En HTML/frontend, utilisez directement:
  ```html
  <img src="http://localhost:3001/uploads/photo_001.jpg" alt="Souvenir">
  ```

---

### Exemples d'Utilisation

#### Exemple 1: Flux Complet (BASH + curl)

```bash
#!/bin/bash

# 1. Se connecter
TOKEN=$(curl -s -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' | jq -r '.token')

echo "Token: $TOKEN"

# 2. Obtenir les données du couple
curl -s http://localhost:3001/api/couple-data | jq '.'

# 3. Créer un souvenir
MEMORY=$(curl -s -X POST http://localhost:3001/api/memories \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Jour à la Plage","description":"Ensoleillé et romantique"}')

MEMORY_ID=$(echo $MEMORY | jq -r '.id')
echo "ID du souvenir créé: $MEMORY_ID"

# 4. Télécharger une photo pour ce souvenir
curl -X PUT http://localhost:3001/api/memories/$MEMORY_ID \
  -H "Authorization: Bearer $TOKEN" \
  -F "photo=@/chemin/vers/votre/photo.jpg" \
  -F "title=Jour à la Plage" \
  -F "description=Ensoleillé et romantique"

# 5. Récupérer tous les souvenirs
curl -s http://localhost:3001/api/memories | jq '.'

# 6. Mettre à jour une perspective
curl -s -X POST http://localhost:3001/api/perspectives \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"perspective_number":1,"content":"J'\''espère que nous voyagerons ensemble pour toujours"}'

# 7. Supprimer un souvenir
curl -X DELETE http://localhost:3001/api/memories/$MEMORY_ID \
  -H "Authorization: Bearer $TOKEN"
```

#### Exemple 2: Fetch JavaScript (Navigateur)

```javascript
const API_BASE = 'http://localhost:3001';
const TOKEN = localStorage.getItem('auth_token');

// Fonction d'aide
async function apiCall(method, path, body = null) {
    const opts = {
        method,
        headers: {
            'Authorization': `Bearer ${TOKEN}`,
            'Content-Type': 'application/json'
        }
    };
    if (body) opts.body = JSON.stringify(body);
    
    const res = await fetch(API_BASE + path, opts);
    if (!res.ok) throw new Error(`Erreur API: ${res.status}`);
    return res.json();
}

// Créer un souvenir
const memory = await apiCall('POST', '/api/memories', {
    title: 'Coucher de Soleil',
    description: 'Une belle soirée ensemble'
});
console.log('Créé:', memory);

// Télécharger une photo
const formData = new FormData();
formData.append('photo', fileInputElement.files[0]);
formData.append('title', 'Coucher de Soleil');
formData.append('description', 'Une belle soirée ensemble');

const res = await fetch(`${API_BASE}/api/memories/${memory.id}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${TOKEN}` },
    body: formData
});
const updated = await res.json();
console.log('Mis à jour avec photo:', updated);

// Mettre à jour une perspective
const perspective = await apiCall('POST', '/api/perspectives', {
    perspective_number: 1,
    content: 'Nous voyagerons autour du monde ensemble'
});
console.log('Perspective:', perspective);

// Supprimer un souvenir
await apiCall('DELETE', `/api/memories/${memory.id}`);
console.log('Supprimé');
```

#### Exemple 3: Python Requests

```python
import requests
import json

API_BASE = 'http://localhost:3001'

# Se connecter
login_res = requests.post(f'{API_BASE}/api/auth/login', json={
    'username': 'admin',
    'password': 'password'
})
token = login_res.json()['token']
headers = {'Authorization': f'Bearer {token}'}

# Créer un souvenir
memory_res = requests.post(f'{API_BASE}/api/memories', 
    headers=headers,
    json={
        'title': 'Randonnée en Montagne',
        'description': 'Vues incroyables et temps ensemble'
    }
)
memory = memory_res.json()
print(f"Souvenir créé: {memory['id']}")

# Télécharger une photo
with open('/chemin/vers/photo.jpg', 'rb') as f:
    files = {'photo': f}
    data = {'title': 'Randonnée en Montagne', 'description': 'Vues incroyables...'}
    upload_res = requests.put(
        f'{API_BASE}/api/memories/{memory["id"]}',
        headers=headers,
        files=files,
        data=data
    )
    print(upload_res.json())

# Obtenir tous les souvenirs
memories = requests.get(f'{API_BASE}/api/memories').json()
print(f"Total des souvenirs: {len(memories)}")

# Supprimer
requests.delete(f'{API_BASE}/api/memories/{memory["id"]}', headers=headers)
```

---

### Sécurité

#### Configuration Actuelle (Développement)

- **Secret JWT**: `dev-jwt-secret` (changez en production !)
- **Admin Par Défaut**: nom d'utilisateur `admin`, mot de passe `password`
- **Fallback Clé API**: `dev-key`
- **Stockage**: Système de fichiers local (non chiffré)

#### Recommandations pour la Production

1. **Définir les Variables d'Environnement** (avant d'exécuter `python3 app.py`):
   ```bash
   export BACKEND_API_KEY="votre-clé-aléatoire-forte"
   export BACKEND_JWT_SECRET="votre-secret-aléatoire-long"
   export BACKEND_ADMIN_USER="votre-nom-d-utilisateur"
   export BACKEND_ADMIN_PASS="votre-mot-de-passe-fort"
   ```

2. **Supprimer le Fallback Clé API**: Modifiez `backend/app.py` et supprimez la vérification de l'en-tête `X-API-KEY` pour forcer l'authentification JWT uniquement

3. **Activer HTTPS**: Utilisez un proxy inverse (nginx) ou déployez sur une plateforme qui active automatiquement SSL (Heroku, Render, etc.)

4. **Utiliser des Cookies HTTP-Only**: Au lieu de localStorage pour les tokens JWT, utilisez des cookies HTTP-only pour éviter les attaques XSS

5. **Hachage des Mots de Passe**: Ajoutez `werkzeug.security` pour hacher les mots de passe:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

6. **Limitation de Débit**: Ajoutez `Flask-Limiter` pour éviter les attaques par force brute

7. **Validation des Entrées**: Validez et nettoyez toutes les entrées utilisateur

8. **Redirection HTTPS**: Redirigez automatiquement HTTP vers HTTPS en production

9. **Stockage Cloud**: Déplacez les photos vers S3, Cloudinary, ou similaire (évitez le stockage en local en production)

10. **Sauvegardes Régulières**: Sauvegardez la base de données SQLite fréquemment

#### Sécurité du Téléchargement de Fichiers

- Les fichiers téléchargés sont stockés dans `backend/uploads/` avec leurs noms d'origine
- Pour la production, envisagez:
  - Renommer les fichiers avec des UUID pour éviter l'énumération
  - Valider les types de fichiers (vérifier les octets de signature, pas seulement l'extension)
  - Scanner les malwares
  - Compresser/redimensionner les images pour économiser de l'espace

---

### Dépannage

#### Problème: Le Backend ne démarre pas (`python3 app.py`)

**Erreur**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
cd backend
pip3 install -r requirements.txt
```

---

#### Problème: Impossible de se connecter au backend (`curl: Failed to connect`)

**Causes possibles**:
1. Le backend ne s'exécute pas
2. Mauvais port
3. Pare-feu bloquant

**Débogage**:
```bash
# Vérifier si le port 3001 est utilisé
lsof -i :3001

# Vérifier si Flask s'exécute
ps aux | grep python3

# Essayer d'accéder depuis le répertoire backend
cd backend
curl -s http://localhost:3001/api/health | python3 -m json.tool
```

---

#### Problème: Erreur CORS dans la console du navigateur

**Erreur**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
- Assurez-vous que le backend s'exécute (les en-têtes CORS sont définis par Flask-CORS)
- Vérifiez que le frontend appelle `http://localhost:3001` (pas un autre hôte)
- Vérifiez que le backend comprend:
  ```python
  from flask_cors import CORS
  CORS(app)
  ```

---

#### Problème: Le téléchargement de photo échoue

**Erreur**: `Upload failed` ou `413 Payload Too Large`

**Solutions**:
1. Vérifiez la taille du fichier (la limite par défaut de Flask est 16 Mo)
2. Pour augmenter: ajoutez à `backend/app.py`:
   ```python
   app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 Mo
   ```
3. Assurez-vous que le répertoire `backend/uploads/` existe et est accessible en écriture:
   ```bash
   mkdir -p backend/uploads
   chmod 755 backend/uploads
   ```

---

#### Problème: Erreurs de base de données

**Erreur**: `database is locked` ou `no such table`

**Solution**:
- Supprimez la base de données et laissez-la s'auto-initialiser:
  ```bash
  rm backend/moi_aimer_toi.db
  python3 backend/app.py  # Cela la recréera
  ```

---

#### Problème: La connexion ne fonctionne pas

**Erreur**: Les identifiants sont rejetés ou le token est invalide

**Débogage**:
```bash
# Tester la connexion directement
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Vérifier si JWT_SECRET est correctement défini
echo $BACKEND_JWT_SECRET
```

---

### Prochaines Étapes & Améliorations

#### 1. **Améliorations de l'UI/UX**
- [ ] Remplacer les prompts du navigateur par un formulaire de connexion modal magnifique
- [ ] Ajouter un aperçu d'image avant le téléchargement
- [ ] Ajouter la fonction glisser-déposer pour les téléchargements de photos
- [ ] Ajouter des dialogues de confirmation avant les suppressions
- [ ] Ajouter des animations fluides pour les nouveaux souvenirs apparaissant

#### 2. **Authentification Améliorée**
- [ ] Ajouter le hachage des mots de passe (werkzeug.security)
- [ ] Implémenter un mécanisme d'actualisation du token JWT
- [ ] Ajouter la fonctionnalité "Se souvenir de moi"
- [ ] Support de plusieurs comptes d'utilisateur (pas seulement admin)
- [ ] Ajouter la réinitialisation de mot de passe par e-mail
- [ ] Authentification à deux facteurs (2FA)

#### 3. **Optimisation des Images**
- [ ] Compresser les images lors du téléchargement (PIL/Pillow)
- [ ] Générer des aperçus des vignettes
- [ ] Supporter plusieurs résolutions pour un chargement réactif
- [ ] Déplacer le stockage vers AWS S3, Google Cloud Storage ou Cloudinary

#### 4. **Gestion des Données**
- [ ] Exporter les souvenirs au format PDF/album
- [ ] Système de sauvegarde automatique
- [ ] Importation de données depuis JSON/CSV
- [ ] Vue chronologique (trier les souvenirs par date)
- [ ] Fonctionnalité de recherche pour les souvenirs

#### 5. **Fonctionnalités Sociales**
- [ ] Partager les souvenirs sélectionnés via un lien
- [ ] Ajouter des commentaires/réactions aux souvenirs
- [ ] Vue chronologique avec événements
- [ ] Rappels quotidiens/hebdomadaires de souvenirs

#### 6. **Performance et Fiabilité**
- [ ] Ajouter un pooling de connexions à la base de données
- [ ] Implémenter la mise en cache (Redis)
- [ ] Ajouter des migrations de base de données (Alembic)
- [ ] Tests unitaires et d'intégration
- [ ] Limitation de débit de l'API
- [ ] Enregistrement des requêtes et surveillance

#### 7. **Déploiement**
- [ ] Conteneurisation Docker (Dockerfile déjà créé)
- [ ] Déployer sur Heroku, Render ou Railway
- [ ] Utiliser des variables d'environnement pour la configuration
- [ ] Configurer un pipeline CI/CD (GitHub Actions)
- [ ] Ajouter des tests automatisés au push

#### 8. **Analytique et Surveillance**
- [ ] Suivi des souvenirs les plus consultés
- [ ] Surveillance des temps de réponse de l'API
- [ ] Enregistrement des erreurs et alertes
- [ ] Tableau de bord pour les statistiques

#### 9. **Mobile et PWA**
- [ ] Ajouter le support PWA (service workers, manifest)
- [ ] Mise en cache des données hors ligne
- [ ] Installer en tant qu'application sur téléphone
- [ ] Notifications push

#### 10. **Fonctionnalités Supplémentaires**
- [ ] Liste de tâches pour le couple
- [ ] Suivi du budget pour les dépenses partagées
- [ ] Calendrier pour les dates importantes
- [ ] Téléchargements de vidéos (pas seulement des photos)
- [ ] Notes vocales/messages vidéo
- [ ] Toggle de mode sombre

---

## License

Ce projet est fourni à titre personnel et à usage privé. Tous les droits sont réservés.

For questions, issues, or contributions, please open an issue or contact the repository owner.

---

**Version**: 1.0  
**Last Updated**: 27 November 2025
