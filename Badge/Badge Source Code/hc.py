import urequests
import ujson

webserver = "www.hackerschallenge.org"
hcid = HCID.getHCID()

sc_headers = {
  "User-Agent": "SCBadge-v1.0 " + hcid
}

def request(id):
  try: 
    r = urequests.get('https://' + webserver + '/scoreapi/keyscore/' + id, headers = sc_headers)
    response = r.text
    r.close()
    return response
  except:
    print("request to the gameserver had. . . an issue.")
    pass
  return "Error"

def get_score(id):
  response = request(id)
    
  if (response=="There was an error." or response == "Error") :
    return "Error"
  else:
    try:
      json = ujson.loads(response)
      return json["total_score"]
    except:
      print("unable to load response as a json: " + response)
      return "Error"

def does_hcid_exist(id):
  response = hc.request(id)
  if response=="There was an error.":
    return false
  else:
    return true



