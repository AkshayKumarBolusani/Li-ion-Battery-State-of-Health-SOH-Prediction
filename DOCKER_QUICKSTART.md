# Docker Quick Start Guide

Run the Battery SOH Prediction API on **any operating system** using Docker.

---

## Prerequisites

Install Docker on your system:

| OS | Installation |
|----|--------------|
| **Windows** | Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) |
| **macOS** | Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) |
| **Linux** | Run: `sudo apt install docker.io docker-compose` (Ubuntu/Debian) |

**Verify installation:**
```bash
docker --version
docker-compose --version
```

---

## Option 1: Run Pre-built Image (Easiest)

If someone shared the Docker image file with you:

### Step 1: Load the image
```bash
# Load from .tar file
docker load -i battery-soh-predictor.tar
```

### Step 2: Run the container
```bash
docker run -d -p 8000:8000 --name battery-api battery-soh-predictor:latest
```

### Step 3: Open in browser
```
http://localhost:8000
```

### Step 4: Stop when done
```bash
docker stop battery-api
docker rm battery-api
```

---

## Option 2: Build from Source

If you have the source code:

### Step 1: Navigate to project folder
```bash
cd "path/to/li-ion battery"
```

### Step 2: Build the image
```bash
docker build -t battery-soh-predictor:latest .
```

### Step 3: Run the container
```bash
docker run -d -p 8000:8000 --name battery-api battery-soh-predictor:latest
```

### Step 4: Open in browser
```
http://localhost:8000
```

---

## Option 3: Use Docker Compose (Recommended)

### Step 1: Create environment file
```bash
# macOS/Linux
cp .env.example .env

# Windows PowerShell
copy .env.example .env
```

Edit `.env` and set your values (especially `OPENAI_API_KEY`).

### Step 2: Start
```bash
docker compose up -d --build
```

### Step 3: View logs
```bash
docker compose logs -f
```

### Step 4: Stop
```bash
docker compose down
```

The container runs with production defaults (Gunicorn + Uvicorn workers, restart policy, healthcheck).

---

## Accessing the Application

Once running, open your browser:

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Web Interface (main app) |
| http://localhost:8000/docs | API Documentation (Swagger UI) |
| http://localhost:8000/health | Health Check |
| http://localhost:8000/model/info | Model Information |

---

## Using a Different Port

If port 8000 is already in use:

```bash
# Use port 9000 instead
docker run -d -p 9000:8000 --name battery-api battery-soh-predictor:latest
```

Then access at `http://localhost:9000`

---

## Sharing the Docker Image

### Export image to file
```bash
# Save to .tar file (can be shared via USB, cloud storage, etc.)
docker save -o battery-soh-predictor.tar battery-soh-predictor:latest
```

### Share with others
Send the `battery-soh-predictor.tar` file (~500MB-1GB depending on dependencies)

### Recipient loads the image
```bash
docker load -i battery-soh-predictor.tar
docker run -d -p 8000:8000 --name battery-api battery-soh-predictor:latest
```

---

## Push to Docker Hub (Optional)

Share publicly via Docker Hub:

### Step 1: Create Docker Hub account
Go to https://hub.docker.com and create a free account.

### Step 2: Login
```bash
docker login
```

### Step 3: Tag and push
```bash
# Replace 'yourusername' with your Docker Hub username
docker tag battery-soh-predictor:latest yourusername/battery-soh-predictor:latest
docker push yourusername/battery-soh-predictor:latest
```

### Others can then run:
```bash
docker run -d -p 8000:8000 yourusername/battery-soh-predictor:latest
```

---

## Troubleshooting

### "Cannot connect to Docker daemon"
- **Windows/Mac:** Open Docker Desktop app and wait for it to start
- **Linux:** Run `sudo systemctl start docker`

### "Port 8000 already in use"
```bash
# Use a different port
docker run -d -p 9000:8000 --name battery-api battery-soh-predictor:latest
```

### "Container exits immediately"
```bash
# Check logs for errors
docker logs battery-api
```

### "Image not found"
```bash
# Make sure you built or loaded the image
docker images | grep battery
```

### Remove old containers
```bash
# Stop and remove
docker stop battery-api
docker rm battery-api

# Or force remove
docker rm -f battery-api
```

### Clean up everything
```bash
# Remove all stopped containers and unused images
docker system prune -a
```

---

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| RAM | 2 GB |
| Disk Space | 2 GB |
| Docker | 20.10+ |

---

## Quick Reference

```bash
# Build
docker build -t battery-soh-predictor:latest .

# Run
docker run -d -p 8000:8000 --name battery-api battery-soh-predictor:latest

# Stop
docker stop battery-api

# Remove
docker rm battery-api

# View logs
docker logs battery-api

# Export image
docker save -o battery-soh-predictor.tar battery-soh-predictor:latest

# Import image
docker load -i battery-soh-predictor.tar

# List running containers
docker ps

# List all images
docker images

# Compose (recommended)
docker compose up -d --build
docker compose logs -f
docker compose down
```

---

## What's Included in the Container

- ✅ FastAPI backend server
- ✅ Web frontend interface
- ✅ Pre-trained Ridge regression model
- ✅ Feature scaler
- ✅ All Python dependencies
- ✅ Health check endpoint

**NOT included (to keep image small):**
- ❌ Raw datasets (NASA, Mendeley)
- ❌ Jupyter notebooks
- ❌ Training code
- ❌ Deep learning models (PyTorch)

---

## API Usage Example

Once running, you can call the API from any language:

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "features": {
            "voltage_mean": 3.5,
            "voltage_std": 0.3,
            "voltage_min": 2.7,
            "voltage_max": 4.2,
            "voltage_range": 1.5,
            "current_mean": 1.5,
            "current_std": 0.2,
            "capacity": 1.8,
            "discharge_time": 3600,
            "temp_mean": 25.0,
            "temp_max": 28.0,
            "temp_delta": 3.0,
            "temp_std": 1.0
        }
    }
)
print(f"Predicted SOH: {response.json()['soh']:.1f}%")
```

### cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": {"voltage_mean": 3.5, "capacity": 1.8}}'
```

### JavaScript
```javascript
fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        features: {voltage_mean: 3.5, capacity: 1.8}
    })
})
.then(r => r.json())
.then(data => console.log(`SOH: ${data.soh}%`));
```

---

**Need help?** Check the logs: `docker logs battery-api`
