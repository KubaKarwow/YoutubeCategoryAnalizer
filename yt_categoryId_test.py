import numpy as np
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import matplotlib.pyplot as plt


# Load API key from an environment variable for security
from matplotlib import gridspec
from sympy.physics.control.control_plots import plt

from google_trends import get_trends

api_key = os.getenv('AIzaSyDLJcwCV5jyuHeKHk2uGdrvFoeAmojoqRY')

# Scopes required for accessing YouTube data
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# OAuth 2.0 flow
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
credentials = flow.run_local_server(port=0)

# Build the YouTube service with OAuth credentials
youtube = build('youtube', 'v3', credentials=credentials)

# Get the playlists of the authenticated user
request = youtube.videos().list(
    part='snippet,contentDetails',
    myRating='like',
    maxResults=50  # Number of liked videos to retrieve, you can change this as needed
)

response = request.execute()

category_counts = {}

# Category names mapping
category_names = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '18': 'Short Movies',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '21': 'Videoblogging',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism',
    '30': 'Movies',
    '31': 'Anime/Animation',
    '32': 'Action/Adventure',
    '33': 'Classics',
    '34': 'Comedy',
    '35': 'Documentary',
    '36': 'Drama',
    '37': 'Family',
    '38': 'Foreign',
    '39': 'Horror',
    '40': 'Sci-Fi/Fantasy',
    '41': 'Thriller',
    '42': 'Shorts',
    '43': 'Shows',
    '44': 'Trailers'
}
allCategoriesWatched = []
# Iterate through the playlists and count the category occurrences
for video in response['items']:
    category_id = video['snippet']['categoryId']
   # allCategoriesWatched.append(category_names[category_id])
    if category_id in category_counts:
        category_counts[category_id] += 1
    else:
        category_counts[category_id] = 1


print(category_counts.keys())
for key in category_counts.keys():
    allCategoriesWatched.append(category_names[key])
print(allCategoriesWatched)

trends = get_trends(allCategoriesWatched)
print(trends)

total_videos = sum(category_counts.values())

# Create figure and grid layout
fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2], width_ratios=[3, 1])

# Sorting categories by count descending for pie charts
sorted_cats_1 = sorted(category_counts, key=lambda x: category_counts[x])
labels_1 = [category_names[cat_id] for cat_id in sorted_cats_1]
sizes_1 = [100 * category_counts[cat_id] / total_videos for cat_id in sorted_cats_1]

sorted_cats_2 = sorted(trends, key=lambda x: trends[x])
labels_2 = sorted_cats_2
sizes_2 = [trends[cat] for cat in sorted_cats_2]

# First pie chart on left
ax1 = fig.add_subplot(gs[:, 0])
wedges_1, texts_1= ax1.pie(sizes_1, startangle=90)
ax1.set_title("User's categories")
labels_1.reverse()
wedges_1.reverse()
sizes_1.reverse()
ax1.legend(wedges_1, [f"{l} - {s:.1f}%" for l, s in zip(labels_1, sizes_1)], title="Categories", loc="center", bbox_to_anchor=(-0.1, 0.5))

# Second pie chart in upper right
ax2 = fig.add_subplot(gs[0, 1])
wedges_2, texts_2= ax2.pie(sizes_2, startangle=90)
ax2.set_title("Global categories")
labels_2.reverse()
wedges_2.reverse()
sizes_2.reverse()
ax2.legend(wedges_2, [f"{l} - {s:.1f}%" for l, s in zip(labels_2, sizes_2)], title="Categories", loc="center left", bbox_to_anchor=(1.1, 0.5))

# Bar chart for all categories comparison in percentage
ax3 = fig.add_subplot(gs[1, 1])
# [category_names[cat_key] for cat_key in category_counts.keys()]
categories = sorted(set([category_names[cat_key] for cat_key in category_counts.keys()]) | set(trends.keys()))
bar_width = 0.35
index = np.arange(len(categories))
bar1 = [100 * category_counts.get(cat, 0) / total_videos for cat in category_counts]
bar2 = [trends.get(cat, 0) for cat in categories]
ax3.bar(index - bar_width/2, bar1, bar_width, label='User Data')
ax3.bar(index + bar_width/2, bar2, bar_width, label='Global Data')
ax3.set_xlabel('Categories')
ax3.set_ylabel('Percentage')
ax3.set_title('Comparison of Interests Across Datasets')
ax3.set_xticks(index)
ax3.set_xticklabels([cat for cat in categories], rotation=45, ha="right")
ax3.legend()

# Layout adjustments
plt.tight_layout()
plt.show()