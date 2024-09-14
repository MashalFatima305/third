#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import altair as alt
import os

# Enable VegaFusion data transformer
alt.data_transformers.enable("vegafusion")

# Define the path to your CSV file
file_path = os.path.expanduser('Downloads/altman_z_scores.csv')

# Check if the file exists in the specified path
if os.path.exists(file_path):
    # Load data from the CSV file
    df = pd.read_csv(file_path)

    # Clean column names to remove any extra spaces or newline characters
    df.columns = df.columns.str.strip()

    # Add a Period column with numerical values ranging from 1 to the length of the dataframe
    df['Period'] = range(1, len(df) + 1)

    # Ensure the Altman Z-Score column is numeric
    df['Altman Z-Score'] = pd.to_numeric(df['Altman Z-Score'], errors='coerce')

    # Streamlit app
    st.title('Altman Z-Score Dashboard')

    # Display the data
    st.write(df)

    # Function to plot Altman Z-Score
    def plot_altman_z_score(data):
        # Define the safe zone (> 2.99) and distress zone (< 1.81)
        safe_zone = 2.99
        distress_zone = 1.81

        # Create the base chart
        base = alt.Chart(data).encode(
            x=alt.X('Period:Q', title='Period'),  # Use the 'Period' column for the x-axis
            y=alt.Y('Altman Z-Score:Q', title='Altman Z-Score')  # Ensure your CSV has the correct column name
        )

        # Line chart for Altman Z-Score
        line = base.mark_line().encode(
            tooltip=['Period', 'Altman Z-Score']
        )

        # Safe zone
        safe = alt.Chart(pd.DataFrame({'y': [safe_zone]})).mark_rule(color='green').encode(y='y:Q')

        # Distress zone
        distress = alt.Chart(pd.DataFrame({'y': [distress_zone]})).mark_rule(color='red').encode(y='y:Q')

        # Combine the charts
        chart = alt.layer(line, safe, distress).properties(
            title='Altman Z-Score Over Time',
            width=800,
            height=400
        ).interactive()

        return chart

    # Display the chart
    chart = plot_altman_z_score(df)
    st.altair_chart(chart, use_container_width=True)

else:
    st.error(f"File not found at {file_path}. Please check the path.")


# In[ ]:




