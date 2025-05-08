from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from models import (
    get_all_admins, delete_admin_by_id, get_admin_by_id, get_admin_by_username, create_admin, update_admin_password_in_db,
    get_jobs, count_jobs, jobs_collection, get_job_by_id,
    get_results, count_results, results_collection, insert_result, update_result_in_db, delete_result,
    get_admit_cards, count_admit_cards, admit_cards_collection, insert_admit_card, update_admit_card_in_db, delete_admit_card,
    insert_subscriber,
    insert_job, update_job_in_db, delete_job,
    get_important_links,
    get_answer_keys, count_answer_keys, get_answer_key_by_id, insert_answer_key, update_answer_key_in_db, delete_answer_key, # Added answer key functions
    get_syllabus, count_syllabus, get_syllabus_by_id, insert_syllabus, update_syllabus_in_db, delete_syllabus # Added syllabus functions
)
import traceback
from bson.objectid import ObjectId
from datetime import datetime
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_default_secret_key') # Add a secret key for session management

# Ensure the default admin user exists
def ensure_admin_user():
    admin_user = get_admin_by_username('admin')
    if not admin_user:
        default_password = generate_password_hash("admin123") # Default password
        create_admin('admin', default_password)

ensure_admin_user() # Call this function at startup

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login first.')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Function to update admin password (no longer needed globally)
# def update_admin_password(new_password):
#     global ADMIN_PASSWORD
#     ADMIN_PASSWORD = generate_password_hash(new_password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        q = request.args.get('q', '')
        category = request.args.get('category', '')
        eligibility = request.args.get('eligibility', '')
        
        filter_query = {}
        if q:
            filter_query['title'] = {'$regex': q, '$options': 'i'}
        if category:
            filter_query['category'] = category
        if eligibility:
            filter_query['eligibility'] = eligibility
            
        skip = (page - 1) * limit
        jobs_list = get_jobs(filter_query, skip, limit)
        total = count_jobs(filter_query)
        locations = jobs_collection.distinct('location')
        
        # Define categories and eligibility lists
        categories = ["Central", "State", "Other"]
        eligibility_list = ["10th pass", "12th pass", "Graduate", "Other"]
        
        total_pages = (total + limit - 1) // limit
        
        return render_template('jobs.html', 
                             jobs=jobs_list, 
                             page=page, 
                             limit=limit, 
                             total_pages=total_pages,
                             locations=locations,
                             categories=categories,
                             eligibility_list=eligibility_list)
    except Exception as e:
        app.logger.error(f"Error in jobs route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e))

@app.route('/jobs/<job_id>')
def job_details(job_id):
    try:
        job = get_job_by_id(job_id)
        if not job:
            return render_template('error.html', error='Job not found'), 404
        return render_template('job_details.html', job=job)
    except Exception as e:
        app.logger.error(f"Error in job_details route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e))

@app.route('/results')
def results():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit
        results_list = get_results(skip, limit)
        total = count_results()
        total_pages = (total + limit - 1) // limit
        return render_template('results.html', 
                             results=results_list, 
                             page=page, 
                             limit=limit, 
                             total_pages=total_pages)
    except Exception as e:
        app.logger.error(f"Error in results route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e))

@app.route('/admit-cards')
def admit_cards():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit
        admit_cards_list = get_admit_cards(skip, limit)
        total = count_admit_cards()
        total_pages = (total + limit - 1) // limit
        return render_template('admit_cards.html', 
                             admit_cards=admit_cards_list, 
                             page=page, 
                             limit=limit, 
                             total_pages=total_pages)
    except Exception as e:
        app.logger.error(f"Error in admit_cards route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e))

@app.route('/important-links')
def important_links():
    try:
        links = get_important_links()
        return render_template('important_links.html', links=links)
    except Exception as e:
        app.logger.error(f"Error in important_links route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin_user = get_admin_by_username(username)
        
        if admin_user and check_password_hash(admin_user['password'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username # Store username in session
            flash('Login successful!')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None) # Remove username from session
    flash('You have been logged out.')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        username = session.get('admin_username') # Get username from session

        if not username:
            flash('Admin user not found in session. Please log in again.')
            return redirect(url_for('admin_login'))

        admin_user = get_admin_by_username(username)

        if not admin_user:
            flash('Admin user not found. Please contact support.')
            return redirect(url_for('admin_login'))
        
        # Verify current password
        if not check_password_hash(admin_user['password'], current_password):
            flash('Current password is incorrect')
            return redirect(url_for('change_password'))
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match')
            return redirect(url_for('change_password'))
        
        # Update password in the database
        new_hashed_password = generate_password_hash(new_password)
        update_admin_password_in_db(username, new_hashed_password)
        flash('Password changed successfully!')
        return redirect(url_for('admin'))
    
    return render_template('change_password.html')

# Route to manage admin users
@app.route('/admin/users')
@login_required
def manage_users():
    admins = get_all_admins()
    return render_template('admin_users.html', admins=admins)

# Route to add a new admin user
@app.route('/admin/add-user', methods=['GET', 'POST'])
@login_required
def add_admin_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password or not confirm_password:
            flash('All fields are required.')
            return redirect(url_for('add_admin_user'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('add_admin_user'))

        existing_admin = get_admin_by_username(username)
        if existing_admin:
            flash('Username already exists.')
            return redirect(url_for('add_admin_user'))

        hashed_password = generate_password_hash(password)
        create_admin(username, hashed_password)
        flash(f'Admin user {username} added successfully!')
        return redirect(url_for('manage_users'))

    return render_template('add_admin_user.html')

# Route to delete an admin user
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
@login_required
def delete_admin_user(user_id):
    admin_to_delete = get_admin_by_id(user_id)
    current_admin_username = session.get('admin_username')

    if not admin_to_delete:
        flash('Admin user not found.')
        return redirect(url_for('manage_users'))

    # Prevent admin from deleting themselves
    if admin_to_delete['username'] == current_admin_username:
        flash('You cannot delete your own account.')
        return redirect(url_for('manage_users'))

    delete_admin_by_id(user_id)
    flash('Admin user deleted successfully!')
    return redirect(url_for('manage_users'))

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.form.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        insert_subscriber(email)
        return jsonify({'success': True, 'message': 'Subscribed successfully!'})
    except Exception as e:
        app.logger.error(f"Error in subscribe route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': str(e)}), 500

# RESTful API endpoints for jobs
@app.route('/api/jobs', methods=['GET'])
def get_jobs_api():
    try:
        jobs_list = list(jobs_collection.find())
        for job in jobs_list:
            job['_id'] = str(job['_id'])
        return jsonify(jobs_list)
    except Exception as e:
        app.logger.error(f"Error fetching jobs: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch jobs: {str(e)}'}), 500

@app.route('/api/jobs', methods=['POST'])
@login_required
def add_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['title', 'category', 'eligibility']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        result = insert_job(data)
        if result is None:
            return jsonify({'error': 'A job with this title and category already exists'}), 409

        return jsonify({'message': 'Job added successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding job: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to add job: {str(e)}'}), 500

@app.route('/api/jobs/<job_id>', methods=['PUT'])
@login_required
def update_job(job_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        result = update_job_in_db(job_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({'message': 'Job updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating job: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update job: {str(e)}'}), 500

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
@login_required
def delete_job_api(job_id):
    try:
        result = delete_job(job_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({'message': 'Job deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting job: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete job: {str(e)}'}), 500

# RESTful API endpoints for results
@app.route('/api/results', methods=['GET'])
def get_results_api():
    try:
        results_list = list(results_collection.find())
        for result in results_list:
            result['_id'] = str(result['_id'])
        return jsonify(results_list)
    except Exception as e:
        app.logger.error(f"Error fetching results: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch results: {str(e)}'}), 500

@app.route('/api/results', methods=['POST'])
@login_required
def add_result():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['title', 'link', 'date_published']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        result = insert_result(data)
        if result is None:
            return jsonify({'error': 'A result with this title and link already exists'}), 409

        return jsonify({'message': 'Result added successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding result: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to add result: {str(e)}'}), 500

@app.route('/api/results/<result_id>', methods=['PUT'])
@login_required
def update_result(result_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        result = update_result_in_db(result_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Result not found'}), 404
        
        return jsonify({'message': 'Result updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating result: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update result: {str(e)}'}), 500

@app.route('/api/results/<result_id>', methods=['DELETE'])
@login_required
def delete_result_api(result_id):
    try:
        result = delete_result(result_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Result not found'}), 404
        
        return jsonify({'message': 'Result deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting result: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete result: {str(e)}'}), 500

# RESTful API endpoints for admit cards
@app.route('/api/admit-cards', methods=['GET'])
def get_admit_cards_api():
    try:
        admit_cards_list = list(admit_cards_collection.find())
        for admit_card in admit_cards_list:
            admit_card['_id'] = str(admit_card['_id'])
        return jsonify(admit_cards_list)
    except Exception as e:
        app.logger.error(f"Error fetching admit cards: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch admit cards: {str(e)}'}), 500

@app.route('/api/admit-cards', methods=['POST'])
@login_required
def add_admit_card():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['title', 'link', 'date_published']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        result = insert_admit_card(data)
        if result is None:
            return jsonify({'error': 'An admit card with this title and link already exists'}), 409

        return jsonify({'message': 'Admit card added successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding admit card: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to add admit card: {str(e)}'}), 500

@app.route('/api/admit-cards/<admit_card_id>', methods=['PUT'])
@login_required
def update_admit_card(admit_card_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        result = update_admit_card_in_db(admit_card_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Admit card not found'}), 404
        
        return jsonify({'message': 'Admit card updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating admit card: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update admit card: {str(e)}'}), 500

@app.route('/api/admit-cards/<admit_card_id>', methods=['DELETE'])
@login_required
def delete_admit_card_api(admit_card_id):
    try:
        result = delete_admit_card(admit_card_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Admit card not found'}), 404
        
        return jsonify({'message': 'Admit card deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting admit card: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete admit card: {str(e)}'}), 500

# RESTful API endpoints for important links
@app.route('/api/important-links', methods=['GET'])
def get_important_links_api():
    try:
        links = get_important_links()
        for link in links:
            link['_id'] = str(link['_id'])
        return jsonify(links)
    except Exception as e:
        app.logger.error(f"Error fetching important links: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch important links: {str(e)}'}), 500

@app.route('/api/important-links', methods=['POST'])
@login_required
def add_important_link():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['title', 'url', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        result = insert_important_link(data)
        if result is None:
            return jsonify({'error': 'A link with this title and URL already exists'}), 409

        return jsonify({'message': 'Important link added successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding important link: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to add important link: {str(e)}'}), 500

@app.route('/api/important-links/<link_id>', methods=['PUT'])
@login_required
def update_important_link_api(link_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        result = update_important_link(link_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Important link not found'}), 404
        
        return jsonify({'message': 'Important link updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating important link: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update important link: {str(e)}'}), 500

@app.route('/api/important-links/<link_id>', methods=['DELETE'])
@login_required
def delete_important_link_api(link_id):
    try:
        result = delete_important_link(link_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Important link not found'}), 404
        
        return jsonify({'message': 'Important link deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting important link: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete important link: {str(e)}'}), 500

@app.route('/api/important-links/<link_id>', methods=['GET'])
def get_important_link(link_id):
    try:
        link = important_links_collection.find_one({'_id': ObjectId(link_id)})
        if not link:
            return jsonify({'error': 'Link not found'}), 404
        
        link['_id'] = str(link['_id'])
        return jsonify(link)
    except Exception as e:
        app.logger.error(f"Error fetching important link: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch important link: {str(e)}'}), 500

# Add secret key for session management
app.secret_key = os.urandom(24)  # In production, use a secure secret key

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error="Internal Server Error"), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error="Forbidden"), 403

@app.route('/admin/add_result', methods=['POST'])
def add_result_form():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    title = request.form.get('title')
    link = request.form.get('link')
    date_published = request.form.get('date_published')
    pdf_link = request.form.get('pdf_link')
    
    if not all([title, link, date_published]):
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('admin'))
    
    try:
        result_data = {
            'title': title,
            'link': link,
            'date_published': date_published,
            'pdf_link': pdf_link
        }
        result = insert_result(result_data)
        if result:
            flash('Result added successfully!', 'success')
        else:
            flash('Error: Duplicate result entry detected', 'error')
    except Exception as e:
        flash(f'Error adding result: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/edit_result/<result_id>', methods=['POST'])
def edit_result(result_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    title = request.form.get('title')
    link = request.form.get('link')
    date_published = request.form.get('date_published')
    pdf_link = request.form.get('pdf_link')
    
    if not all([title, link, date_published]):
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('admin'))
    
    try:
        result_data = {
            'title': title,
            'link': link,
            'date_published': date_published,
            'pdf_link': pdf_link
        }
        result = update_result_in_db(result_id, result_data)
        if result.matched_count > 0:
            flash('Result updated successfully!', 'success')
        else:
            flash('Error: Result not found', 'error')
    except Exception as e:
        flash(f'Error updating result: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/answer-keys')
def answer_keys():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        q = request.args.get('q', '')
        
        filter_query = {}
        if q:
            filter_query['title'] = {'$regex': q, '$options': 'i'}
        
        skip = (page - 1) * limit
        answer_keys = get_answer_keys(skip, limit)
        total = count_answer_keys()
        
        return render_template('answer_keys.html', 
                             answer_keys=answer_keys,
                             current_page=page,
                             total_pages=(total + limit - 1) // limit,
                             query=q)
    except Exception as e:
        flash('An error occurred while fetching answer keys.')
        return redirect(url_for('index'))

@app.route('/syllabus')
def syllabus():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        q = request.args.get('q', '')
        
        filter_query = {}
        if q:
            filter_query['title'] = {'$regex': q, '$options': 'i'}
        
        skip = (page - 1) * limit
        syllabus_list = get_syllabus(skip, limit)
        total = count_syllabus()
        
        return render_template('syllabus.html', 
                             syllabus_list=syllabus_list,
                             current_page=page,
                             total_pages=(total + limit - 1) // limit,
                             query=q)
    except Exception as e:
        flash('An error occurred while fetching syllabus.')
        return redirect(url_for('index'))

# RESTful API endpoints for Answer Keys
@app.route('/api/answer-keys', methods=['GET'])
def get_answer_keys_api():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit
        answer_keys_list = get_answer_keys(skip, limit)
        total = count_answer_keys()
        total_pages = (total + limit - 1) // limit
        
        # Convert ObjectId to string for JSON serialization
        for key in answer_keys_list:
            key['_id'] = str(key['_id'])
            
        return jsonify({
            'answer_keys': answer_keys_list,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'total_items': total
        })
    except Exception as e:
        app.logger.error(f"Error fetching answer keys: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch answer keys: {str(e)}'}), 500

@app.route('/api/answer-keys/<answer_key_id>', methods=['GET'])
@login_required
def get_answer_key_api(answer_key_id):
    try:
        answer_key = get_answer_key_by_id(answer_key_id)
        if not answer_key:
            return jsonify({'error': 'Answer Key not found'}), 404
        answer_key['_id'] = str(answer_key['_id']) # Convert ObjectId to string
        return jsonify(answer_key)
    except Exception as e:
        app.logger.error(f"Error fetching answer key {answer_key_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch answer key: {str(e)}'}), 500

@app.route('/api/answer-keys', methods=['POST'])
@login_required
def add_answer_key_api():
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'link' not in data or 'date_published' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Convert date string to datetime object if necessary
        # Assuming date_published is sent as YYYY-MM-DD string
        try:
            data['date_published'] = datetime.strptime(data['date_published'], '%Y-%m-%d')
        except ValueError:
             # Handle cases where date might already be in correct format or invalid
             pass # Or add specific error handling

        result = insert_answer_key(data)
        if result is None:
             return jsonify({'error': 'Answer Key with this title and link already exists'}), 409 # Conflict
        
        return jsonify({'message': 'Answer Key added successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding answer key: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to add answer key: {str(e)}'}), 500

@app.route('/api/answer-keys/<answer_key_id>', methods=['PUT'])
@login_required
def update_answer_key_api(answer_key_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided for update'}), 400

        # Convert date string to datetime object if necessary
        if 'date_published' in data:
            try:
                data['date_published'] = datetime.strptime(data['date_published'], '%Y-%m-%d')
            except (ValueError, TypeError):
                 # Handle cases where date might already be in correct format or invalid
                 pass # Or add specific error handling

        result = update_answer_key_in_db(answer_key_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Answer Key not found'}), 404
        
        return jsonify({'message': 'Answer Key updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating answer key {answer_key_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update answer key: {str(e)}'}), 500

@app.route('/api/answer-keys/<answer_key_id>', methods=['DELETE'])
@login_required
def delete_answer_key_api(answer_key_id):
    try:
        result = delete_answer_key(answer_key_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Answer Key not found'}), 404
        
        return jsonify({'message': 'Answer Key deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting answer key {answer_key_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete answer key: {str(e)}'}), 500

# RESTful API endpoints for Syllabus
@app.route('/api/syllabus', methods=['GET'])
def get_syllabus_api():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit
        syllabus_list = get_syllabus(skip, limit)
        total = count_syllabus()
        total_pages = (total + limit - 1) // limit
        
        # Convert ObjectId to string for JSON serialization
        for item in syllabus_list:
            item['_id'] = str(item['_id'])
            
        return jsonify({
            'syllabus': syllabus_list,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'total_items': total
        })
    except Exception as e:
        app.logger.error(f"Error fetching syllabus: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch syllabus: {str(e)}'}), 500

@app.route('/api/syllabus/<syllabus_id>', methods=['GET'])
@login_required
def get_single_syllabus_api(syllabus_id):
    try:
        syllabus_item = get_syllabus_by_id(syllabus_id)
        if not syllabus_item:
            return jsonify({'error': 'Syllabus not found'}), 404
        syllabus_item['_id'] = str(syllabus_item['_id']) # Convert ObjectId to string
        return jsonify(syllabus_item)
    except Exception as e:
        app.logger.error(f"Error fetching syllabus {syllabus_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch syllabus: {str(e)}'}), 500

@app.route('/api/syllabus', methods=['POST'])
@login_required
def add_syllabus_api():
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'link' not in data or 'date_published' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Convert date string to datetime object if necessary
        try:
            data['date_published'] = datetime.strptime(data['date_published'], '%Y-%m-%d')
        except ValueError:
             pass # Or add specific error handling

        result = insert_syllabus(data)
        if result is None:
             return jsonify({'error': 'Syllabus with this title and link already exists'}), 409 # Conflict

        return jsonify({'message': 'Syllabus added successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding syllabus: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to add syllabus: {str(e)}'}), 500

@app.route('/api/syllabus/<syllabus_id>', methods=['PUT'])
@login_required
def update_syllabus_api(syllabus_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided for update'}), 400

        # Convert date string to datetime object if necessary
        if 'date_published' in data:
            try:
                data['date_published'] = datetime.strptime(data['date_published'], '%Y-%m-%d')
            except (ValueError, TypeError):
                 pass # Or add specific error handling

        result = update_syllabus_in_db(syllabus_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Syllabus not found'}), 404
        
        return jsonify({'message': 'Syllabus updated successfully'})
    except Exception as e:
        app.logger.error(f"Error updating syllabus {syllabus_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update syllabus: {str(e)}'}), 500

@app.route('/api/syllabus/<syllabus_id>', methods=['DELETE'])
@login_required
def delete_syllabus_api(syllabus_id):
    try:
        result = delete_syllabus(syllabus_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Syllabus not found'}), 404
        
        return jsonify({'message': 'Syllabus deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting syllabus {syllabus_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete syllabus: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)