# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "marimo>=0.19.9",
#     "openaq==1.0.0rc2",
#     "pandas==3.0.1",
#     "wigglystuff==0.2.34",
#     "vegafusion>=2.0.3",
#     "vl-convert-python>=1.8.0"
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **OpenAQ Python SDK tutorials**
    - **OpenAQ Python SDK version:** 1.0.0rc2
    - **Last updated:** 2026-03-03
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(f"""
    In this tutorial, we will go over the most common use and workflow of using OpenAQ API via its Python SDK. Each topic, sometimes accompanied by one or more problems, will cover a workflow that serves as the building block for the next topics and attemps to solve those problems. **By the end of the tutorial, you will learn to:**
    - Set up your OpenAQ client in Python to access the API programmatically
    - Use the [OpenAQ Python documentation](https://openaq.github.io/openaq-python/) to help you work with the resources
    - Understand and use the most common resources: Locations, Sensors, and Measurements
    - Integrate OpenAQ Python in your data analysis and visualization pipeline
    - Utilize the API to solve problems for your air quality needs.

    **Before starting this tutorial, make sure that:**
    1. You have the latest version of OpenAQ Python SDK installed: **1.0.0rc2**
        - **If you're on molab:** Click on the box icon (Manage packages) on the sidebar on the left of your molab window
        - **If you're running the tutorials locally and not using marimo notebooks:** run `pip install openaq==1.0.0rc2` on your CLI and run `pip show openaq` once the PC finishes downloading to ensure it is installed correctly. You might also need to install `pandas`, `altair`, `vegafusion`, and `wigglystuff` to get the notebook to work on a non-marimo local deployment.

    2. You have your OpenAQ API key ready. If you don't yet have an API key, you can [register for an account](explore.openaq.org/register) and access you API key via [OpenAQ Explorer account settings page](explore.openaq.org/account).

    3. You are familiar with Python syntax and basic data structures. The tutorial chooses pandas and altair for manipulating and visualizing the data. It is helplful to know them to follow along, but not necessary if you already use other packages for the same purpose and just need to learn how to use the OpenAQ Python SDK.

    **To use this tutorial, you can:**
    - Run each cell and go through them one by one, or,
    - Run all the cells at once and then go through them. Note that there will be an error at first prompting you to input your OpenAQ API key before the rest could be run.

    _This tutorial is designed and maintained by [Minh Nghiem](https://github.com/mngh037). All feedbacks to make this better are welcome and appreciated._
    """)
    return


@app.cell
def _():
    # Import the packages
    import os
    import warnings
    import marimo as mo
    import pandas as pd
    import altair as alt
    import vegafusion
    from openaq import OpenAQ
    from wigglystuff import EnvConfig
    from datetime import datetime
    from pprint import pprint

    warnings.filterwarnings("ignore")
    alt.data_transformers.enable("vegafusion")
    return EnvConfig, OpenAQ, alt, datetime, mo, pd, pprint


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Topic 1: Configure the client**
    The first step to every workflow using OpenAQ API via our Python SDK is to configure the client with your uniquely assigned OpenAQ API key.
    - **Your API key should be known to and used only by you and should not be shared with anyone**. To honor that, this tutorial uses an environment configuration widget to hide personal API key credentials behind a cell's UI.
    - There are 2 ways to configure an OpenAQ client: (1) opening and explicitly closing a connection and (2) using a context manager to handle closing automatically. **Option (1) works best for notebooks and Python REPL tools.**
    """)
    return


@app.cell
def _(EnvConfig, mo):
    # Create an environment configuration widget with a simple checker for OpenAQ API key input. Do not modify.
    def validate_key(api_key):
        """
        Check if key has 64 characters as auto-generated.
        """
        if len(api_key) != 64:
            raise ValueError("API key must be 64 characters")

    configure_env = mo.ui.anywidget(
        EnvConfig(
            {
                "OPENAQ_API_KEY": validate_key
            }
        )
    )
    return (configure_env,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To use the tutorial, you must run the cell below, enter you valid OpenAQ API key in the box that pops up, and hit Enter. [Don't have an API key? Get yours by registering for an account here.](explore.openaq.org/register)
    """)
    return


@app.cell
def _(configure_env):
    configure_env
    return


