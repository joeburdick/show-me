# Use an official Python runtime as a parent image
FROM arm64v8/python:3.9.18-bookworm

# Set the working directory in the container to /app
WORKDIR /app

COPY dist/ /app
COPY config/ /app/config
COPY start_script.sh /app

RUN apt update
RUN apt-get -y install python3-rpi.gpio python3-pyaudio portaudio19-dev 
RUN pip install --verbose --extra-index-url https://www.piwheels.org/simple --prefer-binary --no-cache-dir /app/*.tar.gz

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application when the container launches
CMD ["start_script.sh"]
