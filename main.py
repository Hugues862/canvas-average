import requests
import Fetch
import pandas as pd


def getData():
    s = requests.Session()
    Fetch.login(s)
    DATA = Fetch.getGradesData(s)
    DATA = Fetch.formatData(DATA)
    return DATA


def formatData(data):
    df = pd.DataFrame.from_dict(data, orient="index")
    df = df.sort_values(by=0, ascending=False).reset_index()
    df.columns = ['CLASS', 'AVERAGE']
    return df


def getTotalAverage(data):
    return data['AVERAGE'].mean()


data = getData()
data = formatData(data)
average = getTotalAverage(data)

print("Your grades : ")
print(data)
print("Your total average is : " + str(average))
