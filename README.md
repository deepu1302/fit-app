# FitLife Tracker - MySQL Backend Setup

## Prerequisites

1. **MySQL** - Install MySQL Server
   - Download from: https://dev.mysql.com/downloads/mysql/
   - During installation, set a root password

2. **Python** - Python 3.8 or higher
   - Download from: https://www.python.org/downloads/

## Setup Instructions

### Step 1: Set Up MySQL Database

1. Open MySQL Workbench or command line
2. Run the schema script:
   ```
   SOURCE path/to/database/schema.sql;
   ```
   Or copy and run the SQL commands from `database/schema.sql`

### Step 2: Configure Database Connection

1. Open `backend/db.py`
2. Update the DB_CONFIG dictionary with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',        # or your MySQL host
    'user': 'your_username',   # your MySQL username
    'password': 'your_password',  # your MySQL password
    'database': 'fitlife_tracker'
}
```

Or set environment variables:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=fitlife_tracker
```

### Step 3: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Run the Backend Server

```bash
cd backend
python app.py
```

The API will be available at: http://localhost:5000

### Step 5: Update Frontend to Use Backend

1. Open `fit.html` in a text editor
2. Find the line that loads `data_sdk.js`:
   ```html
   <script src="/_sdk/data_sdk.js"></script>
   ```
3. Replace the data SDK loading and usage as shown in the updated fit.html

## Testing the API

Test with curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Register a new user
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "age": 30,
    "height": 175,
    "weight": 80,
    "goal": "lose",
    "diet_type": "both",
    "period": "month"
  }'

# Get user profile
curl http://localhost:5000/api/profile/John

# Log weight
curl -X POST http://localhost:5000/api/weight-log \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "weight": 79.5}'

# Get weight logs
curl http://localhost:5000/api/weight-logs/John
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Create new user profile |
| GET | /api/profile/\<name\> | Get user profile |
| PUT | /api/profile/\<name\> | Update user profile |
| POST | /api/weight-log | Log weight entry |
| GET | /api/weight-logs/\<name\> | Get all weight logs |
| DELETE | /api/weight-log/\<id\> | Delete weight log |
| GET | /api/badges/\<name\> | Get user badges |
| POST | /api/badge | Add badge to user |
| GET | /api/data/\<name\> | Get all user data |
| GET | /api/health | Health check |

## Troubleshooting

### MySQL Connection Error
- Verify MySQL is running
- Check username and password
- Ensure the database exists

### Port Already in Use
- Change the port in `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Use different port
  ```

### CORS Error
- The backend already includes CORS headers
- If issues persist, check browser console

## File Structure

```
major Project/
├── fit.html                    # Frontend application
├── database/
│   └── schema.sql            # MySQL database schema
├── backend/
│   ├── app.py              # Flask API server
│   ├── db.py               # Database connection
│   └── requirements.txt   # Python dependencies
├── TODO.md
└── README.md
```

## Next Steps

1. Deploy the backend to a server (e.g., Render, Heroku, AWS)
2. Update frontend API URL for production
3. Add authentication for user security
