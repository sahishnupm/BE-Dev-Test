# Dad Jokes API

A FastAPI application that manages Dad Jokes with MongoDB integration and periodic synchronization with external API.

## Features

- CRUD operations for jokes
- Automatic synchronization with icanhazdadjoke.com
- MongoDB storage using Beanie ODM
- Comprehensive error handling
- Logging system
- Full test coverage

## Prerequisites

- Python 3.9+
- MongoDB 4.0+
- Docker and Docker Compose (optional)

## Installation

### Local Setup

1. Clone the repository:
    git clone <repository-url>
    cd BE-Dev-Test

2. Create and activate a virtual environment:
    For Linux/Mac
    python -m venv venv
    source venv/bin/activate

    For Windows
    python -m venv venv
    .\venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Set up environment variables:
    Edit .env with your configuration
    MONGODB_URL=mongodb://localhost:27017
    DATABASE_NAME=dad_jokes_db
    DADJOKES_API_URL=https://icanhazdadjoke.com


### Docker Setup

1. Make sure Docker and Docker Compose are installed
2. Build and run the containers:
    docker-compose up --build

## Running the Application

### Local Development
Start MongoDB (if not running)
mongod
Start the application with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

### Production (Docker)
Start all services
docker-compose up
Run in background
docker-compose up -d
Stop services
docker-compose down


## Testing

### Running Tests

Make sure MongoDB is running
Run all tests
pytest
Run tests with coverage
pytest --cov=app tests/
Run specific test file
pytest tests/test_jokes.py
Run tests with verbose output
pytest -v


### Manual Testing
You can test the API endpoints using the Swagger UI documentation:
- Open `http://localhost:8000/docs` in your browser
- Use the interactive API documentation to test endpoints

## API Documentation

### Available Endpoints

- `POST /jokes/` - Create a new joke
- `GET /jokes/` - Get all jokes
- `GET /jokes/{joke_id}` - Get a specific joke
- `PUT /jokes/{joke_id}` - Update a joke
- `DELETE /jokes/{joke_id}` - Delete a joke
- `POST /jokes/sync` - Fetch and save a random joke

Detailed API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## Monitoring and Logs

- Application logs are stored in `logs/app.log`
- Logs are rotated daily and kept for 7 days
- Console output includes colored logging for better readability

To view logs in Docker:
    View logs from all services
    docker-compose logs
    View logs from web service
    docker-compose logs web
    Follow logs
    docker-compose logs -f



## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 404: Not Found
- 503: Service Unavailable

All error responses follow the format:
json
{
"detail": "Error message description"
}


## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Beanie ODM](https://roman-right.github.io/beanie/)
- [icanhazdadjoke.com](https://icanhazdadjoke.com/)