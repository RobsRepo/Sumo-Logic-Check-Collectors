import sys
import ConfigParser
from sumologic import SumoLogic
from slackclient import SlackClient

def main():
	msg = pingCollectors()
	postToSlack(msg)
	print msg

# Pings the collectors and lists out which collectors are offline
def pingCollectors():
	config = ConfigParser.RawConfigParser()
	config.readfp(open('config.properties'))

    # SumoLogic Access ID and Access Key
	accessID = config.get("Config", "accessID")
	accessKey = config.get("Config", "accessKey")

	sumo = SumoLogic(accessID, accessKey)
	theBlob = sumo.collectors()
	outputMsg = "The following collectors are offline:\n"
	empty = True
	for stuff in theBlob:
		collectorName = ''
		collectorAlive = False
		for attribute, value in stuff.iteritems():
			if attribute == 'name' : 
				collectorName = value
			if attribute == 'alive' :
				collectorAlive = value
		if collectorAlive == False :
			empty = False
			outputMsg += collectorName + "\n"
	if empty:
		return ''
	else:
		return outputMsg

# Post the message to a Slack channel
def postToSlack(msg):	
	config = ConfigParser.RawConfigParser()
	config.readfp(open('config.properties'))

	# Retrieves the Slack channel configuration
	try:
		token = config.get("Slack", "token")
		channel = config.get("Slack", "channel")

		if(token and channel and msg):
			sc = SlackClient(token)
			sc.api_call(
			    "chat.postMessage", channel=channel, text=msg,
			    username='SumoLogic Collector Heartbeat', icon_emoji=':robot_face:'
			)
	except ConfigParser.NoOptionError as e:
		print "Not Slack configuration to post to"

main()
