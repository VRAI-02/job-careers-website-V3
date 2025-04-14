from sqlalchemy import create_engine, text,data
import os
# database connection secret key from the environment variable
db_connection_string = os.environ['DB_CONNECTION_STRING']
# creating engine for the database
engine = create_engine(db_connection_string, connect_args={
  "ssl": {
  "ssl_ca": "/etc/ssl/cert.pem" ## DUMMY "ssl-ca" value --> **need to update it to the right ssl_ca**
  }
})

# Funcation to list of jobs --> fetching the value using mysql query from database, connecting engine and converting into a json dictionary
def load_jobs_from_db():
 with engine.connect() as conn:
  result = conn.execute(text("select*from jobs"))
  jobs = []
  for row in result.all():
    jobs.append(dict(row)) 
    return jobs
# Funcation for new page for listed job --> fetching the value using mysql query from database, connecting engine and converting into a json dictionary
# Create table jobs(
# id Int not null Auto_increment,
# title VARCHAR (50) Not null,
# Location VARCHAR (50) Not Null,
# Salary INT,
# Currency VARCHAR(10),
# responsibility VARCHAR(200),
# requirement VARCHAR (200),
# PRIMARY KEY (id)
# );
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
    {"val": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])
#Funcation to add submitted aplication form data to the database
# Create table applicaton(
#   id Int not null Auto_increment,
#   job_id INT NOT NULL,
#   Full_name VARCHAR (50) Not null,
#   email VARCHAR (50) Not Null,
#   linkedin_url VARCHAR (50),
#   work_experience VARCHAR (5000),
#   education VARCHAR (5000),
#   resume_url VARCHAR (500),
#   created_at TIMESTAMP DEFAULT current_timestamp,
#   updated_at TIMESTAMP DEFAULT current_timestamp on update current_timestamp,
#   PRIMARY KEY (id)
# );
def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO application (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
    conn.execute(query, {
       "job_id": job_id,
       "full_name": data['full_name'],
       "email": data['email'],
       "linkedin_url": data['linkedin_url'],
       "work_experience": data['work_experience'],
       "education": data['education'],
       "resume_url": data['resume_url']
       })
#alternte way to add data to the database --> need to check which one is working correctly.
    # conn.execute(query,
    #              job_id=job_id,
    #              full_name=data['full_name'],
    #              email=data['email'],
    #              linkedin_url=data['linkedin_url'],
    #              work_experience=data['work_experience'],
    #              education=data['education'],
    #              resume_url=data['resume_url'])