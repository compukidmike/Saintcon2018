import network
import ubinascii
import sha256

salt = "compukidmike & bashninja"

def getMac():
  mac = ubinascii.hexlify(network.WLAN().config('mac')).decode()
  return mac

def hashMac():
  mac = getMac()
  hashObject = sha256.sha256(mac + salt)
  hash = hashObject.hexdigest()
  return hash

def getHCID():
  hash = hashMac()
  return hash[:10]

def getPassword():
  hash = hashMac()
  return hash[-8:]

def getBadgeWifiPassword():
  return "8UU96BNsxh"

def flag():
  return "flag{compiled_code_is_still_Accessible}"