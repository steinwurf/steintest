import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from datetime import datetime
from scipy import stats
import plotly.graph_objects as go

try: 
    import dataprocessing.queries as q
except:
    import queries as q

TODAY = datetime.utcnow().strftime('%Y-%m-%d')
HISTORICAL_DATA_PATH = Path(__file__).resolve().parents[1] / "historical_data" / "historical_data.csv"
PLOT_PATH = Path(__file__).resolve().parents[1] / "plots" / TODAY 
COLORS = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]




# Load the data
def load_historical_data():
    historical_df = pd.read_csv(HISTORICAL_DATA_PATH)

    # Convert the date column to datetime
    historical_df['date'] = pd.to_datetime(historical_df['date'])
    historical_df['last_report_date'] = pd.to_datetime(historical_df['last_report_date'], errors="coerce")

    return historical_df

def export_all_plots(all_plots):
    # Export all plots to a folder
    
    # Create the folder if it does not exist
    PLOT_PATH.mkdir(parents=True, exist_ok=True)

    
    # Export the plots
    for name, plot in all_plots.items():
        plot.write_image(str(PLOT_PATH.joinpath(f"{name}.png")))


"""The following functions are for the geographical coverage section of the report"""

def map_of_world():
    # A map of the world where each server is depicted as a dot and the size of the dot is the number of tests
    # And there is line between every server and all continents where the lines thickness is the number of tests
    # Since last report date
    pass


def consecutive_lost_packets_histogram(historical_df):
    # A histogram of the number of consecutive lost packets
    # The x axis is the number of consecutive lost packets and the y axis is the number of tests
    # the top 1% of test are removed to make the plot more readable

    cons_lost_packets_array = q.get_array_of_cons_lost_packets(historical_df['last_report_date'].max())

    ## removing outliers 
    threshold = np.quantile(cons_lost_packets_array, 0.99)

    cons_lost_packets_array = [x for x in cons_lost_packets_array if x < threshold]

    fig  = px.histogram(cons_lost_packets_array, color_discrete_sequence=COLORS)

    fig.update_layout(
        title="Histogram of consecutive lost packets",
        xaxis_title="Number of consecutive lost packets",
        yaxis_title="Frequency",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        showlegend=False,
        template="seaborn",
    )

    return fig


""" The following functions are for the all time overview section of the report """

