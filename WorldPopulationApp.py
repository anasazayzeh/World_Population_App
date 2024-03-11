# World Population App
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt 
import numpy as np



# Read the CSV data
df = pd.read_csv("Data.csv", dtype={"Year": object})
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
#df ["Year"] = try_convert_to_numeric("Year", errors='coerce')

# Clean commas in the Year column
#df["Year"] = df["Year"].str.replace(",", "", regex=True)

chart_data = df[["Year", "Population", "PopulationGrowth"]]  

df['Year'].dtype 

df['Population'].dtype 
df['PopulationGrowth'].dtype 
df['Density (Pop/km2)'].dtype 


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

class MyDataObject:
  def __init__(self, value):
    self.value = value


selected_year = MyDataObject(selected_year)

# Function to display population based on selected year
def display_population(selected_year):
  # Filter DataFrame for the chosen year
  filtered_df = new_df[new_df['Year'] == selected_year]

  # Check if any data found for the year
  if filtered_df.empty:
    st.write(f"No data found for year {selected_year}.")
  else:
    # Get population value (assuming a single 'Population' column)
    population = filtered_df['Population'].values[0]
    YearlyGrowth  = filtered_df['Yearly Growth %'].values[0]  # Assuming another column for chart

    st.write(f"Population for year {selected_year}: {population}")

  # Create your desired chart (replace with your chart type and customization)
    plt.figure(figsize=(5, 9))
    plt.bar(selected_year, population, color='skyblue')  # Example bar chart
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title(f"Population in {selected_year}")
    plt.grid(True)
    st.pyplot()

display_population(selected_year)



def create_chart(selected_series):
  plt.figure(figsize=(8, 5))  # Set chart size (optional)
  plt.plot(new_df['Year'], new_df[selected_series])
  plt.xlabel('Year')
  plt.ylabel(selected_series)
  plt.title(f"{selected_series} Over Time")
  plt.grid(True)
  # Customize your chart further (e.g., colors, markers, legends)
  st.pyplot()  # Display the chart in Streamlit


# You can use st.write, st.chart etc. to display data