@app.cell
def _(configure_env):
    # Run simple validation check for valid API key input. Do not modify.
    if not configure_env.all_valid:
        configure_env.require_valid()
    else:
        print("Your OpenAQ API key has been successfully saved as an environment variable. You can proceed with the tutorials.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that your API key is added to the notebook's environment, we will configure an OpenAQ client using that key and test to make sure it works.
    """)
    return


@app.cell
def _(OpenAQ, configure_env):
    # Remember to explicitly close the client connection at the end of your notebook session with `client.close()`
    client = OpenAQ(api_key=configure_env.value["variables"][0]["value"])
    client.locations.get(42)
    return (client,)


@app.cell(disabled=True)
def _(OPENAQ_API_KEY, OpenAQ):
    # Context managers is most convenient for its ability to handle closing the connection automatically for running a Python program. However, they do not work in a notebook or Python REPL tool.
    with OpenAQ(api_key=OPENAQ_API_KEY) as client_context:
        location_context = client_context.locations.get(42)

    location_context # works
    client_context.locations.get(42) # does not work
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The structure of a Response is shared across response types (e.g. `LocationsResponse`, `SensorsResponse`, `MeasurementsResponse`). A Response body typically includes 3 parts, accessible by dot notation: headers, meta, and results. Let's investigate the information provided by each part.
    """)
    return


@app.cell
def _(client, pprint):
    # The .get() method of the Locations resource fetches information about one location
    sample_location = client.locations.get(42)
    pprint(sample_location.headers) # Rate limiting is handled automatically in openaq==1.0.0rc and above
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Topic 2: Query locations in the area of interest**
    The second step typically involves identifying locations or monitoring stations. Depending on your needs, there are 3 ways you can do this with OpenAQ API:
    1. By using filtering with arguments
    2. By using bounding box
    3. By using coordinates and radius

    For this topic, let's find out:

    - **Q2-1.** How many locations in Ghana do we have on OpenAQ?
    - **Q2-2.** How many PM2.5 monitoring locations in Ghana do we have on OpenAQ?
    - **Q2-3.** How many locations in Accra do we have on OpenAQ?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Filtering for locations**

    In the earlier example, we have accessed the Locations resource using a `.get()` method. Now, to answer question 1, we want to get multiple locations. To do this, we access the Locations resource again but now using the `.list()` method.

    Let's learn more about this `.list()` method in our [Python documentation](https://openaq.github.io/openaq-python/).
    """)
    return


@app.cell
def _(client):
    # List of countries' alpha-2 ISO and countries_id: https://docs.openaq.org/resources/countries
    ghana_locations = client.locations.list(iso="GH")
    client.locations.list(countries_id=152)
    return (ghana_locations,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's examine what the LocationsResponse gives us.
    """)
    return


@app.cell
def _(ghana_locations, pprint):
    pprint(ghana_locations)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    By traversing its attributes, we can answer both Q2-1 and Q2-2, and in addition learning another interesting high-level information about air monitoring in Ghana: what pollutants are being measured and how many locations are there readings for each available on OpenAQ?
    """)
    return


@app.cell
def _(ghana_locations):
    # Q2-1
    ghana_locations_count = ghana_locations.meta.found
    print(f"There are {ghana_locations_count} air monitoring locations in Ghana on OpenAQ")
    return


@app.cell
def _(ghana_locations):
    # Q2-2
    ghana_parameters_dict = {}
    for location in ghana_locations.results:
        for sensor in location.sensors:
            if sensor.parameter.name not in ghana_parameters_dict:
                ghana_parameters_dict[sensor.parameter.name] = 1
            else:
                ghana_parameters_dict[sensor.parameter.name] += 1

    print(f"The parameters and the number of locations where they are being measured in Ghana are:\n\t{ghana_parameters_dict}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz:** Can you alternatively answer Q2-2 with one single request to the API, knowing that the parameters_id for PM2.5 is 2? Replace the 'TODO' string in the cell below to print out the number of PM2.5 locations in Ghana.
    """)
    return


