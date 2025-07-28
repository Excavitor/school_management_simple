# School Management System

A comprehensive Django-based school management system with role-based access control, built using Django REST Framework, authentication, and a clean web interface.

## Features

### Authentication & Authorization
- Custom User model with email-based authentication
- JWT token-based API authentication
- Session-based web authentication
- Role-based permissions using Django Groups
- Granular permissions (add, view, change, delete)

### Public Features
- **Home Page**: Welcome page with recent notices and quick links
- **Notice Board**: Public notice listing with search functionality
- **Admission Form**: Online admission application form
- **Responsive Design**: Clean HTML/CSS interface

### Dashboard Features (Authenticated Users)
- **Role-based Dashboard**: Different content based on user permissions
- **Notice Management**: Create, edit, delete, and manage notices
- **Admission Management**: View and manage admission applications
- **Role Management**: Assign roles to users (Superadmin only)
- **Permission-based UI**: Sidebar and actions visible based on user permissions

### API Features
- RESTful API endpoints using Django REST Framework
- JWT authentication for API access
- CORS support for frontend integration
- Djoser integration for user management

## Technology Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: PostgreSQL (configurable to SQLite for development)
- **Authentication**: Djoser, Simple JWT, Django Sessions
- **Frontend**: HTML, CSS, Django Templates
- **Environment**: Python Decouple for configuration

## Quick Start

### 1. Setup Virtual Environment
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate.bat  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
USE_SQLITE=True  # Set to False for PostgreSQL
DATABASE_NAME=school_management
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create sample data (optional)
python create_sample_data.py
```

### 4. Run the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## Default Users (After running create_sample_data.py)

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| Superuser | admin@school.com | admin123 | All permissions |
| Notice Manager | notice.manager@school.com | password123 | Notice management only |
| Admission Manager | admission.manager@school.com | password123 | Admission management only |
| Full Manager | full.manager@school.com | password123 | Both notices and admissions |
| Regular User | regular.user@school.com | password123 | View-only access |

## Project Structure

```
school_management/
├── accounts/           # Custom user model and authentication
├── public/            # Public-facing features (notices, admissions)
├── dashboard/         # Authenticated user dashboard
├── templates/         # HTML templates
│   ├── base/         # Base templates
│   ├── accounts/     # Authentication templates
│   ├── public/       # Public page templates
│   └── dashboard/    # Dashboard templates
├── static/           # Static files (CSS, JS, images)
├── school_management/ # Django project settings
├── manage.py
├── requirements.txt
├── .env             # Environment variables
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/users/` - User registration
- `POST /api/auth/jwt/create/` - Login (get JWT tokens)
- `POST /api/auth/jwt/refresh/` - Refresh JWT token
- `POST /api/auth/jwt/verify/` - Verify JWT token

### Web Routes
- `/` - Home page
- `/notices/` - Public notice list
- `/admission/` - Admission application form
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration page
- `/dashboard/` - User dashboard
- `/admin/` - Django admin interface

## Permission System

The system uses Django's built-in Group and Permission models:

### Groups (Roles)
- **Notice Manager**: Can manage notices
- **Admission Manager**: Can manage admission applications
- **Full Manager**: Can manage both notices and admissions

### Permissions
- `public.add_notice` - Create notices
- `public.view_notice` - View notices
- `public.change_notice` - Edit notices
- `public.delete_notice` - Delete notices
- `public.add_admissionapplication` - Create admission applications
- `public.view_admissionapplication` - View admission applications
- `public.change_admissionapplication` - Edit admission applications
- `public.delete_admissionapplication` - Delete admission applications

## Customization

### Adding New Roles
1. Create a new Group in Django admin
2. Assign appropriate permissions to the group
3. Assign users to the group

### Database Configuration
- For development: Set `USE_SQLITE=True` in `.env`
- For production: Set `USE_SQLITE=False` and configure PostgreSQL credentials

### Frontend Customization
- Templates are located in `templates/` directory
- CSS styles are embedded in `templates/base/base.html`
- Create separate CSS files in `static/` directory for advanced styling

## Development Notes

- The system uses email as the username field
- Users cannot select roles during registration (assigned by admin)
- Sidebar items are dynamically shown based on user permissions
- All forms include CSRF protection
- The system supports both session and JWT authentication

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure PostgreSQL database
3. Set up proper static file serving
4. Configure ALLOWED_HOSTS
5. Use environment variables for sensitive settings
6. Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.