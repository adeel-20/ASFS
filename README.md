# Project Documentation

## Overview
Our web-based application is useful in detecting threats on publicly accessible places. This system will serve the purpose of auto surveillance using CCTV cameras. Threat could be a detected gun, shooting, or explosion at some public place. Most of the time, threats are detectable even before it happens.

## Installation
To run the server locally, use the following commands:
```
git clone https://github.com/adeel-20/ASFS.git
cd ASFS
conda create -n asfs-env
conda activate asfs-env
pip install -r requirements.txt
python manage.py runserver
```


## Usage
1. If you want to try our application before creating an account, go onto the demo page and upload a video from which you want to classify threats or suspicious activity.
2. Once the video is uploaded, you’ll start getting output from our models in 2-4 seconds with threat or suspicious activity area marked (usually bounding box).
3. Once logged in, the Dashboard section will appear on your home page.
   - Go to Dashboard page where you’ll have the option to
     - Add cameras: To add a new camera, you’ll need
       - IP address
       - Camera username
       - Camera password
     - You can add multiple cameras, to view a camera, you’ll need to select a camera from the Drop-down menu.
     - To remove a camera, you need to select a camera from the Drop-down menu and click the Remove Camera option.

## Configuration
Almost all of the content of the project is generic except the servers used, to set up your own:
- Mlflow server:
  - Edit the `.env` file and change:
    - Server address
    - Server username
    - Server password
- DVC Cloud Path:
  - To add DVC cloud path, edit the `.env` file and change:
    - Set Google Drive folder ID
    - Set Google account username
    - Set Google account password

## Object Detection
Having a tracking ID for each object allows us to track the activity of each object. We maintain a state dictionary to keep track of each person that enters the frame, in case of loitering. State dictionary contains bounding box coordinates (x,y,w,h), the first occurrence of the person in the frame, and the last occurrence of the person in the frame. This allows us to compute the time each person was in the frame. If a person just walks by, their state will be deleted. If a person stays in the frame for more than the time specified by the user, it’ll be classified as Loitering (Suspicious Activity), Luggage Abandonment, or Shooting. We are also capable of detecting and reporting unattended luggage in front of any private properties.

## MLflow Integration
The MLflow experiment is named "YOLOv8 Training". The hyperparameters, including the number of epochs, batch size, and learning rate, are defined.

Within an MLflow run, the code loads and preprocesses the dataset using the torchvision library. It then creates an instance of the YOLOv7 model and defines the loss function and optimizer.

The training loop begins, iterating over the specified number of epochs. During each epoch, the model is trained on batches of images and targets. The forward pass, loss calculation, backward pass, and optimization steps are performed. The running loss is accumulated to calculate the average loss for the epoch.

The code logs the average loss as a metric using MLflow's `log_metric()` function, providing a way to track the training progress. After the training loop, the trained model is saved as an MLflow artifact using `mlflow.pytorch.log_model()`, allowing easy access and reproducibility of the trained model.

## DVC Integration
To include the process of adding a dataset to your GitHub repository through DVC, with the .dvc file stored in the repository and the actual data in Google Drive, you can follow these steps:

1. Initialize DVC: Run `dvc init` in your local repository directory to set up a DVC repository.
2. Configure Google Drive as a remote storage: Connect DVC to your Google Drive account by setting up a remote storage using `dvc remote add gdrive_remote gdrive://<remote_path>`, replacing `<remote_path>` with the desired Google Drive folder's path.
3. Add the dataset to DVC: Place your dataset in a local directory within your repository. Add it to DVC using `dvc add <path_to_dataset>`, replacing `<path_to_dataset>` with the dataset's path.
4. Push the dataset to Google Drive: Upload the dataset to the remote storage (Google Drive) using `dvc push -r gdrive_remote`.
5. Commit and push changes: Commit the .dvc file and DVC changes to your GitHub repository using Git. This includes the .dvc file that references the dataset in Google Drive.

To use the dataset:
1. Clone the GitHub repository: Clone the repository containing the code and the .dvc file referencing the dataset.
2. Install DVC: Install DVC on the local machine according to the DVC documentation.
3. Authenticate with Google Drive: Authenticate the Google Drive account with DVC using `dvc remote add gdrive_remote gdrive://<remote_path>`, providing the necessary credentials.
4. Pull the dataset: Use `dvc pull` to fetch the dataset from Google Drive based on the information in the .dvc file.
5. Now, the dataset will be available locally, enabling you to use it alongside the software code.
6. Note: Each user accessing the dataset will need to authenticate their Google Drive account with DVC to retrieve the dataset.

## Jenkins Integration
Install Jenkins: Install Jenkins on a server or machine where your code repository is accessible. You can refer to the official Jenkins documentation for installation instructions.

1. Set up Jenkins job: Once Jenkins is installed, create a new Jenkins job for your Python project. You can do this by selecting "New Item" on the Jenkins dashboard and choosing a suitable project type, such as a freestyle project or a pipeline.
2. Configure the Git repository: In the configuration of your Jenkins job, specify the Git repository URL that contains your Python project. Jenkins will clone this repository to its workspace.
3. Install necessary dependencies: Your Python project likely has specific dependencies for object detection. You can use a tool like pip or conda within your Jenkins job configuration to install these dependencies. This can be done either in a build step or as a part of the environment setup.
4. Configure the build steps: Define the build steps necessary for your project. This could include executing Python scripts, running tests, or any other necessary commands specific to your project. For object detection, you might have a script that performs training or inference on images.
5. Configure post-build actions: After the build steps, you can configure post-build actions to handle the output of the build. For example, you might want to archive the generated models, generate reports, or trigger notifications.
6. Schedule and trigger builds: Jenkins provides various options for triggering builds, such as scheduling periodic builds or triggering builds when changes are pushed to the Git repository. Choose the appropriate trigger for your project.
7. Monitor and review builds: Jenkins provides a dashboard where you can monitor the status of your builds, view build logs, and review build

## Containerization with Docker

Before proceeding, ensure that the following prerequisites are met:

- Docker is installed on your machine. You can download and install Docker from the official website: [https://www.docker.com/get-started](https://www.docker.com/get-started).

# Step 1: Create a Dockerfile

1. Create a file named `Dockerfile` in your project directory.
2. Open the `Dockerfile` file and add the following content:

```Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app/

# Expose the application's port
EXPOSE 9000

# Start the Django development server
CMD python manage.py runserver 0.0.0.0:9000
```

# Step 2: Create a Docker Compose Configuration
## Create a file named docker-compose.yml in your project directory.
## Open the docker-compose.yml file and add the following content:
```docker-compose.yml
version: '3'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "9000:9000"
```
# Step 3: Build docker compose.yml
docker-compose up -d