@app.cell
def _():
    ghana_pm25_locations_quiz = 'TODO'
    ghana_pm25_locations_quiz
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Geospatial queries**
    The `.list()` method also allows you to perform spatial queries to look for locations. These spatial argument options are particularly useful for geographic queries of sub-national level. Note that coordinates must be in the format WGS84 (EPSG:4326).
    """)
    return


@app.cell
def _(client):
    # Bounding box: http://bboxfinder.com/
    accra_locations_bbox = client.locations.list(
        bbox=(-0.271464, 5.513141, -0.131388, 5.600960), # minX, minY, maxX, maxY
        limit=1000
    )

    print(f"{accra_locations_bbox.meta.found} locations are found on OpenAQ in Accra using bounding box around the city")
    return


@app.cell
def _(client):
    # Coordinates and radius (must go together)
    accra_locations_radius = client.locations.list(
        coordinates=(5.556031, -0.204461), # Y, X
        radius=10000, # in meters
        limit=1000
    )

    print(f"{accra_locations_radius.meta.found} locations are found on OpenAQ in Accra using coordinates and radius around city center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Topic 3: Get sensor_ids from locations**
    Each location have one or more sensoring units (called sensors) that record measurements of pollutant or meteorological paramerers, such as PM2.5, PM10, temperature. These sensors are the gateway to getting measurements at locations and are not to be confused with air sensors (location type).

    To get sensors information at a location, you can use the `.sensors()` method on the Locations resource. This method accepts a single argument being `locations_id`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz:** What are the sensors_ids from the locations with ID 3025594? Replace the 'TODO' with a single request to the API.
    """)
    return


@app.cell
def _(pprint):
    sensors_quiz = 'TODO'
    pprint(sensors_quiz)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz: **As you might have noticed, we could also traverse the LocationsResponse body and get the sensors ID. Can you tell the difference between using `.list()` and traversing vs. using `.sensors()`?
    """)
    return


@app.cell
def _(ghana_locations, pprint):
    # Fetch sensors information by traversing LocationsResponse body
    pprint(ghana_locations.results[0].sensors)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Topic 4: Measurements data and evaluate sensor summary statistic**
    Measurements data is often the end goal for accessing OpenAQ API for many. You can do this via the OpenAQ Python package in a number of ways:
    1. Accessing the **latest measurements at a location**: using the `.latest()` method of the Locations resource with a `locations_id`
    2. Accessing **measurements data by the sensor** that records it: using the `.list()` method of the Measurements resource with a `sensors_id`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Accessing measurements data**
    If you are designing an application to report real-time pollutant concentrations or calculate the AQI from those concentrations at a location, using the `.latest()` method of the Locations resource may be useful.
    """)
    return


@app.cell
def _(client, pprint):
    pprint(client.locations.latest(1471855))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But as you can see, that method gives you only data from a single point in time. By using the `.list()` method of the Measurements resource, however, you can access measurements data of various base calculations from any given period. This request below provides raw measurements data in the last week of December 2025 for sensor 10330994.

    **Note:** It is recommended you add constraints in your request to the API, such as `datetime_from` and `datetime_to`, to avoid resource-intensive resoures that would cause request timeout errors.
    """)
    return


@app.cell
def list_measurements_example(client, datetime, pprint):
    pprint(client.measurements.list(sensors_id=10330994, # this sensor outputs measurements every 5 minutes
                             data="measurements", # raw measurements
                             datetime_from=datetime(2025, 12, 25),
                             datetime_to=datetime(2025, 12, 31)
                            )
          )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Evaluating summary statistics
    But a lot of the time, raw measurements at a 5-minute frequency are unnecessary for many analysis tasks. In this section, we will look at summary statistics to identify outliers and/or poorly performing locations in your dataset. In other words, we will answer these questions:
    - **Q4-1.** Using days data for 2025, what are the outliers and unstably performing locations for PM2.5 in Ghana?
    - **Q4-2.** Visualize the median, min, max, interquartile range, and coverage for 3 locations for PM2.5 in Ghana.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, we need to get all sensors_ids that measure PM2.5 for all locations in Ghana.
    """)
    return


