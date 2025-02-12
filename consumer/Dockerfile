FROM python:3.9-slim

# Install dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy consumer script
COPY . /app

# Set Hugging Face API key as an environment variable
ENV HF_API_KEY="your_huggingface_api_key"

CMD ["python", "news_processor.py"]