# YASM.
### yet another social media.

YASM. is a dynamic platform for sharing your thoughts, moments, and creativity in real-time. Just like mainstream social media apps, but with more freedom: express yourself, connect with others, and stay updated with the world, all in one place.

---

## Requirements

Before running the project, ensure [Docker](https://docs.docker.com/get-docker/) is installed, and the Docker Daemon is running on your machine.

---

## Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/imaquar/Yasm
cd yasm
```

### Step 2: Build the Docker image

```bash
docker build -t yasm .
```

### Step 3: Run the Docker container

Run the container with the following command:

```bash
docker run -p 8000:8000 yasm
```

After running this command, you should be able to access the app by visiting http://localhost:8000 in your web browser.

---
##Stopping & removing YASM. container
If you need to stop the running container:

```bash
docker stop yasm
```
To remove the container:

```bash
docker rm yasm
```
