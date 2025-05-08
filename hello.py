from preswald import connect, get_df
from preswald import query
from preswald import table, text
from preswald import plotly
import plotly.express as px
import pandas as pd

# 1. Connect to data source
connect()  # Initialize connection to preswald.toml data sources
df = get_df('solar_data')  # Load solar data

# First, ensure we're using the correct column name
distance_col = "Distance to Substation (Miles) GTET 100 Max Voltage"

# Convert Acres to numeric
df['Acres'] = pd.to_numeric(df['Acres'], errors='coerce')

# Convert Distance to numeric
df[distance_col] = pd.to_numeric(df[distance_col], errors='coerce')

# 2. Query the data with explicit casting
# Query for large-scale solar installations (over 100 acres) in rural areas
sql = """
SELECT * FROM solar_data 
WHERE CAST(Acres AS FLOAT) > 100 AND "Urban or Rural" = 'Rural'
"""

try:
    # Try the SQL query with casting
    filtered_df = query(sql, 'solar_data')
except Exception as e:
    # Fallback to pandas if SQL fails
    text(f"SQL query error: {str(e)}")
    text("Using pandas filtering instead...")
    # Filter using pandas
    filtered_df = df[(df['Acres'] > 100) & (df['Urban or Rural'] == 'Rural')]

# 3. Build an interactive UI
text("# Solar Installation Analysis")
text("## Large Rural Solar Installations (>100 acres)")
text(f"Found {len(filtered_df)} large rural installations")
table(filtered_df, title="Filtered Solar Data")

# 4. Create an improved visualization
text("## Installation Size vs. Distance to Substation")

# Create an improved scatter plot
fig = px.scatter(
    df, 
    x="Acres", 
    y=distance_col,  # Use the variable for consistency
    color="Install Type",
    hover_data=["County", "Combined Class", "Solar Technoeconomic Intersection"],
    title="Solar Installation Size vs. Distance to Substation"
)

# Improve the layout and formatting
fig.update_layout(
    xaxis_title="Installation Size (Acres)",
    yaxis_title="Distance to Substation (Miles)",
    xaxis=dict(
        range=[0, max(df['Acres'])*1.1],  # Add 10% padding to max value
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
    ),
    yaxis=dict(
        range=[0, min(20, df[distance_col].quantile(0.95))],  # Fixed this line - use the same column name variable
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
    ),
    plot_bgcolor='white',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(l=20, r=20, t=40, b=20),
)

# Add a reference line for a reasonable substation distance
fig.add_hline(y=5, line_dash="dash", line_color="red", 
              annotation_text="5 mile reference", 
              annotation_position="bottom right")

plotly(fig)

# 5. Additional insights
text("## Summary Statistics")
county_counts = df['County'].value_counts().head(10).reset_index()
county_counts.columns = ['County', 'Number of Installations']

text("Top 10 Counties by Number of Solar Installations:")
table(county_counts)

# Create an improved bar chart for county distribution
county_fig = px.bar(
    county_counts, 
    x='County', 
    y='Number of Installations',
    title="Solar Installations by County",
    color='Number of Installations',
    color_continuous_scale='Viridis',
)

county_fig.update_layout(
    xaxis_title="County",
    yaxis_title="Number of Installations",
    plot_bgcolor='white',
    bargap=0.2,
)

plotly(county_fig)

# 6. Add a histogram for installation sizes
text("## Distribution of Solar Installation Sizes")
hist_fig = px.histogram(
    df, 
    x="Acres",
    nbins=50,
    color="Install Type",
    title="Distribution of Solar Installation Sizes",
    marginal="box"  # Add a box plot on the margin
)

hist_fig.update_layout(
    xaxis_title="Installation Size (Acres)",
    yaxis_title="Count",
    bargap=0.1,
    plot_bgcolor='white',
)

plotly(hist_fig)