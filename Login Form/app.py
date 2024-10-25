from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to something more secure

# Dummy credentials for regular users and admins
valid_email = "training@jalaacademy.com"
valid_password = "jobprogram"

admin_email = "admin@jalaacademy.com"
admin_password = "admin123"

# Temporary storage for user passwords (in a real app, use a database)
users = {valid_email: valid_password}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email] == password:
        return redirect("https://jalaacademy.com/")
    else:
        flash("Invalid email or password.")
        return redirect(url_for('index'))

@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    email = request.form['admin_email']
    password = request.form['admin_password']

    if email == admin_email and password == admin_password:
        flash("Admin logged in successfully.")
        return redirect(url_for('index'))
    else:
        flash("Invalid admin credentials.")
        return redirect(url_for('admin_login'))

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    
    if email in users:
        return redirect(url_for('password_reset', email=email))
    else:
        flash("Email not found.")
        return redirect(url_for('forgot_password'))

@app.route('/password-reset/<email>')
def password_reset(email):
    return render_template('reset_password.html', email=email)

@app.route('/update-password', methods=['POST'])
def update_password():
    email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password == confirm_password:
        users[email] = new_password
        flash("Password updated successfully. Please log in.")
        return redirect(url_for('index'))
    else:
        flash("Passwords do not match.")
        return redirect(url_for('password_reset', email=email))

if __name__ == '__main__':
    app.run(debug=True)
