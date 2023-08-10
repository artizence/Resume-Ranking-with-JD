import spacy
from spacy import displacy
from  resume_reader_preprocess import *

ENT = [] ## Array of Entities i.e Text example -> "Artizence"
LABEL = [] ## Array of Label i.e Label example -> "ORG"

def entity_detector_maker(ENT:list,LABEL:list):
    entity_detector = spacy.blank("en")
    #Sample text
    patterns = [ ]
    #Create the EntityRuler
    ruler = entity_detector.add_pipe("entity_ruler")
    
    max_range = len(ENT)
    for i in range(0, max_range-1):
        patterns.append({"label":LABEL[i],"pattern": str(ENT[i]).lower()})

    ruler.add_patterns(patterns)

    return entity_detector

class Matcher:

    def __init__(self,job_description:str,resume_paths:list,
                 skills:list,location=[],visa=[],yearofexperience =[],database=False):
        self.job_description = job_description
        self.resume_paths = resume_paths
        self.score = []
        self.df = ''
        self.skills = skills
        self.location =location # max allowered score 1
        self.visa  = visa # max allowered score 1
        self.yearofexperiance = yearofexperience # max allowed score
        self.total_entities =  len(skills)+ len(self.location) + len(self.visa) + len(self.yearofexperiance)
        #print('total entities',self.total_entities)
        self.entities_table = {'skills':skills,'location':location,'visa':visa,'yearofexperiance':[yearofexperience]}
        self.nlp =''

    def job_description_nlp(self):
        # we will feed the entities on the entity_maker
        keys = list(self.entities_table.keys())
        for key in keys:
            for entities in self.entities_table[key]:
                ENT.append(entities),LABEL.append(key)
        ## calling the               
        ## we will open resume one by one
        self.nlp = entity_detector_maker(ENT,LABEL)
    
    def matcher(self):
        ##calling the job description nlp
        self.job_description_nlp()

        ## we will open resume one by one
        for resume_path in self.resume_paths:
            resume = resume_reader(resume_path).lower()
            
            ## we will search for the entities 
            doc = self.nlp(resume)
            detect_entities = []
            for x in doc.ents:
                detect_entities.append(x.text)    
            #print('entities detected ')
            detect_entities = len(list(set(detect_entities)))
            print("detect_entities",detect_entities)

            
            score = ((detect_entities / self.total_entities) *100)
            score = round(score, 2)
            
          
            self.score.append(score)


        df = pd.DataFrame([self.score,self.resume_paths])
        df = df.T
        df.columns =['score','resume']

        df['score'] = df['score'].apply(lambda x : float(x))
        df.sort_values(by=['score'], inplace=True, ascending=False)
        df['Rank'] = [ i for i in range(1,len(self.score)+1)]
        return {'resume':df['resume'].values.tolist(),'score':df['score'].values.tolist(),'rank':df['Rank'].values.tolist() }

## We will load all the devops resumes

## loading the csv file

if __name__ == '__main__':

    db = pd.read_csv('DATA/job_applications_test.csv')
    print(db.head())