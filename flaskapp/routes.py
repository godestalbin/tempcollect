from flask import render_template, request
from datetime import datetime
from flaskapp import tempCollectApp
from flaskapp import firbeix
from flaskapp import wattignies
from flaskapp import mongo
from classes import meteodataset
import os
import platform
if platform.system() == 'Linux':
    os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = "/usr/bin/git"
import git

@tempCollectApp.route('/')
@tempCollectApp.route('/index')
def index():
    wattigniesTemp = str(wattignies.getTemp())
    if '.' not in wattigniesTemp: wattigniesTemp = wattigniesTemp + '.0'
    tempPart = wattigniesTemp.split('.')
    wattigniesTemp = tempPart[0]+'°'+tempPart[1][0:1]

    firbeixTemp = str(firbeix.getTemp())
    if '.' not in firbeixTemp: firbeixTemp = firbeixTemp + '.0'
    tempPart = firbeixTemp.split('.')
    firbeixTemp = tempPart[0]+'°'+tempPart[1][0:1]
    return render_template('index.html', data1=wattigniesTemp , data2=firbeixTemp)

@tempCollectApp.route('/tempChart')
def tempChart():
    startDateArg = request.args.get('startDate').split('-')
    endDateArg = request.args.get('endDate').split('-')
    startDate = datetime(int(startDateArg[0]), int(startDateArg[1]), int(startDateArg[2]))
    endDate = datetime(int(endDateArg[0]), int(endDateArg[1]), int(endDateArg[2]), 23, 59)
    groupBy = int(request.args.get('groupBy'))
    firbeixTemp = []
    xAxis = []
    groupByCount = 1
    tempSum = 0
    for temp in mongo.get({'date': { '$gte': startDate, '$lte': endDate }, 'city': 'Firbeix'}):
        tempSum += temp['temp']
        if groupByCount == 1: xAxis += [temp['date'].strftime('%Y-%m-%d %H:%M:%S')]
        if groupByCount == groupBy: # Group by reached, we calculate the value
            firbeixTemp += [round(tempSum / groupBy, 1)]
            groupByCount = 0
            tempSum = 0
        groupByCount += 1
    # print('groupByCount:', groupByCount)
    # if groupByCount < groupBy:
    #     firbeixTemp += [tempSum / groupByCount]
            
    wattigniesTemp = []
    groupByCount = 1
    tempSum = 0
    for temp in mongo.get({'date': { '$gte': startDate, '$lte': endDate }, 'city': 'Wattignies'}):
        # wattigniesTemp = wattigniesTemp + [temp['temp']]
        tempSum += temp['temp']
        if groupByCount == groupBy: # Group by reached, we calculate the value
            wattigniesTemp += [round(tempSum / groupBy, 1)]
            groupByCount = 0
            tempSum = 0
        groupByCount += 1

    data1 = {
                    'name': 'Firbeix',
                    'data': firbeixTemp
                }
    data2 = {
                    'name': 'Wattignies',
                    'data': wattigniesTemp
                }
    # dateRange = "&startDate=" + request.args.get('startDate').rstrip() + "&endDate=" + request.args.get('endDate')
    # print(dateRange)
    return render_template('tempchart.html', groupBy=groupBy, startDate=request.args.get('startDate').rstrip(), endDate=request.args.get('endDate'), xAxis=xAxis, data1=data1, data2=data2)

@tempCollectApp.route('/meteo')
def meteo():
    # meteo = firbeix.getMeteo()
    meteo = wattignies.getMeteo()
    return render_template('meteo.html', meteo=meteo)

@tempCollectApp.route('/pullNewVersion', methods=['POST'])
def pullNewVersion():
    # return render_template('pullNewVersion.html')
    if request.method == 'POST':
        # git.refresh("/usr/bin/git")
        repo = git.Repo('/var/www/tempcollect')
        # repo = git.Repo('C:/Users/20000263/Documents/Dev/tempcollect')
        origin = repo.remotes.origin
        origin.pull()
        return 'Tempcollect git pull completed successfully', 200
    else:
        return 'Wrong event type', 400