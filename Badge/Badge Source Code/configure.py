import network
from microWebSrv import MicroWebSrv
import ujson
import wifi_config
import time
import hcid

web_dir = "www/"
wifi_config_file = "wifi.json"
default_ssid = "BadgeHerd"
default_password = "SECRETPASSWORD"
default_custom_message = ""
hcid = hcid.getHCID()

def letswait(seconds):
  count = 0
  while count <= seconds:
    time.sleep(1) # this sleep sucks
    print(".", end='')
    count = count + 1

def _acceptWebSocketCallback(webSocket, httpClient) :
 print("WS ACCEPT")
 webSocket.RecvTextCallback   = _recvTextCallback
 webSocket.RecvBinaryCallback = _recvBinaryCallback
 webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
 print("WS RECV TEXT : %s" % msg)
 webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
 print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
 print("WS CLOSED")

# ----------------------------------------------------------------------------

@MicroWebSrv.route('/', 'GET')
def _httpHandlerFinish(httpClient, httpResponse) :
  
  try:
    print("1")
    config = wifi_config.readConfig(wifi_config_file)
    ssid = config["ssid"]
    password = config["password"]
    custom_message = config["custom_message"]
  except OSError:
    print("2")
    ssid = default_ssid
    password = default_password
    custom_message = default_custom_message
    
  print("3")
  f = open( web_dir + 'index_1.html', 'r')
  page = str(f.read())
  f.close()
  print("4")
  page = page + """<table style="margin-left: auto; margin-right: auto;"><tbody><tr><td>SSIDs:</td><td><input name="ssid" type="text" value="%s" /></td></tr><tr><td>Wifi Password:</td><td><input name="password" type="password" value="%s" /></td></tr><tr><td></td><td><input type="button" class="button" value="Reset Wifi Settings" Onclick="window.location.href='/reset'"></td></tr><tr><td><h1 style="text-align: center;"><span style="color: #f90;">Other Settings</span></h1></td></tr><tr><td>Hacker's Challenge ID:</td><td>%s</td></tr><tr><td>Custom Message:</td><td><input name="custom_message" maxlength="250" type="text" value="%s" /></td></tr></tbody></table>""" % ( MicroWebSrv.HTMLEscape(ssid), MicroWebSrv.HTMLEscape(password), MicroWebSrv.HTMLEscape(hcid), MicroWebSrv.HTMLEscape(custom_message) )f = open( web_dir + 'index_2.html', 'r')
  page = page + str(f.read())
  f.close()
  print("5")

  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         = page )
  print("User hit the Main Page.")
  
@MicroWebSrv.route('/reset', 'GET')
def _httpHandlerFinish(httpClient, httpResponse) :
  f = open( web_dir + 'config_1.html', 'r')
  content = str(f.read())
  f.close()
  
  content += str("Reset Wifi Settings to Default")
  
  f = open( web_dir + 'config_2.html', 'r')
  content += str(f.read())
  f.close()

  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         = content )
  print("User hit the RESET Page.")
  try:
    config = wifi_config.readConfig(wifi_config_file)
    custom_message = config["custom_message"]
  except OSError:
    custom_message = default_custom_message
  config_data = {'ssid': MicroWebSrv.HTMLEscape(default_ssid), 'password': MicroWebSrv.HTMLEscape(default_password), 'custom_message': MicroWebSrv.HTMLEscape(custom_message)}
  
  f = open(wifi_config_file, "w")
  json = ujson.dumps(config_data)
  f.write(json)
  f.close()

@MicroWebSrv.route('/configure', 'POST')
def _httpHandlerConfigurePost(httpClient, httpResponse) :
  formData  = httpClient.ReadRequestPostedFormData()
  ssid  = formData["ssid"]
  password  = formData["password"]
  custom_message = formData["custom_message"]
  f = open( web_dir + 'config_1.html', 'r')
  content = str(f.read())
  f.close()
  
  config_data = {'ssid': MicroWebSrv.HTMLEscape(ssid), 'password': MicroWebSrv.HTMLEscape(password), 'custom_message': MicroWebSrv.HTMLEscape(custom_message)}

  content += str(config_data)
  
  f = open( web_dir + 'config_2.html', 'r')
  content += str(f.read())
  f.close()
  
  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         =  content)

  f = open(wifi_config_file, "w")
  json = ujson.dumps(config_data)
  f.write(json)
  f.close()
  print("User POSTED settings to /configure")
  print("Wrote the following to " + wifi_config_file + "\n" + json)

@MicroWebSrv.route('/finish', 'GET')
def _httpHandlerFinish(httpClient, httpResponse) :
  file = open( web_dir + 'end.html', 'r')
  page = str(file.read())
  file.close()
  print("1")
  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         = page )
  print("User hit the Finished button. Closing down WebServer & AP.")
  stop_ap()
  stop_webserver()

def start_ap(essid_name, ap_password, authmode_setting):
  ap.active(True)
  ap.config(essid=essid_name, password=ap_password, authmode=authmode_setting)
  print("Badge SSID: '{:s}'".format(essid_name)) # It would be good to show this on the badge screen.
  print("Badge Wifi Password: {:s}".format(ap_password))

def stop_ap():
  print("Stopping AP", end='')
  letswait(5)
  print()
  ap.active(False)
  print("--- Stopped AP ---")
  
def stop_webserver():
  srv.Stop()
  print("--- Stopped WebServer ---")
  
def start_wifi_config(essid_name, ap_password, authmode_setting):
  print()
  print("====================== Start Wifi Config ======================")
  print()
  letswait(3)
  start_ap(essid_name, ap_password, authmode_setting)
  # Start WebServer
  ip = ap.ifconfig()[0]
  print("Web Server: Listening http://{}:80/".format(ip))  # It would be good to show this on the badge screen.
  srv.Start(threaded=False);

# ----------------------------------------------------------------------------

def main():
  start_wifi_config("Saintcon Badge")
  
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
ip = "No IP Set"

# Setup Webserver (does not start it)
srv = MicroWebSrv(webPath=web_dir)
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded = False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback











