#!/usr/bin/python2.7
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import re
import time
import requests
import json
import paho.mqtt.client as mqtt

from pygrovepi import grovepi
from pygrovepi import grovepilib
from urlparse import urlparse, parse_qs

# define some variables to ease configuration.
# IPADDR = "http://192.168.1.102"
IPADDR = "http://ec2-54-85-42-249.compute-1.amazonaws.com"
PORT = "8086"
DATABASE = 'sensors'

topic_counter ="testubuntucore/counter"
topic_button="testubuntucore/button"
topic_command = "testubuntucore/command"
topic_result = "testubuntucore/result"

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 1883

payload = "None"
qos = "0"
retain = "False"

#Use this for MQTT servers needing authentication
username = "guest"
password = "guest"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected to ThingStudio sandbox with result code "+str(rc))
	# use this to subscribe to the counter feed for debug purposes to listen to your counter feed
	#   client.subscribe(topic_counter)
	# use this to subscribe to the command feed to receive commands
	client.subscribe(topic_command)
	# use this to subscribe to the result feed for debug purposes to listen to your result feed
#    client.subscribe(topic_result)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print("Received the message : "+str(msg.payload)+" on topic : "+str(msg.topic))
#strip the incoming command from its json - TODO
	command = str(msg.payload)
	print ("Received command: " + command )
	# Write code to test what command we have received and respond accordingly right now testing on non stripped json
	if command == '\"on\"':
		message = "{\"Message\":\"I received the ON command\"}"
		# client.publish(topic_result, message)
		grovepilib.led_write_blue(1)
		print("blue light if ON")
	elif command == '\"off\"':
		message = "{\"Message\":\"I received the OFF command\"}"
		# client.publish(topic_result, message)
		grovepilib.led_write_blue(0)
		print("blue light if OFF!")
	else:
		message = "{\"Message\":\"I received an unkown command\"}"
		client.publish(topic_result, message)
		print("Sent unknown")

def on_publish(mosq, obj, mid):
	print("Publishing successful")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.will_set(topic_command, payload=None, qos=0, retain=False)
client.username_pw_set(username,password)
#client.connect("mqtt.thingstud.io",1883,60)
client.connect(DEFAULT_HOST, DEFAULT_PORT)

# The following is a forever loop checking the status of the sensors
while client.loop() == 0:
	temp = grovepilib.sensor_read_temp()
	print 'temperature: ' + str(temp)
	
	humidity = grovepilib.sensor_read_humidity()
	print 'humidity: ' + str(humidity)
	
	# once the data is collected post them
	v = [{'name': 'data', 'columns': ['temp', 'humi'], 'points': [[temp, humidity]]}]
	url = IPADDR + ":" + PORT +"/db/%s/series?u=grafana&p=grafana"
	# print url % DATABASE
	
#	r = requests.post( url % DATABASE, data=json.dumps(v))
	
#	if r.status_code != 200:
#		print 'Failed to add point to influxdb -- aborting.'
#		sys.exit(1)	
#	else:
#		print "Successfully sent data!"
		
	# Use MQTT protocol to broadcast the temperature here
	message = "\""+str(temp)+"\""
	print("Sending on topic: "+str(topic_counter)+" the message :"+str(message))
	# client.publish(topic_counter, message)

	# Read in the button input
	button_input = grovepilib.button_read()
	print 'button input: ' + str(button_input)
	# client.publish(topic_button, str(button_input))

        print("Going to publish data info")
        data = { 'button': str(button_input), \
                 'Humidity':  str(humidity), \
                 'temp':  str(temp)
              }
        
        s = json.dumps(data)
        client.publish("data",  s)
	
	# Read the light data
	# light = grovepilib.sensor_read_light()
	# print 'light: ' + str(light)	
	
	# Turn on the blue light
	# grovepilib.led_write_blue(1)
	
	time.sleep(1)  # sleep for 3 seconds before next call
