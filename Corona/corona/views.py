import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
from bs4 import BeautifulSoup
import smtplib

import pickle

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from collections import namedtuple
from django.shortcuts import render



    
# Create your views here.
def detection(request):
    

    def scrape_worldometer(url, class_name, find_all=True):

        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')
	
        if find_all:
            return soup.find_all('div', class_=class_name)
        return soup.find(
            'table', class_=class_name)
    	
    stat_table = scrape_worldometer('https://www.worldometers.info/coronavirus/#countries', "table table-bordered table-hover main_table_countries", False)
    data = namedtuple("Data", "country, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, total_casesperM, deaths_perM, total_tests, testsperM, continent".split(", "))
    nepal_data = india_data = None
    
    global_data = scrape_worldometer('https://www.worldometers.info/coronavirus/', "maincounter-number")
    cases, death, recovered = [div.find('span').text for div in global_data]
    
    
    for row in stat_table.find_all('tr'):
        cells = [cell.text.lower() if len(cell) else '0' for cell in row.find_all('td')]
        
        if cells and cells[0] == "nepal":
            nepal_data = data(*cells)
            # country, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, total_casesperM, deaths_perM, total_tests, testsperM, continent = cells   
        elif cells and cells[0] == "india":
            india_data = data(*cells)

    def create_comparefile():
        with open('stat_compare.txt', 'w') as r:
            for row in stat_table.find_all('tr'):
                # print([cell.text.lower() for cell in row.find_all('td')])
                for cell in row.find_all('td'):
                    if(cell.text.lower() == 'nepal'):
                        r.write(row.text)

    # def open_comparefile():
    text_file = open("stat_compare.txt", 'r')
    print(text_file.readline())
    ccountry_name = text_file.readline()
    ctotal_cases = text_file.readline()
    cnew_cases = text_file.readline()
    ctotal_deaths = text_file.readline()
    cnew_deaths = text_file.readline()
    ctotal_recovered = text_file.readline()
    cactive_cases = text_file.readline()
    cserious_critical = text_file.readline()

    text_file.close()

    with open('corona_stat.txt', 'w') as r:
        for row in stat_table.find_all('tr'):
            for cell in row.find_all('td'):
                if(cell.text.lower() == 'nepal'):
                    r.write(row.text)

    text_file = open("corona_stat.txt", 'r')
    print(text_file.readline())
    country_name = text_file.readline()
    total_cases = text_file.readline()
    new_cases = text_file.readline()
    total_deaths = text_file.readline()
    new_deaths = text_file.readline()
    total_recovered = text_file.readline()
    active_cases = text_file.readline()
    serious_critical = text_file.readline()

    text_file.close()

    if (new_cases != cnew_cases):
        sender_email = "covid19notifier@gmail.com"
        rec_email = "abhayraut712@gmail.com"
        password = str("Covid-19notifier")
        body = "New case has occured in Nepal: " + new_cases
        subject = "corona virus updates in nepal"
        message = f'Subject: {subject}\n\n{body}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        server.sendmail(sender_email, rec_email, message)

        print(message)
        create_comparefile()
    else:
        print("No new case has occured in Nepal.")

    columns = ['age', 'sex', 'fever', 'cough', 'fatigue', 'abdominal pain', 'diarrhea',
               'malaise', 'pneumonia', 'aching muscles', 'anorexia', 'asymptomatic',
               'chest discomfort', 'dyspnea', 'nausea', 'vomitting', 'chills',
               'conjuctivitis', 'joint pain', 'headache', 'weakness', 'sore throat',
               'sneezing', 'rhinorrhea', 'dizziness', 'runny nose',
               'difficulty walking', 'sputum', 'pneumonitis', 'physical discomfort',
               'toothache', 'wheezing', 'dry mouth', 'sweating']

    sentences = ""
    op = ""

    if request.method == "POST":

        # Taking all the feature inputs
        age = request.POST['age']
        sex = request.POST['sex']
        fever = request.POST['fever']
        cough = request.POST['cough']
        fatigue = request.POST['fatigue']
        abdominalPain = request.POST['abdominalPain']
        diarrhea = request.POST['diarrhea']
        malaise = request.POST['malaise']
        pneumonia = request.POST['pneumonia']
        achingMuscles = request.POST['achingMuscles']
        anorexia = request.POST['anorexia']
        asymptomatic = request.POST['asymptomatic']
        chestDiscomfort = request.POST['chestDiscomfort']
        dyspnea = request.POST['dyspnea']
        nausea = request.POST['nausea']
        vomitting = request.POST['vomitting']
        chills = request.POST['chills']
        conjuctivitis = request.POST['conjuctivitis']
        jointPain = request.POST['jointPain']
        headache = request.POST['headache']
        weakness = request.POST['weakness']
        soreThroat = request.POST['soreThroat']
        sneezing = request.POST['sneezing']
        rhinorrhea = request.POST['rhinorrhea']
        dizziness = request.POST['dizziness']
        runnyNose = request.POST['runnyNose']
        difficultyWalking = request.POST['difficultyWalking']
        sputum = request.POST['sputum']
        pneumonitis = request.POST['pneumonitis']
        physicalDiscomfort = request.POST['physicalDiscomfort']
        toothache = request.POST['toothache']
        wheezing = request.POST['wheezing']
        dryMouth = request.POST['dryMouth']
        sweating = request.POST['sweating']

        # Initializing the DataFrame
        inpDF = pd.DataFrame(np.nan, index=[0], columns=columns)
        # inp = input("Input the text you want to verify: ")

        # Initializng all the feature columns with 0 values
        inpDF["age"] = np.zeros((1, 1), dtype=float)
        inpDF["sex"] = np.zeros((1, 1), dtype=float)
        inpDF["fever"] = np.zeros((1, 1), dtype=float)
        inpDF["cough"] = np.zeros((1, 1), dtype=float)
        inpDF["fatigue"] = np.zeros((1, 1), dtype=float)
        inpDF["abdominal pain"] = np.zeros((1, 1), dtype=float)
        inpDF["diarrhea"] = np.zeros((1, 1), dtype=float)
        inpDF["malaise"] = np.zeros((1, 1), dtype=float)
        inpDF["pneumonia"] = np.zeros((1, 1), dtype=float)
        inpDF["aching muscles"] = np.zeros((1, 1), dtype=float)
        inpDF["anorexia"] = np.zeros((1, 1), dtype=float)
        inpDF["asymptomatic"] = np.zeros((1, 1), dtype=float)
        inpDF["chest discomfort"] = np.zeros((1, 1), dtype=float)
        inpDF["dyspnea"] = np.zeros((1, 1), dtype=float)
        inpDF["nausea"] = np.zeros((1, 1), dtype=float)
        inpDF["vomitting"] = np.zeros((1, 1), dtype=float)
        inpDF["chills"] = np.zeros((1, 1), dtype=float)
        inpDF["conjuctivitis"] = np.zeros((1, 1), dtype=float)
        inpDF["joint pain"] = np.zeros((1, 1), dtype=float)
        inpDF["headache"] = np.zeros((1, 1), dtype=float)
        inpDF["weakness"] = np.zeros((1, 1), dtype=float)
        inpDF["sore throat"] = np.zeros((1, 1), dtype=float)
        inpDF["sneezing"] = np.zeros((1, 1), dtype=float)
        inpDF["rhinorrhea"] = np.zeros((1, 1), dtype=float)
        inpDF["dizziness"] = np.zeros((1, 1), dtype=float)
        inpDF["runny nose"] = np.zeros((1, 1), dtype=float)
        inpDF["difficulty walking"] = np.zeros((1, 1), dtype=float)
        inpDF["sputum"] = np.zeros((1, 1), dtype=float)
        inpDF["pneumonitis"] = np.zeros((1, 1), dtype=float)
        inpDF["physical discomfort"] = np.zeros((1, 1), dtype=float)
        inpDF["toothache"] = np.zeros((1, 1), dtype=float)
        inpDF["wheezing"] = np.zeros((1, 1), dtype=float)
        inpDF["dry mouth"] = np.zeros((1, 1), dtype=float)
        inpDF["sweating"] = np.zeros((1, 1), dtype=float)

        # Now, the 0 values on feature table is replace by the user inputs
        inpDF["age"] = age
        inpDF["sex"] = sex
        inpDF["fever"] = fever
        inpDF["cough"] = cough
        inpDF["fatigue"] = fatigue
        inpDF["abdominal pain"] = abdominalPain
        inpDF["diarrhea"] = diarrhea
        inpDF["malaise"] = malaise
        inpDF["pneumonia"] = pneumonia
        inpDF["aching muscles"] = achingMuscles
        inpDF["anorexia"] = anorexia
        inpDF["asymptomatic"] = asymptomatic
        inpDF["chest discomfort"] = chestDiscomfort
        inpDF["dyspnea"] = dyspnea
        inpDF["nausea"] = nausea
        inpDF["vomitting"] = vomitting
        inpDF["chills"] = chills
        inpDF["conjuctivitis"] = conjuctivitis
        inpDF["joint pain"] = jointPain
        inpDF["headache"] = headache
        inpDF["weakness"] = weakness
        inpDF["sore throat"] = soreThroat
        inpDF["sneezing"] = sneezing
        inpDF["rhinorrhea"] = rhinorrhea
        inpDF["dizziness"] = dizziness
        inpDF["runny nose"] = runnyNose
        inpDF["difficulty walking"] = difficultyWalking
        inpDF["sputum"] = sputum
        inpDF["pneumonitis"] = pneumonitis
        inpDF["physical discomfort"] = physicalDiscomfort
        inpDF["toothache"] = toothache
        inpDF["wheezing"] = wheezing
        inpDF["dry mouth"] = dryMouth
        inpDF["sweating"] = sweating

        print(inpDF)

        X = inpDF.copy()

        featureModel = 'corona/Models/svmModel.sav'
        loadedFEATmodel = pickle.load(open(featureModel, 'rb'))
        featresult = loadedFEATmodel.predict(X)

        op = (featresult[0])

        print("--------")
        print(op)
        print("--------")

    return render(request, "home.html", context={'text': op, 'nepal_data': nepal_data, 'india_data': india_data, 'cases': cases, 'death': death, 'recovered': recovered})
    # return render(request, "home.html")


def informations(request):
	return render(request, "about.html")
