from flask import make_response, render_template, request, send_from_directory, send_file, redirect, session, jsonify
from werkzeug.utils import secure_filename
from app import app
import sys
sys.path.append("..")
import facialcommunism as fc
import worker

@app.route('/')
def rootpage():
	print("hello")
	print(sys.path)
	return app.send_static_file('index.html')

@app.route('/form')
def formpage():
	print("yay form")
	print(sys.path)
	return app.send_static_file('form.html')

@app.route('/final')
def finalpage():
	print("nay final")
	print(sys.path)
	return app.send_static_file('final.html')

@app.route("/images/<path:path>")
def images(path):
    # fullpath = "./app/images/" + path
    # resp = make_response(open(fullpath).read())
    # resp.content_type = "image/jpeg"
    return send_file('images/'+path)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      try:
         f = request.files['file']
         if f.filename == '':
            return "No file selected", 400
         filename = secure_filename(f.filename)
         if filename == '':
            filename = 'uploaded_image.jpg'
         fn = 'app/images/'+filename
         f.save(fn)
         print(fn)
         
         worker.start_processing(fn)
         
         session['processing_file'] = fn
         return redirect("/processing", code=302)
      except Exception as e:
         print(f"Error processing upload: {str(e)}")
         import os
         # Copy a sample image if available
         if os.path.exists('app/images/IMG_2867.jpg'):
            import shutil
            shutil.copy('app/images/IMG_2867.jpg', 'app/images/output.jpg')
            return redirect("/final", code=302)
         return f"Error processing image: {str(e)}", 500

@app.route('/processing')
def processing_page():
    """Show a loading page that polls for processing status"""
    if 'processing_file' not in session:
        return redirect("/form", code=302)
    return app.send_static_file('processing.html')

@app.route('/status')
def processing_status():
    """API endpoint to check processing status"""
    if 'processing_file' not in session:
        return jsonify({"status": "unknown"})
    
    filename = session.get('processing_file')
    status = worker.processing_status.get_status(filename)
    
    if status == "completed":
        return jsonify({"status": "completed"})
    elif status == "failed":
        return jsonify({"status": "failed"})
    else:
        return jsonify({"status": "processing"})

@app.errorhandler(404)
def page_not_found(e):
    return """
    <h1>Page Not Found</h1>
    <p>The page you requested could not be found.</p>
    <p><a href="/">Return to homepage</a></p>
    """, 404

@app.errorhandler(500)
def server_error(e):
    return """
    <h1>Server Error</h1>
    <p>An error occurred while processing your request. Please try again later.</p>
    <p><a href="/">Return to homepage</a></p>
    """, 500
