# Použij oficiální Python image
FROM python:3.11-slim

# Nastav pracovní adresář
WORKDIR /app

# Zkopíruj dependencies
COPY requirements.txt .

# Nainstaluj dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj zbytek kódu
COPY . .

# Otevři port
EXPOSE 8000

# Spusť FastAPI app pomocí uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
