import pandas as pd
import time
import os

try: #if the dataset loads successfully
    df = pd.read_csv("spotify.csv") #Load dataset
    print("Dataset loaded successfully!")
except FileNotFoundError: 
    print("File not found!") #if dataset is not found, print custom message in program
    exit()

def assign_mood(energy, valence): # Assign mood based on energy and valence
    if energy >= 0.7 and valence >= 0.7:
        return "Happy"
    elif energy >= 0.7 and valence < 0.7:
        return "Energetic"
    elif energy < 0.7 and valence >= 0.7:
        return "Calm"
    else:
        return "Sad"
df["mood"] = df.apply(lambda row: assign_mood(row["energy"], row["valence"]), axis=1)
#This statement creates a new column “mood” in the dataframe.
#apply() processes each row of the dataframe.
#lambda(unnamed) function takes one row at a time, extracts energy and valance
# and passes them to assign_mood() which returns mood(Happy, sad etc.)
def generate_playlist(df):
    choice = input("Generate playlist by Mood / Genre / Artist: ").lower()
     #user input to choose how they want to generate the playlist. uses .lower() to convert input to lower case making it case insensitive.
    if choice == "mood":
        mood = input("Enter a mood (Happy, Energetic, Calm, Sad): ")
        # Filter songs based on user input mood
        filtered_songs = df[df["mood"].str.lower() == mood.lower()] #filters the songs in the df by mood. .str.lower == mood.lower() makes the user input case insensitive. compares mood column in df with user mood.

    elif choice == "genre":
        genre = input("Enter genre: ")
        filtered_songs = df[df["track_genre"].str.lower() == genre.lower()] #converts the track_genre column to lowercase and compares it with the lowercase of user input genre and filters songs based on that.

    elif choice == "artist":
        artist = input("Enter artist name: ")
        filtered_songs = df[df["artists"].str.lower().str.contains(artist.lower())]#converts the artists column to lowercase and compares it with the lowercase of user input artist name and filters songs based on that. .str.contains() allows partial matches, so if user enters "Justin", it will match "Justin Bieber" and "Justin Timberlake".

    else:
        print("Invalid choice")
        return None

    # Check if no songs found
    if filtered_songs.empty: #if the filtered_songs dataframe is empty, it means no songs matched the user's criteria.
        print("No songs found")
        return None #none returns null value to indicate no playlist can be generated.
    
    else:
        #customize playlist length
        num_songs = int(input("How many songs do you want in your playlist? "))

        if num_songs > len(filtered_songs): #if the number of songs requested by the user is greater than the number of songs available in the filtered_songs dataframe(selected songs based on the mood, artist or genre), it adjusts num_songs to be equal to the length of filtered_songs to avoid errors when sampling.
            num_songs = len(filtered_songs)

        print("Generating your customized playlist...")
        time.sleep(2)
        # Randomly pick songs
        playlist = filtered_songs.sample(n=num_songs).reset_index(drop=True) #sample() function is used to randomly select a specified number of rows from the filtered_songs dataframe to create the playlist. n=num_songs specifies how many songs to select based on user input.

        print("\n Your Customized Playlist \n")

        for i, row in enumerate(playlist.itertuples(), start=1):# loop iterates through all the rows in playlist. enumerate() is used to get index and row data and we have initialized it to start from 1 instead of 0. itertuples() returns tuple like object for each row.
            print(f"{i}. {row.track_name} - {row.artists}")  # 1. Song Name - Artist Name

        return playlist
    
#if user wants to delete one or more songs from the customized playlist.
def delete_songs(playlist):
    while True: # loop keeps running until user chooses no.
        delete_choice = input("Do you want to delete any songs from the playlist? (yes/no): ").lower()

        if delete_choice == "yes":
            song_number = int(input("Enter the number of the song you want to delete: ")) # takes song number to delete

            if 1 <= song_number <= len(playlist):
                playlist = playlist.drop(playlist.index[song_number - 1]) # .drop() method is used to remove the specified row from the playlist dataframe. 
                playlist = playlist.reset_index(drop=True)#after dropping the song, we reset the index of the playlist df to maintain a continuous index sequence. drop=True is used to avoid adding the old index as a new column in the dataframe.

                print("Song deleted. Updated Playlist:")

                for i, row in enumerate(playlist.itertuples(), start=1):
                    print(f"{i}. {row.track_name} - {row.artists}") # displays updated plylist with numbering from 1.

            else:
                print("Invalid song number.")

        elif delete_choice == "no":
            break

        else:
            print("Please enter 'yes' or 'no'.")
    return playlist

