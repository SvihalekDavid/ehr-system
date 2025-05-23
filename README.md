Archetypy, Templates a ER diagram jsou ve složce /data


## 📦 Spuštění pomocí Dockeru

### 1. Sestavení obrazu

docker build -t ehr-system .

### 2. Spuštění
docker run -p 8000:8000 ehr-system

### 2. Zobrazení
http://localhost:8000
