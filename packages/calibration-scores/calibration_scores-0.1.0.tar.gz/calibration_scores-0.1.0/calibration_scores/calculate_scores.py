# score calculations

# installations
import os
from dataclasses import dataclass, field

# pylint: disable = import-error, wrong-import-position
import numpy as np
import pandas as pd

os.environ["MPLCONFIGDIR"] = os.getcwd() + "/configs/"
import matplotlib.pyplot as plt

# pylint: enable = import-error, wrong-import-position

@dataclass
class EventData:
    """Dataclass which will force the Event class to have the event_id column"""

    event_id: str


@dataclass
class Event:
    event_df: pd.DataFrame = field(init=False)

    def __init__(self, event_df: pd.DataFrame):
        """This function initiializes an instance of the event class.

        Args:
            event_df (pd.DataFrame): The data collected at a specific event

        Raises:
            ValueError: If the input DataFrame doesn't have a column called 'event_id'
        """
        missing_columns = [
            col
            for col in EventData.__dataclass_fields__
            if col not in event_df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"The following columns are missing: {', '.join(missing_columns)}"
            )

        self.event_df = event_df

        # def __post_init__(self):
        #     event_data = [EventData(row["event_id"]) for _, row in self.event_df.iterrows()]

        #     missing_columns = [col for col in EventData.__dataclass_fields__ if col not in self.event_df.columns]

        #     if missing_columns:
        #         raise ValueError(f"The following columns are missing: {', '.join(missing_columns)}")

        """This function initializes an instance of the Event class.

        Args:
            event_df (pandas DataFrame): The data recorded from one event

        Raises:
            TypeError: If input is not a DataFrame
            ValueError: if DataFrame is empty
        """ """"""

    def values_within_threshold(self, series, threshold):
        """This function takes an array and checks whether any two values have a difference
        greater than the threshold

        Args:
            series (array-like): a list of values
            threshold (float): a value that the function will check the difference between
            each number in the series as.

        Returns:
            Boolean: A T/F value representing whether the series has all of it's values within
            one threshold of each other
        """
        # coerce into np array if not in that format
        if not isinstance(series, np.ndarray):
            series = np.array((series))

        # return always true in base case of 1
        if series.size == 1:
            return True

        # Throw error if passed with series length of zero
        if series.size == 1:
            raise ValueError("Series of length zero passed.")

        # Find the absolute difference between each pair of values in the array
        diff_matrix = np.abs(series[:, np.newaxis] - series)

        # Check if any difference is greater than the set value
        if np.any(diff_matrix > threshold):
            return False

        return True


# @dataclass
# class PitchingData:
#     extension: float
#     relheight: float
#     relside: float