@app.cell
def _(client, ghana_locations):
    ghana_pm25_sensors = {}

    for ghana_location in ghana_locations.results:
        sensors = client.locations.sensors(ghana_location.id)
        for each_sensor in sensors.results:
            if each_sensor.parameter.id == 2:
                ghana_pm25_sensors[ghana_location.id] = each_sensor.id
                break

    # We got 60 PM2.5 sensors, which align with Q2-2 results
    len(ghana_pm25_sensors)
    return (ghana_pm25_sensors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we will make requests to each of those sensors to get their measurements data for every day in 2025 and construct a pandas DataFrame to store those data.
    """)
    return


@app.cell
def _(client, ghana_pm25_sensors, pd):
    summary_stats_dfs = []

    # Iterate through each sensor, look for measurements data and save them to a DataFrame
    for locations_id, sensors_id in ghana_pm25_sensors.items():
        # Quiz: What are the differences between this request and this cell: #scrollTo=list_measurements_example
        ghana_pm25_days_measurements = client.measurements.list(sensors_id=sensors_id,
                                                                data="days", # pre-aggregated days data from hourly data
                                                                date_from="2025-01-01",
                                                                date_to="2025-12-31")

        if ghana_pm25_days_measurements.meta.found > 0:
            summary_stats_df = pd.json_normalize(ghana_pm25_days_measurements.dict()["results"])

            summary_stats_df = summary_stats_df.rename(columns={
                "summary.median": "median",
                "summary.min": "min",
                "summary.max": "max",
                "summary.q25": "q25",
                "summary.q75": "q75",
                "value": "average",
                "coverage.percent_coverage": "coverage"}
                )

            summary_stats_df["locations_id"] = locations_id
            summary_stats_df["pm25_sensors_id"] = sensors_id
            summary_stats_df["date"] = pd.to_datetime(summary_stats_df["period.datetime_from.utc"]).dt.date
            summary_stats_df = summary_stats_df[["locations_id", "pm25_sensors_id", "date", "average",
                                                 "median", "min", "max", "q25", "q75", "coverage"]]

            summary_stats_dfs.append(summary_stats_df)

    # Compile all measurements data for all PM2.5 sensors in Ghana into 1 DataFrame
    if len(summary_stats_dfs) > 0:
        summary_stats = pd.concat(summary_stats_dfs, ignore_index=True)
    else:
        print("PM2.5 days measurements are not found for any of the sensors above.")
    return (summary_stats,)


@app.cell
def _(summary_stats):
    summary_stats
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because days where data is not available will not be returned by the API in the `summary_stats` table, we need to create a grid of 2025 days for each `locations_id` and `pm25_sensors_id` pair and populate them with N/A values. **This new DataFrame will be the key data table to be used through the rest of the tutorials.**
    """)
    return


@app.cell
def _(pd, summary_stats):
    full_year_2025 = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    pairs = summary_stats[["locations_id", "pm25_sensors_id"]].drop_duplicates()
    grid = pairs.assign(key=1).merge(pd.DataFrame({"date": full_year_2025, "key": 1}), on="key").drop("key", axis=1)
    grid["date"] = grid["date"].dt.date

    summary_stats_full_2025 = grid.merge(summary_stats, on=["locations_id", "pm25_sensors_id", "date"], how="left")

    summary_stats_full_2025
    return (summary_stats_full_2025,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are many ways to tackle Q4-1. Here, let's use the daily median of all sensors for 2025 and explore their summary statistics to see what each location looks like using a boxplot chart.
    """)
    return


@app.cell
def _(alt, summary_stats_full_2025):
    alt.Chart(summary_stats_full_2025).mark_boxplot(extent="min-max").encode(
        alt.Y("median:Q").scale(zero=False),
        alt.X("locations_id:N")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, two locations stand out with massive outliers in their data. Realistically, location 2453501 might not be so bad if that max value is just one day. But for this exercise, let's just drop those 2 locations to examine the rest in the same boxplot chart.
    """)
    return


