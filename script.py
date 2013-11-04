import requests
import json
import time
import json
import random
import train_pnr
from chatterbotapi import ChatterBotFactory, ChatterBotType

factory = ChatterBotFactory()

#TOKEN='Your Token Here'

def get_notifications(LASTTIME):


	query = ("SELECT created_time, post_id, actor_id, message FROM stream WHERE filter_key = 'others' AND source_id = me() AND created_time > "+str(LASTTIME)+" LIMIT 1")

	payload = {'q': query, 'access_token': TOKEN}

	r = requests.get('https://graph.facebook.com/fql', params=payload)

	result = json.loads(r.text)
	print result
	print "Size of result : ",len(result["data"])
	#print result["data"][0]
	if len(result["data"])>0:
		LASTTIME=result["data"][0]["created_time"]
	#print result
	return result['data'],LASTTIME

def commentLatest(wallposts,quotations):

	"""Comments thank you on all posts"""

	#TODO convert to batch request later

	for wallpost in wallposts:
		#print wallpost
		r = requests.get('https://graph.facebook.com/%s' % wallpost['actor_id'])
		url = 'https://graph.facebook.com/%s/comments' % wallpost['post_id']
		#print url
		user = json.loads(r.text)
		#print user['first_name']
		
		quoteCreator=random.choice(quotations.keys())
		quote=quotations[quoteCreator][0]
		
		
		if "pnr" in wallpost["message"].lower():
			message ="Your PNR status is as follows : "+ train_pnr.execute(wallpost)
			message+="\n\n"+quote+"\n\t\t--"+quoteCreator
		else:
			message = 'Thanks %s for the post :)' % user['first_name']
			message+="\n\n"+quote+"\n\t\t--"+quoteCreator
			message+="\n\nNitesh will reply you as soon as he reads this post.\n"
			#print message
		payload = {'access_token': TOKEN, 'message': message}
		s = requests.post(url, data=payload)
		#print s
		print "Comment done on post %s" % wallpost['post_id']

def getChatterPosts():
	query = ("SELECT actor_id,message,post_id FROM stream WHERE filter_key = 'others' AND source_id=me() AND strpos(message ,'botpost') >=0")

	payload = {'q': query, 'access_token': TOKEN}

	r = requests.get('https://graph.facebook.com/fql', params=payload)

	result = json.loads(r.text)
	#print result
	#print "Size of result : ",len(result["data"])
	#print result["data"][0]
	#if len(result["data"])>0:
	#	LASTTIME=result["data"][0]["created_time"]
	#print result
	return result['data']

def checkBotPosts(bot2session,botposts):
	for botpost in botposts:
		#SELECT text FROM comment WHERE post_id=
		
		query = ("SELECT fromid,text FROM comment WHERE post_id='"+str(botpost["post_id"])+"'")

		payload = {'q': query, 'access_token': TOKEN}

		r = requests.get('https://graph.facebook.com/fql', params=payload)

		result = json.loads(r.text)
		#print result
		if len(result["data"])==0:
			bot1Text=botpost["message"]
		else:
			lastComment=result["data"][len(result["data"])-1]
			if lastComment["fromid"]==botpost["actor_id"]:
				bot1Text=lastComment["text"]
			else:
				continue
		#print bot1Text
		#return
		
		bot2Comment=bot2session.think(bot1Text);
		
		#print wallpost
#		r = requests.get('https://graph.facebook.com/%s' % wallpost['actor_id'])
		url = 'https://graph.facebook.com/%s/comments' % botpost['post_id']
		#print url
#		user = json.loads(r.text)
		#print user['first_name']
		
#		quoteCreator=random.choice(quotations.keys())
#		quote=quotations[quoteCreator][0]
		
		
#		if "pnr" in wallpost["message"].lower():
#			message ="Your PNR status is as follows : "+ train_pnr.execute(wallpost)
#			message+="\n\n"+quote+"\n\t\t--"+quoteCreator
#		else:
#		message = 'Thanks %s for the post :)' % user['first_name']
#		message+="\n\n"+quote+"\n\t\t--"+quoteCreator
#		message+="\n\nNitesh will reply you as soon as he reads this post.\n"
		#print message
		payload = {'access_token': TOKEN, 'message': bot2Comment}
		s = requests.post(url, data=payload)
		#print s
		print "Comment done on post %s" % botpost['post_id']


if __name__ == '__main__':
	#comment_all(get_posts())
	bot2 = factory.create(ChatterBotType.CLEVERBOT)
	bot2session = bot2.create_session()
	json_data=open('quotations.json')
	quotations = json.load(json_data)
	#print quotations
	#exit(1)
	f=open("lastPostProcessed","r")
	lastPostProcessed=f.read()
	f.close()
	lastPostProcessed=lastPostProcessed.strip()
	#print lastPostProcessed
	#exit(1)
	
	#exit(1)
	LASTTIME=lastPostProcessed
	runtime=1
	while 1:
#		notidata,LASTTIME=get_notifications(LASTTIME)
#		commentLatest(notidata,quotations)
		f=open("lastPostProcessed","w")
		print >> f,LASTTIME
		f.close()
		print runtime
		runtime=runtime+1
		for i in range(0,2):
			chatPostID=getChatterPosts()
			checkBotPosts(bot2session,chatPostID)
			time.sleep(30)
