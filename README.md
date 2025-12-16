# NumeriLogic

A FastAPI web app for calculations with user authentication and profile management.

## Getting Started

### Prerequisites
- Python 3.12+
- WSL (if on Windows)

### Setup

1. **Navigate to project:**
```bash
cd /home/saketh/IS601/module12
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the app:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 5000
```

Open your browser to `http://localhost:5000`

### Running Tests

```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Features

- User registration and login with JWT authentication
- Multiple calculation types: addition, subtraction, multiplication, division, modulus, power, sin, cos, tan, exponential
- View and edit calculation history
- User profile settings (update username, email, password)
- Responsive UI with Tailwind CSS

## Test Coverage

- 27 passing tests with 62% code coverage
- Unit tests for all calculation types
- Integration tests for authentication and routes
- Automated tests via GitHub Actions

## Docker Hub Link
https://hub.docker.com/repository/docker/saketh008/is601_module12/general



