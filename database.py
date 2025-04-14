from sqlalchemy import create_engine, text
import os
# database connection secret key from the environment variable
db_connection_string = os.environ['DB_CONNECTION_STRING']
# creating engine for the database
engine = create_engine(db_connection_string, connect_args={
  "ssl": {
  "ssl_ca": "/etc/ssl/cert.pem" ## DUMMY "ssl-ca" value --> **need to update it to the right ssl_ca**
  }
})

# List of jobs --> fetching the value using mysql query from database, connecting engine and converting into a dictionary
def load_jobs_from_db():
 with engine.connect() as conn:
  result = conn.execute(text("select*from jobs"))
  jobs = []
  for row in result.all():
    jobs.append(dict(row)) 
    return jobs
# New page for listed job -->fetching the value using mysql query from database, connecting engine and converting into a dictionary
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
    {"val": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])