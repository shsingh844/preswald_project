from preswald import connect, get_df
from preswald import query
from preswald import table, text
from preswald import plotly
import plotly.express as px

# 1. Connect to data source
connect()  # Initialize connection to preswald.toml data sources
df = get_df('solar_data')  # Load solar data

# 2. Query the data
# Query for large-scale solar installations (over 100 acres) in rural areas
sql = """
SELECT * FROM solar_data 
WHERE Acres > 100 AND "Urban or Rural" = 'Rural'
"""
filtered_df = query(sql, 'solar_data')

# 3. Build an interactive UI
text("# Solar Installation Analysis")
text("## Large Rural Solar Installations (>100 acres)")
table(filtered_df, title="Filtered Solar Data")

# 4. Create a visualization
# Create a scatter plot comparing installation size to distance from substations
fig = px.scatter(
    df, 
    x="Acres", 
    y="Distance to Substation (Miles) GTET 100 Max Voltage",
    color="Install Type",
    hover_data=["County", "Combined Class", "Solar Technoeconomic Intersection"],
    title="Solar Installation Size vs. Distance to Substation"
)
fig.update_layout(
    xaxis_title="Installation Size (Acres)",
    yaxis_title="Distance to Substation (Miles)"
)
plotly(fig)

# 5. Additional insights
text("## Summary Statistics")
county_counts = df['County'].value_counts().head(10).reset_index()
county_counts.columns = ['County', 'Number of Installations']

text("Top 10 Counties by Number of Solar Installations:")
table(county_counts)

# Create a bar chart for county distribution
county_fig = px.bar(
    county_counts, 
    x='County', 
    y='Number of Installations',
    title="Solar Installations by County"
)
plotly(county_fig)
