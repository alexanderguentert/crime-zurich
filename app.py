# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import functions as f # functions for data handling


# texts to be shown in the app.
tabtitle = '''Kriminalität Kanton Zürich'''
header = '''Kriminalitätsentwicklung im Kanton Zürich'''
intro_text = '''Kriminalitätsentwicklung im Kanton Zürich. Aufbereitung der Tabellen aus dem statistischen Jahrbuch des Kantons Zürich. Die Originaldaten finden Sie [hier](https://statistik.zh.ch/internet/justiz_inneres/statistik/de/daten/tabellen.html?tbname=D5-101).'''
titles_chart_1 = '''Entwicklung aller Straftaten zusammengefasst'''
titles_chart_2 = '''Verschiedene Kategorien von Straftaten im Vergleich'''
sub_titles_chart_2 = '''Bitte beachten Sie, dass aus Gründen der Lesbarkeit die y-Achse in den folgenden Darstellungen logarithmisch dargestellt wird.'''
titles_chart_3  = '''Vergleich der Unterkategorien'''
sub_titles_chart_3 = '''Wählen Sie eine Kategorie um mehr über die zugehörigen Straftaten zu erfahren:'''
footnotes = '''Fussnoten:

¹: Ehrverletzungsdelikte werden neu ab 1.1.2011 durch die Polizei/Staatsanwaltschaften und nicht mehr durch den Friedensrichter untersucht.
Quelle: Polizeiliche Kriminalstatistik (PKS)

Hinweis: Ab 1. Januar 2009 ersetzt die Polizeiliche Kriminalstatistik (PKS) die Kriminalstatistik des Kantons Zürich (KRISTA). Mit der PKS wurde landesweit eine nach einheitlichen Kriterien und Regeln erfasste und auswertbare Kriminalstatistik eingeführt.

Datenquelle: https://statistik.zh.ch/internet/justiz_inneres/statistik/de/daten/tabellen.html?tbname=D5-101

Erstellt durch: Alexander Güntert (https://github.com/alexanderguentert)'''



#### data handling
crime = f.get_data(download=True)

# plot for total crimes
total_crimes_plot = f.chart_total_crimes(crime)

# levels
crime_super = f.add_levels(crime)
# select only superordinate categories
crime_super = crime_super[crime_super['Ebene'].notna()]
# drop level columns
crime_super = crime_super.drop(['Ebene','Unterebene'],axis='columns')
crime_super_plot = f.chart(f.preprocessing_chart(crime_super))

# list for dropdown
list_levels = crime_super['Art der Straftat']


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# Layout
app.layout = html.Div(children=[
    html.H1(children=header),
    dcc.Markdown(children=intro_text),
    html.H3(children=titles_chart_1),
	dcc.Graph(id='total_crimes',figure=total_crimes_plot),
	html.H3(children=titles_chart_2),
    dcc.Markdown(children=sub_titles_chart_2),
	dcc.Graph(id='crimes_ueber',figure=crime_super_plot),
    html.H3(children=titles_chart_3),
    dcc.Markdown(children=sub_titles_chart_3),
	dcc.Dropdown(
		id='dropdown_levels',
		options=[{'label': i, 'value': i} for i in list_levels],
		value=list_levels[0]),
	dcc.Graph(id='crimes_sub',),#figure=crime_sub_plot),
    dcc.Markdown(children=footnotes)
])

# Callbacks for updating graphs
@app.callback(
	dash.dependencies.Output('crimes_sub', 'figure'),
	[dash.dependencies.Input('dropdown_levels', 'value')]
	)

def update_crimes_sub(dropdown_levels):
    '''
    Update plot for sub levels.
    '''
    sub = f.select_sub(crime,dropdown_levels)
    crime_sub_plot = f.chart(f.preprocessing_chart(sub))
    return crime_sub_plot

if __name__ == '__main__':
    app.run_server(debug=True)
