# 🚀 Gateway
A FastAPI Gateway connecting the frontend with microservices.

---

## 📦 Installation

### ✅ **Prerequisites**
- Ensure you have **Python 3.11** installed.

### 🔹 **Create a Virtual Environment**

#### **MacOS/Linux**
```bash
python3 -m venv venv
```

#### **Windows**
```bash
python -m venv venv
```

---

### 🔹 **Activate Virtual Environment**

#### **MacOS/Linux**
```bash
source venv/bin/activate
```

#### **Windows**
```bash
venv\Scripts\activate
```

---

### 🔹 **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### 🔹 **For NixOS (No venv required)**
```nix
nix develop
```

---

## 📜 Dependencies

Main dependencies used in this project:
- **fastapi** - Fast web framework for building APIs
- **uvicorn** - ASGI server implementation
- **kafka-python** - Python client for Apache Kafka distributed stream processing system
- **mongoengine** - MongoDB Object-Document Mapper
- **pymongo** - MongoDB driver for Python
- **pydantic** - Data validation and settings management
- **pytest** - Testing framework
- **httpx** - Fully featured HTTP client for Python

---

## 🚀 Running the Application locally

To run the application, follow the steps below. The order of the steps is important for 1-3. Use a separate terminal for steps 2-4 (or run in the background or using a multplexer (e.g. [tmux](https://github.com/tmux/tmux/wiki)).

1. Install and start Kafka (for example using Docker Compose):
   ```bash
   docker-compose up -d
   ```
2. Run the data processor:
   ```bash
   python -m app.data_processor
   ```
3. Run the simulation:
   ```bash
   python -m app.simulation
   ```
4. Start the API (development mode):
   ```bash
   uvicorn app.main:app --reload
   ```
5. Open the API documentation in your browser (after starting the API):
	```bash
	http://localhost:8002/docs
	```
---