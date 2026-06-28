import pandas as pd
table_1= pd.read_json("StreamingHistory_music_0.json")
table_2=pd.read_json("StreamingHistory_music_1.json")
data_frame=pd.concat([table_1,table_2], ignore_index=True)

print("Total rows loaded:", len(data_frame))
print(data_frame.head()) #head() gives us the first 5 rows (default)

track_count= data_frame.groupby("trackName").size() #func 1: groupby() is looking for the same tracknames, func2: size() is couting the rows
#note: this is all happening in the data_frame
track_sortedt=track_count.sort_values(ascending=False) #we need the values of 'trackName' (sort_value()) and in descending order!

print("Top songs: ", track_sortedt.head()) 

myTopTrack=track_sortedt.index[0] #taking the top song
topTrack_data= data_frame[data_frame["trackName"]==myTopTrack] #extracting details about my top track/song
topTrack_artist=topTrack_data["artistName"]
mstimeTotal= topTrack_data["msPlayed"].sum() #we add up all the times it has played for milliseconds

total_time=mstimeTotal/(1000*60*60) #in hours

print(f"you played the top song for : {total_time:0.2f} hours")


artist_sorted= data_frame.groupby("artistName").size().sort_values(ascending=False)

topArtist_dataf=artist_sorted.head(5).reset_index() #reset_index() makes a proper table 
topArtist_dataf.columns=["Artist Name", "Total Plays"]
