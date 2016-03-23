# Offline Sumo Logic Collectors

I've had a couple of clients ask for a way to be notified whenever their Sumo Logic collectors went offline. This script handles this. Specifically, these Python script does the following:

1. Makes a REST call to the Sumo Logic Collector API
2. Prints out a list of collectors that are offline.
3. Posts the list of offline collectors to a Slack channel

## Prerequisites
-	You will need Python 2.7
-	You will need the SlackClient Python package. Run "pip install SlackClient"
- A Slack account or access to a Slack account.

##Build:
1. Add the Sumo Logic Access ID and Access Key to the config.properties. You can create Sumo Logic keys by navigating to Manage --> Collection --> Access Keys.
2. Add the Slack token and Slack channel. To create the token follow the instructions here: https://api.slack.com/web#authentication
3. Give executable permissions to the collectorPing.sh. Run "chmod +x collectorPing.sh"

##Run
./collectorPing.sh