@app.cell
def summary_stats_boxplot(alt, summary_stats):
    not_great_locations = [9764, 2453501]

    alt.Chart(summary_stats).mark_boxplot(extent="min-max").encode(
        alt.Y("median:Q").scale(zero=False),
        alt.X("locations_id:N"),
        alt.Tooltip("count():Q")
    ).transform_filter(
        ~alt.FieldOneOfPredicate(field='locations_id', oneOf=not_great_locations)
    )
    return (not_great_locations,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz: **What are some interpretations looking at these 2 boxplots? Any information you wish you knew that would help with the interpretations?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we know which locations seem problematic, let's visualize what individual stations look like the entire year to further investigate the trend.
    """)
    return


@app.cell
def _(alt, summary_stats_full_2025):
    def visualize_summary_stats_2025(locations_id):
        """
        Outputs a percentile ribbon chart for PM2.5 daily reading in 2025. Input (int): the location ID.
        """
        df = summary_stats_full_2025[summary_stats_full_2025["locations_id"] == locations_id]

        summary_median = alt.Chart(df).mark_line(color="#4682B4").encode(
            x="date:T",
            y="median:Q",
            tooltip=["median"])

        summary_interquartiles = alt.Chart(df).mark_area(color="#89CFF0").encode(
            x="date:T",
            y="q25:Q",
            y2="q75:Q",
            tooltip=["q25", "q75"])

        summary_minmax = alt.Chart(df).mark_area(color="#A7C7E7").encode(
            x="date:T",
            y="min:Q",
            y2="max:Q",
            tooltip=["min", "max"])

        percentile_chart = alt.layer(
            summary_minmax.encode(x='date:T'),
            summary_interquartiles.encode(x='date:T'),
            summary_median.encode(x='date:T')
        ).properties(width=860, height=300)

        color_condition = alt.when(alt.datum.coverage == None).then(alt.value('white')) \
                             .when(alt.datum.coverage >= 75).then(alt.value('steelblue')) \
                             .otherwise(alt.value('maroon'))

        coverage_chart = alt.Chart(df, title="Daily coverage (%)").mark_bar().encode(
            x=alt.X("date:T").title(None).axis(labels=False, ticks=False),
            y=alt.value(0),
            color=color_condition,
            tooltip=["date", "coverage"]
        ).properties(width=860, height=20)

        final_chart = alt.vconcat(
            percentile_chart, 
            coverage_chart
        ).resolve_scale(x='shared')

        return final_chart
    return (visualize_summary_stats_2025,)


@app.cell
def _(visualize_summary_stats_2025):
    visualize_summary_stats_2025(3025589)
    return


@app.cell
def _(visualize_summary_stats_2025):
    visualize_summary_stats_2025(3025593)
    return


@app.cell
def _(visualize_summary_stats_2025):
    visualize_summary_stats_2025(6109067)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Topic 5: Evaluate sensor coverage for time period of interest**
    Coverage is accessible via the Measurement() object whenever a Measurements resource is called. From the visualizations above, we have a hint of how coverage might be important in aggregation. This section describes one of the ways coverage might be used in analysis by answering these questions:
    - **Q5-1.** What’s the annual average PM2.5 concentration at each station (assume the annual average is computed from daily averages)? WHO suggests that annual average concentrations of PM2.5 should not exceed 5 µg/m3.
    - **Q5-2.** What if we include only days with >=75% coverage?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Coverage outlines the expected number of data points from the data period queried, and assesses data availability actually ingested in that time period. Thus, coverage percentage is measurement count actually ingested over measurement count expected. Note that the expected measurement count does not account for first active date of locations or sensors; it is simply a multiplier of interval and time period.
    """)
    return


@app.cell
def _(client, pprint):
    pprint(client.measurements.list(sensors_id=10330994,
                             data="days",
                             date_from="2025-12-01",
                             date_to="2025-12-02"
                            ).results
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quiz:** How many Measurement() objects might you find in the result of this request? How many expected_count in coverage will you see in each object?
    """)
    return


@app.cell
def _(client):
    coverage_quiz = client.measurements.list(sensors_id=10330994,
                             data="years", # data is always pre-computed and aggregated from hourly averages
                             date_from="2025-01-01",
                             date_to="2025-12-31"
                            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Additionally, you could also manually choose the data and roll them up on the fly for options unavailable at the data level or if you want a different base calculations (the default for data is hour averages). This will be slower so **only use rollup when you really need it.**

    **Quiz:** How many records might we see in the results?
    """)
    return


@app.cell
def _(client):
    # Fetch monthly data in 2025 computed on the fly from day averages
    monthly_measurements_2025_example = client.measurements.list(sensors_id=10330994,
                                                      data="days", # use days as base measurement data
                                                      rollup="monthly", # and then roll up them to get monthly summaries
                                                      date_from="2025-01-01",
                                                      date_to="2025-12-31"
                                                     )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's answer Q5-1. Since we have already created a DataFrame `summary_stats_full_2025` with days measurement data from Topic 4, let's use that data.
    """)
    return


@app.cell
def _(not_great_locations, summary_stats_full_2025):
    # Annual average PM2.5 conc. at each locations (excluding < 75% coverage days)
    all_coverage_2025 = summary_stats_full_2025[
        ~summary_stats_full_2025.isin(not_great_locations)].groupby("locations_id")["average"].mean().reset_index()

    all_coverage_2025
    return (all_coverage_2025,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As we have seen in the prior charts, monitors can be spotty and these calculations so far do not take into account the coverage metric. For Q5-2., let's do these calculations again, but this time we will exclude days that do not have >= 75% coverage.
    """)
    return


