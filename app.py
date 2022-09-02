

import os
import numpy as np
import pandas as pd
import json
import plotly.express as px
import streamlit as st
from PIL import Image


BASIN_AREA = 8827  # Km2
st.set_page_config(page_title="BMRecharge-App", layout="wide")

#%% Main functions and Load data
@st.cache
def get_root_path():
    return os.path.abspath(os.path.dirname(__file__))

root = get_root_path()

@st.cache
def read_timeseries():
    database = {
        "Aquifers": {
            "Ground Gauges": pd.read_csv(os.path.join(root, "series", "Ground Gauges_Aquifers.csv"), index_col=[0]),
            "CHIRPS": pd.read_csv(os.path.join(root, "series", "CHIRPS_Aquifers.csv"), index_col=[0]),
            "CHIRPSC": pd.read_csv(os.path.join(root, "series", "CHIRPSC_Aquifers.csv"), index_col=[0]),
            "CHIRPS-Daymet": pd.read_csv(os.path.join(root, "series", "CHIRPS-Daymet_Aquifers.csv"), index_col=[0]),
        },
        "Zones": {
            "Ground Gauges": pd.read_csv(os.path.join(root, "series", "Ground Gauges_Zones.csv"), index_col=[0]),
            "CHIRPS": pd.read_csv(os.path.join(root, "series", "CHIRPS_Zones.csv"), index_col=[0]),
            "CHIRPSC": pd.read_csv(os.path.join(root, "series", "CHIRPSC_Zones.csv"), index_col=[0]),
            "CHIRPS-Daymet": pd.read_csv(os.path.join(root, "series", "CHIRPS-Daymet_Zones.csv"), index_col=[0]),
        },
        "Basin-wide": pd.read_csv(os.path.join(root, "series", "Recharge.csv"), index_col=[0])
    }
    return database

database = read_timeseries()


@st.cache
def read_layers(allow_output_mutation=True):
    grid = json.load(open(os.path.join(root, "maps", "RechargeGrid.geojson"), "r", encoding="utf-8"))
    aquifers = json.load(open(os.path.join(root, "layers", "Aquifers.geojson"), "r", encoding="utf-8"))
    zones = json.load(open(os.path.join(root, "layers", "Zones.geojson"), "r", encoding="utf-8"))
    layers = {
        "Basin-wide": grid,
        "Aquifers": aquifers,
        "Zones": zones
    }

    return layers


@st.cache
def read_attributes():
    attributes = {
        "Aquifers": pd.read_csv(os.path.join(root, "layers", "Aquifers.csv"), index_col=[0]),
        "Zones": pd.read_csv(os.path.join(root, "layers", "Zones.csv"), index_col=[0]),
        "Basin-wide": {
            "CHIRPS": pd.read_csv(os.path.join(root, "maps", "CHIRPS.csv"), index_col=[0]),
            "CHIRPSC": pd.read_csv(os.path.join(root, "maps", "CHIRPSC.csv"), index_col=[0]),
            "CHIRPS-Daymet": pd.read_csv(os.path.join(root, "maps", "CHIRPS-Daymet.csv"), index_col=[0]),
            "Ground Gauges": pd.read_csv(os.path.join(root, "maps", "Ground Gauges.csv"), index_col=[0]),
        }
    }
    pixel_area = 2000 * 2000
    for key in attributes["Basin-wide"].keys():
        table = attributes["Basin-wide"][key].melt(ignore_index=False).reset_index()
        table.columns = ["ID", "Year", "Recharge (mm)"]
        table["Recharge (lps)"] = (table["Recharge (mm)"]  * pixel_area / (86400 * 365)).round(2)
        table["Year"] = table["Year"].astype(int)
        attributes["Basin-wide"][key] = table

    for key in ("Aquifers", "Zones"):
        attributes[key].index = [str(x) for x in attributes[key].index]

    return attributes

layers = read_layers()
attributes = read_attributes()


