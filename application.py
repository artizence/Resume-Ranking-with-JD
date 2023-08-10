from flask import Flask, render_template, request, flash, send_from_directory , jsonify ,redirect
from werkzeug.utils import secure_filename
import os
import requests
import json
from matcher import Matcher
import ast
import nltk 
nltk.download('punkt')


application = Flask(__name__)
app=application

app.config['UPLOAD_FOLDER'] = 'Resume'
ROOT_DIR = os.path.dirname(os.path. abspath(__file__))

@app.route('/api',methods=['GET','POST'])
def hello():
    return str('api working')


@app.route('/', methods=["GET"])
def home():
    #print(uploaded_files)
    return jsonify(
        {
        'message':'working',
        'status':200,
        'server':'Running',
        'endpoints': '/api/' ,
        'matcher':'/api/matcher/',
        }
    )

ALLOWED_EXTENSIONS = set(['pdf', 'docx',])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

  
@app.route('/api/matcher/',methods=['POST','GET'])
def upload_file_multi():
    """
	Entities 
	skill (mandatory)
	location
	visa
	yearofexperience
	"""
	## getting the entities 
	## deadling with saving the resumes
    if request.method == "GET":
	    return jsonify({'status':200,'message': 'working',})

    if request.form.get('skill') is None:
    	return jsonify({
    		'status':404,
    		'error':'skill entity is missing',
    		
    		})

    ''' 
    if 'file' not in request.files:
      return 'No file uploaded', 400
    '''
	#  ast.literal_eval convert string to list keeping in mind string is a syntax of list    	
    ## if skill is present we will search for other entities
    skill =  ast.literal_eval(request.form.get('skill'))
    ## location
    try:
	    location =  ast.literal_eval(request.form.get('location'))
    except ValueError:
	    print('ValueError at Location')
	    location = []
    except:
	    location = []
	    print('ERROR in location')

    ## job description 
    try:
	    jd = ast.literal_eval(request.form.get('job_description')) 

    except ValueError:
        print('ValueError at job_description')
        jd = []
    except:
        jd = []
        print('ERROR in job_description')


    try:
        visa =  ast.literal_eval(request.form.get('visa'))
    except ValueError:
        print('ValueError at visa')
        visa = []
    except:
        visa = []
        print('ERROR in visa')


    try:
        year_of_experience = ast.literal_eval(request.form.get('year_of_experience'))
    except ValueError:
        print('ValueError at year_of_experience')
        year_of_experience = []
    except:
        year_of_experience = []
        print('ERROR in year_of_experience')




    ## uploaded files
    uploaded_files = request.files.getlist("file")
    #resume_filename = []
    path = []  
    for file in uploaded_files:
      filename = secure_filename(file.filename)
      #resume_filename.append(filename)
      ##path of the resumes to be parsed
      path.append(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	
	## getting the entities
	## we will call the matcher when eveything is upload

    match = Matcher(job_description=jd,resume_paths=path,skills=skill,location=location,
				visa=visa,yearofexperience = year_of_experience)
	

    match.job_description_nlp()
	## score contains the resume name and their score
    data = match.matcher()
    ## removing the save resume from the 
    #for file in resume_filename:
      #os.remove(f'Resume/{file}')
    resp = jsonify({'message':'parsing successfully','data':data })
    resp.status_code = 201	
    return resp 

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