@dataclass
class TrackmanPitchingScores(Event):
    """Class that allows for specific operations on pitching data. With this class, the
    user can calculate scores for trackman data as well as plot player data and event
    data.

    Args:
        Event (DataFrame): A dataframe containing event data. This DataFrame must have
        the columns specified in the dataclass

    Raises:
        ValueError: If required columns are missing
        ValueError: If event records are empty

    """

    extension: float = field(init=False)
    relheight: float = field(init=False)
    relside: float = field(init=False)
    # SHOULD THIS BE AN OBJECT?
    calibrationid: object = field(init=False)

    def __init__(self, event_df):
        super().__init__(event_df)

        required_columns = {
            "extension": float,
            "relheight": float,
            "relside": float,
            "calibrationid": object,
        }
        missing_columns = [
            col
            for col, dtype in required_columns.items()
            if col not in event_df.columns or event_df[col].dtype != dtype
        ]

        if missing_columns:
            raise ValueError(
                f"The following columns are missing or have incorrect data types: {', '.join(missing_columns)}"
            )

        if event_df.empty:
            raise ValueError("Event records cannot be empty.")

        self.historical_data = self.get_historical_data_trackman()

    def get_historical_data_trackman(self):
        """This functions reads necessary historical data from the tests folder into
        a csv, and the init function assign the data as a member of the class

        Returns:
            dataframe: the historical data needed to validate calibrations
        """
        # Get the current directory of the calculate_scores module
        module_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to the CSV in the tests directory (using relative path)
        csv_file_path = os.path.join(
            module_directory, "tests", "pitchers-and-pitches-main.csv"
        )

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
        return df

    def get_calibrations(self):
        """Gets all unique calibrations from event."""
        return self.event_df["calibrationid"].unique()

    def get_calibration_score(self, calibrationid, metric):
        """This function gets the  score of any one metric based on one calibration.

        Args:
            calibrationid (string): The unique id of the calibration in question.
            metric (string): The name of the field that user wishes to take a look at.

        Returns:
            float: The score, from 0-1, of the calibration as it related to the given metric.
        """
        # initialize misses to 0
        misses = 0

        # define dataframe for just calibration
        calibrationDF = self.event_df[
            self.event_df["calibrationid"] == calibrationid
        ]

        for pitcher in calibrationDF["pitcherid"].unique():
            # create df with just individual pitcher
            pitcherDF = self.historical_data[
                self.historical_data["pitcherid"] == pitcher
            ]

            # find all pitches a pitcher has thrown across entire dataset
            series = pitcherDF[metric].values

            # use helper function to set validity
            valid = self.values_within_threshold(
                series, abs(self.historical_data[metric]).std()
            )

            # in case of miss, increment misses
            if not valid:
                misses += 1
        num_pitchers = len(calibrationDF["pitcherid"].unique())

        # raise error with zero pitchers
        if num_pitchers == 0:
            raise ValueError("No pitchers in this calibration.")

        final_score = 1 - (misses / num_pitchers)

        return final_score

    def get_event_breakdown(self, metric):
        """This function gets the breakdown of each calibration at one event and it's score
        based on a metric.

        Args:
            metric (string): The name of the field that user wishes to take a look at.

        Returns:
            dataframe: a pandas DataFrame with one column denoting the calibraition id and the
            other column denoting the score.
        """
        # get list of calibrations at the event to iterate through
        calibration_list = self.get_calibrations()

        # initialize empty score list that will become our scores column
        score_list = []

        # iterate through calibrations and get score for that calibration,
        # appending it to list
        for calibration in calibration_list:
            score_list.append(self.get_calibration_score(calibration, metric))

        # create dict -> turn dict into DataFrame
        final_data = {"calibration": calibration_list, "score": score_list}

        return pd.DataFrame(data=final_data)

    def get_event_score(self, metric):
        """This function gets an overall event score for any metric.

        Args:
            metric (string): The name of the field that user wishes to take a look at.

        Returns:
            float: the final event score for this particula event
        """
        # initialize variable to hold total scores
        score_aggregate = 0

        # get list of calibrations to iterate through
        calibration_list = self.get_calibrations()

        # get score for each calibration, appending score to aggregate
        for calibration in calibration_list:
            score_aggregate += self.get_calibration_score(calibration, metric)

        # divide by number of calibrations
        event_score = score_aggregate / len(calibration_list)

        return event_score

    def plot_calibration(self, calibrationid, metric):
        """This function plots the values in one calibration of a given metric.

        Args:
            calibrationid (string): The unique id of the calibration in question.
            metric (string): The name of the field that user wishes to take a look at.
        """
        calibrationDF = self.event_df[
            self.event_df["calibrationid"] == calibrationid
        ]

        plt.figure(figsize=(10, 7))

        for pitcher in calibrationDF["pitcherid"].unique():
            specific_pitcher_df = calibrationDF[
                calibrationDF["pitcherid"] == pitcher
            ]
            plt.scatter(
                specific_pitcher_df["pitchno"],
                specific_pitcher_df[metric],
                s=75,
            )

        plt.xlabel("pitch number")
        plt.ylabel(metric)
        plt.title(
            f"All {metric}s in calibration {str(calibrationid)} (each color = one pitcher)"
        )
        plt.axhline(
            self.historical_data[metric].mean(),
            color="red",
            label="Database average " + metric,
        )
        plt.legend()
        plt.show()

    def get_colors(self, series, metric):
        """This function is a helper function of the plot_player_chart function. It returns
        a list of colors, where each color represents the colora data point, and the colors are determined
        by whether or not the data point is within the upper and lower controls

        Args:
            series (array-like): A list of values to assign colors to
            metric (string): The metric being considered, important to assign a value
            to the standard deviation based on historical pitch data


        Returns:
            list: A list of colors used to help in plotting
        """
        # declare empty list to hold colors
        col = []

        # compute metric standard deviation
        std = abs(self.historical_data[metric]).std()

        # find series mean, series upper bound and lower bound
        series_mean = series.mean()
        series_upper = series_mean + std
        series_lower = series_mean - std

        for event in series:
            if event < series_lower or event > series_upper:
                col.append("red")
            else:
                col.append("blue")
        return col

    def plot_player_chart(self, pitcherid, metric):
        """
        This function takes a player's historical data based on
        one metric and plots all values


        Args:
            pitcherid (int): The pitcher you wish to plot's id
            metric (string): The metric you wish to analyze and plot

        Raises:
            ValueError: If no matching pitcher id is found in the event.
        """
        # Raise value error if pitcher isn't found
        if pitcherid not in self.historical_data["pitcherid"].values:
            raise ValueError("PitcherID not found in historical data.")

        # get only relevant pitches from data
        player_pitches = self.historical_data[
            self.historical_data["pitcherid"] == pitcherid
        ]

        # save player name for plotting
        player_name = str(player_pitches.pitcher.unique()[0])

        # increase figure size
        plt.figure(figsize=(12, 8))

        # get values to plot
        values = player_pitches[metric].unique()

        # filter out nan values
        values = values[~np.isnan(values)]

        pitch_numbers = np.arange(1, len(values) + 1)

        # get color of points
        col = self.get_colors(values, metric)

        # plot points
        plt.scatter(pitch_numbers, values, s=75, c=col)
        plt.xlabel("pitch #")
        plt.ylabel(metric)
        plt.title(f"All {metric}s from {player_name} (id: {str(pitcherid)})")

        # compute metric standard deviation
        std = abs(self.historical_data[metric]).std()

        # draw lines at mean and standard deviation
        plt.axhline(
            values.mean(), color="red", label="Player historical average"
        )
        plt.axhline(
            values.mean() + std,
            color="orange",
            linestyle="--",
            label="Upper control limit",
        )
        plt.axhline(
            values.mean() - std,
            color="orange",
            linestyle="--",
            label="Lower control limit",
        )

        plt.legend()
        plt.show()


