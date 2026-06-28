import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 

st.set_page_config(page_title="Spotify Analysis", layout="wide")
st.subheader("Last 90-days Spotify Consumption.")
st.write("I'm impatient, lets see how I consumed Spotify in the last 90 days!")
st.warning("For 90 days this is a lot, i think.")

#Spotify forwarded 2 Streaming history file. 
table_1= pd.read_json("StreamingHistory_music_0.json")
table_2=pd.read_json("StreamingHistory_music_1.json")
data_frame=pd.concat([table_1,table_2], ignore_index=True)

track_count= data_frame.groupby("trackName").size() #func 1: groupby() is looking for the same tracknames, func2: size() is couting the rows
#note: this is all happening in the data_frame
track_sortedt=track_count.sort_values(ascending=False) #we need the values of 'trackName' (sort_value()) and in descending order!

myTopTrack=track_sortedt.index[0] #taking the top song, 0th position text
frequency=track_sortedt.iloc[0] #extracting the times the song played, 0th position integer

top_5_tracks=track_sortedt.head(5).reset_index() #instead of a 1-column list, we will have a 2 column table with reset_index()!
top_5_tracks.columns=["Track Name", "Total Plays"] #naming the columns here


topTrack_data= data_frame[data_frame["trackName"]==myTopTrack] #extracting details about my top track/song
topTrack_artist=topTrack_data["artistName"].iloc[0] #storing the top song's artist, use iloc[] to actually get the
mstimeTotal= topTrack_data["msPlayed"].sum() #we add up all the times it has played for milli seconds

total_time_top=mstimeTotal/(1000*60*60) #in hours

artist_sorted= data_frame.groupby("artistName").size().sort_values(ascending=False) #similar to the top track

topArtist_dataf=artist_sorted.head(5).reset_index() 
topArtist_dataf.columns=["Artist Name", "Total Plays"] 

total_hours_app=data_frame["msPlayed"].sum()/(1000*60*60)

st.markdown("---") #this function in markdown is giving us a clean line

st.subheader("My top song since last winter:")
st.markdown(f"### **{myTopTrack}**")
st.write(f"By {topTrack_artist}") #let's not ignore the artist.

col1, col2=st.columns(2)
with col1:
    st.metric(label= "Total Plays:", value=f"{frequency} times")
with col2:
    st.metric(label="Time Spent:", value= f" {total_time_top:0.3f} hours" )

st.markdown("---")
st.markdown("### **My Top Tracks (exam presure edition)**")
col_table_track, col_chart_track=st.columns([1,1.5])
with col_table_track:
    st.dataframe(top_5_tracks, width= "stretch", hide_index=True, )

with col_chart_track:
    fig, ax=plt.subplots(figsize=(6,3)) #ax is where the lines and bars go #fig is basically the whole chart
    sns.barplot(data=top_5_tracks, x="Total Plays", y="Track Name", ax=ax,palette="plasma") #using seaborn we get the bars
    #taking vertical bars made the songs overlap

    ax.set_xlabel("Total Streams")
    ax.set_ylabel("")

    sns.despine() #for aesthetic purpose, stripping away the borders
    st.pyplot(fig) #streamlit takes out the complicated figure from matplotlib into the data dashboard

st.markdown("---")
st.subheader("90-days listening hours:")
st.markdown(f"### **{total_hours_app:0.3f} hours**")
st.markdown("---")

st.subheader("The top 5 artist: (!)")

col_table, col_chart=st.columns([1, 1.5]) #spliting the table and chart towards the sides. chart is 1.5 times wider
with col_table:
    st.dataframe(topArtist_dataf, width="stretch", hide_index=True)

with col_chart:
    fig, ax=plt.subplots(figsize=(6,3)) #ax is where the lines and bars go #fig is basically the whole chart
    sns.barplot(data=topArtist_dataf, x="Total Plays", y="Artist Name", ax=ax,palette="plasma")

    ax.set_xlabel("Total Streams")
    ax.set_ylabel("")

    sns.despine() #for aesthetic purpose, stripping away the borders
    st.pyplot(fig) #streamlit takes out the complicated figure from matplotlib into the data dashboard
