from twitter import *
from operator import itemgetter
import networkx as nx
from matplot_helper import save_graph
from cookbook import make_twitter_request
import random
from networkx import diameter
from networkx import average_shortest_path_length

# author - Carl Poole
# version - 1.0
# 
# description - This is a python program that gets friend connections
#				and creates a graph.
#
# works cited:	matplot_helper made by Shelby Shum to make image
# 				cookbook methods imported for make_twitter_request

# --- oAuth Information -- This is secret... shhh! --------------------

OAUTH_TOKEN		= ''
OAUTH_SECRET		= ''
CONSUMER_KEY		= ''
CONSUMER_SECRET	= ''

# ---------------------------------------------------------------------

# A class to manage the Twitter API interactions and graphing
class CarlTwitNet:

	# Constructs a new CarlTwitNet class with oAuth information
	def __init__(self,OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET):
		
		# Setup Twitter API
		self.t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
		
		# Number of followers/friends to cut off at
		self.MAX = 1000
		
		# Keep track of users we look up
		self.alreadyGot = []
		
		# Setup empty graph for networking
		self.G = nx.Graph()
		
	# Given a list of user ids, return a list of tuples (screen_name,follower_count)
	def batchUserLookup(self, users):
		# print users
		userList = []
		for n in range(0, len(users["ids"]), 100):
			ids = users["ids"][n:n+100]
			subquery = make_twitter_request(self.t.users.lookup, user_id=ids)
			
			if subquery is not None:
				userList += [ (user["screen_name"], user["followers_count"]) 
								for user in subquery 
								if user["followers_count"] < self.MAX 
								and user['protected'] == False ]
			
		userList = sorted(userList,key=itemgetter(1), reverse=True)
		return userList
		
	# Given a username, return the top 5 followers for that user
	def getTopFollowers(self, username):
		# print 'looking up for ' + username
		query = make_twitter_request(self.t.followers.ids,screen_name=username)
		userList = self.batchUserLookup(query)
		return userList
			
	# Given a username, return the top 5 friends for that user
	def getTopFriends(self, username):
		# print 'looking up for ' + username
		query = make_twitter_request(self.t.friends.ids,screen_name=username)
		userList = self.batchUserLookup(query)
		return userList
		
	# Given a username, return the top 5 reciprocal friends for that user
	def getTopFiveReciprocalFriends(self, username):
		reciprocal = list(set(self.getTopFollowers(username)) & set(self.getTopFriends(username)))
		reciprocal = sorted(reciprocal,key=itemgetter(1), reverse=True)
		reciprocal = reciprocal[:5]
		print reciprocal
		return reciprocal
		
	# Return tuples of top 5 reciprocal friends from list of provided users
	def getTopFiveReciprocalFriendsTuples(self, listOfUsers):		
		resolve = [ (user,
							[ item[0] for item in self.getTopFiveReciprocalFriends(user) ]
																) for user in listOfUsers ]
																
		tuples = [ [ (user[0],top) for top in user[1]] for user in resolve ]
		return tuples
		
	# Create social network and graph
	def mapNetwork(self,username):
		print "Loading Users..."
		topLevel = self.getTopFiveReciprocalFriends(username)
		topLevel = [ user[0] for user in topLevel ]
		topLevel = topLevel[:5]
		tuples   = [ (username, user) for user in topLevel ]
		self.G.add_edges_from(tuples)
		
		self.alreadyGot += topLevel
		self.alreadyGot.append(username)
																
		tuples = self.getTopFiveReciprocalFriendsTuples(topLevel)
		process = [ self.G.add_edges_from(edges) for edges in tuples ]
		
		# keep getting more top5 users to put over 100
		for x in range(0, 5):
			untriedUsers = list(set(self.G.nodes()).difference(set(self.alreadyGot)))		
			again = random.sample(untriedUsers, 5)
			self.alreadyGot += again
			tuples = self.getTopFiveReciprocalFriendsTuples(again)
			process = [ self.G.add_edges_from(edges) for edges in tuples ]
		
		# Print statistics
		print '-------------------------------'
		print 'Network Size'
		print '-------------------------------'
		print ''
		print 'Nodes: ' + str(len(self.G.nodes()))
		print 'Edges: ' + str(len(self.G.edges()))
		print "Distance: " + str(diameter(self.G))
		print "Average distance: " + str(average_shortest_path_length(self.G))
		
		# Save a picture representation of the graph!
		save_graph(self.G, "test.png")
						
if __name__ == "__main__": 
	
	# Setup the CarlTwitNet class
	ct = CarlTwitNet(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
	
	# Pick core user
	coreUser = 'cpoole98'
	
	# Run program
	ct.mapNetwork(coreUser)
	
	
	
	
	
	
	
	