@dataclass
class BlastScores(Event):
    """Class that allows for specific operations on blast data. With this class, the
    user can calculate scores for blast data as well as plot player data and event
    data.

    Args:
        Event (DataFrame): A dataframe containing event data. This DataFrame must have
        the columns specified in the dataclass

    Raises:
        ValueError: If required columns are missing
        ValueError: If event records are empty

    """

    bat_speed: float = field(init=False)
    peak_hand_speed: float = field(init=False)
    rotational_acceleration: float = field(init=False)
    on_plane_efficiency: float = field(init=False)

    event_id: int = field(init=False)

    def __init__(self, event_df):
        super().__init__(event_df)

        required_columns = {
            "bat_speed": float,
            "peak_hand_speed": float,
            "rotational_acceleration": float,
            "on_plane_efficiency": float,
            "event_id": int,
        }
        missing_columns = [
            col
            for col, dtype in required_columns.items()
            if col not in event_df.columns or event_df[col].dtype != dtype
        ]

        if missing_columns:
            raise ValueError(
                f"The following columns are missing or have incorrect data types: {', '.join(missing_columns)}"
            )

        if event_df.empty:
            raise ValueError("Event records cannot be empty.")

        self.historical_data = self.get_historical_data_blast()

    def get_historical_data_blast(self):
        """This functions reads necessary historical blast data from the tests folder into
        a csv, and the init function assign the data as a member of the class

        Returns:
            dataframe: the historical data needed to validate calibrations
        """
        # Get the current directory of the calculate_scores module
        module_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to the CSV in the tests directory (using relative path)
        csv_file_path = os.path.join(
            module_directory, "tests", "blast-full.csv"
        )

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
        return df

    def get_event_score(self, metric):
        """This function gets the  score of any one metric based on one event.

        Args:
            metric (string): The name of the field that user wishes to take a look at.

        Returns:
            float: The score, from 0-1, of the calibration as it related to the given metric.
        """
        # initialize misses to 0
        misses = 0

        for batter in self.event_df["pbr_id"].unique():
            # create df with just individual pitcher
            batterDF = self.historical_data[
                self.historical_data["pbr_id"] == batter
            ]

            # find all pitches a pitcher has thrown across entire dataset
            series = batterDF[metric].values

            # use helper function to set validity
            valid = self.values_within_threshold(
                series, abs(self.historical_data[metric]).std()
            )

            # in case of miss, increment misses
            if not valid:
                misses += 1
        num_hitters = len(self.event_df["pbr_id"].unique())

        # raise error with zero pitchers
        if num_hitters == 0:
            raise ValueError("No hitters in this calibration.")

        final_score = 1 - (misses / num_hitters)

        return final_score

    def plot_event(self, metric):
        """This function plots the values in one event of a given metric.

        Args:
            metric (string): The name of the field that user wishes to take a look at.
        """
        plt.figure(figsize=(10, 7))

        self.event_df["swing_number"] = np.arange(len(self.event_df))

        for hitter in self.event_df["pbr_id"].unique():
            specific_hitter_df = self.event_df[
                self.event_df["pbr_id"] == hitter
            ]
            plt.scatter(
                specific_hitter_df["swing_number"],
                specific_hitter_df[metric],
                s=75,
            )

        # save event id for plot title
        event_id = str(self.event_df["event_id"].unique())

        plt.xlabel("swing number")
        plt.ylabel(metric)
        plt.title(
            f"All {metric}s in event {event_id} (each color = one hitter)"
        )
        plt.axhline(
            self.historical_data[metric].mean(),
            color="red",
            label="Database average " + metric,
        )
        plt.legend()
        plt.show()

    def get_colors(self, series, metric):
        """This function is a helper function of the plot_player_chart function. It returns
        a list of colors, where each color represents the colora data point, and the colors are determined
        by whether or not the data point is within the upper and lower controls

        Args:
            series (array-like): A list of values to assign colors to
            metric (string): The metric being considered, important to assign a value
            to the standard deviation based on historical pitch data


        Returns:
            list: A list of colors used to help in plotting
        """
        # declare empty list to hold colors
        col = []

        # compute metric standard deviation
        std = abs(self.historical_data[metric]).std()

        # find series mean, series upper bound and lower bound
        series_mean = series.mean()
        series_upper = series_mean + std
        series_lower = series_mean - std

        for event in series:
            if event < series_lower or event > series_upper:
                col.append("red")
            else:
                col.append("blue")
        return col

    def plot_player_chart(self, pbr_id, metric):
        """
        This function takes a player's historical data based on
        one metric and plots all values.


        Args:
            pbr_id (int): The id of the hitter who's data you wish to plot
            metric (string): The metric you wish to analyze and plot

        Raises:
            ValueError: If no matching pitcher id is found in the event.
        """
        # Raise value error if player isn't found
        if pbr_id not in self.historical_data["pbr_id"].values:
            raise ValueError("PBR ID not found in historical data.")

        # get only relevant swings from data
        player_swings = self.historical_data[
            self.historical_data["pbr_id"] == pbr_id
        ]

        # save player name for plotting
        player_id = str(player_swings["pbr_id"].unique()[0])

        # increase figure size
        plt.figure(figsize=(12, 8))

        # get values to plot
        values = player_swings[metric].values

        # filter out nan values
        values = values[~np.isnan(values)]

        swing_numbers = np.arange(1, len(values) + 1)

        # #get color of points
        col = self.get_colors(values, metric)

        # plot points
        plt.scatter(swing_numbers, values, s=75, c=col)
        plt.xlabel("swing #")
        plt.ylabel(metric)
        plt.title(f"All {metric}s from player {player_id}")

        # compute metric standard deviation
        std = abs(self.historical_data[metric]).std()

        # draw lines at mean and standard deviation
        plt.axhline(
            values.mean(), color="red", label="Player historical average"
        )
        plt.axhline(
            values.mean() + std,
            color="orange",
            linestyle="--",
            label="Upper control limit",
        )
        plt.axhline(
            values.mean() - std,
            color="orange",
            linestyle="--",
            label="Lower control limit",
        )

        plt.legend()
        plt.show()


