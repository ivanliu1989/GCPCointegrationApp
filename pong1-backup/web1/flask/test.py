import src.lib.connecttodb as connecttodb
import src.lib.getpair as getpair
import pandas
import numpy as np
import pygal
from pygal.style import DarkStyle


kind = 'EUR_USD'
df = getpair.getalldata(kind)

tuples = [tuple(x) for x in df[['time',kind]].values]
from pygal.style import Style
custom_style = Style(
background='black',
plot_background='transparent',
foreground='#53E89B',
foreground_strong='#53A0E8',
foreground_subtle='#630C0D',
opacity='.6',
opacity_hover='.9',
transition='400ms ease-in',
colors=('rgba(255, 45, 20, .3)', 'rgba(92, 213, 255, .3)', 'yellow', '#E89B53'))
graph = pygal.DateTimeLine(
    x_label_rotation=0, truncate_label=-1,spacing=0,width=40000,height=500,
    x_value_formatter=lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'), style=custom_style)


dfforecast = pandas.DataFrame(connecttodb.selectforecast(kind))

result = df.append(dfforecast, ignore_index=True)
result.sort_values(['time'], ascending=[True], inplace=True)
v = []
for i in range(len(result)):
	if np.isnan(result[kind].iloc[i]):
		v.append(v[len(v)-1])
	else:
		v.append(result[kind].iloc[i])
result['value'] = v
#result = result.dropna(subset=[kind])

dfdown = result[result['predict']=='down']
#dfdown['c'] = df[kind].mean()
#dfdown = dfdown.dropna(axis=0, how='any')
tuples2 = [tuple(x) for x in dfdown[['time','value']].values]
graph.add('down', tuples2, show_dots=True, dots_size=10, stroke=False)

dfup = result[result['predict']=='up']
#dfup['c'] = df[kind].mean()
#dfup = dfup.dropna(axis=0, how='any')
tuples3 = [tuple(x) for x in dfup[['time','value']].values]
graph.add('up', tuples3, show_dots=True, dots_size=10, stroke=False)

graph.add(kind, tuples, show_dots=True, dots_size=2, stroke=False)

print (dfdown)
print (dfup)