# SarkariResult Clone - Job Portal

A full-stack job portal inspired by sarkariresult.com, built with Flask, MongoDB, HTML, CSS, and Bootstrap 5.

## Features
- Homepage with Latest Government Jobs, Admit Cards, Exam Results, and search bar
- Paginated and filterable job listings
- Dedicated pages for jobs, results, and admit cards
- Job details page
- Admin panel for managing jobs, results, and admit cards (CRUD with modals and AJAX)
- Responsive design (Bootstrap 5)
- Email subscription form
- RESTful backend API with pagination

## Folder Structure
```
FlaskProject1/
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── static/
│   ├── style.css
│   └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   ├── job_details.html
│   ├── results.html
│   ├── admit_cards.html
│   └── admin.html
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB running locally or a MongoDB URI

### Installation
1. Clone the repository or copy the project files.
2. Navigate to the project directory:
   ```
   cd FlaskProject1
   ```
3. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set the MongoDB URI (if not using default):
   - By default, connects to `mongodb://localhost:27017/`
   - To use a different URI, set the `MONGO_URI` environment variable.

### Running the App
```
python app.py
```
- The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Deployment
- Use a production server like Gunicorn or uWSGI for deployment.
- Set environment variables for production (e.g., `FLASK_ENV=production`).
- Ensure MongoDB is accessible from your deployment environment.

## Admin Panel
- Visit `/admin` to manage jobs, results, and admit cards.
- All CRUD operations are modal-based and use AJAX.

## API Endpoints
- `/api/jobs`, `/api/results`, `/api/admit-cards` (GET, POST, PUT, DELETE)
- Supports pagination via `?page=1&limit=10`

## License
MIT