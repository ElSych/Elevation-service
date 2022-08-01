from flask import Flask
import rasterio

app = Flask(__name__)

elevation_file = 'srtm_N55E160.tif'


def get_elevation(lat, lon):
    coords = ((lat, lon), (lat, lon))
    with rasterio.open(elevation_file) as src:
        vals = src.sample(coords)
        for val in vals:
            elevation = val[0]
            return elevation



@app.route('/')
def mainpage():
    return 'Welcome to the main page'


@app.route('/main/POINT(<float:crd1> <float:crd2>)')
def point(crd1, crd2):
    return ('For POINT(' + str(crd1) + ' ' + str(crd2) + ' ' + ')' + ' Elevation is ' + str(get_elevation(crd1, crd2)))


@app.route('/main/LINESTRING(<coords>)')
def linestring(coords):
    coords = coords.replace(',', '')
    coordsspl = coords.split()
    lengh = len(coordsspl)
    i = 0
    answer = ''
    while i < (lengh - 1):
        answer = answer + str(coordsspl[i]) + ' ' + str(coordsspl[i + 1]) + ' ' + str(get_elevation(float(coordsspl[i]), float(coordsspl[i + 1]))) + ', '
        i += 2
        answer = answer[:-2]
    return 'LINESTRING(' + str(answer) + ')'

if __name__ == '__main__':
    app.run()
