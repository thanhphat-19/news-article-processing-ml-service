# Setup Instructions

!!! note Notice
    - This setup is designed for **Linux systems** (specifically Ubuntu 22.04 - which I'm currently using)
    - This service **not design for ready-production**

## 1. Environment Setup



## 1.1 Miniconda and Python

### Step 1: Download and Install Miniconda

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

After installing, close and reopen your terminal application or refresh it by running the following command:

```bash
source ~/miniconda3/bin/activate
```

Then, initialize conda on all available shells by running the following command:

```bash
conda init --all
```

### Step 2: Create a New Environment

```bash
conda create -n text_services python=3.10
conda activate text_services
```

### Step 3: Verify Installation

```bash
conda --version
python --version
```

!!! example "Expected Output"
    ```
    conda 24.5.0
    Python 3.10.16
    ```

!!! tip "Additional Resources"
    Please refer to the [Miniconda documentation](https://www.anaconda.com/docs/getting-started/miniconda/install#macos-linux-installation) for further details.

---

## 1.2 Docker and Docker Compose

### Step 1: Install Docker Engine
  
Set up Docker's repository:

```bash
# Update the apt package index and install packages to allow apt to use a repository over HTTPS
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker Engine:

```bash
# Update the apt package index
sudo apt-get update

# Install Docker Engine, containerd, and Docker Compose
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

!!! warning "Post-installation Steps"
    To run Docker without sudo, add your user to the docker group:
    ```bash
    sudo usermod -aG docker $USER
    newgrp docker  # Apply the new group membership
    ```
    You may need to log out and back in for this to take effect.

### Step 2: Verify Installation

Verify that Docker Engine is installed correctly by running the hello-world image:

```bash
docker run hello-world
```

Check installed versions:

```bash
docker --version
docker compose version
```

!!! example "Expected Output"
    ```
    Docker version 25.0.3, build 4debf41
    Docker Compose version v2.24.7
    ```

!!! tip "Additional Resources"
    Please refer to the [official Docker documentation](https://docs.docker.com/engine/install/ubuntu/) for further details.







# Start off the service 

```bash
cd text-services
bash ./scripts/dev.sh 
```



## Service Endpoints

When running in Docker, access the services at:

| Component | Access URL |
|-----------|------------|
| FastAPI Swaggers| http://localhost:8000/docs |
| RabbitMQ Admin | http://localhost:15672 |
| Gradio UI | http://localhost:7860 |
| API and Promting-Strategy Documentation | http://localhost:8080|
| Celery Flower | http://localhost:5555 |
