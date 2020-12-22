from flask import render_template, request
from flaskapp import tempCollectApp
from flaskapp import firbeix
from flaskapp import wattignies
# import git

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

@tempCollectApp.route('/pullNewVersion', methods=['POST'])
def pullNewVersion():
    # return render_template('pullNewVersion.html')
    if request.method == 'POST':
        repo = git.Repo('https://github.com/godestalbin/tempcollect.git')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400