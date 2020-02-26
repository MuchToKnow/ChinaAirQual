import plotly.express as px
from pymongo import MongoClient
import time
client = MongoClient()
db = client.chinaAir

# Aggregates data in mongo into scatter plot with timespan size averaged values and saves chart as a png
# timespan: Number of seconds for aggregation window (eg: 3600 will aggregate hourly, 86400 for daily)
# dataKey: key for data of interest e.g. 'pm25', 'so2'
# dpat (Data point aggregation threshold): Number of datapoints required to be averaged out and included as a point in the graph
def aggregateData(timespan=3600, dataKey='pm25', dpat=30):
  currentTime = 0
  timeString = ""
  currentCount = 0
  currentTotal = 0
  times = []
  pm25averages = []
  for doc in db.air.find().sort('time.v'):
    t = int(doc['time']['v'])
    pm25 = float(doc['iaqi'][dataKey]['v'])
    ts = doc['time']['s']
    if currentTime == 0:
      currentTime = t
      timeString = ts
    # Need to average and count value if we have passed our data window
    elif t >= currentTime + timespan:
      # Make sure we have enough datapoints for a valid average
      if currentCount > dpat-1:
        times.append(timeString)
        pm25averages.append(currentCount/currentTotal)
      currentCount = pm25
      currentTotal = 1
      currentTime = t
      timeString = ts
    else:
      currentTotal += 1
      currentCount += pm25

  # Append the last datapoint after the forloop
  if currentCount > dpat-1:
    times.append(timeString)
    pm25averages.append(currentCount/currentTotal)

  # Create chart and write it to this directory for now
  fig = px.scatter(x=times, y=pm25averages)
  fig.update_layout(title="Average " + dataKey + " of top 50 chinese cities by population aggregated every " + str(timespan) + " seconds",
  xaxis_title="Time",
  yaxis_title=dataKey)
  fig.write_image("./images/" + str(currentTime) + dataKey +  ".png")

aggregateData(dataKey="pm10")
