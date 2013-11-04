#####################################
# Checking PNR status App For Jasmine
# Made by -         Harsh Gupta
#                Rishikesh Ghewari
#                Shagun Rawat                
#                Deepanshu Goyal
#####################################

import json
import urllib2
import re
import string
import math
import random

####################
# Public Functions #
####################

#Identifies the app in a unique id.
app_id = "TrainPNR"

#In any lib_* file, "check" function checks if the post/news item is of the app's corresponding post
def check(post):
#matchObj = re.search(r"^(?:(pnr|PNR))\s*[\?!]*\s*",post['message'])
        matchObj = re.search(r"^[a-zA-Z,:;' .!?/<>=]*[p|P][n|N][r|R][a-zA-Z,:;' .!?/<>=]*[0-9]{10}[[a-zA-Z,:;' .!?/<>=]*|[ ][0-9a-zA-Z,:;' .!?/<>=]*]$",post['message'])
        if matchObj:
                return True
        return False

#After confirming that the message/status corresponds to the current app using the "check" function above, "execute" function
#is called to do the actual work

def execute(post):
        pnr = post['message'];
        plist = pnr.split()
        i = ""
        for p in plist:
                try:
                        p = ''.join(x for x in p if x.isdigit())
                        if(len(p)==10):
                                int(p)
                                i = p
                                break
                        else:
                                 continue
                except:
                        continue

        if i == "":
                return "pnr must be a 10 digit integer"
        else:
                try:
		            query = "http://pnrapi.alagu.net/api/v1.0/pnr/" + i
		            req = urllib2.Request(query)
		            resp = urllib2.urlopen(req)
		            text = json.load(resp)
		            output = "PNR : "+i +'\n'
		            output += "Status : " + text['status'] + '\n'
		            if text['status'] == 'INVALID':
		                    data = text["data"]
		                    for key in data:
		                            output += key + " : " + str(data[key]) + '\n'
		            else:
		                    data = text["data"]
		                    output += "Train Name : "+data['train_name'] + '\n'
		                    output += "Train Number : "+data['train_number'] + '\n'
		                    output += "From - \n\t\tName : "+data['from']['name'] +" \n\t\tcode : "+data['from']['code'] + '\n'
		                    output += "To - \n\t\tName : "+data['to']['name'] +"\n\t\tcode : "+data['to']['code'] + '\n'
		                    output += "Class : "+data['class'] + '\n'
		                    output += "Date : "+data['travel_date']['date'] + '\n'
		                    output += "Passenger : "
		                    for k in data['passenger']:
		                            output += "\n\tSeat No :"+k['seat_number']
		                    output += "\nChart Prepared : "+str(data['chart_prepared']) + '\n'
                except:
                	output="Not a valid PNR.\n"
        return output
