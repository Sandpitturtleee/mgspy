# mgspy

**mgspy** is a tool for collecting, managing, and visualizing player activity data for online game Margonem.  
It consists of a PostgreSQL database backend, backend utilities, and a NiceGUI-based interactive frontend.

---

## Features

- Stores player profile and activity data in PostgreSQL
- Backend utilities for querying and analyzing player activity
- Modern interactive frontend to view player statistics and activity plots
- Docker-ready deployment (optional)

---

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
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)

## Getting Started

### Requirements

- Python 3.11+
- PostgreSQL 15+
- [NiceGUI](https://nicegui.io/)
- Docker (optional)

---

### Setup

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
**3. Running the Backend**
```bash
cd backend
python3 main.py
```
**4. Running the Frontend**
```bash
cd frontend
python3 main.py
```
