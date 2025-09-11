# mgspy

**mgspy** is a tool for collecting, managing, and visualizing player activity data for online game Margonem.  
It consists of a PostgreSQL database backend, backend utilities, and a NiceGUI-based interactive frontend.

---

## Features

- Stores player profile and activity data in PostgreSQL
- Backend utilities for querying and analyzing player activity
- Modern interactive frontend to view player statistics and activity plots
- Docker-ready deployment
---

## Getting Started

### Requirements

- Python 3.11+
- PostgreSQL 15+
- [NiceGUI](https://nicegui.io/)
- Docker (for full setup with db)

---
### Docker Setup

**1. Clone the repository**
```bash
git clone https://github.com/Sandpitturtleee/mgspy.git
cd mgspy
```
**2.  Build and start all services**
```bash
docker compose up --build
```
**3. Services**

- Frontend GUI: http://localhost:8080 
- Backend: runs in background
- Database

**4. GUI input examples**
- Cycu Dzik
- p gł zav dmp rc dsotm
- Kari Mata Hari
- Luxvyu
- berufs engineer
---
### Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/Sandpitturtleee/mgspy.git
cd mgspy
```
**2. Install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
**3. Running Backend**
```bash
cd backend
python3 createjsons.py
```
**4. Running Frontend**
```bash
cd frontend
python3 createjsons.py
```

## Project Structure
 * [backend](./backend)
   * [app_processes.py](./backend/app_processes.py)
   * [db_operations.py](./backend/db_operations.py)
   * [main.py](./backend/main.py)
   * [web_scrapper.py](./backend/web_scrapper.py)
 * [frontend](./frontend)
   * [data_collectors.py](./frontend/data_collectors.py)
   * [gui.py](./frontend/gui.py)
   * [main.py](./frontend/main.py)
 * [.gitignore](./.gitignore)
 * [DATABASE.md](./DATABASE.md)
 * [dbdump.sql](./dbdump.sql)
 * [docker-compose.yml](./docker-compose.yml)
 * [Dockerfile.backend](./Dockerfile.backend)
 * [Dockerfile.frontend](./Dockerfile.frontend)
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)
