#!/usr/bin/env python
# coding: utf-8

# In[1]:


# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# Load your data
df = pd.read_csv(r"D:\Rohini Personal\Data Analysis\Projects Datasets\Zones\test data.csv")


# In[ ]:


st.sidebar.header("Filters")

batsman = st.sidebar.selectbox(
    "Select Batsman", ["All"] + sorted(df["BatsmanName"].unique())
)
bowler = st.sidebar.selectbox(
    "Select Bowler",  ["All"] + sorted(df["BowlerName"].unique())
)
bat_team = st.sidebar.selectbox(
    "Select Batting Team", ["All"] + sorted(df["BattingTeam"].unique())
)
bowl_team = st.sidebar.selectbox(
    "Select Bowling Team", ["All"] + sorted(df["BowlingTeam"].unique())
)

# -------------------------------------------------------------------
# 3. APPLY FILTERS
# -------------------------------------------------------------------
filtered = df.copy()
if batsman != "All":
    filtered = filtered[filtered["BatsmanName"] == batsman]
if bowler != "All":
    filtered = filtered[filtered["BowlerName"] == bowler]
if bat_team != "All":
    filtered = filtered[filtered["BattingTeam"] == bat_team]
if bowl_team != "All":
    filtered = filtered[filtered["BowlingTeam"] == bowl_team]

# -------------------------------------------------------------------
# 4. ASSIGN ZONES (using CreaseY / CreaseZ)
# -------------------------------------------------------------------
def assign_zone(row):
    x, y = row["CreaseY"], row["CreaseZ"]
    if 0 <= x < 7 and 0 <= y < 28:
        return "Zone 1"
    elif 7 <= x < 14 and 0 <= y < 11:
        return "Zone 2"
    elif 14 <= x <= 21 and 0 <= y < 11:
        return "Zone 3"
    elif 7 <= x < 14 and 11 <= y < 21:
        return "Zone 4"
    elif 14 <= x <= 21 and 11 <= y < 21:
        return "Zone 5"
    elif 7 <= x <= 21 and 21 <= y <= 28:
        return "Zone 6"
    else:
        return "Other"

filtered["Zone"] = filtered.apply(assign_zone, axis=1)
filtered = filtered[filtered["Zone"] != "Other"]

# -------------------------------------------------------------------
# 5. TOTAL RUNS PER ZONE
# -------------------------------------------------------------------
zone_runs = (
    filtered.groupby("Zone")["Runs"]
    .sum()
    .reindex(["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6"])
    .fillna(0)
)

# -------------------------------------------------------------------
# 6. DRAW PITCH MAP WITH TOTAL RUNS
# -------------------------------------------------------------------
zones_layout = {
    "Zone 1": (0, 0, 7, 28),
    "Zone 2": (7, 0, 7, 11),
    "Zone 3": (14, 0, 7, 11),
    "Zone 4": (7, 11, 7, 10),
    "Zone 5": (14, 11, 7, 10),
    "Zone 6": (7, 21, 14, 7),
}
colors = ['#FFCCCC', '#CCFFCC', '#CCCCFF', '#FFFFCC', '#FFCCFF', '#CCE5FF']

fig, ax = plt.subplots(figsize=(7, 10))

for (zone, (x, y, w, h)), color in zip(zones_layout.items(), colors):
    ax.add_patch(
        patches.Rectangle((x, y), w, h, edgecolor="black",
                          facecolor=color, linewidth=2)
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        f"{zone}\nRuns: {int(zone_runs.get(zone, 0))}",
        ha="center",
        va="center",
        weight="bold",
    )

ax.set_xlim(0, 22)
ax.set_ylim(0, 28)
ax.set_xlabel("CreaseY (Width of Pitch)")
ax.set_ylabel("CreaseZ (Length of Pitch)")
ax.set_title("Zone‑wise Runs (custom 6‑zone layout)")
ax.grid(True)

st.pyplot(fig)

