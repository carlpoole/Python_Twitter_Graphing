Python_Twitter_Graphing
=======================

I created this Twitter graphing program for an assignment for my Social Media Mining class at Syracuse University.

After entering your auth credentials, pick a core user. The program is designed to find the intersection between 
your friends and followers (reciprocal friends) on Twitter and return the top 5 (determined by number of followers,
which are capped at 1000 in my example). The top 5 reciprocal friends of those subsequent friends are then found
and returned. At this point, the program will loop 5 more times, picking 5 people from the available gathered 
users to get their top 5 reciprocal friends, and so on.

Once this is complete, a graph is created and a PNG file is created to visualize the graph. Some stats are then printed.

Sample Output from user @cpoole98:

Image: https://github.com/carlpoole/Python_Twitter_Graphing/blob/master/Output%20Image.png

Nodes: 123
Edges: 144
Distance: 11
Average distance: 5.44608823137
