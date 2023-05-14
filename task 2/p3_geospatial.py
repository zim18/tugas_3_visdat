import pandas as pd
import requests
import us
from tzwhere import tzwhere

# Load the data from USAir97v2.json
data = pd.read_csv("USAir97.csv")

# Convert 'id' column to integer
data['id'] = data['id'].astype('int')

# Define coordinates for each city
coords = {d['id']: (float(d['longitude']), float(d['latitude'])) for _, d in data.iterrows()}

# Define trace for cities
tz = tzwhere.tzwhere()
def get_color_offset(lat, long):
    timezone = tz.tzNameAt(lat, long)
    if timezone is None:
        timezone = 'UTC'
    tz_offset = pd.Timestamp.now(tz=timezone).utcoffset()
    if tz_offset is None:
        tz_offset = pd.Timestamp.now(tz='UTC').utcoffset()
    tz_offset_hours = tz_offset.total_seconds() / 3600
    return tz_offset_hours

trace_cities = dict(
    type='scattergeo',
    lat=[coords[d['id']][1] for _, d in data.iterrows()],
    lon=[coords[d['id']][0] for _, d in data.iterrows()],
    text=[d['id'] for _, d in data.iterrows()],
    mode='markers',
    marker=dict(
        size=5,
        color=[get_color_offset(d['latitude'], d['longitude']) for _, d in data.iterrows()],
        colorscale='Jet',
        colorbar=dict(
            title='Time Zone Offset (Hours)'
        )
    )
)

# Define layout for map
layout_map = dict(
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
        showland=True,
        landcolor='rgb(217, 217, 217)',
        subunitcolor='rgb(255, 255, 255)',
        countrycolor='rgb(255, 255, 255)',
        countrywidth=0.5,
        subunitwidth=0.5
    ),
    title='US Airports',
    autosize=False,
    width=1200,
    height=800,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4
    )
)

# Create figure for map
fig_map = dict(data=[trace_cities], layout=layout_map)

# Display map
import plotly.graph_objs as go
from plotly.offline import iplot

iplot(fig_map)