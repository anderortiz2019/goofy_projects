import matplotlib.pyplot as plt

#  data
Year = ['\'95',	'\'96',	'\'97',	'\'98',	'\'99',	'\'00',	'\'01',	'\'02',	'\'03',	'\'04',	'\'05',	'\'06',	
        '\'07',	'\'08',	'\'09',	'\'10',	'\'11',	'\'12',	'\'13',	'\'14',	'\'15',	'\'16',	'\'17',	'\'18',	'\'19',
        '\'20',	'\'21',	'\'22',	'\'23']

values = [1, 0,	0,	9,	4,	6,	6,	4,	6,	6,	6,	4,	3,	5,	1,	3,	3,	7,	1,	3,	0,	4,	3,	4,	6,	11,	5,	3,	0]

# Create figure and axes
fig, ax = plt.subplots()

# Plot the bar graph
bars = ax.bar(Year, values, color='white')

# Set the background color of the figure to black
fig.set_facecolor('black')

# Set the face color of the axes to white
ax.set_facecolor('black')

# Set the color of the bars to black
for bar in bars:
    bar.set_color('white')

# Set the color of the tick labels to white
ax.tick_params(axis='both', colors='white')

# Set the color of the axes labels to white
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.title.set_color('white')


# Set the background color to black
fig.set_facecolor('black')

# Create a bar graph
plt.bar(Year, values, color='cornflowerblue', alpha=0.5)

# Adding labels and title
plt.xlabel('Year',)
plt.ylabel('Number of Tropical Cyclones',)
plt.title('Tropical Cyclones in the Atlantic Basin That Have Undergone Extratropical Transition Since 1995', fontsize=9, y=1.02)

# data labels
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2),
        ha='center', va='bottom', color='white', fontsize=7.5)

# Set the font size of the year labels on the x-axis
plt.xticks(fontsize=6)

# Add a white border around the entire graph
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

# Display the graph
plt.show()
