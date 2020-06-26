# tb_python_gateway

This project is for the Thingsboard IOT system of Karma3's fly farming project. 

Device_control_gateway.py is the device control gateway of Thingsboard. 
  this file is run at boot up, which is configured in /etc/systemd/system/mqttclient.service.  See the following link for configuration details. 
  https://raspberrypi.stackexchange.com/questions/76804/trying-to-autorun-paho-mqtt-client-script-on-boot-up/76809#76809?newreg=c97ad870fe08477cba60b94872581772
  

Thingsboard IOT Gateway is used for the uplink gateway for the service. 
1. Add the custom_mqtt_uplink_converter_habs.py to /var/lib/thingsboard_gateway
2. Update the thingsboard configuration file in /etc/thingsboard-gateway/config (tb_gateway.yaml and mqtt.json)

