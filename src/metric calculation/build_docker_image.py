import os
import subprocess
import configparser

def create_dockerfile():
    # Start of the Dockerfile content
    dockerfile_content = """
    # Use an official Python runtime as a parent image
    FROM python:3.10-slim-buster

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Expose port
    EXPOSE 80
    """

    # Add environment variables from .env file
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    dockerfile_content += f"ENV {line}\n"

    # Finish with the CMD instruction
    dockerfile_content += 'CMD ["python", "workflow.py"]'

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
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
    image_name = config['DockerConfig']['image_name']
    image_store_location = config['DockerConfig']['image_store_location']

    create_dockerfile()
    build_docker_image(image_name, image_store_location)
