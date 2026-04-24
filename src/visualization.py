import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FixedLocator

# read processed_data
processed_df = pd.read_csv("data/processed/processed_data.csv")

# change device code to name for readability
device_name = {'b8:27:eb:bf:9d:51': 'Device A',
    '00:0f:00:70:91:0a': 'Device B',
    '1c:bf:ce:15:ec:4d': 'Device C'
}
processed_df['device']= processed_df['device'].map(device_name)

# colour dictionary to keep colour of each device consistent
device_palette = {
    'Device A': "#66c2a5",  
    'Device B': "#fc8d62", 
    'Device C': '#8da0cb'   
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAGE 4 : DATA VISUALIZATION
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Dashborad using processd data csv for 4 graphs
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Processed Data Graph Overview", fontsize=14)


# GRAPH 1: histogram of temperature with KDE
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
sns.scatterplot(data=processed_df,
                x='co',
                y='smoke',
                hue='device',
                alpha=0.5,
                palette=device_palette,
                ax=axes[1,0])

axes[1,0].set_title("CO vs Smoke by Device")


# GRAPH 4: line graph of temperature over weekday
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
plt.savefig('outputs/figures/dashboard_version1.2.png', dpi=150, bbox_inches='tight')
plt.show()

# GRAPH 5: stacked bar chart of comfort level dy device
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
fig5.savefig('outputs/figures/comfort_distribution.png', dpi=150, bbox_inches='tight')
plt.show()