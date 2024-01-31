import os
import subprocess
import configparser

def create_dockerfile():
    dockerfile_content = """
    # Use an official Python runtime as a parent image
    FROM python:3.8-slim-buster

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Make port available to the world outside this container
    EXPOSE 80

    # Define environment variable
    ENV NAME World

    # Run main.py when the container launches
    CMD ["python", "main.py"]
    """
    with open("Dockerfile", "w") as file:
        file.write(dockerfile_content)

def build_docker_image(image_name, image_store_location):
    try:
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        subprocess.run(["docker", "save", "-o", os.path.join(image_store_location, f"{image_name}.tar"), image_name], check=True)
        print(f"Docker image '{image_name}' built and saved successfully at '{image_store_location}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to build and save Docker image: {e}")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    image_name = config['DockerConfig']['image_name']
    image_store_location = config['DockerConfig']['image_store_location']
    
    create_dockerfile()
    build_docker_image(image_name, image_store_location)