@dataclass
class SwiftScores(Event):
    swifttenyard: float = field(init=False)
    swiftthirtyyard: float = field(init=False)
    swiftsixtyyard: float = field(init=False)

    event_id: int = field(init=False)

    def __init__(self, event_df):
        super().__init__(event_df)

        required_columns = {
            "swifttenyard": float,
            "swiftthirtyyard": float,
            "swiftsixtyyard": float,
            "event_id": int,
        }
        missing_columns = [
            col
            for col, dtype in required_columns.items()
            if col not in event_df.columns or event_df[col].dtype != dtype
        ]

        if missing_columns:
            raise ValueError(
                f"The following columns are missing or have incorrect data types: {', '.join(missing_columns)}"
            )

        if event_df.empty:
            raise ValueError("Event records cannot be empty.")

        self.historical_data = self.get_historical_data_swift()
        self.add_splits(historical=True)
        self.add_splits()

    def get_historical_data_swift(self):
        """This functions reads necessary historical data from the tests folder into
        a csv, and the init function assign the data as a member of the class

        Returns:
            dataframe: the historical data needed to validate calibrations
        """
        # Get the current directory of the calculate_scores module
        module_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to the CSV in the tests directory (using relative path)
        csv_file_path = os.path.join(
            module_directory, "tests", "sixty-times.csv"
        )

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        return df

    def add_splits(self, historical=False):
        """This is a wrapper function that calls two other functions, one
        which adds the split times, and another which adds split percentiles.
        This function is called by default upon construction of a SwiftScores
        object.

        Args:
            historical (bool, optional): This parameter is used to alert the
            setter functions to whether they want to set the split values and
            percentiles on the instance's historical data member or current
            event data member. Defaults to False.
        """
        if not historical:
            self.event_df = self.set_split_times()
            self.event_df = self.set_percentile_ranks()
        else:
            self.historical_data = self.set_split_times(historical=True)
            self.historical_data = self.set_percentile_ranks(historical=True)

    def set_split_times(self, historical=False):
        """This function will be automatically called in the constructor, and it will
        find the time of the 0-10 yard, 10-30 yard and 30-60 yard splits using subtraction

        Args:
            historical (bool, optional): This parameter is used to alert the
            function to whether we want to set the split values
            on the instance's historical data member or current
            event data member. Defaults to False.

        Returns:
            pandas DataFrame: An updated dataframe containing the split columns
        """
        if not historical:
            updated_df = self.event_df.copy()
        else:
            updated_df = self.historical_data.copy()

        updated_df["0-10"] = updated_df["swifttenyard"]
        updated_df["10-30"] = (
            updated_df["swiftthirtyyard"] - updated_df["swifttenyard"]
        )
        updated_df["30-60"] = (
            updated_df["swiftsixtyyard"] - updated_df["swiftthirtyyard"]
        )

        return updated_df

    def calculate_percentile_values(self):
        # Calculate the percentile values for each column in historical_data
        self.percentile_values = self.historical_data.quantile([0.1, 0.3, 0.5, 0.7, 0.9])

    # NOTE: The following function only works on either the event or historical data, I haven't
    # incoorporated the ability to to both yet
    def set_percentile_ranks(self, historical=False):
        """This function sets the percentile rank of each player for each split. It
        will be used to determine if a player's splits are inconcistent. The percentile
        rankings are based on class.

        Args:
            historical (bool, optional): This parameter is used to alert the
            function to whether we want to set the percentile values
            on the instance's historical data member or current
            event data member. Defaults to False.

        Returns:
            pandas DataFrame: An updated dataframe containing the percentile columns
        """

        # Create a new DataFrame to store the percentile rankings
        result_df = pd.DataFrame()

        # create temporary df to update
        if not historical:
            temp_df = self.event_df.copy()
        else:
            temp_df = self.historical_data.copy()

        # define value columns we want to find percentiles to
        value_columns = ["0-10", "10-30", "30-60"]

        # Iterate through each unique class in the 'class' column
        for class_value in temp_df["class"].unique():
            # Select the rows for the current class
            class_df = temp_df[temp_df["class"] == class_value][value_columns]

            # Calculate percentile rankings for each value column
            percentile_ranks = 1 - class_df[value_columns].rank(pct=True)

            # Concatenate the percentile rankings for the current class to the result DataFrame
            result_df = pd.concat([result_df, percentile_ranks], axis=0)

        # Rename the columns in the result DataFrame
        result_df.columns = [f"{col}_percentile" for col in value_columns]

        # Concatenate the percentile rankings with the original DataFrame and return
        return pd.concat([temp_df, result_df], axis=1)

    def get_event_score_swift(self, threshold=0.3):
        """This function gets the event score from any one event according to all the
        records in that event. The event score is a number 0-1, with 1 having no questionable
        times and 0 having all questionable times.

        Args:
            threshold (float): The number to use in each comparison. Set to 0.3 by default.
            This means that if the percentile ranking for their specific class
            in any of the three splits exceeds the thresshold, the run will
            be flagged.

        Returns:
            float: The event score, a number 0-1 representing the
            percentage of runs which were not flagged.
        """
        # initialize questionable results counter to zero
        questionable_results = 0

        # iterate through rows in dataframe
        for idx in self.event_df.index:
            # get percentiles necessary for comparison
            series = [
                self.event_df["0-10_percentile"][idx],
                self.event_df["10-30_percentile"][idx],
                self.event_df["30-60_percentile"][idx],
            ]

            # check percentiles against threshold of 0.3, append in case of questionable results
            if not self.values_within_threshold(series, threshold):
                questionable_results += 1

        # return percentage of correct results
        return 1 - (questionable_results / len(self.event_df))

    def plot_swift_player_chart(self, pbr_id):
        # get list of columns that are important to plotting
        cols = ["0-10_percentile", "10-30_percentile", "30-60_percentile"]

        # Filter the dataframes for given pbr id
        historical_player_data = self.historical_data[
            self.historical_data["pbr_id"] == pbr_id
        ][cols]
        current_player_data = self.event_df[self.event_df["pbr_id"] == pbr_id][
            cols
        ]

        #concatenate historical and current player data for plotting
        player_data = pd.concat([historical_player_data, current_player_data]).dropna().reset_index()

        # Increase figure size and fix dimentions
        plt.figure(figsize=(10, 6))
        plt.ylim(-0.1, 1.1)

        # create lists for colors and markers for plotting purposes
        colors = [
            "red",
            "blue",
            "green",
            "orange",
            "gray",
            "purple",
            "orange",
            "black",
        ]
        markers = [
            "o",
            "x",
            "^",
            "s",
            "D",
            "*",
            "P",
            "H",
            "v",
            ">",
            "<",
            "p",
            "|",
            "_",
        ]

        # counter to determine position of marker and color list
        counter = 0
        for row in player_data.index:
            # set color and marker for this iteration
            col = colors[counter]
            mark = markers[counter]

            # plot splits
            ten_split = player_data["0-10_percentile"][row]
            plt.scatter("0-10", ten_split, color=col, marker=mark, s=75)

            twenty_split = player_data["10-30_percentile"][row]
            plt.scatter("10-30", twenty_split, color=col, marker=mark, s=75)

            thirty_split = player_data["30-60_percentile"][row]
            plt.scatter("30-60", thirty_split, color=col, marker=mark, s=75)

            # increment counter to change color and marker for next iteration
            counter += 1

        # add titles and show plot
        plt.title("Split percentiles from player " + str(pbr_id))
        plt.xlabel("Split")
        plt.ylabel("Speed percentile")

        plt.show()
