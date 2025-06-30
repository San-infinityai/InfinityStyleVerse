from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/profile')
def profile():
    return render_template('profile.html')

@main_bp.route('/login')
def login_page():
    return render_template('login.html')

@main_bp.route('/register')
def register_page():
    return render_template('register.html')

@main_bp.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@main_bp.route('/creator/dashboard')
def creator_dashboard():
    return render_template('creator/creator_dashboard.html')

@main_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/admindashboard.html')

@main_bp.route('/customer/home')
def customer_home():
    return render_template('')

@main_bp.route('/staff/dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')

@main_bp.route('/index')
def index():
    return render_template('index.html')

@main_bp.route('/addproduct')
def addproduct():
    return render_template('addproduct.html')

@main_bp.route('/profileview')
def profileview():
    return render_template('profile.html')