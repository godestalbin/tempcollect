from flask import render_template
from flaskapp import tempCollectApp
from flaskapp import firbeix
from flaskapp import wattignies

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