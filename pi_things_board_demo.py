import paho.mqtt.client as mqtt
import json
from Habs import Habs

hab1 = Habs('Hab1')
hab2 = Habs('Hab2')

THINGSBOARD_HOST = 'ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com'
ACCESS_TOKEN = 'CSndajbEyIhDajkjc8OM'

LOCAL_HOST = '192.168.1.125'
LOCAL_USER = 'karma3'
LOCAL_PW = '2016Karma3'



hab2_state = {"Hab2":{"Attribute1":True }}
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/gateway/rpc')
    # Sending current GPIO status
    data_out = json.dumps(hab2_state)
    client.publish('v1/gateway/attributes', json.dumps(hab2_state), 1)
    
    client.publish('v1/gateway/connect', json.dumps({"device":"Hab2"}), 1)



    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print ('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)['data']
    device = json.loads(msg.payload)['device']
    # Check request method
    # if data['method'] == 'getAuto_status':
    #     # Here we need to 
    #     client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    # elif data['method'] == 'setGpioStatus':
    #     # Update GPIO status and reply
    #     set_gpio_status(data['params']['pin'], data['params']['enabled'])
    #     client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    #     client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
    

    if device == 'Hab2':
        if data['method'] == 'setFanSpeedAtTemp' : 
            # Parse the message. 
            fanSpeedAtTemp = float(data['params'])
            client_local.publish('Habs/Hab2/ExtractionFan/FanSpeedAtTemperature', fanSpeedAtTemp, retain= True)
        elif data['method'] == "getFanSpeedAtTemp":
            reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
            temp = json.dumps(reply_msg) 
            print("reply message: " + temp)
            client.publish('v1/gateway/rpc', json.dumps(reply_msg))
            

    
    return

            

def on_connect_local(client_local, userdata, rc, *extra_params):
    print('Connected to local Pi MQTT with result code ' + str(rc))
    client_local.subscribe('Habs/Hab2/ExtractionFan/+')
    return

def on_message_local(client_local, userdata, msg):

    if msg.topic == 'Habs/Hab2/ExtractionFan/FanSpeedAtTemperature':
        hab2.fanSpeedAtTemp = msg.payload 

    return




# Using board GPIO layout
# GPIO.setmode(GPIO.BOARD)
# for pin in gpio_state:
#     # Set output mode for all GPIO pins
#     GPIO.setup(pin, GPIO.OUT)

client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)



client_local = mqtt.Client()
client_local.on_connect = on_connect_local
client_local.on_message = on_message_local
client_local.username_pw_set(LOCAL_USER, LOCAL_PW)

client_local.connect(LOCAL_HOST, 1883, 60); 

client.loop_start()
client_local.loop_start()


while True:
    a = 10
