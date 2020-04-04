from flask import Flask, render_template, request
import requests
import time
import json

app = Flask(__name__)

lokey_api_url = "http://lo-key.io/API/"

def timed_requests(r_url, r_time):
    count = 0
    max_retry = 6
    while count < max_retry:
        try:
            r = requests.get(url=r_url, timeout=r_time)
            print("status: ", r)
            print("content", json.loads(r.text)['Data'])
            print()
            if json.loads(r.text)['Data'] == None:
                print("EMPTY, RETRYING", count + 1)
                raise Exception("EMPTY RESPONSE FROM LO-KEY API")
            else:
                return r
        except Exception as e:
            time.sleep(2**count)
            count += 1
            if count >= max_retry:
                raise e

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

    slk = timed_requests(slk_address, 75).json()['Data']
    # print slk
    lk = timed_requests(lk_address, 75).json()['Data']
    # print lk
    klk = timed_requests(klk_address, 75).json()['Data']
    # print klk

    return render_template('home.html', results=[], bool1='None', bool2='Block', target=artist, slk_results=slk, lk_results=lk, klk_results=klk)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8888, debug='ON')
