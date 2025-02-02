# Use official Python image
FROM python:3.10

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8000

# RUN python manage.py migrate --noinput

# Start the application using Gunicorn (for production)
# CMD ["gunicorn", "todo.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn todo.wsgi:application --bind 0.0.0.0:8000"]