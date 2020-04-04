from flask import Flask, render_template, request
from json import load, dumps
import requests

app = Flask(__name__)

lokey_api_url = "http://lo-key.io/API/"

@app.route('/')
def home():
    return render_template('home.html', bool1='None', bool2='None')

@app.route('/search', methods=['GET','POST'])
def search():
    text = str(request.form.get('text'))
    search_address = lokey_api_url + 'SearchArtist?SearchQuery=' + text
    r = requests.get(url=search_address)
    data = r.json()['Data']
    if not data:
        data = {}
    return render_template('home.html',results=data, bool1='Block', bool2='None')

@app.route('/artist_details/<string:artist>', methods=['GET','POST'])
def details(artist):
    details_address = lokey_api_url + 'ArtistDetails?ArtistName=' + artist
    artist_data = requests.get(url=details_address).json()['Data']
    similar_address= lokey_api_url + 'FindSimilarArtist?ArtistId=' + str(artist_data['ArtistId'])

    slk_address = similar_address + '&MaxFollowers=' + str(artist_data['SLKFol']) + '&MaxPopularity=' + str(artist_data['SLKPop']) + '&MinFollowers=' + str(artist_data['MinKFol']) + '&MinPopularity=' + str(artist_data['MinKPop'])
    lk_address = similar_address + '&MaxFollowers=' + str(artist_data['LKFol']) + '&MaxPopularity=' + str(artist_data['LKPop']) + '&MinFollowers=' + str(artist_data['SLKFol']) + '&MinPopularity=' + str(artist_data['SLKPop'])
    klk_address = similar_address + '&MaxFollowers=' + str(artist_data['KLKFol']) + '&MaxPopularity=' + str(artist_data['KLKPop']) + '&MinFollowers=' + str(artist_data['LKFol']) + '&MinPopularity=' + str(artist_data['LKPop'])

    slk = requests.get(url=slk_address, timeout=25).json()['Data']
    # print slk
    lk = requests.get(url=lk_address, timeout=25).json()['Data']
    # print lk
    klk = requests.get(url=klk_address, timeout=25).json()['Data']
    # print klk

    return render_template('home.html', results=[], bool1='None', bool2='Block', target=artist, slk_results=slk, lk_results=lk, klk_results=klk)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8888)
