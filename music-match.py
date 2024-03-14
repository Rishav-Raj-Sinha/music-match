import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from fuzzywuzzy import fuzz

#css
page_bg_image = """
<style>
[data-testid="stAppViewContainer"]{
background-color: rgb(30 215 96)
}
</style>
"""
st.markdown(page_bg_image,unsafe_allow_html=True)



#title and description
st.title("Music-Match")
st.markdown("Enter your details and music preference below.")

#establishing connection with google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

#fetch data
existing_data = conn.read(worksheet="info", usecols=list(range(4)), ttl=60)
existing_data = existing_data.dropna(how="all")
#creating a panda dataframe with existing data
df = pd.DataFrame(existing_data)
#creating a pandas dataframe with just the "genres" column
col_data = df["genres"]
st.dataframe(df) 
#list of genres
genre_options = [
    "Pop",
    "Rock",
    "Hip Hop",
    "R&B",
    "Country",
    "Electronic",
    "Jazz",
    "Blues",
    "Classical",
    "Reggae",
    "Indie",
    "Metal",
    "Folk",
    "Punk",
    "Soul",
    "Funk",
    "Disco",
    "EDM",
    "Rap",
    "Alternative",
    "Gospel",
    "Ska",
    "Dubstep",
    "House",
    "Techno",
    "K-pop",
    "Latin",
    "J-Pop",
    "Bollywood",
    "Ambient",
    "Trance",
    "Grime",
    "Chillout",
    "Salsa",
    "Bluegrass",
    "Swing",
    "Acoustic",
    "New Age",
    "Dancehall",
    "Hard Rock",
    "Trap",
    "Psychedelic",
    "World",
    "Reggaeton",
    "Instrumental",
    "Garage",
    "Samba",
    "Rock and Roll"
]
#creating the form
with st.form(key="user_form"):
    name = st.text_input(label="Create an username*")
    spotify = st.text_input(label="your Spotify username")
    usergenres = st.multiselect("Select your favorite genres", options=genre_options)
    hours = st.slider("How many hours do you listen to music per day",0,24,1)

    #mandatory fields
    st.markdown("**required field*")

    #button
    submit = st.form_submit_button(label="Submit")
    #button click action
    if submit:
        if not name:
            st.warning("Ensure that the mandatory fields are filled")
            st.stop()
        elif existing_data["username"].str.contains(name).any():
            st.warning("username already exists, please choose another username")
            st.stop()
        else:
            #calculation of scores
            reference_string = usergenres
            similarity_scores = df['genres'].apply(lambda x: fuzz.ratio(reference_string, x))
#            st.write(similarity_scores)
            index_of_max_value = similarity_scores.idxmax()
            name_at_index = df.loc[index_of_max_value, 'username']
            #creation of dataframe to be pushed in the form
            info = pd.DataFrame(
                [
                    {
                        "username": name,
                        "genres": ",".join(usergenres),
                        "spotify_username": spotify,
                        "hours_listened": hours,
                    }
                ]
            )
            updated_info = pd.concat([existing_data, info], ignore_index=True)

            #push to google sheets
            conn.update(worksheet="info", data=updated_info)

#            st.success("calculating")


            st.write('Hey,',name,'your music-match is',name_at_index)

#finding score
#reference_string = usergenres
#similarity_scores = df['genres'].apply(lambda x: fuzz.ratio(reference_string, x))
#st.write(similarity_scores)

