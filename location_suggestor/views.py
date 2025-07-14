# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import json
import math
import firebase_admin
from firebase_admin import credentials
import os
from firebase_admin import db
from django.views.decorators.csrf import csrf_exempt

raw_env = os.getenv("FIREBASE_SECRET")
service_account_info = json.loads(raw_env.encode('utf-8').decode('unicode_escape'))

 # service_account_info = json.loads(raw_env)

if not firebase_admin._apps:
  cred = credentials.Certificate(service_account_info)
  firebase_admin.initialize_app(cred, {
      'databaseURL': 'https://yaari-dba-default-rtdb.firebaseio.com/'
  })



ref = db.reference('/')
data = (ref.get())

@csrf_exempt
def suggest(req):
  if req.method == "GET":
    print(type(data))
    lat = req.GET.get('lat')
    lon = req.GET.get('lon')
    curr_lat = float(lat)
    curr_lon = float(lon)

    def haversine_formula(lat1, lon1, lat2, lon2):
      R = 6371.0
      phi1 = math.radians(lat1)
      phi2 = math.radians(lat2)
      delta_phi = math.radians(lat2 - lat1)
      delta_lambda = math.radians(lon2 - lon1)
      a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
      distance = R * c
      return distance

    dispatch_payload = []
    for coord in data:
      dist = haversine_formula(curr_lat, curr_lon, coord['lat'], coord['lon'])
      if(dist <= 7):
        coord.update({'distance': f"{round(dist, 1)} km", 'measure': dist})
        dispatch_payload.append(coord)
      dispatch_payload = sorted(dispatch_payload, key = lambda a: a['measure'])

  return JsonResponse({"suggest": dispatch_payload})