@st.cache(persist=True)
def create_map(mtype, dname, cmap, layers, attributes):
    if mtype == "Basin-wide":
        data = attributes[mtype][dname]

        fig = px.choropleth_mapbox(
            data,
            geojson=layers["Basin-wide"],
            animation_frame="Year",
            color="Recharge (mm)",
            locations="ID",
            featureidkey="properties.ID",
            hover_data=["ID", "Recharge (mm)", "Recharge (lps)"],
            range_color=(5, 300),
            opacity=0.6,
            center={"lat": 19.58775, "lon": -98.87349},
            color_continuous_scale=cmap,
            mapbox_style="carto-positron",
            zoom=7.5
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    elif mtype == "Aquifers":
        data = database[mtype][dname].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "ID", "Recharge (mm)"]
        data.set_index("ID", drop=False, inplace=True)
        data = data.join(attributes[mtype], how="left")
        data.columns = ["Year", "ID", "Recharge (mm)", "Aquifer", "Area (km2)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * data["Area (km2)"] * 1e3 / (86400 * 365), 2)

        fig = px.choropleth_mapbox(
            data,
            geojson=layers["Aquifers"],
            animation_frame="Year",
            color="Recharge (mm)",
            locations="ID",
            featureidkey="properties.ID",
            hover_data=["ID", "Aquifer", "Area (km2)", "Recharge (mm)", "Recharge (m3/s)"],
            range_color=(5, 100),
            opacity=0.6,
            center={"lat": 19.58775, "lon": -98.87349},
            color_continuous_scale=cmap,
            mapbox_style="carto-positron",
            zoom=7.5
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
    elif mtype == "Zones":
        data = database[mtype][dname].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "ID", "Recharge (mm)"]
        data.set_index("ID", drop=False, inplace=True)
        data = data.join(attributes[mtype], how="left")
        data.columns = ["Year", "ID", "Recharge (mm)", "Zone", "Area (km2)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * data["Area (km2)"] * 1e3 / (86400 * 365), 2)

        fig = px.choropleth_mapbox(
            data,
            geojson=layers["Zones"],
            animation_frame="Year",
            color="Recharge (mm)",
            locations="ID",
            featureidkey="properties.ID",
            hover_data=["ID", "Zone", "Area (km2)", "Recharge (mm)", "Recharge (m3/s)"],
            range_color=(5, 150),
            opacity=0.6,
            center={"lat": 19.58775, "lon": -98.87349},
            color_continuous_scale=cmap,
            mapbox_style="carto-positron",
            zoom=7.5
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


@st.cache
def read_serie(mtype, dname, attributes):
    if mtype == "Basin-wide":
        data = database[mtype].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "Database", "Recharge (mm)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * BASIN_AREA * 1e3 / (86400 * 365), 2)
        data = data.loc[:, ["Year", "Database", "Recharge (mm)", "Recharge (m3/s)"]]

    else:
        data = database[mtype][dname].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "ID", "Recharge (mm)"]
        data.set_index("ID", drop=False, inplace=True)
        data = data.join(attributes[mtype], how="left")
        data.columns = ["Year", "ID", "Recharge (mm)", "Aquifer", "Area (km2)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * data["Area (km2)"] * 1e3 / (86400 * 365), 2)
        data = data.loc[:, ["Year", "Aquifer", "Recharge (mm)", "Recharge (m3/s)"]]

    return data

def create_timeserie(mtype, dname, attributes):
    if mtype == "Basin-wide":
        data = database[mtype].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "Database", "Recharge (mm)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * BASIN_AREA * 1e3 / (86400 * 365), 2)

        fig = px.line(data, x="Year", y="Recharge (mm)", color="Database", width=800, height=400)
        fig.update_yaxes(title="Recharge (mm)", title_font={"size": 18})

        fig1 = px.line(data, x="Year", y="Recharge (m3/s)", color="Database", width=800, height=400)
        fig1.update_yaxes(title="Recharge (m3/s)", title_font={"size": 18})

    elif mtype == "Aquifers":
        data = database[mtype][dname].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "ID", "Recharge (mm)"]
        data.set_index("ID", drop=False, inplace=True)
        data = data.join(attributes[mtype], how="left")
        data.columns = ["Year", "ID", "Recharge (mm)", "Aquifer", "Area (km2)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * data["Area (km2)"] * 1e3 / (86400 * 365), 2)

        fig = px.line(data, x="Year", y="Recharge (mm)", color="Aquifer", width=800, height=400)
        fig.update_yaxes(title="Recharge (mm)", title_font={"size": 18})

        fig1 = px.line(data, x="Year", y="Recharge (m3/s)", color="Aquifer", width=800, height=400)
        fig1.update_yaxes(title="Recharge (m3/s)", title_font={"size": 18})
    
    elif mtype == "Zones":
        data = database[mtype][dname].melt(ignore_index=False).reset_index()
        data.columns = ["Year", "ID", "Recharge (mm)"]
        data.set_index("ID", drop=False, inplace=True)
        data = data.join(attributes[mtype], how="left")
        data.columns = ["Year", "ID", "Recharge (mm)", "Zone", "Area (km2)"]
        data["Recharge (m3/s)"] = np.round(data["Recharge (mm)"] * data["Area (km2)"] * 1e3 / (86400 * 365), 2)

        fig = px.line(data, x="Year", y="Recharge (mm)", color="Zone", width=800, height=400)
        fig.update_yaxes(title="Recharge (mm)", title_font={"size": 18})

        fig1 = px.line(data, x="Year", y="Recharge (m3/s)", color="Zone", width=800, height=400)
        fig1.update_yaxes(title="Recharge (m3/s)", title_font={"size": 18})

    return fig, fig1


@st.cache
def convert_df(df):
    return pd.pivot_table(df, values="Recharge (mm)", index="Year", columns=df.columns[1]).to_csv().encode('utf-8')


@st.cache
def convert_df1(df):
    return pd.pivot_table(df, values="Recharge (m3/s)", index="Year", columns=df.columns[1]).to_csv().encode('utf-8')


#%% Sidebar
st.sidebar.title("BMRecharge Inputs")
mtype = st.sidebar.selectbox("Select data type:", ("About", "Basin-wide", "Aquifers", "Zones"))


if mtype == "About":
    with open(os.path.join(root, "about_en.md"), "r") as fid:
        about_text = fid.read()
    st.markdown(about_text)
    st.image(Image.open(os.path.join(root, "img", "logo.png")), width=250)

else:
    dname  = st.sidebar.selectbox("Select database:", ("CHIRPS-Daymet", "CHIRPS", "CHIRPSC", "Ground Gauges"))
    cmap = st.sidebar.selectbox("Select a map's color gradient:", ("Spectral", "YlGnBu", "Viridis"))

    # generate objetcs
    fig1 = create_map(mtype, dname, cmap, layers, attributes)
    fig2, fig3 = create_timeserie(mtype, dname, attributes)
    timeseries = read_serie(mtype, dname, attributes)

    #%% Create output
    st.title("BMRecharge - Basin of Mexico Recharge App")

    # Map
    st.subheader("Interactive map of annual potential recharge")
    st.markdown("""

    Use the cursor to query the values and propperties in the map.
    
    You can push the play and stop buttons below the map to animate the map.""")
    st.plotly_chart(fig1, use_container_width=True)

    # Timeseries
    if mtype == "Basin-wide":
        zone_type = "Basin of Mexico"
    else:
        zone_type = mtype
    
    st.subheader("Annual Recharge Equivalent Thickness")
    st.markdown(f"The time series of recharge equivalent thickness were computed by averaging the gridded modeled recharge over the {zone_type} extension.")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Annual Recharge Rate")
    st.markdown(f"The Annual Recharge Equivalent Thickness time series were multiplied by {zone_type} areas and divided by the seconds in a year.")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Recharge statistics
    st.subheader("Annual Recharge Average")
    st.markdown("The following table contains the average values of the annual potential recharge obtained from the time series shown above.")
    st.table(timeseries.iloc[:, 1:].groupby(timeseries.columns[1]).mean().round(3))

    # Output data
    st.subheader("Download Data")
    st.markdown("Select the annual time-series to download.")
    if mtype == "Basin-wide":
        saveas  = f"MexicoBasin_Average_Recharge_mm.csv"
        saveas1 = f"MexicoBasin_Average_Recharge_m3-s.csv"
    else:
        saveas  = f"{mtype}_{dname}_Recharge_mm.csv"
        saveas1 = f"{mtype}_{dname}_Recharge_m3-s.csv"

    output = convert_df(timeseries)
    st.download_button(
        label=f"Download Recharge in mm (csv)",
        data=output,
        file_name=saveas,
        mime="text/csv",
    )

    output1 = convert_df1(timeseries)
    st.download_button(
        label=f"Download Recharge in m3-s (csv)",
        data=output1,
        file_name=saveas1,
        mime="text/csv",
    )


