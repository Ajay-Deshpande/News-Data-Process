FROM python:3.9-slim

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy producer script
COPY . /app

CMD ["python", "news_scraper.py"]
