## This File is responsible for updating the database automatically

## we will first establish a connection with the database 
import mysql.connector
from pprint import pprint
from resume_download import resume_downloder
from matcher import Matcher
import asyncio


mydb = mysql.connector.connect(
  host="xxxxxxxx",
  user="xxxxx",
  password="xxxxx",
  database="xxxxx"

)


mycursor = mydb.cursor()

def updater_class():

  mycursor.execute("SELECT * FROM job_applications")

  job_applicants = mycursor.fetchall()

  for applicant in job_applicants:

      #print(applicant)
      #break 
      mycursor.execute(f'SELECT * from jobs where id = {applicant[1]}')   
      
      job = mycursor.fetchall()


      #if True:
      try: 
        skills = job[-1][17]
        year_of_experience = job[-1][31]
        experience_requirement = job[-1][20]
        education_requirement = job[-1][19]
        description = job[-1][16] 
        exp_level = job[-1][15]

        resume_path = applicant[9]

        ##downlaoding the resume then calling the matcher

        print(resume_path)

        resume_file_loc = asyncio.run(resume_downloder(resume_path))

        #print("resume_file_loc",resume_file_loc)

        #print(skills,year_of_experience,experience_requirement,education_requirement,
        #  description,exp_level)
        ##calling the matcher
        print(resume_file_loc)


        match = Matcher(job_description=" ",
                        resume_paths=[resume_file_loc],
                        skills=[skills],
				                #visa=[visa],
                        yearofexperience = [year_of_experience],
                        database=True,
                        )


        print("score" ,match.matcher())
      #"""
      except IndexError:
        pass

      except Exception as e :
        #print(e,job)
        print(e)
        
      #"""
if __name__ == "__main__":
  updater_class()




#mycursor.execute(f'SELECT * from jobs where id = {myresult[0][1]}')

#job = mycursor.fetchall()

#print(myresult[1][1])


#pprint(myresult[1])

##calling the mather && we don't have resume access as of now