def save_playlist(playlist):
    save_choice = input("Do you want to save the playlist? (yes/no): ").lower()

    if save_choice == "yes":
        filename = input("Enter file name: ") #name of the playlist file to be saved.
        file_type = input("Save as csv or txt? ").lower() #user input for type of file to save the playlist as.

        if file_type == "csv":
            playlist.to_csv(filename + ".csv", index=False) #to save dataframe as CSV file, index=False is used to avoid saving the index as a column in the CSV file. 
            print("Playlist saved successfully as CSV file!")

        elif file_type == "txt":
            with open(filename + ".txt", "w") as file: #opens a new text file with the specified filename in write mode. If the file already exists, it will be overwritten.
                for i, row in enumerate(playlist.itertuples(), start=1):
                    file.write(f"{i}. {row.track_name} - {row.artists}\n")

            print("Playlist saved successfully as TXT file!")

        else:
            print("Invalid file type.")

    elif save_choice == "no":
        print("Playlist not saved.")

    else:
        print("Please enter yes or no.")

def show_playlists(): #just shows the list of playlists available in the current directory without displaying their content.
    files = []

    for file in os.listdir():
        if file.endswith(".csv") or file.endswith(".txt"):
            files.append(file)

    if not files:
        print("No playlists found.")

    else:
        print("\n List of Playlists \n")

        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")

def display_playlist():
    files = []

    for file in os.listdir():
        if (file.endswith(".csv") or file.endswith(".txt")) and file != "spotify.csv":
            files.append(file)

    if not files:
        print("No playlists found.")
        return

    if len(files) == 1:
        filename = files[0]
        print(f"Only one playlist found: {filename}")
    else:
        print("\nAvailable Playlists:\n")

        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")

        select = input("Enter playlist number: ")

        if not select.isdigit():
            print("Invalid choice.")
            return

        select = int(select)

        if 1 <= select <= len(files):
            filename = files[select - 1]
        else:
            print("Invalid choice.")
            return

    print(f"\nDisplaying {filename}\n")

    if filename.endswith(".csv"):
        playlist = pd.read_csv(filename)

        for i, row in enumerate(playlist.itertuples(index=False), start=1):
            print(f"{i}. {row.track_name} - {row.artists}")

    else:
        with open(filename, "r") as file:
            print(file.read())

def search_song():
    files = []

    for file in os.listdir():
        if file.endswith(".csv") or file.endswith(".txt"):
            files.append(file)#used again to check all saved playlists currently available for search.

    if not files:
        print("No playlists found.")
        return

    elif len(files) == 1:
        filename = files[0]

    else:
        print("\nAvailable Playlists:\n")

        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}") # shows the list of available playlists.

        choice = int(input("Which playlist do you want to search in? "))

        if 1 <= choice <= len(files):
            filename = files[choice - 1]
        else:
            print("Invalid choice.")
            return

    song_name = input("Enter song name to search: ").lower() # song that wants to be searched in the selected playlist.

    print("Searching song...")
    time.sleep(1) #delay of 1 sec to enhance user experience.

    if filename.endswith(".csv"):
        playlist = pd.read_csv(filename)

        result = playlist[
            playlist["track_name"].str.lower().str.contains(song_name)# searches that song name in the track_name column. contains() allows partial matches, so if user enters "love" it can show "love yourself" by justin bieber or "love story" by taylor swift
        ]

        if result.empty:
            print("Song not found.")

        else:
            print("\nSearch Results:\n")

            for i, row in enumerate(result.itertuples(), start=1):
                print(f"{i}. {row.track_name} - {row.artists}")

    elif filename.endswith(".txt"):
        with open(filename, "r") as file:
            content = file.readlines() # reads all lines from file and stores in list in content.

        found = False #flag variable because at first no song found but after loop song matches can be there.

        print("\nSearch Results:\n")

        for line in content:
            if song_name in line.lower():
                print(line.strip())
                found = True #song found

        if found == False: #not found
            print("Song not found.")

