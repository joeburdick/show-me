# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the entire dist directory contents into the container at /app
COPY dist/ /app

RUN pip install --no-cache-dir /app/*.tar.gz

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application when the container launches
CMD ["python", "-c", "import show_me.web_app.web_app; show_me.web_app.web_app.app.run(debug=True, host='0.0.0.0')"]