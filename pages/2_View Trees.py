import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

if "name" in st.session_state:
    st.write("Hello ",st.session_state["name"])



loc_button = Button(label="Get Location")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_LOCATION" in result:
        st.write(result.get("GET_LOCATION")["lon"],type(result.get("GET_LOCATION")["lat"]))
        loc_pd=pd.DataFrame({'lon':[result.get("GET_LOCATION")["lon"]],'lat':[result.get("GET_LOCATION")["lat"]]})
        loc={'lon':result.get("GET_LOCATION")["lon"],'lat':result.get("GET_LOCATION")["lat"]}
        midpoint=(result.get("GET_LOCATION")["lon"],result.get("GET_LOCATION")["lat"])
        mat=np.zeros((1,2),dtype=float)
        st.write(mat[0][0],mat[0][1],mat)
        st.write(loc["lat"],loc["lon"])
        mat[0][0],mat[0][1]=loc["lat"],loc["lon"]
        
        df = pd.DataFrame(mat,
                          columns=['lat', 'lon'])
        st.pydeck_chart(pdk.Deck(
     map_style=None,
     initial_view_state=pdk.ViewState(
         latitude=loc["lat"],
         longitude=loc["lon"],
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=20,
         ),
     ],
 ))
