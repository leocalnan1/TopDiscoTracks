import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# For Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# For YouTube API
from googleapiclient.discovery import build

# For Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def scrape_beatport_nu_disco():
    url = 'https://www.beatport.com/genre/nu-disco-disco/50/top-100'

    # Update with your ChromeDriver path
    chrome_driver_path = 'C:\\Users\\leoca\\OneDrive\\Documents\\chromedriver-win64\\chromedriver.exe'  # Replace with actual path to your chromedriver

    # Initialize WebDriver with Service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Load the page
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    tracks = []




    # Find all track rows
    track_elements_wide = soup.find_all('div', class_=re.compile('Table-style__TableCell-sc-'))

    track_elements_thin = soup.find_all('div', class_=re.compile('Lists-shared-style__MetaRow-sc-'))

    for idx, track in enumerate(track_elements_thin[:100], 1):
        try:
            # Extract the track title from the first <a> tag inside the track element
            title_tag = track.find('a', title=True)
            title = title_tag['title'].strip() if title_tag else 'Unknown Title'

            # Extract the artist name from the second <a> tag inside the track element
            artist_tag = track.find('div', class_='ArtistNames-sc-72fc6023-0 gsievp').find('a', title=True)
            artist = artist_tag['title'].strip() if artist_tag else 'Unknown Artist'

            # Append the track info to the list
            tracks.append({
                'position': idx,
                'title': title,
                'artist': artist,
                'source': 'Beatport_nu_disco'
            })

        except AttributeError:
            print(f"Error parsing track at position {idx}")
            continue

    return tracks

def scrape_beatport_indie_dance():
    url = 'https://www.beatport.com/genre/indie-dance/37/top-100'

    # Update with your ChromeDriver path
    chrome_driver_path = 'C:\\Users\\leoca\\OneDrive\\Documents\\chromedriver-win64\\chromedriver.exe'  # Replace with actual path to your chromedriver

    # Initialize WebDriver with Service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Load the page
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    tracks = []




    # Find all track rows
    track_elements_wide = soup.find_all('div', class_=re.compile('Table-style__TableCell-sc-'))

    track_elements_thin = soup.find_all('div', class_=re.compile('Lists-shared-style__MetaRow-sc-'))

    for idx, track in enumerate(track_elements_thin[:100], 1):
        try:
            # Extract the track title from the first <a> tag inside the track element
            title_tag = track.find('a', title=True)
            title = title_tag['title'].strip() if title_tag else 'Unknown Title'

            # Extract the artist name from the second <a> tag inside the track element
            artist_tag = track.find('div', class_='ArtistNames-sc-72fc6023-0 gsievp').find('a', title=True)
            artist = artist_tag['title'].strip() if artist_tag else 'Unknown Artist'

            # Append the track info to the list
            tracks.append({
                'position': idx,
                'title': title,
                'artist': artist,
                'source': 'Beatport_indie_dance'
            })

        except AttributeError:
            print(f"Error parsing track at position {idx}")
            continue

    return tracks

def scrape_traxsource():
    url = 'https://www.traxsource.com/genre/17/nu-disco-indie-dance/top'

    # Update with your ChromeDriver path
    chrome_driver_path = 'C:\\Users\\leoca\\OneDrive\\Documents\\chromedriver-win64\\chromedriver.exe'  # Replace with actual path to your chromedriver

    # Initialize WebDriver with Service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Load the page
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    tracks = []

    # Find all track rows
    track_titles = soup.find_all('div', class_='trk-cell title')
    track_artists = soup.find_all('div', class_='trk-cell artists')

    for idx, (title_div, artist_div) in enumerate(zip(track_titles[1:101], track_artists[1:101]), 1):
        try:
            # Extract the track title from the <a> tag inside the title div
            title = title_div.find('a').text.strip()

            # Extract the artist name from the <a> tag inside the artist div
            artist = artist_div.find('a').text.strip()

            tracks.append({
                'position': idx,
                'title': title,
                'artist': artist,
                'source': 'Traxsource'
            })
        except AttributeError:
            print(f"Error parsing track at position {idx}")
            continue

    return tracks

def assign_chart_scores(tracks):
    for track in tracks:
        position = track.get('position', 101)
        track['chart_score'] = 101 - position if position <= 100 else 0

    return tracks

def combine_tracks(*args):
    combined = {}
    for track_list in args:
        for track in track_list:
            key = (track['title'].lower(), track['artist'].lower())
            if key not in combined:
                combined[key] = track
            else:
                combined[key]['chart_score'] += track.get('chart_score', 0)

    return list(combined.values())

def calculate_total_scores(tracks):
    for track in tracks:
        track['total_score'] = (
            track.get('chart_score', 0)
            #track.get('spotify_score', 0) +
            #track.get('youtube_score', 0)
        )
    return tracks

if __name__ == '__main__':
    # Scrape data from Beatport and Traxsource
    beatport_tracks_nu_disco = scrape_beatport_nu_disco()
    beatport_tracks_indie_dance = scrape_beatport_nu_disco()
    traxsource_tracks = scrape_traxsource()

    # Assign chart scores
    beatport_tracks_nu_disco = assign_chart_scores(beatport_tracks_nu_disco)
    beatport_tracks_indie_dance = assign_chart_scores(beatport_tracks_indie_dance)
    traxsource_tracks = assign_chart_scores(traxsource_tracks)

    # Combine the tracks from both sources
    all_tracks = combine_tracks(beatport_tracks_nu_disco,
                                beatport_tracks_indie_dance,
                                traxsource_tracks)

    # Calculate total scores (right now only chart_score is used)
    all_tracks = calculate_total_scores(all_tracks)

    # Display or save the results (e.g., output to a CSV file or print the tracks)
    df = pd.DataFrame(all_tracks)
    df.to_csv('top_nu_disco_tracks.csv', index=False)
    print(df.head(10))  # Print top 10 tracks
