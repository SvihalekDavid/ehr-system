Archetypy, Templates, Terminologie a ER diagram jsou ve složce /data

Je potřeba nejdříve vytvořit Organizaci (nemocnice) a pak User (doktor) v Admin části aplikace.


## 📦 Spuštění pomocí Dockeru

### 1. Sestavení image

docker build -t ehr-system .

### 2. Spuštění
docker run -p 8000:8000 ehr-system

### 3. Zobrazení
http://localhost:8000
