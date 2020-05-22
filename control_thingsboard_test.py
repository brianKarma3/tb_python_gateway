import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'ec2-13-55-186-158.ap-southeast-2.compute.amazonaws.com'
ACCESS_TOKEN = 'A1_TEST_TOKEN'

# We assume that all GPIOs are LOW
gpio_state = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
              31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}

switch_status = True
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    client.publish('v1/devices/me/attributes', switch_status, 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print ('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getValue':
        # Reply with GPIO status
        client.publish(msg.topic.replace('request', 'response'), switch_status, 1)
    elif data['method'] == 'setValue':
        # Update GPIO status and reply
        switch_status = data['params']
        client.publish(msg.topic.replace('request', 'response'), switch_status, 1)
        client.publish('v1/devices/me/attributes', switch_status, 1)


def get_gpio_status():
    # Encode GPIOs state to json
    return json.dumps(gpio_state)


def set_gpio_status(pin, status):
    # Output GPIOs state
    # GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
    # Update GPIOs state
    gpio_state[pin] = status


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

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()