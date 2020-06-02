import paho.mqtt.client as mqtt
import json
from Habs import Habs

hab1 = Habs('Hab1')
hab2 = Habs('Hab2')
hab3 = Habs('Hab3')
hab4 = Habs('Hab4')


hab_list = [hab1, hab2, hab3, hab4]

THINGSBOARD_HOST = 'ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com'
ACCESS_TOKEN = 'CSndajbEyIhDajkjc8OM'

LOCAL_HOST = '192.168.1.125'
LOCAL_USER = 'karma3'
LOCAL_PW = '2016Karma3'



hab2_state = {"Hab2":{"Attribute1":True }}
hab3_state = {"Hab2":{"Attribute1":True }}
# This function is used to strip the hab number from hab name string. e.g. 'hab1' will return 0, so we can call hab_list[0]. 
def _get_hab_index(hab_name):
    return int(hab_name[-1]) - 1



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/gateway/rpc')
    # Sending current GPIO status
    data_out = json.dumps(hab2_state)
    client.publish('v1/gateway/attributes', json.dumps(hab2_state), 1)
    
    client.publish('v1/gateway/connect', json.dumps({"device":"Hab2"}), 1)
    client.publish('v1/gateway/connect', json.dumps({"device":"Hab3"}), 1)
    

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
    hab_index = _get_hab_index(device)

    # For the at temp control knob on the TB_dashboard for all 4 habs. 
    if data['method'] == 'setFanSpeedAtTemp' : 
        # Parse the message. 
        fanSpeedAtTemp = float(data['params'])
        hab_list[hab_index]._set_fan_speed_at_temp(data,device)
        client_local.publish(hab_list[hab_index]._set_fan_speed_at_temp(data,device), fanSpeedAtTemp, retain= True)

    elif data['method'] == "getFanSpeedAtTemp":
        # reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
        # temp = json.dumps(reply_msg) 
        tb_topic = hab_list[ _get_hab_index(device)]._upload_speed_at_temp(data, device)
        print(tb_topic)
        client.publish('v1/gateway/rpc', tb_topic)
    
    #For the temp low control knob on the 
    elif data['method'] == 'setFanSpeedLowTemp' : 
        # Parse the message. 
        fanSpeedLowTemp = float(data['params'])
        temp = hab_list[hab_index]._set_fan_speed_low_temp(data,device)
        client_local.publish(temp, fanSpeedLowTemp, retain= True)
    elif data['method'] == "getFanSpeedLowTemp":
        # reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
        # temp = json.dumps(reply_msg) 
        tb_topic = hab_list[ _get_hab_index(device)]._upload_speed_low_temp(data, device)
        print(tb_topic)
        client.publish('v1/gateway/rpc', tb_topic)  
    
    # For fan speed temp high knob. 
    elif data['method'] == 'setFanSpeedHighTemp' : 
        # Parse the message. 
        fanSpeedHighTemp = float(data['params'])
        local_topic = hab_list[hab_index]._set_fan_speed_high_temp(data,device)
        client_local.publish(local_topic, fanSpeedHighTemp, retain= True)
    elif data['method'] == "getFanSpeedHighTemp":
        # reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
        # temp = json.dumps(reply_msg) 
        tb_topic = hab_list[ _get_hab_index(device)]._upload_speed_high_temp(data, device)
        print(tb_topic)
        client.publish('v1/gateway/rpc', tb_topic)  

     # For extraction fan target temperature setting knob
    elif data['method'] == 'setSetTemp' : 
        # Parse the message. 
        fanSpeedHighTemp = float(data['params'])
        for x in hab_list[hab_index]._set_set_temp(data,device):
            client_local.publish(x, fanSpeedHighTemp, retain= True)
    elif data['method'] == "getSetTemp":
        # reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
        # temp = json.dumps(reply_msg) 
        tb_topic = hab_list[ _get_hab_index(device)]._upload_set_temp(data, device)
        print(tb_topic)
        client.publish('v1/gateway/rpc', tb_topic)  

    elif data['method'] == 'setAutoMode' : 
        # Parse the message.
        autoMode = 0  
        if data['params']: autoMode = 1 
        x = hab_list[hab_index]._set_auto_mode(data,device)


        print(x)
        print(autoMode)
        client_local.publish(x, autoMode, retain= True)
    elif data['method'] == "getAutoMode":
        # reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
        # temp = json.dumps(reply_msg) 
        tb_topic = hab_list[ _get_hab_index(device)]._upload_auto_mode(data, device)
        print(tb_topic)
        client.publish('v1/gateway/rpc', tb_topic)  

    elif data['method'] == 'setManualFanSpeed' : 
        # Parse the message.
        manualFanSpeed = float(data['params'])
        x = hab_list[hab_index]._set_manual_fan_speed(data,device)

        # Check if automode is 0. Only change the fan speed if the hab fan is in manual mode. 
        if hab_list[hab_index].automode ==0:
            client_local.publish(x, manualFanSpeed, retain= True)
    elif data['method'] == "getManualFanSpeed":
        # reply_msg = {'device': device, 'id': data['id'], 'data':  float(hab2.fanSpeedAtTemp)}
        # temp = json.dumps(reply_msg) 
        tb_topic = hab_list[ _get_hab_index(device)]._upload_manual_fan_speed(data, device)
        print(tb_topic)
        client.publish('v1/gateway/rpc', tb_topic)      
    return

            

def on_connect_local(client_local, userdata, rc, *extra_params):
    print('Connected to local Pi MQTT with result code ' + str(rc))
    client_local.subscribe('Habs/+/ExtractionFan/+')
    return

def on_message_local(client_local, userdata, msg):

    topic_list = msg.topic.split('/')
    device = topic_list[1]
    hab_index = _get_hab_index(device)


    # if msg.topic == 'Habs/Hab2/ExtractionFan/FanSpeedAtTemperature':
    #     hab2.fanSpeedAtTemp = msg.payload 

    # Check if the 3rd level of the topic is ExtractionFan. 
    if topic_list[2] == 'ExtractionFan':
        if topic_list[3] == 'FanSpeedAtTemperature':
            hab_list[hab_index].fanSpeedAtTemp = msg.payload
        elif topic_list[3] == 'FanSpeedTemperatureLow':
            hab_list[hab_index].fanSpeedTempLow = msg.payload
        elif topic_list[3] == 'FanSpeedTemperatureHigh':
            hab_list[hab_index].fanSpeedTempHigh = msg.payload
        elif topic_list[3] == 'FanTemperatureSetPoint':
            hab_list[hab_index].tempSetPoint = msg.payload
        elif topic_list[3] == 'TemperatureSetPoint':
            hab_list[hab_index].tempSetPoint = msg.payload
        elif topic_list[3] == 'AutomaticMode':
            hab_list[hab_index].automode = int(msg.payload)
        elif topic_list[3] == 'Speed':
            hab_list[hab_index].manualFanSpeed = int(msg.payload)
            
           



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
