import webbrowser
import re
import wikipedia
import speedtest
import requests
from urllib.parse import quote
import websites


def googleSearch(request):
	if 'image' in request:
		request += "&tbm=isch"
	request = request.replace('images', '')
	request = request.replace('image', '')
	request = request.replace('search', '')
	request = request.replace('show', '')
	request = request.replace('google', '')
	request = request.replace('tell me about', '')
	request = request.replace('for', '')
	webbrowser.open("https://www.google.com/search?q=" + request)
	return "Here you go..."

def youtube(request):
	"""Search and play YouTube videos using direct URL approach"""
	try:
		# Clean up the request
		request = request.replace('play', ' ')
		request = request.replace('on youtube', ' ')
		request = request.replace('youtube', ' ')
		request = request.strip()
		
		print("Searching for videos...")
		
		# Use YouTube search URL directly
		search_query = quote(request)
		youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"
		
		print("Opening YouTube search...")
		webbrowser.open(youtube_search_url)
		
		return "Opening YouTube search results for you..."
		
	except Exception as e:
		print(f"YouTube search error: {e}")
		# Fallback to direct YouTube homepage
		webbrowser.open("https://www.youtube.com")
		return "Opening YouTube homepage..."

def youtube_direct_play(request):
	"""Alternative YouTube function that tries to get first result"""
	try:
		from youtubesearchpython import VideosSearch
		
		request = request.replace('play', ' ')
		request = request.replace('on youtube', ' ')
		request = request.replace('youtube', ' ')
		request = request.strip()

		print("Searching for videos...")
		videosSearch = VideosSearch(request, limit=1)
		results = videosSearch.result()['result']
		print("Finished searching!")

		if results:
			webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
			return "Playing video..."
		else:
			return youtube(request)  # Fallback to search results
			
	except Exception as e:
		print(f"Direct YouTube play failed: {e}")
		return youtube(request)  # Fallback to search results

def open_specified_website(request):
	website = request[5:]  # Extract website name after "open "
	if website in websites.websites_dict:
		url = websites.websites_dict[website]
		webbrowser.open(url)
		return True
	else:
		return None

def get_speedtest():
	try:
		internet = speedtest.Speedtest()
		speed = f"Your network's Download Speed is {round(internet.download() / 8388608, 2)}MBps\n" \
			   f"Your network's Upload Speed is {round(internet.upload() / 8388608, 2)}MBps"
		return speed
	except (speedtest.SpeedtestException, KeyboardInterrupt) as e:
		return None

def tell_me_about(request):
	try:
		topic = request.replace("tell me about ", "")
		result = wikipedia.summary(topic, sentences=3)
		result = re.sub(r'\[.*]', '', result)
		return result
	except (wikipedia.WikipediaException, Exception) as e:
		return None

def get_map(request):
	webbrowser.open(f'https://www.google.com/maps/search/{request}')