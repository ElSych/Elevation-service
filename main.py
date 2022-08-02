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


@app.route('/main/<somegeometry>(<coords>)')
def GEOMETRY(somegeometry, coords):
    coords = coords.replace(',', '')
    coordsspl = coords.split()
    lengh = len(coordsspl)
    if (somegeometry.upper() == 'POINT'):
        return ('Thats a POINT(' + str(coordsspl[0]) + ' ' + str(coordsspl[1]) + ' ' + ')' + ' elevation is ' + str(get_elevation(float(coordsspl[0]), float(coordsspl[1]))))
    elif (somegeometry.upper() == 'LINESTRING'):
        i = 0
        answer = ''
        while i < (lengh - 1):
            answer = answer + str(coordsspl[i]) + ' ' + str(coordsspl[i + 1]) + ' ' + str(get_elevation(float(coordsspl[i]), float(coordsspl[i + 1]))) + ',' + ' '
            i += 2
            answer = answer[:-2]
        return 'Thats a LINESTRING(' + str(answer) + ')'

if __name__ == '__main__':
    app.run()
