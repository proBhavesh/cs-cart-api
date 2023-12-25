# Use Python 3.10 as the parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend (which includes the `api` package) to the container
COPY src/app/backend ./backend

# Install the `api` package from the backend directory
RUN pip install ./backend

# Copy the rest of your application's code
COPY src/ ./src

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Set the command to run your app (adjust the path as needed)
CMD ["streamlit", "run", "src/app/client/app.py"]
