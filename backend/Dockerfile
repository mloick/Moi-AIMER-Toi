FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# Create uploads directory
RUN mkdir -p /app/uploads

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=3001

EXPOSE 3001

CMD ["gunicorn", "-b", "0.0.0.0:3001", "app:app"]