def sort_playlist():
    print("Sorting feature is available only for CSV playlists.")
    files = []

    for file in os.listdir():
        if file.endswith(".csv"):
            files.append(file)# used again check all saved playlists currently available for sorting

    if not files:
        print("No CSV playlists found. Sorting is only available for CSV files.")
        return

    elif len(files) == 1:
        filename = files[0]

    else:
        print("\nAvailable Playlists:\n")

        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")

        choice = int(input("Which playlist do you want to sort? "))

        if 1 <= choice <= len(files):
            filename = files[choice - 1]
        else:
            print("Invalid choice.")
            return

    playlist = pd.read_csv(filename)

    print("\nSort Options:\n")
    print("1. Song Name A-Z")
    print("2. Song Name Z-A")
    print("3. Artist Name A-Z")
    print("4. Duration Low to High")

    option = input("Enter your choice: ")

    if option == "1":
        playlist = playlist.sort_values("track_name") #ascending order sorting A-Z

    elif option == "2":
        playlist = playlist.sort_values("track_name", ascending=False) # ascending=false hence reverse Z-A just like reverse=true

    elif option == "3":
        playlist = playlist.sort_values("artists") #A-Z from Artist names

    elif option == "4":
        playlist = playlist.sort_values("duration_ms") #sorting from duration_ms column from low to high i.e. ascending.

    else:
        print("Invalid choice.")
        return

    playlist.to_csv(filename, index=False) #save sorted playlist without index numbers.

    print("\nPlaylist sorted successfully!\n")

    for i, row in enumerate(playlist.itertuples(), start=1):
        print(f"{i}. {row.track_name} - {row.artists}")

def rename_playlist():
    files = []
    for file in os.listdir():
        if file.endswith(".csv") or file.endswith(".txt"):
            files.append(file) #used again to check available playlists for renaming.

    if not files:
        print("No playlists found.")
        return

    elif len(files) == 1:
        old_name = files[0] #if only one playlist exists, select it automatically

    else:
        print("\nAvailable Playlists:\n")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}") #displays playlist names with index numbers from 1
        choice = int(input("Which playlist do you want to rename? "))
        if 1 <= choice <= len(files):
            old_name = files[choice - 1]# old_name is equal to the nth index (or choice -1) of files
        else:
            print("Invalid choice.")
            return

    new_name = input("Enter new playlist name: ")#user input for new name of playlist

    if old_name.endswith(".csv"):
        new_name = new_name + ".csv" #new name of playlist with extention .csv

    elif old_name.endswith(".txt"):
        new_name = new_name + ".txt" #new name of playlist with extention .txt

    os.rename(old_name, new_name) #using .rename() function changing name from old to new
    print("Playlist renamed successfully!")

def delete_playlist():
    files = []

    for file in os.listdir():
        if file.endswith(".csv") or file.endswith(".txt"):
            files.append(file) #used again to check all saved playlists currently available for delete.

    if not files:
        print("No playlists found.")
        return

    elif len(files) == 1:
        filename = files[0] #if only one playlist is fould in the list files, it automatically selects the playlist and deletes it.

    else:
        print("\nAvailable Playlists:\n")

        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")# display the names of available playlists with numbers for user to choose which one to delete.

        choice = int(input("Which playlist do you want to delete? "))

        if 1 <= choice <= len(files):
            filename = files[choice - 1]
        else:
            print("Invalid choice.")
            return

    confirm = input(f"Are you sure you want to delete {filename}? (yes/no): ").lower()# confirm message to prevnt accidental deletion.

    if confirm == "yes":
        os.remove(filename) # .remove() method to delete the selected playlist file from the list files directory.  
        print("Playlist deleted successfully!")

    else:
        print("Playlist not deleted.")
