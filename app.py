import folium
import pandas as pd

def confirmed_rate(n=30):
    corona_df = pd.read_csv("india.csv")
    by_country = corona_df.groupby('Province_State').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    return cdf

def zone_color(recovered_rate):
    if recovered_rate >= 90:
        return 'green'
    elif recovered_rate >= 50:
        return 'yellow'
    else:
        return 'red'

def circle_maker(x):
    recovered_rate = (x[4] / x[2]) * 100
    color = zone_color(recovered_rate)
    folium.Circle(location=[x[0], x[1]],
                  radius=float(x[2]),
                  color=color,
                  fill=True,
                  fill_color=color,
                  popup='Confirmed cases: {}<br>Death cases: {}<br>Recovered cases: {}<br>Recovered rate: {:.2f}%'.format(x[2], x[3], x[4], recovered_rate)).add_to(m)

cdf = confirmed_rate()
pairs = [(country, confirmed, death, recovered, active) for country, confirmed, death, recovered, active in zip(cdf.index, cdf['Confirmed'], cdf['Deaths'], cdf['Active'], cdf['Recovered'])]

corona_df = pd.read_csv("india.csv")
corona_df = corona_df[['Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
corona_df = corona_df.dropna()
# print(corona_df) #to check does the correct path is given

m = folium.Map(location=[19.663280, 75.300293], tiles='Stamen Terrain', zoom_start=5)

corona_df.apply(lambda x: circle_maker(x), axis=1)

html_map = m._repr_html_()

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", table=cdf, cmap=html_map, pairs=pairs)

if __name__ == "__main__":
    app.run(debug=False)