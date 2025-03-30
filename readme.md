# 🤖 AI-Powered Comment Moderation Microservice

A scalable Django + PostgreSQL microservice for moderating user comments on predefined posts using Google Cloud Natural Language API. Automatically flags inappropriate content and notifies users via email.

---

## 🚀 Features

- JWT-based **authentication system** (signup & login)
- 5 **predefined posts** stored via migrations
- **Commenting system** per post
- Real-time **content moderation** using **Google Cloud NLP API**
- **Flagged comments** stored per user
- **Email notifications** for flagged comments
- Fully **Dockerized** and scalable

---

## 🚧 Tech Stack

- Backend: **Django**, **Django Rest Framework**
- Database: **PostgreSQL**
- Auth: **JWT**
- Content Moderation: **Google Cloud NLP API**
- Email: **SMTP with Gmail**
- Containerization: **Docker & Docker Compose**

---

## 📁 Project Structure

```
moderation_service/
├── comments/                # Comment endpoints, moderation logic
├── posts/                   # Predefined posts
├── users/                   # Signup, login, JWT logic
├── moderation_service/      # Settings, URL config
├── scenic-setup-*.json      # GCP credentials (not committed)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── wait_for_postgres.sh
└── .env
```

---

## 🚩 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/moderation_service.git
cd moderation_service
```

### 2. Add Environment Variables
Create a `.env` file:
```env
POSTGRES_DB=moderation
POSTGRES_USER=your_user_m
POSTGRES_PASSWORD=your_password
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json
```

### 3. Add GCP Key
Place your `scenic-setup-...json` file in the root and make sure it's listed in `.gitignore`.

### 4. Run Docker
```bash
docker-compose down -v
docker-compose up --build
```

App runs at: [http://localhost:8001](http://localhost:8000)

---

## 📊 API Endpoints

### Auth
- `POST /api/signup/` - Register user
- `POST /api/login/` - Login, returns JWT token

### Posts
- `GET /api/posts/` - List all posts

### Comments
- `POST /api/posts/<id>/comment/` - Add comment to a post
- `GET /api/comments/flagged/` - View user's flagged comments

---

## 📧 Email Notifications
Uses Gmail SMTP to notify users if their comment is flagged by moderation logic. App passwords recommended.

---

## 🌐 Deployment

- [Deployed on render] (https://moderation-service-yw9r.onrender.com)
- [Deploy on Local] Naviagte to the project folder and run Docker Compose up --build. 



## 🙏 Acknowledgements
- [Google Cloud NLP](https://cloud.google.com/natural-language)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## 👤 Author
Built with ❤️ by Vivekanand S J