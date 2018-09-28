import network
import ujson
import time
import hcid as HCID

web_dir = "www/"
wifi_config_file = "wifi.json"
sta = network.WLAN(network.STA_IF)

def readConfig(filename):
  try:
    f = open(filename, 'r')
    json = f.read()
    f.close()
  except OSError:
    print("Unable to find " + filename)
    raise
  
  config_data = ujson.loads(json)
  return config_data

def connect(ssid, password):
    if password == "SECRETPASSWORD":
      password = HCID.getBadgeWifiPassword()
    sta.active(True)
    if sta.isconnected():
        return None
    print('Trying to connect to %s' % ssid)
    sta.connect(ssid, password)
    for retry in range(200):
        connected = sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', sta.ifconfig())
    else:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print('\nFailed. Not Connected to: ' + ssid)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        sta.active(False)
    return connected
    
def is_wifi_connected():
   return sta.isconnected()
   
def get_device_ip():
   return sta.ifconfig()[0]
   
def get_custom_message():
  config = readConfig(wifi_config_file)
  return config["custom_message"]
  
def get_ssid():
  config = readConfig(wifi_config_file)
  return config["ssid"]

def start_wifi():
  print("---------- Starting Wifi ----------")
  
  try:
    print("Loading config file: " + wifi_config_file)
    config = readConfig(wifi_config_file)
    print("SSID: " + config["ssid"])
    print("Password: " + config["password"])
    connect(config["ssid"], config["password"])
  except OSError:
    pass





