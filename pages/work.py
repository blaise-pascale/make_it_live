import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
import folium
from streamlit_folium import folium_static
from streamlit_bokeh_events import streamlit_bokeh_events
from shapely import geometry
import geopandas as gpd

def find_nearby():

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
            #GET NEARBY LOC FROM SQL
            nrby_loc=[]
            mat=np.zeros((1,2),dtype=float)
            st.write(mat[0][0],mat[0][1],mat)
            st.write(loc["lat"],loc["lon"])
            mat[0][0],mat[0][1]=loc["lat"],loc["lon"]
            #curr_loc=[]
            st.write(mat[0][:])
            with st.echo():
                m = folium.Map(location=[mat[0][0],mat[0][1]], zoom_start=16)
                tooltip = "You are Here!"
                a=folium.Marker([mat[0][0],mat[0][1]], popup="You are Here!",draggable=False,tooltip=tooltip).add_to(m)
                folium_static(m)
                warehouse_loc = (mat[0][0],mat[0][1])
                warehouse_locs = [geometry.Point(warehouse_loc)]
                buffers_df = func_radius_around_point(warehouse_locs,[100000,150000,200000],crs_from=4326,crs_to=3857)
                map_ = folium.Map(location=(warehouse_loc[-1],warehouse_loc[0]))
                poly = folium.GeoJson(buffers_df.buffered_100000[0])
                map_.add_child(poly)
                poly = folium.GeoJson(buffers_df.buffered_150000[0])
                map_.add_child(poly)

def func_radius_around_point(point_list,m_list,crs_from,crs_to):
    points_df = pd.DataFrame(point_list).reset_index()
    points_df = points_df.rename(columns={0:'geometry'})
    points_gpd = gpd.GeoDataFrame(points_df,geometry='geometry',crs=crs_from)
    for m in m_list:
        buffered= points_gpd.to_crs(epsg=crs_to).buffer(m).to_crs(epsg=crs_from)
        col_name = 'buffered_{m}'.format(m=m)
        points_gpd[col_name] = buffered
    return points_gpd #x,y
find_nearby()
