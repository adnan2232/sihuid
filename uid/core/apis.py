import json
import requests

def getStudentsData():
    
    studentsData = requests.get("http://localhost:8080/getStudents").json()
    print(studentsData[0])
    
def getFilterStudents(certificate_name="JAVA_STACK"):
    params = {"certificate_name":certificate_name}
    studentsData =  requests.get("http://localhost:8080/getFilterStudents",params=params)
    print(studentsData)