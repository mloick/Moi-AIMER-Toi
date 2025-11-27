# 🎯 Quick Start Guide - Backend Setup

## What Has Been Created

Your backend system is now ready! Here's what you have:

### Backend Files
```
backend/
├── server.js              # Main Express server with all API endpoints
├── database.js            # SQLite database configuration
├── package.json           # Node.js dependencies
├── setup.sh              # Setup script for easy installation
├── README.md             # Complete API documentation
├── INTEGRATION_GUIDE.md  # How to integrate with frontend
└── .gitignore            # Git ignore file
```

### Database Structure
- **couple_data** - Stores start date, home message, intro text
- **memories** - Stores all memories with photos (base64 encoded)
- **perspectives** - Stores dreams for the future (2 perspectives)

## Installation & Launch

### Step 1: Install Backend Dependencies

Open a terminal and run:
```bash
cd backend
npm install
```

Or use the setup script (macOS/Linux):
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Start the Backend Server

```bash
npm start
```

You should see:
```
🚀 Server is running on http://localhost:3001
```

### Step 3: Verify It's Working

Open another terminal and test:
```bash
curl http://localhost:3001/api/health
```

You should get:
```json
{"status":"Backend is running!","timestamp":"..."}
```

### Step 4: Frontend is Already Running

Your frontend at `http://localhost:8000` is still running (from earlier).

## What's Next?

### Option A: Use Current Frontend with localStorage (Quick)
Your frontend is already working with localStorage. Continue using it as-is.

### Option B: Integrate Backend with Frontend (Recommended)
Update `index.html` to use the backend API. See files in the backend folder:

1. Read: `backend/INTEGRATION_GUIDE.md` - Step-by-step integration
2. Modify your `index.html` with the provided function replacements
3. Test everything works

## Quick API Examples

### Get All Memories
```bash
curl http://localhost:3001/api/memories
```

### Create a New Memory
```bash
curl -X POST http://localhost:3001/api/memories \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Our First Date",
    "description": "A beautiful evening...",
    "photo_base64": null
  }'
```

### Update Start Date
```bash
curl -X PUT http://localhost:3001/api/couple-data/start-date \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2023-11-10"}'
```

### Get All Perspectives
```bash
curl http://localhost:3001/api/perspectives
```

## Folder Structure Overview

```
Moi-AIMER-Toi/
├── index.html              ← Your beautiful website
├── backend/                ← New backend folder
│   ├── server.js          ← API server
│   ├── database.js        ← Database setup
│   ├── package.json       ← Dependencies
│   ├── moi_aimer_toi.db  ← SQLite database (created after first run)
│   └── README.md          ← Full API docs
└── README.md
```

## Running Both Frontend & Backend

**Terminal 1 - Frontend:**
```bash
cd /Users/apple/Moi-aimer-toi/Moi-AIMER-Toi
python3 -m http.server 8000
```

**Terminal 2 - Backend:**
```bash
cd /Users/apple/Moi-aimer-toi/Moi-AIMER-Toi/backend
npm start
```

Then open: `http://localhost:8000`

## Troubleshooting

### Error: "npm: command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Error: "Port 3001 already in use"
**Solution:** Edit `server.js` and change `PORT = 3000` to another number

### Error: "Cannot find module"
**Solution:** Run `npm install` in the backend folder

### API not responding
**Solution:** Make sure backend is running (`npm start`)

## Key Features of Your Backend

✅ **SQLite Database** - All data persists permanently
✅ **RESTful API** - Standard HTTP methods (GET, POST, PUT, DELETE)
✅ **Photo Storage** - Base64 encoded images stored in database
✅ **CORS Enabled** - Works with frontend on different port
✅ **Timestamps** - Every record has created_at and updated_at
✅ **Error Handling** - Proper HTTP status codes and messages

## Next Steps

1. ✅ Backend is set up
2. ⏭️ Optionally integrate frontend with backend (see INTEGRATION_GUIDE.md)
3. ⏭️ Test all functionality
4. ⏭️ Deploy to production (requires hosting service)

## Documentation Files

- `backend/README.md` - Complete API reference
- `backend/INTEGRATION_GUIDE.md` - How to update frontend
- This file - Quick start overview

## Need Help?

1. Check the API error messages in the terminal
2. Look at `backend/README.md` for endpoint details
3. Check browser console (F12) for frontend errors
4. Network tab (F12) shows API requests and responses

Enjoy your digital love journal! 💜❤️