def tests_over_time():
    # A line plot where the x axis is the date and the y axis is the number of tests
    timestamps = q.get_timestamp_for_all_tests()

    
    df = pd.DataFrame(timestamps , columns=['timestamp'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    df = df.sort_values(by=['datetime'])
    df.insert(0, 'cum_sum', range(0, len(df)))

    fig = px.line(df, x='datetime', y='cum_sum', color_discrete_sequence=COLORS)
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b <br> %y")


    fig.update_layout(
        title="Number of tests over time",
        xaxis_title="Month",
        yaxis_title="Number of tests",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        showlegend=False,
        template="seaborn",
    )

    return fig

def tests_over_time_per_server():
    # A line plot where the x axis is the date and the y axis is the number of tests
    # And there is a line for every server
    list_of_docs = q.get_tests_over_time_per_server()


    # Some Data manipulation to get the data in the right format
    df = pd.DataFrame.from_records(list_of_docs).explode('res').rename(columns={'res': 'timestamps', '_id': 'server'})
    df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
    df.reset_index(inplace=True, drop=True)
    df['dummy'] = 1

    df["cumsum"] = df.groupby(['server'], sort=True)["dummy"].cumsum()

    # Plotting
    fig = px.line(df, x='timestamps', y='cumsum', color='server', color_discrete_sequence=COLORS)
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b <br> %y")

    fig.update_layout(
        title="Number of tests over time",
        xaxis_title="Month",
        yaxis_title="Number of tests",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        showlegend=True,
        template="seaborn",
    ) 

    return fig

def tests_over_time_per_continent():
    # A line plot where the x axis is the date and the y axis is the number of tests
    # And there is a line for every continent
    list_of_docs = q.get_tests_over_time_per_continent()
    df = pd.DataFrame.from_records(list_of_docs).explode('res').rename(columns={'res': 'timestamps', '_id': 'continent'})
    df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
    df.reset_index(inplace=True, drop=True)
    
    df['dummy'] = 1

    df["cumsum"] = df.groupby(['continent'], sort=True)["dummy"].cumsum()

    # Plotting
    fig = px.line(df, x='timestamps', y='cumsum', color='continent', color_discrete_sequence=COLORS)
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b <br> %y")


    fig.update_layout(
        title="Number of tests over time",
        xaxis_title="Month",
        yaxis_title="Number of tests",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        showlegend=True,
        template="seaborn",
    )
    return fig

def scatter_of_distance_to_server_and_packetloss():
    # A scatter plot where the x axis is the distance to the server and the y axis is the packet loss
    # also provide the correlation coefficient
    df = q.get_distance_to_server_for_each_test()

    fig = px.scatter(df, x="distance", y="PacketLossPercentage", color="destinationserver", 
    labels={"destinationserver" : "Server"}, color_discrete_sequence=COLORS)

    fig.update_layout(
        title="Distance to server and packet loss",
        xaxis_title="Distance to server (km)",
        yaxis_title="Packet loss (%)",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        template="seaborn",
    )
    return fig

def box_plots_over_OS():
    # A box plot where the x axis is the OS and the y axis is the packet loss
    df = q.get_packetloss_per_OS()


    fig = px.box(df, x="OS", y="PacketLossPercentage", color="OS", color_discrete_sequence=COLORS)

    fig.update_layout(
        title="Box plot over packet loss per OS",
        xaxis_title="OS",
        yaxis_title="Packet loss (%)",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        template="seaborn",
    )

    # Adding the number of tests per OS to the plot
    for s in df["OS"].unique():
        fig.add_annotation(x=s,
                       y = df[df['OS']==s]['PacketLossPercentage'].median(),
                       text = f"n = {str(len(df[df['OS']==s]['PacketLossPercentage']))}",
                       yshift = 10,
                       showarrow = False
                      )

    return fig

def box_plots_of_packetloss_per_continent():
    # A box plot where the x axis is the continent and the y axis is the packet loss
    
    df = q.get_tests_packetloss_and_continent()

    fig = px.box(df, x="Continent", y="PacketLossPercentage", color="Continent", color_discrete_sequence=COLORS)

    fig.update_layout(
        title="Box plot over packet loss per continent",
        xaxis_title="Continent",
        yaxis_title="Packet loss (%)",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        template="seaborn",
    )

    # Adding the number of tests per continent to the plot
    for s in df["Continent"].unique():
        fig.add_annotation(x=s,
                       y = df[df['Continent']==s]['PacketLossPercentage'].median(),
                       text = f"n = {str(len(df[df['Continent']==s]['PacketLossPercentage']))}",
                       yshift = 10,
                       showarrow = False
                      )
    return fig

def scatter_plot_of_packetloss_and_latency():
    # A scatter plot where the x axis is the latency and the y axis is the packet loss

    df = q.get_latency_and_packetloss_for_each_test()

    fig = px.scatter(df, x="Latency", y="PacketLossPercentage", color_discrete_sequence=COLORS)

    fig.update_layout(
        title="Scatterplot of latency and packet loss",
        xaxis_title="Latency (ms)",
        yaxis_title="Packet loss (%)",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        template="seaborn",
    )
    return fig

def scatter_plot_of_latency_and_distance_to_server():
    # A scatter plot where the y axis is the latency and the x axis is the distance to the server
    pass 

def scatterplot_of_speed_and_packetloss():
    
    df = q.get_packetloss_and_speed()

    fig = px.scatter(df, x="Speed", y="PacketLossPercentage", color_discrete_sequence=COLORS)

    fig.update_layout(
        title="Speed and packet loss",
        xaxis_title="Speed (Mbps)",
        yaxis_title="Packet loss (%)",
        font=dict(
            family="Times, monospace",
            size=18,
            color="#000000"
        ),
        template="seaborn",
    )
    return fig

def morten_plot():
    result_df = pd.DataFrame(columns=['x', 'lossless'])



    df = q.morten()
    for i in range(11):
        lossless = len(df[df['MaxConsLostPackets'] <= i])
        result_df = result_df.append({'x': i, 'lossless': lossless}, ignore_index=True)


    result_df['lossless'] = result_df['lossless'] / len(df) * 100


    fig = px.line(result_df, x='x', y='lossless', color_discrete_sequence=COLORS)
    fig.update_layout(xaxis_range=[-0,10])

    """ fig = go.Figure(data=[go.Pie(labels=['Lossless', 'Lossy'], values=[lossless, lossy])]) """



    """ fig = px.ecdf(df, x="MaxConsLostPackets", ecdfmode="reversed")
    fig.update_layout(yaxis_range=[0,1],
                      xaxis_range=[0,4])   
 """

    fig.show()





def generate_plots():
    all_plots = {}

    historical_df = load_historical_data()

    """     all_plots["tests_over_time"] = tests_over_time()
    all_plots["consecutive_lost_packets_histogram"] = consecutive_lost_packets_histogram(historical_df)
    all_plots["tests_over_time_per_server"] = tests_over_time_per_server()
    all_plots["tests_over_time_per_continent"] = tests_over_time_per_continent()
    all_plots["scatter_plot_of_distance_to_server_and_packetloss"] = scatter_of_distance_to_server_and_packetloss()
    all_plots["box_plots_over_OS"] = box_plots_over_OS()
    all_plots["scatter_plot_of_speed_and_packetloss"] = scatterplot_of_speed_and_packetloss()
    all_plots["scatter_plot_of_packetloss_and_latency"] = scatter_plot_of_packetloss_and_latency()
    all_plots["box_plots_of_packetloss_per_continent"] = box_plots_of_packetloss_per_continent() """

    all_plots["test"] = morten_plot()

    export_all_plots(all_plots)



if __name__ == "__main__":
    generate_plots()

