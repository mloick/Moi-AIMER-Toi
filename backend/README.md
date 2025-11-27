# 🚀 Moi AIMER Toi Backend Setup

## Overview
This backend provides a RESTful API to store and manage all your couple data, memories, and perspectives in a SQLite database.

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm (comes with Node.js)

### Steps

1. **Navigate to the backend folder:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the server:**
```bash
npm start
```

The server will run on `http://localhost:3001` by default.

## API Endpoints

### Health Check
- **GET** `/api/health`
  - Check if the backend server is running
  - Response: `{ status: "Backend is running!", timestamp: "..." }`

### Couple Data
- **GET** `/api/couple-data`
  - Get couple's shared data (start date, messages, intro)
  - Response: `{ id, start_date, home_message, intro_text, created_at, updated_at }`

- **PUT** `/api/couple-data/start-date`
  - Update the relationship start date
  - Body: `{ start_date: "YYYY-MM-DD" }`

- **PUT** `/api/couple-data/home-message`
  - Update the home page message
  - Body: `{ home_message: "Your message here" }`

- **PUT** `/api/couple-data/intro`
  - Update the "Our Meeting" story
  - Body: `{ intro_text: "Your story here" }`

### Memories
- **GET** `/api/memories`
  - Get all memories (sorted by newest first)
  - Response: `[{ id, title, description, photo_base64, created_at, updated_at }, ...]`

- **GET** `/api/memories/:id`
  - Get a specific memory by ID
  - Response: `{ id, title, description, photo_base64, created_at, updated_at }`

- **POST** `/api/memories`
  - Create a new memory
  - Body: `{ title: "string", description: "string", photo_base64: "base64_string_or_null" }`
  - Response: `{ id, title, description, photo_base64, created_at }`

- **PUT** `/api/memories/:id`
  - Update an existing memory
  - Body: `{ title: "string", description: "string", photo_base64: "base64_string_or_null" }`

- **DELETE** `/api/memories/:id`
  - Delete a memory by ID
  - Response: `{ success: true, message: "Memory deleted" }`

### Perspectives
- **GET** `/api/perspectives`
  - Get all perspectives
  - Response: `[{ id, perspective_number, content, created_at, updated_at }, ...]`

- **GET** `/api/perspectives/:number`
  - Get a specific perspective (1 or 2)
  - Response: `{ id, perspective_number, content, created_at, updated_at }`

- **POST** `/api/perspectives`
  - Create or get a perspective
  - Body: `{ perspective_number: 1 or 2, content: "Your perspective" }`

- **PUT** `/api/perspectives/:number`
  - Update a perspective
  - Body: `{ content: "Updated perspective" }`

## Database Schema

### couple_data
```sql
- id: Integer (Primary Key)
- start_date: Text (format: YYYY-MM-DD)
- home_message: Text
- intro_text: Text
- created_at: DateTime
- updated_at: DateTime
```

### memories
```sql
- id: Integer (Primary Key)
- title: Text
- description: Text
- photo_filename: Text
- photo_base64: LongText (Base64 encoded image)
- created_at: DateTime
- updated_at: DateTime
```

### perspectives
```sql
- id: Integer (Primary Key)
- perspective_number: Integer (1 or 2)
- content: Text
- created_at: DateTime
- updated_at: DateTime
```

## Frontend Integration

The frontend (`index.html`) needs to be updated to make API calls instead of using localStorage. See the accompanying integration guide for detailed changes.

## Example Usage

### Create a Memory
```javascript
fetch('http://localhost:3001/api/memories', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Our First Date',
    description: 'A wonderful evening at...',
    photo_base64: null // or base64 encoded image string
  })
})
```

### Update Home Message
```javascript
fetch('http://localhost:3001/api/couple-data/home-message', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    home_message: 'Updated message...'
  })
})
```

### Get All Memories
```javascript
fetch('http://localhost:3001/api/memories')
  .then(res => res.json())
  .then(data => console.log(data))
```

## Troubleshooting

- **Port already in use**: Change PORT in `server.js`
- **Module not found**: Run `npm install` again
- **Database locked**: Close other instances of the app and restart
- **CORS errors**: Make sure the frontend is calling from `http://localhost:3001`

## Future Enhancements
- [ ] Authentication & authorization
- [ ] Backup/export functionality
- [ ] Image compression
- [ ] Pagination for memories
- [ ] Search functionality
- [ ] Admin panel
