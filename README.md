# PlentiFood Backend API

[The backend is deployed on Render with PostgreSQL.](https://plentifood-api.onrender.com/) Production configuration uses environment variables for secure database and secret management.

# About

PlentiFood Backend is a RESTful API built with Flask and PostgreSQL to support the PlentiFood mobile application (iOS and Android).

The API enables organizations to manage food assistance sites and allows users to search for nearby sites using radius-based geolocation filtering.

This project simulates a real-world environment where multiple frontend teams share a common backend service.

# Tech Stack

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-Migrate (Alembic)
- Pytest
- Render (Deployment)

# Core Features

- Admin registration and authentication
- Organization management
- Site CRUD operations
- Many-to-many relationship between Sites and Services
- Radius-based search (/sites/nearby)
- Bounding box + Haversine geolocation filtering
- JSONB storage for flexible operating hours
- Unit testing for models and routes

# Instructions how to run this app

1. Clone the Repository
git clone <repository_url>
cd backend

2. Create and Activate Virtual Environment
```
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

4. Install Dependencies
```
pip install -r requirements.txt
```

6. Configure Environment Variables

Create a .env file in the root directory:
```
DATABASE_URL=postgresql://localhost/plentifood_db
SECRET_KEY=your_secret_key
FLASK_ENV=development
```

Ensure PostgreSQL is running locally and the database exists.

5. Run Database Migrations
```
flask db upgrade
```

6. Start the Server
```
flask run
```

The application will run at:
```
http://localhost:5000
```

7. Running Tests
```
pytest
```
