import PlaylistsModule as pm
playlist = None

while True:
    try:
        print("\n----- MUSIC PLAYLIST MANAGER -----")
        # Creation & Editing
        print("1. Generate New Playlist")
        print("2. Delete Songs)")
        print("3. Save current Playlist")
        
        # Viewing & Searching
        print("4. Show List of Saved Playlists")
        print("5. Display Playlist Content")
        print("6. Search for a Song")
        
        # File Management
        print("7. Sort a Playlist (CSV)")
        print("8. Rename a Playlist")
        print("9. Delete a Playlist File")
        print("10. Exit")

        choice = input("\nEnter your choice (1-10): ")

        if choice == "1":
            playlist = pm.generate_playlist(pm.df)

        elif choice == "2":
            if playlist is not None:
                playlist = pm.delete_songs(playlist)
            else:
                print("Generate a playlist first.")

        elif choice == "3":
            if playlist is not None:
                pm.save_playlist(playlist)
            else:
                print("Generate a playlist first.")

        elif choice == "4":
            pm.show_playlists()

        elif choice == "5":
            pm.display_playlist()

        elif choice == "6":
            pm.search_song()

        elif choice == "7":
            pm.sort_playlist()

        elif choice == "8":
            pm.rename_playlist()

        elif choice == "9":
            pm.delete_playlist()

        elif choice == "10":
            print("Thank you for using the program!")
            break

        else:
            print("Invalid choice.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to continue...")

