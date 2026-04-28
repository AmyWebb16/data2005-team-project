import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FixedLocator

# read processed_data
processed_df = pd.read_csv("data/processed/processed_data.csv")
comfort = pd.read_csv('data/processed/comfort.csv')
anomalies = pd.read_csv('data/processed/anomalies.csv')

# change device code to name for readability
device_name = {'b8:27:eb:bf:9d:51': 'Device A',
    '00:0f:00:70:91:0a': 'Device B',
    '1c:bf:ce:15:ec:4d': 'Device C'
}
processed_df['device']= processed_df['device'].map(device_name)

# remap device names for comfort graph
comfort["device"] = comfort["device"].map({
    'Sensor A': 'Device A',
    'Sensor B': 'Device B',
    'Sensor C': 'Device C'
})

# remap device names for anomalies graph
anomalies["device"] = anomalies["device"].map({
    'Sensor A': 'Device A',
    'Sensor B': 'Device B',
    'Sensor C': 'Device C'
})

# colour dictionary to keep colour of each device consistent
device_palette = {
    'Device A': "#66c2a5",  
    'Device B': "#fc8d62", 
    'Device C': '#8da0cb'   
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAGE 4 : DATA VISUALIZATION
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""Create six graphs from processed data csv:
    dashborad with 4 graphs (temp distribution, motion counts, CO vs smoke, temp by weekday)
    comformt distribution (stacked bar chart by device comfort levels)
    heatmap of anomalies (anomaly count by device and time of day)
"""

# Dashborad using processd data csv for 4 graphs
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Processed Data Graph Overview", fontsize=14)


# GRAPH 1: histogram of temperature with KDE
""" Histogram with KDE showing temperature distribution for each device.
    Shows each device's readings obey normal distribution and highlights ranges.
 """

sns.histplot(data=processed_df,
            x='temp',
            hue='device',
            kde=True,
            ax=axes[0,0],
            alpha =0.5,
            palette=device_palette)

axes[0,0].set_title("Temperature Distribution by Device")
axes[0,0].set_xlabel("Temperature (°C)")


# GRAPH 2: number of motions per device
""" Bar chart of sum of motion detection per device.
    Only true rows are shown, so shows when device is triggered.
"""
sns.countplot(data=processed_df[processed_df['motion'] == True],
              x='device',
              hue='device',
              palette=device_palette,
              ax=axes[0,1],
              legend=False)

axes[0,1].set_title("Number of Motions per Device")
axes[0,1].set_xlabel("Device")
axes[0,1].set_ylabel("Count")
axes[0,1].tick_params(axis="x",labelsize=8, rotation=0)


# GRAPH 3: scatter of CO2 vs Smoke (coloured per device)
""" Scater plot of CO vs Smoke coloured by device.
    Shows correlation between the two gases and how it differs by device.
"""
sns.scatterplot(data=processed_df,
                x='co',
                y='smoke',
                hue='device',
                alpha=0.5,
                palette=device_palette,
                ax=axes[1,0])

axes[1,0].set_title("CO vs Smoke by Device")


# GRAPH 4: line graph of temperature over weekday
""" Line graph of mean temp per weekday with 95% confidence intervals.
    x-axis ordered by Monday-Sunday.
"""
weekday_order = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# cast so order is maintained
processed_df['weekday'] = pd.Categorical(processed_df['weekday'], categories=weekday_order, ordered=True)

sns.lineplot(data=processed_df,
             x='weekday',
             y='temp',
             hue='device',
             palette=device_palette,
             linewidth=2,
             marker='o',
             errorbar='ci',
             ax=axes[1,1])

axes[1,1].set_title("Temperature by Weekday (mean =/- 95% CI)")
axes[1,1].set_xlabel("Weekday")
axes[1,1].set_ylabel("Temperature (°C)")
axes[1,1].xaxis.set_major_locator(FixedLocator(range(len(weekday_order))))
axes[1,1].set_xticklabels(weekday_order, rotation=0)
axes[1,1].legend(title="Device", loc="upper right", framealpha=0.5)

plt.tight_layout()
plt.savefig('outputs/figures/dashboard_v1.2.png', dpi=150, bbox_inches='tight')
plt.show()

# GRAPH 5: stacked bar chart of comfort level dy device
""" Stacked bar chaty showing comfortable vs uncomfortable records 
    per device using std thersholds in analyse phase.
"""
fig5, ax5 = plt.subplots(figsize=(7, 5))
comfort_counts = comfort.groupby(['device', 'comfort']).size().unstack(fill_value=0)

comfort_counts.plot(kind='bar',
                    stacked=True,
                    color=['#66c2a5', '#fc8d62'],
                    edgecolor='white',
                    ax=ax5
                )

ax5.set_title("Comfort Level Distribution by Device")
ax5.set_xlabel("Device")
ax5.set_ylabel("Count")
ax5.legend(title="Comfort Level", loc="upper right")
ax5.tick_params(axis='x', rotation=0)

fig5.tight_layout()
fig5.savefig('outputs/figures/comfort_distribution_v1.1.png', dpi=150, bbox_inches='tight')
plt.show()

# GRAPH 6:  heatmap of anomalies by device and hour of day
""" Heatmap showing anomaly counts and what hour of the dat the occur. 
    Tick labels shown every 3 hours to reduce overcroeding.
"""

fig6, ax6 = plt.subplots(figsize=(16, 5))

anomalies['hour'] = pd.to_datetime(anomalies['time'],format='mixed').dt.hour
anomaly_counts = anomalies.groupby(['device', 'hour']).size().unstack(fill_value=0)
anomaly_counts = anomaly_counts.reindex(columns=range(24), fill_value=0)

ax = sns.heatmap(
    anomaly_counts,
    cmap='Reds',
    annot=True,
    fmt='d',
    linewidths=0.4,
    linecolor='white',
    cbar_kws={'label': 'Anomaly count', 'shrink': 0.8, 'pad': 0.02},
    annot_kws={'size': 8},
    ax=ax6
)

ax6.set_title("Anomalies by device and hour of day", fontsize=13, fontweight='medium', pad=12)
ax6.set_xlabel("Hour of day", fontsize=11, labelpad=8)
ax6.set_ylabel("Device", fontsize=11, labelpad=8)

#Every 3 hours for layout to look nicer
hour_labels = [str(h) if h % 3 == 0 else '' for h in range(24)]
ax6.xaxis.set_major_locator(FixedLocator(range(24))) 
ax6.set_xticklabels(hour_labels, rotation=0, fontsize=9)
ax6.set_yticklabels(ax6.get_yticklabels(), rotation=0, fontsize=9)
ax6.tick_params(axis='both', length=0)

fig6.tight_layout(pad=1.5)
fig6.savefig('outputs/figures/heatmapgraph_v1.1.png', dpi=150, bbox_inches='tight')
plt.show()