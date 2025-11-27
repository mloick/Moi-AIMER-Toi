# Frontend Integration with Backend API

This guide shows how to integrate your `index.html` with the backend API.

## Overview
Replace localStorage calls with fetch API calls to the backend server running on `http://localhost:3001`.

## Key Changes

### 1. Update Fetch Calls

Instead of:
```javascript
localStorage.setItem('memories', JSON.stringify(memories));
```

Use:
```javascript
fetch('http://localhost:3001/api/memories', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title, description, photo_base64 })
})
```

### 2. Replace localStorage with API Calls

Replace these functions in your index.html:

#### For Memories
```javascript
// OLD (localStorage)
function saveMemories() {
  saveToStorage('memories', JSON.stringify(memories));
}

// NEW (API)
function saveMemories() {
  // Individual saves on each memory change
  // See updated functions below
}
```

#### For Couple Data (Start Date, Home Message, Intro)
```javascript
// OLD
saveToStorage('startDate', newDate);

// NEW
fetch('http://localhost:3001/api/couple-data/start-date', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ start_date: newDate })
});
```

## Complete Integration Steps

1. **Load couple data on page load:**
```javascript
window.addEventListener('DOMContentLoaded', async function() {
  try {
    const response = await fetch('http://localhost:3001/api/couple-data');
    const coupleData = await response.json();
    
    if (coupleData.start_date) {
      document.getElementById('startDateDisplay').textContent = 
        new Date(coupleData.start_date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
    }
    if (coupleData.home_message) {
      document.getElementById('homeMessageDisplay').textContent = coupleData.home_message;
    }
    if (coupleData.intro_text) {
      document.getElementById('introDisplay').textContent = coupleData.intro_text;
    }
    
    // Load memories
    const memoriesResponse = await fetch('http://localhost:3001/api/memories');
    const memoriesData = await memoriesResponse.json();
    memories = memoriesData;
    memoriesData.forEach(memory => createMemoryElement(memory));
    
    // Load perspectives
    const perspectivesResponse = await fetch('http://localhost:3001/api/perspectives');
    const perspectivesData = await perspectivesResponse.json();
    perspectivesData.forEach(p => {
      document.getElementById('perspective' + p.perspective_number + 'Display').textContent = p.content;
    });
    
    updateCountdown();
  } catch (error) {
    console.error('Error loading data:', error);
  }
});
```

2. **Update memory operations:**
```javascript
// Add new memory
async function addNewMemory() {
  const title = prompt('Titre du souvenir :', 'Un Moment Spécial');
  if (!title) return;
  
  const description = prompt('Description du souvenir :', 'Décrivez ce moment précieux...');
  if (!description) return;

  try {
    const response = await fetch('http://localhost:3001/api/memories', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, photo_base64: null })
    });
    
    const memory = await response.json();
    memories.push(memory);
    createMemoryElement(memory);
  } catch (error) {
    console.error('Error creating memory:', error);
  }
}

// Update memory
async function editMemoryItem(id) {
  const memory = memories.find(m => m.id === id);
  if (!memory) return;
  
  const newTitle = prompt('Nouveau titre :', memory.title);
  if (!newTitle) return;
  
  const newDesc = prompt('Nouvelle description :', memory.description);
  if (!newDesc) return;

  try {
    await fetch(`http://localhost:3001/api/memories/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: newTitle,
        description: newDesc,
        photo_base64: memory.photo_base64
      })
    });
    
    memory.title = newTitle;
    memory.description = newDesc;
    document.getElementById(`title-${id}`).textContent = newTitle;
    document.getElementById(`text-${id}`).textContent = newDesc;
  } catch (error) {
    console.error('Error updating memory:', error);
  }
}

// Delete memory
async function deleteMemory(id) {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce souvenir ?')) return;
  
  try {
    await fetch(`http://localhost:3001/api/memories/${id}`, {
      method: 'DELETE'
    });
    
    memories = memories.filter(m => m.id !== id);
    const element = document.querySelector(`[data-id="${id}"]`);
    if (element) element.remove();
  } catch (error) {
    console.error('Error deleting memory:', error);
  }
}
```

3. **Update message save functions:**
```javascript
async function saveHomeMessage() {
  const display = document.getElementById('homeMessageDisplay');
  const edit = document.getElementById('homeMessageEdit');
  const textarea = document.getElementById('homeMessageText');
  
  try {
    await fetch('http://localhost:3001/api/couple-data/home-message', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ home_message: textarea.value })
    });
    
    display.textContent = textarea.value;
    display.style.display = 'block';
    edit.classList.add('hidden');
  } catch (error) {
    console.error('Error saving message:', error);
  }
}

async function saveIntro() {
  const display = document.getElementById('introDisplay');
  const edit = document.getElementById('introEdit');
  const textarea = document.getElementById('introText');
  
  try {
    await fetch('http://localhost:3001/api/couple-data/intro', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ intro_text: textarea.value })
    });
    
    display.textContent = textarea.value;
    display.style.display = 'block';
    edit.classList.add('hidden');
  } catch (error) {
    console.error('Error saving intro:', error);
  }
}

async function savePerspective(num) {
  const display = document.getElementById('perspective' + num + 'Display');
  const edit = document.getElementById('perspective' + num + 'Edit');
  const textarea = document.getElementById('perspective' + num + 'Text');
  
  try {
    await fetch('http://localhost:3001/api/perspectives', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        perspective_number: num,
        content: textarea.value
      })
    });
    
    display.textContent = textarea.value;
    display.style.display = 'block';
    display.nextElementSibling.style.display = 'block';
    edit.classList.add('hidden');
  } catch (error) {
    console.error('Error saving perspective:', error);
  }
}
```

4. **Handle photo upload with base64:**
```javascript
async function loadMemoryImage(id) {
  const file = document.getElementById(`upload-${id}`).files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = async function(e) {
      const img = document.getElementById(`photo-${id}`);
      const placeholder = document.getElementById(`placeholder-${id}`);
      const base64String = e.target.result;
      
      img.src = base64String;
      img.style.display = 'block';
      placeholder.style.display = 'none';
      
      // Update in backend
      const memory = memories.find(m => m.id === id);
      if (memory) {
        try {
          await fetch(`http://localhost:3001/api/memories/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              title: memory.title,
              description: memory.description,
              photo_base64: base64String
            })
          });
          memory.photo_base64 = base64String;
        } catch (error) {
          console.error('Error uploading photo:', error);
        }
      }
    };
    reader.readAsDataURL(file);
  }
}
```

## Running Both Frontend & Backend

**Terminal 1 - Start Backend:**
```bash
cd backend
npm install
npm start
```

**Terminal 2 - Start Frontend Server:**
```bash
# Keep the Python server running from before
python3 -m http.server 8000
```

Your frontend will be at: `http://localhost:8000`
Your backend API will be at: `http://localhost:3001`

## Testing the Integration

1. Open `http://localhost:8000` in your browser
2. Check the browser console (F12 → Console) for any errors
3. Try creating a new memory - it should save to the database
4. Refresh the page - the memory should still be there (now from the database!)
5. Check backend output in Terminal 1 to see API requests

## Notes
- All photo data is stored as Base64 strings in the database
- The database file (`moi_aimer_toi.db`) is stored in the `/backend` folder
- Use Chrome DevTools Network tab to monitor API calls
- Make sure CORS is enabled (it is by default in our setup)
