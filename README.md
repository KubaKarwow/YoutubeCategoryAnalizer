# YoutubeCategoryAnalizer

This was the end of semester project during my python classes, done with a classmate. 

Functionality:
-
Using google auth 2.0, after user logs in this app makes an api call to retrieve last 50 liked videos on youtube. 

Based on these it makes a circular graph showing users interest (by video category)

Following that it makes another API call to google trends comparing the users interest to youtube searches of given categories.

It takes in the result of google trends and makes another circular graph clearly showing the differences. 

Libraries used:
-
matplotlib, googleapiclient, google_auth_oauthlib, TrendReq

Video Presentation (in polish):
-
https://www.youtube.com/watch?v=znEOis0qFoI

libraries:
-
-pip install --upgrade google-auth-oauthlib google-auth-httplib2
- pip install googleapiclient
- pip install --upgrade google-api-python-client

