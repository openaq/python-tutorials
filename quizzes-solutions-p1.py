# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "marimo>=0.19.9",
#     "openaq==1.0.3",
#     "pandas==3.0.1",
#     "wigglystuff==0.2.34",
#     "vegafusion>=2.0.3",
#     "vl-convert-python>=1.8.0",
#     "pyarrow==23.0.1",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from datetime import datetime
    from pprint import pprint
    from openaq import OpenAQ
    return OpenAQ, datetime, mo, pprint


@app.cell
def _(OpenAQ):
    client = OpenAQ(api_key="YOUR-API-KEY-HERE")
    return (client,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz 1:** How many PM2.5 monitoring locations in Ghana do we have on OpenAQ? Answer with one single request to the API, knowing that the parameters_id for PM2.5 is 2. Replace the 'TODO' string in the cell below to print out the number of PM2.5 locations in Ghana.
    """)
    return


@app.cell
def _(client):
    # Hint: review the Locations resource documentation
    ghana_pm25_locations_quiz = client.locations.list(iso="GH", parameters_id=2, limit=1000).meta.found
    ghana_pm25_locations_quiz
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz 2:** How many air quality monitoring stations are there in your country that are on OpenAQ?
    """)
    return


@app.cell
def _(client):
    homecountry_locations_quiz = client.locations.list(iso="VN", limit=1000).meta.found
    homecountry_locations_quiz
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz 3:** Using one of the 2 geospatial queries provided in the tutorials, how many PM2.5-monitoring stations are there in your hometown/city that are on OpenAQ? The ID for PM2.5 within OpenAQ database is 2.
    """)
    return


@app.cell
def _(client):
    hometown_pm25_locations_quiz = client.locations.list(
        coordinates=(21.032917,105.856361), 
        radius=10000, 
        limit=1000).meta.found
    hometown_pm25_locations_quiz
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz 4:** What are the sensors_ids from the locations with ID 3025594? Replace the 'TODO' with a single request to the API.
    """)
    return


@app.cell
def _(client, pprint):
    sensors_quiz = client.locations.sensors(3025594)
    pprint(sensors_quiz)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz 5:** As you might have noticed, we could also traverse the LocationsResponse body and get the sensors ID. From the results, can you tell the difference between using .list() and traversing vs. using .sensors()?
    """)
    return


@app.cell
def _(client, pprint):
    # Fetch sensors information by traversing LocationsResponse body
    ghana_locations = client.locations.list(iso="GH", limit=1000)
    pprint(ghana_locations.results[0].sensors)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz 6:** Can you find the 2025 average measurements of PM2.5 at one station in your home country? Alternatively, you can choose any one station in Ghana. Feel free to approach this however you want (using one or multiple cells is fine)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Option 1:** Eye-balling for an appropriate location
    """)
    return


@app.cell
def _(client, pprint):
    # Use this cell to answer Quiz 6
    vietnam_locs = client.locations.list(iso="VN", parameters_id=2, limit=1000)
    pprint(vietnam_locs)
    return


@app.cell
def _(client, pprint):
    yearly_avg = client.measurements.list(sensors_id=21632, data="years", date_from="2025-01-01", date_to="2025-12-31")
    pprint(yearly_avg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Option 2:** Doing it programmatically
    """)
    return


@app.cell
def _(client):
    client.measurements.list(sensors_id=4681, data="years", date_from="2025-01-01", date_to="2025-12-31")
    return


@app.cell
def _(client, datetime):
    # Get all locations from country
    locs = client.locations.list(iso="VN", parameters_id=2, limit=1000).results

    # Pick a location with data available in 2025
    for loc in locs:
        if loc.datetime_first is not None and loc.datetime_last is not None:
            if datetime.fromisoformat(loc.datetime_first.local).replace(tzinfo=None) >= datetime(2025, 1, 1) and datetime.fromisoformat(loc.datetime_last.local).replace(tzinfo=None) <= datetime(2025, 12, 31):
                loc_id = loc.id
                break

    # Get that location's PM2.5 sensor ID
    sensors = client.locations.sensors(loc_id).results
    for sensor in sensors:
        if sensor.parameter.id == 2:
            sensor_id = sensor.id
            break

    # Find yearly measurement
    client.measurements.list(sensors_id=sensor_id, data="years", date_from="2025-01-01", date_to="2025-12-31")
    return


if __name__ == "__main__":
    app.run()
