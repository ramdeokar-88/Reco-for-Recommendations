# import necessary libraries
import pandas as pd    # For reading and writing CSV files
import os              # For checking file/folder existence and creating directories
import base64    
import random 
# For encoding audio files into base64 strings

# file and folder consta,nts
SONGS_FILE = "songs.csv"       # Path to the CSV file that stores song metadata
SONGS_FOLDER = "local_songs"   # Folder where actual audio files are stored


def ensure_songs_file():
    """
    Ensure that the 'songs.csv' file exists.
    If it doesn't exist, create it with the required column headers.
    """
    if not os.path.exists(SONGS_FILE):  
        # If songs.csv doesnt exist, create an empty DataFrame with columns:
        # mood, title, artist, and file (file = path to audio file)
        pd.DataFrame(columns=["mood", "title", "artist", "file"]).to_csv(SONGS_FILE, index=False)


def get_songs_by_mood(mood):
    """
    Retrieve all songs that match a specific mood from the CSV file.
    The audio files are read, encoded in base64, and returned as part of the song data.
    Returns:
    - List[dict]: Each dict contains:
        {
            "title": song title,
            "artist": song artist,
            "audio_data": base64 encoded audio content
        }
    """
    # Read the entire songs.csv into a DataFrame
    songs = pd.read_csv(SONGS_FILE)

    # Filter rows where the 'mood' column matches the given mood (case-insensitive)
    mood_songs = songs[songs["mood"].str.lower() == mood.lower()]

    # Prepare a list to store results
    results = []

    # Loop through each matching song row
    for _, row in mood_songs.iterrows():
        file_path = row["file"]  # Path to the audio file
        
        # Check if the file actually exists on the system
         # Read the file content and encode it to base64
         # Open the audio file in binary read mode
        if os.path.exists(file_path):
            
            with open(file_path, "rb") as f:
               
                encoded = base64.b64encode(f.read()).decode("utf-8")
            
            # Append the song details and encoded audio to results
            results.append({
                "title": row["title"],
                "artist": row["artist"],
                "audio_data": encoded
            })
    
    # Return all matching songs with audio data
    return results


def get_random_song_by_mood(mood):
    songs = pd.read_csv(SONGS_FILE)
    mood_songs = songs[songs["mood"].str.lower() == mood.lower()]
    if mood_songs.empty:
        return None
    row = mood_songs.sample(1, random_state=None).iloc[0]
    file_path = row["file"]
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return {"title": row["title"], "artist": row["artist"], "audio_data": encoded}


def ensure_songs_folder():
    """
    Ensure that the folder for storing songs exists.
    If it doesn't exist, create it.
    """
    # Create the folder if it does not already exist
    os.makedirs(SONGS_FOLDER, exist_ok=True)
