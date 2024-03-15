# World Population App
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt 
import numpy as np



# Read the CSV data
df = pd.read_csv(r"https://github.com/anasazayzeh/World_Population_App/blob/main/Data.csv", dtype={"Year": object})
df = df.rename(columns={'Number': 'PopulationGrowth'})



# Title for your app
st.title("Interesting facts about world population")

# Add your data visualizations and interesting fact explanations here

st.dataframe(df)

# Clean commas in the Population column
df["Population"] = df["Population"].str.replace(",", "", regex=True)

# Clean commas in the PopulationGrowth column
df["PopulationGrowth"] = df["PopulationGrowth"].str.replace(",", "", regex=True)


def try_convert_to_numeric(column_name, errors='coerce'):
  """Attempts to convert a column to numeric, handling potential errors.

  Args:
      column_name (str): Name of the column to convert.
      errors (str, optional): How to handle non-numeric values. Defaults to 'coerce'.

  Returns:
      pandas.Series: The converted column (numeric) if successful,
                     original column otherwise.
  """
  try:
    return pd.to_numeric(df[column_name], errors=errors)
  except ValueError:
    st.error(f"Error: Could not convert '{column_name}' column to numeric.")
    return df[column_name]  # Return original column if conversion fails
  

df ["Population"] = try_convert_to_numeric("Population", errors='coerce')
df ["PopulationGrowth"] = try_convert_to_numeric("PopulationGrowth", errors='ignore')

# Clean commas in the Year column
#df["Year"] = df["Year"].str.replace(",", "", regex=True)

chart_data = df[["Year", "Population", "PopulationGrowth"]]  

#df['Year'].dtype 

#df['Population'].dtype 
#df['PopulationGrowth'].dtype 
#df['Density (Pop/km2)'].dtype 


#chart_data["Population"] = chart_data["Population"] / 1000000  
st.bar_chart(chart_data, x="Year", y="Population",)
st.bar_chart(chart_data, x="Year", y="PopulationGrowth",)

# Assuming "Area" column stores area values (replace with actual column name)
new_df = df.assign(PopulationArea=df['Population'] / df['Density (Pop/km2)'])

# Display interesting facts (assuming new_df has calculated PopulationDensity (Pop/km2))
st.write("Interesting facts about world population:")
st.write(f"Average population Density (Pop/km2): {new_df['PopulationArea'].mean():.2f}")  # Example: Calculate and display average Density (Pop/km2)

st.dataframe(new_df)

new_chart_data = new_df[["Year", "Population", "PopulationGrowth", "PopulationArea",'Density (Pop/km2)', "Yearly Growth %"]]  

st.bar_chart(new_chart_data, x="Year", y="PopulationArea",)

st.scatter_chart(new_chart_data, 
                 x="Year", 
                 y=["Population","PopulationArea", ],
                  color=None,
                    size="Density (Pop/km2)", 
                    width=0, 
                    height=0, 
                    use_container_width=True)

st.line_chart(new_chart_data, x="Year", y=["PopulationGrowth","PopulationArea"], color=None, width=0, height=0, use_container_width=True)

# Minimum and maximum years from the DataFrame
#min_year = new_df[new_df['Year'] == "1951"]
#max_year = new_df[new_df['Year'] == "2023"]

min_year = new_df['Year'].min()
max_year = new_df['Year'].max()

min_year = int(min_year)
max_year = int(max_year)

# Slider for year selection (integer values)
selected_year = st.slider("Select Year:", min_year , max_year)

# Display the selected year as a label
st.write(f"Selected Year: {selected_year}")



Startyear = 1970  # Example value
Endyear = 2000  # Example value
selected_range = st.slider("Select Range of Years:", min_year, max_year, (Startyear, Endyear))

Startyear = selected_range[0]  # Assuming first element is start year
Endyear = selected_range[1]   # Assuming second element is end year
st.write(f"Selected Years: {Startyear} - {Endyear}")


Startyear = int(selected_range[0])
Endyear = int(selected_range[1])
new_df ["Year"] = try_convert_to_numeric("Year", errors='coerce')


filtered_df = new_df[new_df['Year'].between(Startyear, Endyear)]

filtered_df['Year'] = filtered_df['Year'].astype(str)
filtered_df["Year"] = filtered_df["Year"].str.replace(",", "", regex=True)

st.line_chart(filtered_df, x="Year", y=["PopulationGrowth","PopulationArea"], color=None, width=0, height=0, use_container_width=True)


# You can use st.write, st.chart etc. to display data

