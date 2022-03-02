from bs4 import BeautifulSoup
import json
import requests
import logging
import os

EMAIL = ""
PASSWORD = ""


logging.basicConfig(filename="std.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


path = os.path.abspath(__file__).split("/")
path.pop()
path = "/".join(path)

print(path)


def login(s):
    login_url = 'https://canvas.supinfo.com/login/canvas'
    req = s.get(login_url)
    soup = BeautifulSoup(req.content, "html.parser")
    auth_token = soup.find_all("input")[1].get('value')

    login_data = {
        "authenticity_token": auth_token,
        "pseudonym_session[unique_id]": EMAIL,
        "pseudonym_session[password]": PASSWORD,
        "pseudonym_session[remember_me]": "1"
    }

    login_request = s.post(login_url, login_data)
    if login_request.history[0].status_code == 302:
        logger.info(" - Login successful")
    else:
        logger.error(" - Login Failed")
        exit()


def getGradesData(s):
    grades_url = 'https://canvas.supinfo.com/grades'

    grades = grades_request = s.get(grades_url)
    soup = BeautifulSoup(grades.content, "html.parser")
    p = soup.find(class_="student_grades")
    res = p.find_all("tr")

    logger.info(" - Getting grades successful")

    return res


def formatData(DATA):
    res = {}
    for i in range(len(DATA)):
        res[DATA[i].a.string.split()[0]] = DATA[i].find(
            class_="percent").string.split()[-1]

    for item in res:
        res[item] = res[item].split()[-1]
        try:
            try:
                res[item] = int(res[item][:-1].replace(',', '.'))
            except:
                res[item] = float(res[item][:-1].replace(',', '.'))
        except:
            res[item] = None
    return res

    logger.info(" - Data formatting successful")


def saveDataToFile(DATA):
    with open(path+'/data.json', 'w') as file:
        file.write(json.dumps(DATA))
    logger.info(" - Saved to file successful")


def getDataFromFile():
    with open(path+'/data.json', 'r') as file:
        DATA = json.load(file)
    return DATA
    logger.info(" - Retrieved from file successful")
