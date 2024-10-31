import plotly.express as px
import pandas as pd
import country_converter as coco

# Read data
df_trustpilot = pd.read_csv('data/data_trustpilot.csv', engine='python')

# Aggregate ratings by location
location_ratings = df_trustpilot.groupby('location')['rating'].mean().reset_index()

# Convert ISO-2 to ISO-3 country codes
cc = coco.CountryConverter()
location_ratings['location_iso3'] = cc.convert(location_ratings['location'], to='ISO3')

# Create choropleth map
fig = px.choropleth(location_ratings,
                    locations='location_iso3',  # Use the new ISO-3 column
                    locationmode='ISO-3',  # Now we can use ISO-3
                    color='rating',
                    color_continuous_scale="RdYlGn",
                    range_color=(1, 5),
                    title='Average Ratings by Country',
                    labels={'rating': 'Average Rating'}
                    )

# Update layout
fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0},
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
)

print("\nRating statistics:")
print(location_ratings['rating'].describe())

fig.show()