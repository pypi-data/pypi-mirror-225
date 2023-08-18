import re
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import yaml

from utils import utils_ref
from services import (
    services_export_granularity,
    timeseries
)
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import adfuller, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

warnings.filterwarnings("ignore")


class ExploratoryAnalysis:

    def __init__(self, df = pd.DataFrame):

        # definitions
        self.df = df.copy()
        self.__window_map = {
            'minute': 60,
            'fifty_minutes': 4,
            'hour': 24,
            'day': 30,
            'month': 12
        }
        self.__minute = utils_ref.ref_min()
        self.__fifty_minutes = utils_ref.ref_15_min()
        self.__hour = utils_ref.ref_hora()
        self.__day = utils_ref.ref_dia()
        self.__month = utils_ref.ref_mes()

        self.__freq_map = {
            "minute": utils_ref.ref_min(),
            "fifty_minutes": utils_ref.ref_15_min(),
            "hour": utils_ref.ref_hora(),
            "day": utils_ref.ref_dia(),
            "month": utils_ref.ref_mes()
        }

        self.ref_frequencies = self.__minute + self.__fifty_minutes + self.__hour + self.__day + self.__month
        self.ref_frequencies = [x for x in self.ref_frequencies if x > 0]

        with open('services/services_reference.yml', 'r') as file:
            self.__interface = yaml.safe_load(file)


    def check_date_column(self) -> list:
        """
        This method aims to check all columns of the dataframe which can be used as datetime.

        For do that, this method verifies if each rows in all columns has a pattern.
            pattern: number/number/number or number-number-number

        If true, the name of the column is append in a list. After that, the method removes
        all duplicated values of the list.

        In the final loop, it's checked if the first value is equals to the 24nd value, to avoid
        coincidence mistakes.

        Args:
            None
            
        Returns:
            list with all date columns of dataframe
            
        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.check_date_column()
        """
        
        # Defining pattern and lists
        data_pattern = r'\d{1,4}[-/]\d{2}[-/]\d{1,4}'
        date_column_list = []
        temporary_date_column_list = []

        # Searching the pattern for each column and row in the dataframe
        for column in self.df.columns:
            for valor in self.df[column]:
                valor = str(valor)
                if isinstance(valor, str) and re.search(data_pattern, valor):
                    temporary_date_column_list.append(column)
        
        temporary_date_column_list = list(set(temporary_date_column_list))

        # Checking if the found pattern was not a coincidence
        for column in temporary_date_column_list:
            if list(self.df[column])[0] != list(self.df[column])[23]:
                date_column_list.append(column)

        return date_column_list


    def check_timestamp(self) -> str:
        """
        This method aims to check date interval. To do that, the class transforms
        the date column to datetime e makes some changes: 
            1 - subtracts a sample for another;
            2 - drops NaN values;
            3 - finds the mode of the column (most repeated value)
        
        After that, the code gets the components: hour, minutes and seconds and then
        makes the date format.


        Args:
            None
            
        Returns:
            string with date format
            
        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.check_timestamp()
        """

        column = self.check_date_column()[0]
        self.df[column] = pd.to_datetime(self.df[column])
        timestamp_column = self.df[column].sort_values()
        timestamp_column = timestamp_column.diff()
        timestamp_column = timestamp_column.dropna()
        timestamp_column = timestamp_column.mode()[0]

        hours = timestamp_column.components.hours
        minutes = timestamp_column.components.minutes
        seconds = timestamp_column.components.seconds

        timestamp_column = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

        return timestamp_column
    

    def check_frequency(self) -> pd.DataFrame():
        """
        This method aims to get the 10 most importants frequencies of the data series.

        To do that, the code uses Fourier Transform for each available dataframe column.
        Note: "available" means float or int data type. 

        All steps in this method are simples, they just appends or filter values in lists,
        after in a dictionary and then in a DataFrame.
        
        Args:
            None
            
        Returns:
            Pandas DataFrame, where each column is an available column in the initial df.
            
        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.check_frequency()
        """

        results = {}
        
        try:
            for column in self.df.columns:
                dtype = self.df[column].dtype
                if dtype in ['float64', 'int64']:
                    
                    # Transforming the column in a numpy array
                    y = self.df[column].values  

                    # Calculating the Fourier Transform
                    fourier = np.fft.fft(y)

                    # Array with frequencies of the fft
                    freq = np.fft.fftfreq(len(y), 1)  # 1 is the difference between samples

                    # Taking the 10 frequencies with the highest amplitudes
                    higher_amplitudes_indices = np.argsort(np.abs(fourier))[-20:]
                    higher_amplitudes_indices = sorted(higher_amplitudes_indices)

                    # reference frequencies list
                    frequencies_list = []

                    # Adding labels
                    for indice in higher_amplitudes_indices:
                        frequencies_list.append(freq[indice])
                    
                    # Ascend ordering
                    frequencies_list = [abs(float(f'{x:.5f}')) for x in frequencies_list]
                    frequencies_list = set(frequencies_list)
                    
                    # Filtering values higher than zero
                    period_list = [x for x in frequencies_list if x > 0]

                    # Putting in a dictionary
                    results[column] = period_list


            # Creating DataFrame
            df_result = pd.DataFrame(results)
        except:
            df_result = pd.DataFrame(columns=self.df.columns)

        return df_result


    def check_reference_frequencies(self) -> tuple:
        """
        This method aims check if there is a frequency which belongs to a reference frequencies list.
        
        This method returns a tuple with two elements.

        First, a dataframe wich has a number of columns equals to columns available in
        the initial dataframe (self.df). Note: columns available are those which have float
        or int type.
        
        There is a column called 'check' in this dataframe that represents if a frequency in that
        row are in reference frequencies. If true, check = 1, else check = 0.

        The second term in the tuple is a string that shows where the frequency was found (which list)
        
        Args:
            None
            
        Returns:
            Tuple (dataframe, list)
            
        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.check_reference_frequencies()
        """
        # Creates two dataframes because their columns will be compared
        df_freq = self.check_frequency()
        df_freq2 = df_freq.copy()

        # Checks if each frequency are in the reference
        for column in df_freq.columns:
            freq_list = [1 if freq in self.ref_frequencies else 0 for freq in df_freq[column]]

            # Creates a new column for each column checked
            df_freq2[f'check_{column}'] = freq_list

        # Checks the differents columns
        unique_columns = set(df_freq2) - set(df_freq)

        # Creates a dataframe only with new columns
        df_freq2 = df_freq2[list(unique_columns)]

        # Creates a colum that is 0 when everybody is 0, else 1.
        df_freq2['check'] = (df_freq2 != 0).any(axis=1).astype(int)

        # Copies the new column to original dataframe
        df_freq['check'] = df_freq2['check']

        # Search in which reference list the last columns belongs - this part of the code will be improved later
        for freq, check in zip(df_freq[column], df_freq['check']):
            # Check in which list belongs the frequency
            if check == 1:
                found_list = next((list_ for list_, freq_list in self.__freq_map.items() if freq in freq_list), "No list was found")
                break
            else:
                found_list = "No list was found"

        return (df_freq, found_list)


    def check_frequencies_interval(self) -> tuple:
        """
        This method aims check if there is a frequency which belongs to a reference frequencies list
        plus +- 5% of interval for each frequency.

        For example, if there is a frequency in a reference frequency list equals to 1. Then, this method will
        check in the interval: [0.95 ~ 1.05]
        
        This method returns a tuple with two elements.

        First, a dataframe wich has a number of columns equals to columns available in
        the initial dataframe (self.df). Note: columns available are those which have float
        or int type.
        
        There is a column called 'check' in this dataframe that represents if a frequency in that
        row are in reference frequencies interval. If true, check = 1, else check = 0.

        The second term in the tuple is a string that shows where the frequency was found (which list)
        
        Args:
            None
            
        Returns:
            Tuple (dataframe, list)
            
        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.check_frequencies_interval()
        """
        # Creates two dataframes because their columns will be compared
        df_freq = self.check_frequency()
        df_freq2 = df_freq.copy()

        list_ref = [utils_ref.ref_min(), utils_ref.ref_15_min(), utils_ref.ref_hora(), utils_ref.ref_dia(), utils_ref.ref_mes()]

        dict_of_lists_95, dict_of_lists_105, dict_all_freq = {}, {}, {}

        # dict_of_lists_95 = {'granularity': [freq * 0.95]} and dict_of_lists_105 = {'granularity': [freq * 1.05]}
        for i, list in enumerate(list_ref):
            dict_of_lists_95[i] = [round(0.95*x, 5) for x in list]
            dict_of_lists_105[i] = [round(1.05*x, 5) for x in list]

        # For each key-value of 0.95, starts at 0.95 until 1.05 summing 0.00001
        for key, value in dict_of_lists_95.items():
            dict_all_freq[key] = [np.arange(value[i], dict_of_lists_105[key][i], 0.00001) for i in range(len(value))]

        # Transforming array in list
        for key, value in dict_all_freq.items():
            dict_all_freq[key] = np.concatenate(value).tolist()

        # Rounding to 5 decimal cases
        for key, values in dict_all_freq.items():
            dict_all_freq[key] = [round(value, 5) for value in values]
        
        # Putting all lists in a single list
        dict_values = [value for values in dict_all_freq.values() for value in values]
        
        # Checking if all frequencies belong to spectre
        for column in df_freq.columns:
            freq_list = []
            for freq in df_freq[column]:
                if freq in dict_values:
                    freq_list.append(1)
                else:
                    freq_list.append(0)
            
            df_freq2[f'check_{column}'] = freq_list

        # Checking diffents columns
        unique_columns = set(df_freq2) - set(df_freq)
        unique_columns = [x for x in unique_columns]

        # Create a dataframe only with differents columns
        df_freq2 = df_freq2[unique_columns]

        # Creates a colum that is 0 when everybody is 0, else 1.
        df_freq2['check'] = (df_freq2 != 0).any(axis=1).astype(int)

        # Copies the new column to original dataframe
        df_freq['check'] = df_freq2['check']

        # Rename the name keys in the dict, because they were as numbers
        renamed_keys = {'minute': 0, 'fifty_minutes': 1, 'hour': 2, 'day': 3, 'month': 4}
        dict_all_freq = {new_key: dict_all_freq[old_key] for new_key, old_key in renamed_keys.items()}
        
        # Search in which reference list the last columns belongs - this part of the code will be improved later
        for freq, check in zip(df_freq[column], df_freq['check']):
            if check == 1:
                found_list = next((lista for lista, freq_list in dict_all_freq.items() if freq in freq_list), "No list was found")
                break
            else:
                found_list = "No list was found"
        
        return (df_freq, found_list)
        

    def multiple_frequncies(self) -> tuple:
        """
        This method aims check if there is a frequency is equals to a multiple of a reference frequencies.
        It's only calculated if there are no frequencies in the reference or in the interval.
        
        This method returns a tuple with two elements.

        First, a dataframe wich has a number of columns equals to columns available in
        the initial dataframe (self.df). Note: columns available are those which have float
        or int type.
        
        There is a column called 'check' in this dataframe that represents if a frequency in that
        row are multiple of reference frequencies. If true, check = 1, else check = 0.

        The second term in the tuple is a string that shows where the frequency was found (which list)
        
        Args:
            None
            
        Returns:
            Tuple (dataframe, list)
            
        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.multiple_frequncies()
        """
        # Check if it's necessary to continue with the code
        df_reference_frequencies = self.check_reference_frequencies()[0]
        df_interval_frequencies = self.check_frequencies_interval()[0]
        if max(df_reference_frequencies['check']) == 0 and max(df_interval_frequencies['check']) == 0:

            for column in df_interval_frequencies.columns:
                # For each frequency, checks if it's possible to divide for each value in the reference list
                # If true, the method returns the frequency. Else, returns 0.
                df_interval_frequencies[column] = df_interval_frequencies[column].apply(lambda x: x if any(x for freq in self.__ref_frequencies if x % freq == 0) else 0)

            # Creates a check column like the last two methods
            df_interval_frequencies['check'] = [0 if x == 0 else 1 for x in df_interval_frequencies[list(df_interval_frequencies.columns)[0]]]

            # Search in which reference list the last columns belongs - this part of the code will be improved later
            for freq, check in zip(df_interval_frequencies[column], df_interval_frequencies['check']):
                # Check in which list belongs the frequency
                if check == 1:
                    lista_encontrada = next((lista for lista, freq_list in self.__freq_map.items() if freq in freq_list), "No list was found")
                    break

            return (df_interval_frequencies, lista_encontrada)
        
        else:
            return (pd.DataFrame({'check': [0]}), 'No list was found')


    def plot_series(self) -> None:
        """
        Plots a series of subplots for each relevant column with various aggregations.

        This method creates a series of subplots with aggregated data for each relevant column in the dataframe.
        The aggregations are specified in the configuration file provided by '__interface' attribute.

        Args:
            None
        
        Returns:
            None

        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.plot_series()
        """
        
        # Create a copy of the original dataframe
        df = self.df.copy()
        
        # Take the first date column of dataframe
        date_colum = self.check_date_column()[0]

        # Make sure if the column is in datetime
        df[date_colum] = pd.to_datetime(df[date_colum])

        # Set index
        df.index = df[date_colum]

        # Order by index
        df = df.sort_index(ascending=True)

        # Iterates for each column, if the column is in float or int type
        for col in self.df.columns:
            dtype = self.df[col].dtype
            if dtype in ['float64', 'int64']:
                title_text = col

                # Initialize a subplot
                fig = make_subplots(rows=8, cols=1,
                                    vertical_spacing=0.025,
                                    shared_yaxes=True,
                                    shared_xaxes=True)
                
                # Set subplot layout
                fig.update_layout(height=1000, title_text=title_text, title_x=0.5)
                
                df_col = df[[col]].copy()
                
                # Create a scatter plot for 10-min interval
                min10 = go.Scatter(
                            name='10 min',
                            x=df_col.index,
                            y=df_col[col],
                            mode='lines',
                            line=dict(color='rgb(12,44,132)'))
                
                fig.add_trace(min10, row=1, col=1)
                fig.update_yaxes(title_text="10 min", row=1, col=1)

                # Iterates by 'sampling' key in the yml file. 'i' is the index value and 'sample' is the value               
                for i, sample in enumerate(self.__interface['sampling']):
                    # Plot a chart for each aggregation
                    series = timeseries.resample(dataset=df_col, rule=sample['rule'])
                    trace = go.Scatter(name=sample['name'],
                                    x=series.index,
                                    y=series['mean'],
                                    mode='lines',
                                    line=dict(color='rgb(12,44,132)'))
                    
                    fig.add_trace(trace, row=i+2, col=1)
                    fig.update_yaxes(title_text=sample['title'], row=i+2, col=1)
                fig.show()
        
        return None


    def plot_date(self, year: int, month: int=None, day: int=None) -> None:
        """
        This method plots a line chart for a specific period for each available column in DataFrame.

        Note: available means column with float or int type.

        Args:
            year (int): The year to filter data for.
            month (int, optional): The month to filter data for.
            day (int, optional): The day to filter data for.

        Returns:
            None

        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.plot_date()
        """
        # Create a copy of the original dataframe
        df = self.df.copy()
        
        # Capture the first date column
        date_colum = self.check_date_column()[0]

        # Ensure the date column is in datetime format
        df[date_colum] = pd.to_datetime(df[date_colum])

        # Set the index
        df.index = df[date_colum]

        # Sort in ascending order by index
        df = df.sort_index(ascending=True)

        # If clause to check if the method is calling by the right way
        if year == None:
            raise ValueError('Year cannot be empty')

        # Get date values
        if year!= None and month != None and day != None:
            df = df.loc[(df.index.year == year) & (df.index.month == month) & (df.index.day == day)]
            name = "{}-{}-{}".format(year, month, day)
        elif year!= None and month != None and day == None:
            df = df.loc[(df.index.year == year) & (df.index.month == month)]
            name = "{}-{}".format(year, month)
        elif year!= None and month == None and day == None:
            df = df.loc[(df.index.year == year)]
            name = "{}".format(year)

        # Plot figure
        for col in self.df.columns:
            title_text = f'{col}'
            dtype = self.df[col].dtype
            if dtype in ['float64', 'int64']:
                df_col = df[[col]].copy()
                year = go.Scatter(
                            name=name,
                            x=df_col.index,
                            y=df_col[col],
                            mode='lines',
                            line=dict(color='rgb(12,44,132)'))

                fig = go.Figure()
                fig.update_layout(height=300, title_text=title_text, title_x=0.5)
                fig.add_trace(year)

                fig.show()
        
        return None


    def missing_status(self) -> None:
        """
        This method aims to check if there are missing values in the series

        Args:
            None

        Returns:
            None

        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.missing_status()
        """
        # Create a copy of the original dataframe
        df = self.df.copy()
        
        # Capture the first date column
        date_colum = self.check_date_column()[0]

        # Ensure the date column is in datetime format
        df[date_colum] = pd.to_datetime(df[date_colum])

        # Set index
        df.index = df[date_colum]

        # Sort in ascending order by index
        df = df.sort_index(ascending=True)
        
        # Check missing values for each column
        for col in self.df.columns:
            dtype = self.df[col].dtype
            if dtype in ['float64', 'int64']:
                missing = self.df.loc[(self.df[col].isnull() == True)]
                
                if missing.shape[0] == 0:
                    return ("There are no missing values in the series.")
                else:
                    return timeseries.missing_stats(original_df=self.df,
                                                    missing_df=missing,
                                                    interface=self.__interface['missing'],
                                                    verbose=True)
        
        return None
                

    def decompose(self, plot=True, period=False) -> pd.DataFrame():
        """
        This method decomposes the time series in trend, sazo and residual
        and shows the results in a chart for each available column.

        Not: available column: type of float or int

        Args:
            plot: 
                - True
                - False
            period:
                - h: hourly
                - d: daily
                - w: weekly
                - m: monthly
                - q: quarterly
                - 2q: bi-annual

        Returns:
            A dataframe where, for each available column, there are 3 new columns:
                1 - f'{coluna}_sazonal'
                2 - f'{coluna}_tendencia'
                3 - f'{coluna}_residuos'

        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.decompose()           
        """
        # Create a copy of the original dataframe
        df = self.df.copy()
        
        # Check the first period of the series
        reference = self.check_reference_frequencies()[0]
        if max(reference['check']) == 1:
            first_freq = float(reference.iloc[:2, 0][reference['check'] == 1])
            first_period = round(1/first_freq)

        interval = self.check_frequencies_interval()[0]
        if max(interval['check']) == 1:
            first_freq = float(interval.iloc[:2, 0][interval['check'] == 1])
            first_period = round(1/first_freq)
        
        multiple = self.multiple_frequncies()[0]
        if max(multiple['check']) == 1:
            first_freq = float(multiple.iloc[:2, 0][multiple['check'] == 1])
            first_period = round(1/first_freq)

        # Capture the first date column
        date_colum = self.check_date_column()[0]

        # Ensure the date column is in datetime format
        df[date_colum] = pd.to_datetime(df[date_colum])

        # Set index
        df.index = df[date_colum]

        # Sort in ascending order by index
        df = df.sort_index(ascending=True)

        df_result = pd.DataFrame()
        for i, coluna in enumerate(self.df.columns):
            dtype = self.df[coluna].dtype
            if dtype in ['float64', 'int64']:
                title_text = f'{coluna} decomposition'
                df_col = df[[coluna]].copy()

                # If period was declared, the code tries to do the decomposition by the period.
                # If it can't, the decomposition will be done using the own time series period.
                if period:
                    try:
                        sample = list(filter(lambda x: x['rule'] == period, self.__interface['sampling']))[0]
                        series = timeseries.resample(dataset=df_col, rule=sample['rule'])[['mean']].dropna(subset=['mean'])
                        decomposition = seasonal_decompose(df_col[coluna], period=eval(sample['period']), model='additive')
                    except:
                        print("este nível de granularidade não é permitido para esta série")
                        print(f"construindo decomposição a partir do período: {first_period}")
                        decomposition = seasonal_decompose(df_col[coluna], period=first_period, model='additive')
                else:
                    decomposition = sm.tsa.seasonal_decompose(df_col[coluna], period=first_period, model='additive')
                
                # Makes the series decomposition
                self.trend = decomposition.trend
                self.seasonal = decomposition.seasonal
                self.residue = decomposition.resid

                # Creates a new dataframe column for each component of the decomposition 
                df_result[f'{coluna}_sazonal'] = decomposition.seasonal
                df_result[f'{coluna}_tendencia'] = decomposition.trend
                df_result[f'{coluna}_residuos'] = decomposition.resid
                
                # If plot == True, then plots charts
                if plot:
                    # Create scatter plots for the different components of decomposition
                    series = go.Scatter(
                                name='series',
                                x=df_col.index,
                                y=df_col[coluna],
                                mode='lines',
                                line=dict(color='rgb(12,44,132)'))

                    trend = go.Scatter(
                                name='trend',
                                x=decomposition.trend.index,
                                y=decomposition.trend,
                                mode='lines',
                                line=dict(color='rgb(12,44,132)'))
                    seasonal = go.Scatter(
                                name='seasonal',
                                x=decomposition.seasonal.index,
                                y=decomposition.seasonal,
                                mode='lines',
                                line=dict(color='rgb(12,44,132)'))
                    resid = go.Scatter(
                                name='resid',
                                x=decomposition.resid.index,
                                y=decomposition.resid,
                                mode='lines',
                                line=dict(color='rgb(12,44,132)'))

                    # Create a subplot with multiple rows and shared axes
                    fig = make_subplots(rows=5, cols=1,
                                        vertical_spacing=0.025,
                                        shared_yaxes=True,
                                        shared_xaxes=True)

                    # Customize the layout of the plot
                    fig.update_layout(height=1000,
                                    title_text=title_text,
                                    xaxis4_showticklabels=True,
                                    showlegend=False,
                                    title_x=0.5)
                    
                    # Add each scatter plot to the subplot
                    fig.add_trace(series, row=1, col=1)
                    fig.add_trace(trend, row=2, col=1)
                    fig.add_trace(seasonal, row=3, col=1)
                    fig.add_trace(resid, row=4, col=1)

                    # Update y-axis titles for each subplot
                    fig.update_yaxes(title_text=self.__interface['decomposition']['yaxis']['title'], row=1, col=1)
                    fig.update_yaxes(title_text=self.__interface['decomposition']['yaxis']['trend'], row=2, col=1)
                    fig.update_yaxes(title_text=self.__interface['decomposition']['yaxis']['season'], row=3, col=1)
                    fig.update_yaxes(title_text=self.__interface['decomposition']['yaxis']['residue'], row=4, col=1)

                    # Show the final plot
                    fig.show()

        return df_result


    def export_file(self) -> str:
        """
        This method exports data in many granularities. The output format files are .csv.
        To do that, it uses a service called services_export_granularity.

        Args:
            None

        Returns:
            A phrase which says that the export was a success.

        Note:
            This method calls two another methods. So, their return must be not None.        
        """
        # Checks data timestamp
        if self.check_timestamp() == '00:15:00':
            list_ref_15m = utils_ref.ref_15_min()
        else:
            list_ref_15m = None
        
        # Calls the return dataframe of each method
        self.df_frequency = self.check_frequencies_interval()[0]
        self.date_column = self.check_date_column()[0]

        # Creates some lists which will be used soon
        lista_colunas, lista_colunas2, lista_colunas3, lista_colunas4 = [], [], [], []

        # Drops 'check' column, because it's needed only the frequency columns
        df_frequency_copy = self.df_frequency.drop('check', axis=1).copy()

        # Gets the column names
        list_frequencies_column_name = list(df_frequency_copy.columns)

        # For each column, fills lists
        for coluna in list_frequencies_column_name:
            export = services_export_granularity.exportFile(df=self.df, df_frequency=self.df_frequency, date_column=self.date_column)

            result = export.create_hour(coluna=coluna)
            result2 = export.create_day(coluna=coluna)
            result3 = export.create_month(coluna=coluna)
            result4 = export.create_year(coluna=coluna)
            
            lista_colunas.append(result[0])
            lista_colunas.append(result[1])

            lista_colunas2.append(result2[0])
            lista_colunas2.append(result2[1])

            lista_colunas3.append(result3[0])
            lista_colunas3.append(result3[1])      

            lista_colunas4.append(result4[0])
            lista_colunas4.append(result4[1])

            # Special case if the data series has 15 min granularity 
            if list_ref_15m is not None:
                lista_colunas_15 = []
                result_15 = export.create_15_minutes(coluna=coluna)
                lista_colunas_15.append(result_15[0])
                lista_colunas_15.append(result_15[1])

                df_final_cd = pd.DataFrame(data=lista_colunas_15).T
                df_final_cd.index = result_15[2]
                df_final_cd = df_final_cd.dropna(how='all')

                df_frequency_copy = self.df_frequency.drop('check', axis=1).copy()

                nome_colunas = df_frequency_copy.columns
                novos_nome_colunas = [item + suffix for item in nome_colunas for suffix in ('_du', '_fds')]
                
                df_final_cd.columns = novos_nome_colunas
                df_final_cd.to_csv(f'_15_min.csv', sep=';')
        
        # In the end, export all files
        export.create_dataframe(lista=lista_colunas, tupla=result, nome=f'_horario')
        export.create_dataframe(lista=lista_colunas2, tupla=result2, nome=f'_diario')
        export.create_dataframe(lista=lista_colunas3, tupla=result3, nome=f'_mensal')
        export.create_dataframe(lista=lista_colunas4, tupla=result4, nome=f'_anual')

        return "The file was successfully exported!"

    
    def export_raw_df(self, file_name=None) -> str:
        """
        This method export all data historical in a .csv file.

        Args:
            None

        Returns:
            A exported file in .csv format.

        Note:
            This method assumes that the data is stored in the 'df' attribute of the class.

        Example:
            instance = YourClass()
            instance.export_raw_df()           
        """
        # Calling the date colum and the main dataframe
        date_column = self.check_date_column()[0]
        raw_df = self.df

        # Set date colum as index
        raw_df.index = raw_df[date_column]

        # Create a list to get all columns, except the date column
        filtered_columns = [col for col in raw_df.columns if col != date_column]

        # Filters df
        raw_df = raw_df[filtered_columns]

        # Gets customer name
        if file_name is None:
            client_name = raw_df.iloc[1, 0]
        else:
            client_name = file_name

        raw_df.to_csv(f'data_history_{client_name}.csv', sep=';')

        return 'The file was exported!'
    

    def check_kind_freq(self) -> str:
        """
        This method checks what kind of frequency group the time series is alocated.
        To do it, the codes check the 'max' column of each result dataframe of these 3 methods:
        check_reference_frequencies(), check_frequencies_interval() and multiple_frequncies().

        Args:
            None

        Returns:
            A phrase

        Note:
            This method calls three another methods. So, their return must be not None.
   
        """
        # Defines the results dataframes
        df_reference_frequencies = self.check_reference_frequencies()[0]
        df_interval_frequencies = self.check_frequencies_interval()[0]
        df_multiple_frequencies = self.multiple_frequncies()[0]

        # Checks if the max value in 'check' column for each dataframe is 1.
        try:
            if max(df_reference_frequencies['check']) == 1:
                return ("It's in the reference frequencies")
            elif max(df_interval_frequencies['check']) == 1:
                return ("It's in the interval frequencies")
            elif max(df_multiple_frequencies['check']) == 1:
                return ("It's in the multiple reference frequencies ")
            else:
                return ("No detectable frequency")
        except:
            return ("No detectable frequency")
  

    def check_stationarity(self, agg: str, plot=True) -> pd.DataFrame():
        """
        This method checks the stationarity of time series data by performing the Augmented Dickey-Fuller test on each column.

        Args:
            agg (str): 
                - h: hourly
                - d: daily
                - w: weekly
                - m: monthly
                - q: quarterly
                - 2q: bi-annual

        Returns:
            pd.DataFrame: A DataFrame with columns as time series variables and rows indicating stationarity (1 for stationary, 0 for non-stationary).
        """
        # Calls the main dataframe
        df = self.df

        # Takes the first date column
        date_colum = self.check_date_column()[0]

        # Ensure the date column is in the datetime format
        df[date_colum] = pd.to_datetime(df[date_colum])

        # Sets index
        df.index = df[date_colum]

        # Resample based on the aggregation
        df = df.resample(agg).sum()

        # Sort the index in ascending order
        df = df.sort_index(ascending=True)

        # Dictionary to store the final results
        dict_result = {}

        for col in self.df.columns:
            dtype = self.df[col].dtype
            if dtype in ['float64', 'int64']:
                lista_col = []
                # ADF Test. "result" = (result, pvalue, lags_used, nobs, critical_values, icbest)
                result = adfuller(df[col])

                if plot:
                    # Interpret result
                    print(f'column: {col}')
                    print(f'Test Statistic: {result[0]:.5f}')
                    print(f'P-Value: {result[1]:.5f}')
                    print(f'Number of Lags Used: {result[2]}')
                    print(f'Number of Observations Used: {result[3]}')
                    print('Critical Values:')
                    for key, value in result[4].items():
                        print(f'   {key}: {value:.5f}')
                    
                # Check stationarity
                if result[1] <= 0.05:
                    print('The series is stationary (we reject the null hypothesis)')
                    lista_col.append(1)
                else:
                    print('The series is not stationary (we fail to reject the null hypothesis)')
                    lista_col.append(0)

                print("\n")
                # Append the result of each column to the dictionary
                dict_result[col] = lista_col
        
        return pd.DataFrame(dict_result)


    def check_autocorrelation(self, agg: str, lags=False, plot=True) -> pd.DataFrame():
        """
        This method checks the autocorrelation of the time series data for each column in the DataFrame.
        
        Args:
            agg (str): Aggregation level ('h' for hourly, 'd' for daily, 'w' for weekly, 'm' for monthly).
            lags (int or bool): Number of lags to consider or False to calculate based on aggregation level.
            plot (bool): Whether to plot the autocorrelation and partial autocorrelation plots.
            
        Returns:
            pandas.DataFrame: DataFrame containing significant partial autocorrelation values and their lags.
                            Empty DataFrame if no significant values found.
        """
        
        df = self.df
        # Takes first date column
        date_colum = self.check_date_column()[0]

        # Ensure the date column is in datetime format
        df[date_colum] = pd.to_datetime(df[date_colum])

        # Sets index
        df.index = df[date_colum]

        # Resamples the data based on the given aggregation level
        df = df.resample(agg).sum()

        # Sorts the DataFrame based on the index
        df = df.sort_index(ascending=True)
        
        if lags == False:
            # Determines the appropriate window based on aggregation level
            if agg == 'h':
                window = 24
            elif agg == 'd':
                window = 30
            elif agg == 'w':
                window = 4
            elif agg == 'm':
                window = 12
            else:
                window = 1
        else:
            window = lags
        
        for col in self.df.columns:
            dtype = self.df[col].dtype
            if dtype in ['float64', 'int64']:
                try:
                    if plot:
                        # Plots the time series data and autocorrelation plots
                        plt.figure(figsize=(12, 6))
                        plt.plot(df[col])
                        plt.xlabel('Lags')
                        plt.ylabel('ACF')
                        plt.title(f'ACF {col}')
                        plt.show()
                        
                        plt.figure(figsize=(12, 6))
                        plot_acf(df[col], lags=window, alpha=0.05)
                        plt.xlabel('Lags')
                        plt.ylabel('ACF')
                        plt.title(f'ACF {col}')
                        plt.show()
                        
                        plt.figure(figsize=(12, 6))
                        plot_pacf(df[col], lags=window)
                        plt.xlabel('Lags')
                        plt.ylabel('PACF')
                        plt.title(f'PACF {col}')
                        plt.show()

                    # Calculates the partial autocorrelation
                    pacf_values = pacf(df[col], nlags=window)

                    # Selects significant lags based on a threshold (5%)
                    significant_lags = np.where(np.abs(pacf_values) > 0.05)[0]
                    significant_pacf = pacf_values[significant_lags]

                    df_lags = pd.DataFrame(significant_pacf, significant_lags)

                    # Perform the Ljung-Box test
                    results = acorr_ljungbox(df[col], lags=window)

                    p_values = results.iloc[:, 1]
                    significant_lags = np.where(p_values < 0.05)[0]


                    if len(significant_lags) > 0:
                        print(f'Data series has {len(significant_lags)} significant values')
                        return df_lags
                    else:
                        print(f'Data series doesnt have any significant values')
                        return pd.DataFrame()
                except:
                    print('The series doesnt have enough sample.')
                    return pd.DataFrame()
         
                
    def calculate_trend(self, plot=False) -> tuple:
        """
        Calculate the linear trend of a time series using linear regression.
        
        Parameters:
        - plot (bool): If True, a scatter plot with the trendline will be displayed.
        
        Returns:
        - tuple: A tuple containing the slope (a) and intercept (b) of the linear trend equation.
        """
        
        # Get the trend component from the decomposition, disabling plotting
        df_trend = self.decompose(plot=False).iloc[:, 1]
        
        # Remove NaN rows introduced due to the seasonal component removal
        df_trend = df_trend.dropna()

        # Prepare data for linear regression
        x = np.arange(len(df_trend)).reshape(-1, 1)
        y = df_trend

        # Fit linear regression model
        model = LinearRegression()
        model.fit(x, y)

        # Retrieve slope (a) and intercept (b)
        a = model.coef_[0]
        b = model.intercept_

        if plot:
            # Plot the scatter plot with trendline
            fig = px.scatter(x=x.flatten(), y=y, trendline='ols')
            fig.update_layout(
                title_text='Trend Line',
                showlegend=True,
                title_x=0.5)
            fig.show()

        return (a, b)