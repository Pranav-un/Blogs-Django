# Modern Blog Platform 🚀

A feature-rich blog platform built with Django that allows users to create, share, and interact with blog posts. The platform includes modern UI elements, real-time reactions, and a responsive design.

## ✨ Features

- **👤 User Authentication**
  - User registration and login
  - Profile management
  - Blogger profiles with statistics

- **📝 Blog Posts**
  - Create, edit, and delete blog posts
  - Rich text content support
  - Image upload capability
  - Pagination for better navigation

- **💫 Interactions**
  - Facebook-style reactions (Like, Love, Wow)
  - Comments on posts
  - Real-time reaction updates
  - Comment management

- **🎨 Modern UI/UX**
  - Responsive design
  - Animated transitions
  - Interactive elements
  - Clean and intuitive interface

- **🔧 Additional Features**
  - Search functionality
  - Category/tag support
  - User statistics
  - Admin dashboard

## 🛠️ Tech Stack

- **⚙️ Backend**
  - Django 4.2.18
  - Python 3.10
  - SQLite (default database)

- **🎯 Frontend**
  - Bootstrap 5
  - jQuery
  - Font Awesome icons
  - Animate.css for animations

## 📸 Screenshots

### Home Page
![Screenshot (15)](https://github.com/user-attachments/assets/0dea4ec1-badc-42bf-84ad-86ca883b6e43)
*Modern card-based layout with animated transitions*

### Post Detail
![Screenshot (17)](https://github.com/user-attachments/assets/17462429-36d2-4e1a-9139-f6cc6f483a9d)

*Detailed view of a blog post with reactions and comments*

### User Profile
![Screenshot (18)](https://github.com/user-attachments/assets/f1ce69b7-66f8-487a-a973-80d1b15d06c7)

*User profile page with statistics and posts*



## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:9000` in your browser

## 📁 Project Structure

```
blog/
├── blog/                 # Main project directory
│   ├── templates/       # HTML templates
│   ├── static/         # Static files (CSS, JS, images)
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   └── urls.py         # URL routing
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## 🔧 Custom Template Filters

The project includes several custom template filters:

- `multiply`: Multiply two numbers
- `sum_reactions`: Calculate total reactions across posts
- `sum_comments`: Calculate total comments across posts
- `filter_reactions`: Filter reactions by type
- `has_user_reacted`: Check if a user has reacted to a post
- `get_user_reaction_type`: Get a user's reaction type for a post

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
