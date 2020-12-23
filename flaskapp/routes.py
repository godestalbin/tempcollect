from flask import render_template, request
from flaskapp import tempCollectApp
from flaskapp import firbeix
from flaskapp import wattignies
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