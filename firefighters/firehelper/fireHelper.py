from flask import Flask, render_template, request, url_for, redirect
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import googlemaps
import requests, json

app = Flask(__name__, template_folder=".")
GoogleMaps(app)
gmaps = googlemaps.Client(key='APIKEY')
jsonget = requests.get('http://127.0.0.1/')
data = json.loads(jsonget.content)

marks = []
fires = []
fires_n = 0
people_n = 0
datacity = []
posla = 0
poslo = 0
lan = 0
lon = 0
for i in data["path"]:
    marks.append({
	'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
	'lat': i[0],
	'lng': i[1],
	'infobox': "<b>Person phone?</b>"
        })
    people_n += 1

lan=data["path"][0][0]
lon=data["path"][0][1]

for i in data["fires"]:
    location = gmaps.reverse_geocode((i["coords"][0],i["coords"][1]))
    datacity.append(location[0]["formatted_address"])
    fires.append({
        'stroke_color': '#8B0000',
        'stroke_opacity': 1.0,
        'stroke_weight': 1,
        'fill_color': '#8B0000',
        'fill_opacity': 0.2,
        'center': {
            'lat': i["coords"][0],
            'lng': i["coords"][1]
        },
        'radius': i["radius"],
        'infobox': "fire area"
        })
    fires_n += 1
 

@app.route("/")
def mapview():
	map = Map(
	identifier="map",
	lat=lan,
	lng=lon,
	cluster=True,
        cluster_gridsize=70,
        cluster_imagepath="static/images/m",
        style="width:100%;height:100%",
	markers=marks,
	circles=fires,
	)
	return render_template('example.html', map=map, count=fires_n, countp=people_n, countpn=people_n, datacity=datacity)

@app.route("/set", methods=['POST'])
def set():
    name=request.form['list']
    global lon, lan
    lan=data["fires"][int(name)]["coords"][0]
    lon=data["fires"][int(name)]["coords"][1]
    return redirect(url_for('mapview'))

if __name__ == "__main__":
	app.run(debug=True)
