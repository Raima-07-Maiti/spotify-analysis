import pandas as pd
import streamlit as st #now we will make a dashboard!

st.set_page_config(page_title="Spotify Analysis", layout="wide")
st.subheader("Last 90-days Spotify Consumption.")
st.write("I'm impatient, lets see how I consumed Spotify in the last 90 days!")

#Spotify forwarded 2 Streaming history file. 
table_1= pd.read_json("StreamingHistory_music_0.json")
table_2=pd.read_json("StreamingHistory_music_1.json")
data_frame=pd.concat([table_1,table_2], ignore_index=True)

track_count= data_frame.groupby("trackName").size() #func 1: groupby() is looking for the same tracknames, func2: size() is couting the rows
#note: this is all happening in the data_frame
track_sortedt=track_count.sort_values(ascending=False) #we need the values of 'trackName' (sort_value()) and in descending order!

myTopTrack=track_sortedt.index[0] #taking the top song, 0th position text
frequency=track_sortedt.iloc[0] #extracting the times the song played, 0th position integer

topTrack_data= data_frame[data_frame["trackName"]==myTopTrack] #extracting details about my top track/song
topTrack_artist=topTrack_data["artistName"].iloc[0] #storing the top song's artist, use iloc[] to actually get the
mstimeTotal= topTrack_data["msPlayed"].sum() #we add up all the times it has played for milliseconds

total_time=mstimeTotal/(1000*60*60) #in hours

artist_sorted= data_frame.groupby("artistName").size().sort_values(ascending=False) #similar to the top track

topArtist_dataf=artist_sorted.head(5).reset_index() #reset_index() makes a proper table 
topArtist_dataf.columns=["Artist Name", "Total Plays"]

st.markdown("---")

st.subheader("My top song since last winter:")
st.markdown(f"### **{myTopTrack}**")
st.write(f"By {topTrack_artist}")
#creating a table (with columns!)
st.markdown("---")

col1, col2=st.columns(2)

with col1:
    st.metric(label="Time spent w this song", value=f"{total_time:0.2f} hours")
with col2:
    st.metric(label="Play count", value=frequency)

st.markdown("---")

st.subheader("My top 5 artists: ")
st.dataframe(topArtist_dataf, width="stretch", hide_index=True)
