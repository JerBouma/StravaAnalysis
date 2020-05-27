from stravalib.client import Client
import requests

client_id = 36132
client = Client()
login_details = {"email": "jer.bouma@gmail.com", "password": "u@b9Fon#CBgnl@Y50O"}
authorize_url = client.authorization_url(client_id=client_id,
                                         redirect_uri='http://localhost/authorized')

url = requests.get(authorize_url)

data = requests.get('https://www.strava.com/login')