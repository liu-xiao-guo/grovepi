#!/usr/bin/env python2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
import time
#import grovepi

from pygrovepi import grovepi
from pygrovepi import grovepilib
from urlparse import urlparse, parse_qs

PORT_NUMBER = 9000

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		#If this is the root path, show the "Hello, world", indicating the server is up
		if (self.path == "/") :
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# Send the html message
			self.wfile.write("Hello World !")
			return
		
		#This is to return the temperature of the sensor
		elif (None != re.search('/api/v1/temp/', self.path)):
			print "Going to return the temperature"
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# temp = grovepi.temp(sensor,'1.2')
                        d = grovepilib.sensor_read_temp()
                        print 'temperature: ' + str(d)
			# Send the html message
			self.wfile.write(str(d))			
			return

		#This is to return the temperature of the sensor
		elif (None != re.search('/api/v1/humi/', self.path)):
			print "Going to return the humidity"
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
                        d = grovepilib.sensor_read_humidity()
                        print 'humidity: ' + str(d)
			# Send the html message
			self.wfile.write(str(d))			
			return

		#This is to control the green light
		elif (None != re.search('/api/v1/green/', self.path)):
			value = self.path[-1:]
			print "The last digit is: ", value
	
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			retry = grovepilib.led_write_green(int(value))
			# Send the html message
			self.wfile.write(str(retry))						
			return

		#This is to control the red light
		elif (None != re.search('/api/v1/red/', self.path)):
			value = self.path[-1:]
			print "The last digit is: ", value
	
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			retry = grovepilib.led_write_red(int(value))
			# Send the html message
			self.wfile.write(str(retry))						
			return

		#This is to control the buzzer
                elif (None != re.search('/api/v1/buzzer/', self.path)):
			print "path: ", self.path
			params = parse_qs(urlparse(self.path).query)
			
			for key in params:
			        print key, ' ----> ', params[key]	
				
			print params['duration']
			print params['duration'][0]

                        value = params['duration'][0]
                        grovepilib.buzzer_write(float(value))
			
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# Send the html message
			self.wfile.write( params['duration'][0])
                        return		

try:
	#Configure the pins for input/ouput
	print "Going to configure the pins"
	grovepilib.pin_config()
	
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
