from flask import render_template, request
from flaskapp import tempCollectApp
from flaskapp import firbeix
from flaskapp import wattignies
from flaskapp import mongo
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
    firbeixTemp = []
    xAxis = []
    for temp in mongo.get({'city': 'Firbeix'}):
        xAxis = xAxis + [temp['date'].strftime('%Y-%m-%d %H:%M:%S')]
        firbeixTemp = firbeixTemp + [temp['temp']]
    wattigniesTemp = []
    for temp in mongo.get({'city': 'Wattignies'}):
        wattigniesTemp = wattigniesTemp + [temp['temp']]


    data1 = {
                    'name': 'Firbeix',
                    'data': firbeixTemp
                }
    data2 = {
                    'name': 'Wattignies',
                    'data': wattigniesTemp
                }
    return render_template('tempchart.html', xAxis=xAxis, data1=data1, data2=data2)

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