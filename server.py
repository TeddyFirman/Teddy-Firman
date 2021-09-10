import os
import csv
from flask import Flask,render_template,url_for, flash, request, redirect, send_from_directory, request
from werkzeug.utils import secure_filename
 


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_data_csv(data)
            message = 'Form Submitted, Thank You for your message!!!'
            return render_template('thankyou.html', message = message)
        except:
            message = "DID NOT SAVE DATA TO DATABASE!!"
            return render_template('thankyou.html', message = message)
    else:
        message = "FORM NOT SUBMITTED!"
        return render_template('thankyou.html', message = message)


@app.route('/<string:page_name>')
def page(page_name='/'):
    try:
        return render_template(page_name)
    except:
        return redirect('/')

def write_data_csv(data):
    email = data['email']
    subject = data['subject']
    message = data["message"]
    with open('db.csv', 'a', newline='') as csvfile:
        db_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        db_writer.writerow([email, subject, message])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return 

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)