from getpass import getpass
import requests

def authenticate_ambra(username = None, password = None, url = 'https://access.ambrahealth.com/api/v3'):
      while username==None:
          username = input("Username: ")
      while password ==None:
          password = getpass("Password: ")
      res = requests.post(url=url+'/session/login',data={"login":username,"password":password})
      res = res.json()
      sid = res['sid']

      # FOR DUAL AUTHENTICATION
      if 'pin_required' in res.keys() and res['pin_required']:
          pin = input("get pin via "+res['pin_via']+": ")
          req = {"sid":sid,"pin":pin,"remember_device":1}
          res = requests.post(url=url+'/session/pin',data = req)
          res = res.json()

      if res['status']=="OK" and sid != None:
          print("login successful")
          return sid
      else:
          print("error please retry")
          return authenticate_ambra(url=url)