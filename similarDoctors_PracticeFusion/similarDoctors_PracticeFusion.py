import json
import heapq
import csv
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

#Global objects and constants    
similarityMetrics={}
doctorsDictionary=[]
similarDoctorsDict=dict() 
doctorsDic={}
capacity=5

#Creating a dictionary that stores the relationship between the feature and score
def createDict(featureList,scoreList):
    for i in range(len(featureList)):
        if(featureList[i] not in similarityMetrics):
            similarityMetrics[featureList[i]]=scoreList[i]

#This method stores the "doctorID" as the key and the object as the value in the "doctorsDictionary"
def storeDoctor(obj):
    doctorsDictionary.append([obj.doctorID,obj])
    if(obj.doctorID not in doctorsDic):
        doctorsDic[obj.doctorID]=obj
      
#Method that calculates the similarity of the doctors
#Since we can assume that the details of the doctors do not change frequently we can do  the computation of finding similarity between the doctors offline and store the similarity of each doctor in a dictionary. 
#The dictionary "similarDoctorsDict" would contain the "doctorID" as the key and an array of tuples containing the "priority" and "doctorID"
#The numbers of doctors similar to a given doctor is restricted to 5. But this capacity can be changed by changing the global variable.
#"heapq" library in python has been used to build a priority queue of size 5 which stores the most similar doctors 
def calculateSimilarity(doctorsDictionary,similarityMetrics):
    for i in range(len(doctorsDictionary)):
        heapQ=[]
        for j in range(len(doctorsDictionary)):
            similarityScore=0
            if(i!=j):
                if(doctorsDictionary[i][1].speciality==doctorsDictionary[j][1].speciality):
                    similarityScore+=similarityMetrics["speciality"]
                if(doctorsDictionary[i][1].school==doctorsDictionary[j][1].school):
                    similarityScore+=similarityMetrics["school"]
                if(doctorsDictionary[i][1].experience==doctorsDictionary[j][1].experience):
                    similarityScore+=similarityMetrics["experience"]
                if(doctorsDictionary[i][1].area==doctorsDictionary[j][1].area):
                    similarityScore+=similarityMetrics["area"]
                if(doctorsDictionary[i][1].review==doctorsDictionary[j][1].review):
                    similarityScore+=similarityMetrics["review"]
                temp=[doctorsDictionary[j][0],similarityScore]
                '''if(doctorsDictionary[i][0] not in similarDoctorsDict):
                    similarDoctorsDict[doctorsDictionary[i][0]]=[]
                    similarDoctorsDict[doctorsDictionary[i][0]].append(temp)
                else:
                    similarDoctorsDict[doctorsDictionary[i][0]].append(temp) '''
                if(len(heapQ) < capacity):
                    heapq.heappush(heapQ, temp)
                    #heapq.heappush(similarDoctorsDict[doctorsDictionary[i][0]], temp)
                else:
                    item = heapq.heappop(heapQ)
                    if(item[1]>temp[1]):
                        heapq.heappush(heapQ, item) 
                    else:
                        heapq.heappush(heapQ, temp)
            similarDoctorsDict[doctorsDictionary[i][0]]=heapQ
    #print(similarDoctorsDict)        

#This method builds an output json response that is sorted with the "priority" as the key and the doctor object as the value. 
#This is returned to  "similarDoc" function which returns to "main" function  
def jsonSimilarDocs(listOfSimilarDocs):
    jsonResponse={}
    for i in range(len(listOfSimilarDocs)):
        if(listOfSimilarDocs[i][0] in doctorsDic):
            if(listOfSimilarDocs[i][0] not in jsonResponse ):
                jsonResponse[listOfSimilarDocs[i][0]]=[]
                jsonResponse[listOfSimilarDocs[i][0]].append(doctorsDic[listOfSimilarDocs[i][0]])
            else:
                jsonResponse[listOfSimilarDocs[i][0]].append(doctorsDic[listOfSimilarDocs[i][0]])
    return json.dumps(jsonResponse,default=lambda o: o.__dict__, sort_keys=True, indent=4)   

#This method checks for the similar doctors. Given a "doctorID", this method finds the similar doctors that are stored in a dictionary.
#The key is the "doctorID" given as the input parameter and the value is a list of "doctorID" and "Priority"  similar to the input "doctorID"
def similarDoc(doctorInput):
    #print(doctorInput)
    if(similarDoctorsDict[str(doctorInput)]):
        return jsonSimilarDocs(similarDoctorsDict[str(doctorInput)])
    else:
        return None

#Doctor class
class doctor:
    #Constructor function that initializes the doctorID, name,speciality, insurance, experience, languages, school
    languages=[]
    insurance=[]
    review=[]
    def __init__(self, doctorID, name, speciality, experience, school,review,area):
        self.doctorID=doctorID
        self.name=name
        self.speciality=speciality
        self.experience=experience
        self.school=school
        self.review=review
        self.area=area

if __name__=="__main__":
    
    #Read input data from a cvs file and process them into objects
    csvfile = open('sample.csv','r')
    data = csv.reader(csvfile)
    for row in data:
        doc=doctor(row[0], row[1], row[2], row[3], row[4],float(row[5]),row[6])
        storeDoctor(doc)
    #print(doctorsDictionary)
    #print(len(doctorsDictionary))
    
    #Pre-defined similarity metrics and their corresponding scores
    featureList=["speciality","area","experience","school","review"]
    #scoreList=[5,4,3,3,3,2,2]
    scoreList=[8,5,6,4,0.1]
    
    #Creating a dictionary that stores the relationship between the feature and score
    createDict(featureList,scoreList)
    #print(similarityMetrics)
       
    #Calculate similarity using the similarityMetrics
    calculateSimilarity(doctorsDictionary,similarityMetrics)
    print(similarDoc("00012"))