@app.cell
def _(not_great_locations, summary_stats_full_2025):
    # Annual average PM2.5 conc. at each locations (excluding < 75% coverage days)
    over_75_coverage_2025 = summary_stats_full_2025[
        (~summary_stats_full_2025["locations_id"].isin(not_great_locations)) & 
        (summary_stats_full_2025["coverage"] >= 75)
    ].groupby("locations_id")["average"].mean().reset_index()

    over_75_coverage_2025
    return (over_75_coverage_2025,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sometimes answering the question might not tell the whole picture. Let's visualize to compare and interpret the chart.
    """)
    return


@app.cell
def _(all_coverage_2025, alt, over_75_coverage_2025, pd):
    annual_pm25_conc_2025 = pd.merge(all_coverage_2025, over_75_coverage_2025, on="locations_id")
    annual_pm25_conc_2025 = annual_pm25_conc_2025.rename(columns={
        "average_x": "annual_avg_all",
        "average_y": "annual_avg_excluded"
    })

    # Make a dumb bell chart
    annual_pm25_conc_2025_long = pd.melt(annual_pm25_conc_2025, id_vars=["locations_id"], value_vars=["annual_avg_excluded", "annual_avg_all"], var_name="type", value_name="avg_pm25_conc")

    q5_chart = alt.Chart(annual_pm25_conc_2025_long).encode(
        y="avg_pm25_conc:Q", x="locations_id:N")

    q5_line = q5_chart.mark_line(color="#db646f").encode(detail="locations_id:N")
    q5_color = alt.Color("type:N").scale(domain=["annual_avg_all", "annual_avg_excluded"], range=["#e6959c", "#911a24"])

    q5_points = q5_chart.mark_point(size=100,
                              opacity=1,
                              filled=True
                             ).encode(color=q5_color)

    (q5_line + q5_points).properties(width=750, height=300)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Topic 6: Visualize a year of PM2.5 data at a location**
    Now that we have the building blocks done, let's bring it all together and try one final task of comparing PM2.5 daily average for the whole year against WHO recommendation (24-hour average exposures should not exceed 15 µg/m3 more than 3-4 days per year).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's pick a location that has data in >= 75% days (or >= 274 days) of the year. Reviewing the cell `#scrollTo=summary_stats_boxplot`, location 3025582 fits the bill.
    """)
    return


@app.cell
def _(alt, summary_stats_full_2025):
    q6 = summary_stats_full_2025[summary_stats_full_2025["locations_id"] == 3025582]

    def label_data(row):
        if not row["coverage"]:
            return "No data available for this day"
        elif row["coverage"] < 75:
            return "Insufficient day data"
        elif row["coverage"] >= 75:
            if row["average"] > 15:
                return "Over WHO daily AVG conc. recs"
            elif 0 <= row["average"] <= 15:
                return "Within WHO daily AVG conc. recs"
            return "Invalid data"

    q6["data_label"] = q6.apply(label_data, axis=1)

    q6_categories = ["No data available for this day", "Insufficient day data",
                  "Over WHO daily AVG conc. recs",
                  "Within WHO daily AVG conc. recs", "Invalid data"]
    q6_color_mapping = ["#FFFFFF", "#CCCCCC", "#E65C5C", "#A1E972", "#000000"]

    alt.Chart(q6, title="Daily average of PM2.5 concentration against WHO 24-hour recommendation in 2025").mark_rect().encode(
        alt.X("date(date):O").title("Day").axis(format="%e", labelAngle=0),
        alt.Y("month(date):O").title("Month"),
        alt.Color('data_label:N', scale=alt.Scale(domain=q6_categories, range=q6_color_mapping), title=None),
        tooltip=["data_label", "coverage", "average"],
    ).configure_view(
        step=22,
        strokeWidth=0
    ).configure_axis(
        domain=False
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remember to always explicitly close the connection at the end of your notebook session.
    """)
    return


@app.cell
def _():
    # client.close()
    return


if __name__ == "__main__":
    app.run()
