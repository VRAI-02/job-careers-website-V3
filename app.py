from flask import Flask , render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db


app = Flask(__name__)

# routing to the home page
@app.route("/")
def hello_job():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs, company_name='Career Marketplace')##company_name is a variable
# routing to the api page for jobs and converting the data into json format
@app.route("/api/jobs")
def list_jobs():
  jobs= load_jobs_from_db()
  return jsonify (jobs)
# routing to the job page using the primary key "ID" setup in the database
@app.route("/job/<id>")
def show_job (id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html',job=job)

# routing to the apply page posting data in a form
@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id,data)
  return render_template('application_submitted.html', application=data, job=job)
##host="0.0.0.0" makes the server accessible from any network interface, not just localhost.
##while launching in production,it is recommended to disable debug=flase mode since it can expose sensitive information.
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True) 