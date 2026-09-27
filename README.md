# 🏥 Patient Data Management System

A full-stack patient data management application built with **FastAPI** and **Streamlit**, containerized with **Docker**, published to **Docker Hub**, and deployed on **AWS EC2**.

> 🚀 First cloud deployment project — from local development → Docker → Docker Hub → AWS EC2.

## 🏷️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Docker_Hub-Image_Registry-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS_EC2-Cloud-FF9900?style=for-the-badge\&logo=amazonaws\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Server-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)

## ✨ Features

* 👤 Create, view, update and delete patient records
* 🔍 Search patients by ID
* ↕️ Sort patients by age, height, weight and BMI
* 🧮 Automatic BMI calculation and classification
* ✅ Pydantic-based data validation
* 📊 Streamlit dashboard
* 📚 Interactive FastAPI Swagger documentation
* 🐳 Dockerized backend + frontend
* ☁️ Deployed on AWS EC2

## 🏗️ Architecture

```text
                 ┌──────────────────┐
                 │    Streamlit     │
                 │    Frontend      │
                 │      :8501       │
                 └────────┬─────────┘
                          │
                       HTTP/JSON
                          │
                          ▼
                 ┌──────────────────┐
                 │     FastAPI      │
                 │     Backend      │
                 │      :8000       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   patients.json  │
                 └──────────────────┘
```

The complete application runs inside a Docker container and is deployed through Docker Hub to an AWS EC2 instance.

## 📁 Project Structure

```text
├── 📁 backend
│   ├── 🐍 __init__.py
│   ├── 🐍 main.py
│   ├── 🐍 models.py
│   ├── ⚙️ patients.json
│   └── 🐍 utils.py
├── ⚙️ .gitignore
├── 🐳 Dockerfile
├── 📄 LICENSE
├── 📝 README.md
├── 📄 deploy.sh
├── 📄 requirements.txt
├── 📄 start.sh
└── 🐍 streamlit-app.py
```

## ☁️ Deployment

**Docker Hub**

```text
rajesh15phulwaria2006/patient_data_management-api
```

**AWS EC2 — Live Application**

🌐 **Streamlit:**
http://16.178.42.216:8501/

📚 **FastAPI Swagger:**
http://16.178.42.216:8000/docs

## 🔄 Deployment Flow

```text
Local Development
       ↓
Docker Build
       ↓
Docker Hub
       ↓
AWS EC2
       ↓
Docker Container
       ↓
Streamlit + FastAPI
```

## ⚠️ Note

This project is intended for **learning and demonstration purposes**. It currently uses JSON-based persistence and does not implement authentication, authorization, or production-grade handling of medical data.

## 👨‍💻 Author

**Rajesh Phulwaria**

Built as a practical project to learn **REST APIs, frontend-backend integration, containerization, Docker Hub, and cloud deployment with AWS EC2.**
