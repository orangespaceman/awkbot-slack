on run args
    try
        tell application "Spotify"
            set currentTrack to current track
            set currentTrackId to id of currentTrack
            set currentTrackArtist to artist of currentTrack
            set currentTrackName to name of currentTrack
            return currentTrackId & "
" & currentTrackArtist & "
" & currentTrackName
        end tell
    end try
end run
