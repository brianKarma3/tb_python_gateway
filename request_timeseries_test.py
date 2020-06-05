import requests
import datetime
import json

end_time_stamp = datetime.datetime.timestamp( datetime.datetime.now())
start_time_stamp = datetime.datetime.timestamp( datetime.datetime.now() + datetime.timedelta(hours=-1))


# print(end_time_stamp)
# print(start_time_stamp)

#Firstly we need to get upto date token from the thingsboard server. 
url =  'http://ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com:8080/api/auth/login'
header =  {'Content-Type': 'application/json' ,'Accept': 'application/json' }
data ='{"username":"tenant@thingsboard.org", "password":"tenant"}'


r = requests.post(url, data= data, headers = header)
tokens =r.json()


device_entity = '357871a0-94ec-11ea-9d7f-f7ee85f9bf5b' 
# Secondly we can get all the keys from a selected device given the device entity. 
# url = 'http://ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com:8080/api/plugins/telemetry/DEVICE/{0}/keys/timeseries'.format(device_entity)

# headers = {'content-type': 'application/json', "X-Authorization": "Bearer " + tokens['token']} 
# r = requests.get(url, headers=headers)


# Thirdly, we will need to user api to query the thingsboard library for the telemetery data of this device 
url = 'http://ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com:8080/api/plugins/telemetry/DEVICE/{0}/values/timeseries?keys=Humidity,Temperature&startTs={1}&endTs={2}&interval=600000&agg=AVG&limit=1200'.format(device_entity, int(start_time_stamp*1000), int(end_time_stamp*1000))
# url = 'http://ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com:8080/api/plugins/telemetry/DEVICE/{0}/values/timeseries?keys=Humidity,Temperature'.format(device_entity)


headers = {'content-type': 'application/json', "X-Authorization": "Bearer " + tokens['token']} 
r = requests.get(url, headers=headers)

print(int(end_time_stamp*1000))
print(int(start_time_stamp*1000))
print(url)

print(r.text ) 


