import os
import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from data_evaluation.erros import ErrorAnalyzer
from configurations.global_config import GlobalConfig


class DataHandler:

    def __init__(self, ticker, time_interval, num_past_hours, num_prediction_hours):

        """
        Load the data of the specified ticker with the specified time interval that has been pulled.
            Only the samples that were recorded within <num_past_hours> hours are kept.
            If the sample was recorded within <num_prediction_hours> it is put into the test set.
        :param ticker: stock ticker
        :param time_interval: 1min, 5min, ... (specified at pull request)
        :param num_past_hours: how far into the past should the program consider stock prices
        :param num_prediction_hours: how far ahead shall the program predict stock prices
        """

        # get data
        data_pd = pd.read_csv(filepath_or_buffer=os.path.join('../data/stock_csv_files',
                                                              str(ticker) + '_' + str(time_interval) + '.csv'),
                              sep=',', header=0, index_col=False)
        data_dict = data_pd.to_dict(orient='list')
        for key, value in data_dict.items():
            data_dict[key] = value[::-1][1:]

        # extract relevant data
        # time_window_train_start = datetime.now() - timedelta(hours=num_past_hours, minutes=0)
        # time_window_test_start = datetime.now() - timedelta(hours=num_prediction_hours, minutes=0)

        time_window_train_start = datetime.strptime('2022-02-18 20:00:00', '%Y-%m-%d %H:%M:%S') - timedelta(hours=num_past_hours, minutes=0)
        time_window_test_start = datetime.strptime('2022-02-18 20:00:00', '%Y-%m-%d %H:%M:%S') - timedelta(hours=num_prediction_hours, minutes=0)

        self.train_prices = []
        self.train_timestamps = []
        self.test_prices = []
        self.test_timestamps = []
        for ts_idx in range(0, len(list(data_dict.get(GlobalConfig.STOCK_PARAM_TIME)))):
            timestamp = datetime.strptime(data_dict.get(GlobalConfig.STOCK_PARAM_TIME)[ts_idx], '%Y-%m-%d %H:%M:%S')
            if timestamp >= time_window_train_start:
                open_val = data_dict.get(GlobalConfig.STOCK_PARAM_OPEN)[ts_idx]
                if timestamp >= time_window_test_start:
                    self.test_timestamps.append(timestamp.strftime('%H:%M'))
                    self.test_prices.append(open_val)
                else:
                    self.train_timestamps.append(timestamp.strftime('%H:%M'))
                    self.train_prices.append(open_val)


class StockPredictor:

    def __init__(self, ticker, time_interval_str, time_interval_int, num_past_hours, num_prediction_hours, store_in_db):

        # build train and test time series with stock data
        self.data_handler = DataHandler(ticker, time_interval_str, num_past_hours, num_prediction_hours)

        # initialize variables for instance functions
        self.ticker = ticker
        self.time_interval_int = time_interval_int
        self.store_in_db = store_in_db
        self.ses_train = None
        self.ses_test = None
        self.des_train = None
        self.des_test = None
        self.tes_train = None
        self.tes_test = None

    def compute_predictions(self):

        """
        This function performs single, double and triple exponential smoothing over the train time series.
            It then uses bootstrapping to predict the prices in the test time series.
        """

        # get single exponential smoothing (sem) predictions
        self.ses_train, self.ses_test = self.compute_ses(train=self.data_handler.train_prices,
                                                         test=self.data_handler.test_prices,
                                                         alpha=0.5)
        self.compute_forecast_errors(x=self.data_handler.test_prices, y=self.ses_test)
        print(GlobalConfig.SEPARATION_STR)

        # get double exponential smoothing (des) predictions
        self.des_train, self.des_test = self.compute_des(train=self.data_handler.train_prices,
                                                         test=self.data_handler.test_prices,
                                                         alpha=0.5,
                                                         beta=0.5)
        self.compute_forecast_errors(x=self.data_handler.test_prices, y=self.des_test)
        print(GlobalConfig.SEPARATION_STR)

        # Store double exponential smoothing rmse together with ticker in postgres database
        if self.store_in_db:
            conn = psycopg2.connect(database=GlobalConfig.DB_NAME,
                                    user=GlobalConfig.USER,
                                    password=GlobalConfig.PW,
                                    host=GlobalConfig.HOST,
                                    port=GlobalConfig.PORT)
            cur = conn.cursor()
            ticker, rmse = self.ticker, ErrorAnalyzer(original=self.data_handler.test_prices,
                                                      forecast=self.des_test).get_rmse()
            cur.execute("INSERT INTO stock_predictions (ticker, rmse) VALUES(%s, %s);", (self.ticker, rmse))
            conn.commit()
            print('Added record to postgres database.')
            cur.close()
            conn.close()

    def visualize_prediction_results(self):

        """
        The function plots the original time series as well as the different smoothed time series.
            The train and test sections are separated with a vertical line (see samples in <examples> folder).
        """

        timestamps = self.data_handler.train_timestamps + self.data_handler.test_timestamps
        train_prices = self.data_handler.train_prices + self.data_handler.test_prices
        sem = self.ses_train + self.ses_test
        des = self.des_train + self.des_test

        plt.plot(timestamps, train_prices, label='Actual Price')
        plt.plot(timestamps, sem, label='Single Exponential Smoothing')
        plt.plot(timestamps, des, label='Double Exponential Smoothing')

        plt.axvline(x=self.data_handler.train_timestamps[-1], color='black', linestyle='--')
        plt.text(x=self.data_handler.train_timestamps[int(len(self.data_handler.train_timestamps) / 2)],
                 y=min(self.data_handler.train_prices), s='Train Zone')
        plt.text(x=self.data_handler.test_timestamps[int(len(self.data_handler.test_timestamps) / 3)],
                 y=min(self.data_handler.train_prices), s='Prediction Zone')
        plt.title('Stock Price Prediction for ' + str(self.ticker))
        plt.xlabel('Time')
        plt.xticks(rotation=70)
        plt.ylabel('Price')
        plt.legend()

        os.makedirs('../results', exist_ok=True)
        plt.savefig(fname='../results/stock_price_prediction_plot.png', dpi=300)

        plt.show()

    def plot_autocorrelation(self):

        """
        Compute the auto correlation for a number of 24 lags.
            For example, if the value of <time_interval_int> is set to 5,
            the auto correlation for a time lag of 5, 10, ...120 minutes is calculated.
        """

        # get relevant correlations
        x_axis_values = [str(i * self.time_interval_int) + ' min' for i in (range(1, 25))]
        correlation_list = []
        for lag in range(1, 25, 1):
            corr = np.corrcoef(x=self.data_handler.train_prices[lag:],
                               y=self.data_handler.train_prices[:len(self.data_handler.train_prices) - lag])
            correlation_list.append(corr[0, 1])

        # plot results
        plt.bar(x=x_axis_values, height=correlation_list, width=0.9)
        plt.xlabel('Lag')
        plt.xticks(rotation=30)
        plt.ylabel('Correlation')
        plt.title('Auto-correlation plot for ' + str(self.ticker))

        os.makedirs('../results', exist_ok=True)
        plt.savefig(fname='../results/auto_correlation_plot.png', dpi=300)

        plt.show()

    def plot_partial_autocorrelation(self):

        """
        Compute the partial auto correlation for a number of 24 lags.
            For example, if the value of <time_interval_int> is set to 5,
            the auto correlation for a time lag of 5, 10, ...120 minutes is calculated.
        """

        x_axis_values = [str(i * self.time_interval_int) + ' min' for i in (range(1, 25))]
        correlation_list = []

        for lag in range(1, 25, 1):

            # build matrices for closed form regression solution
            design_matrix = []
            y_vector = []
            x_start_idx = 0
            y_idx = x_start_idx + lag
            while y_idx < len(self.data_handler.train_prices):
                data_point = [1] + self.data_handler.train_prices[x_start_idx: x_start_idx + lag]
                design_matrix.append(data_point)
                y_vector.append(self.data_handler.train_prices[y_idx])
                x_start_idx += 1
                y_idx += 1
            design_matrix = np.array(design_matrix)
            y_vector = np.array(y_vector)

            # calculate least squares ridge regression closed form solution
            weight_vector = np.dot(
                                   np.dot(
                                          np.linalg.inv(
                                                        np.dot(design_matrix.T,
                                                               design_matrix) +
                                                        0.0001 * np.identity(design_matrix.shape[1])),
                                          design_matrix.T),
                                   y_vector)

            # extract relevant weight for partial auto correlation at current lag
            partial_auto_correlation = weight_vector[1]
            correlation_list.append(partial_auto_correlation)

        # plot results
        plt.bar(x=x_axis_values, height=correlation_list, width=0.9)
        plt.xlabel('Lag')
        plt.xticks(rotation=30)
        plt.ylabel('Correlation')
        plt.title('Partial auto-correlation plot for ' + str(self.ticker))

        os.makedirs('../results', exist_ok=True)
        plt.savefig(fname='../results/partial_auto_correlation_plot.png', dpi=300)

        plt.show()

    @staticmethod
    def compute_ses(train, test, alpha):

        """
        Compute single exponential smoothing over the train prices
            and use bootstrapping to predict prices after the train period.
        :param train: list of stock prices in the train time frame
        :param test: list of stock prices in the test time frame
        :param alpha: smoothing factor
        """

        # initialize prediction at t=0 and smooth train time series
        y_hat_train_list = [train[0]]
        for t in range(0, len(train) - 1, 1):
            y_hat_t_plus_1 = alpha * train[t] + (1 - alpha) * y_hat_train_list[t]
            y_hat_train_list.append(y_hat_t_plus_1)

        # bootstrapping forecasts
        y_hat_test_list = [y_hat_train_list[-1]]
        for t in range(0, len(test), 1):
            y_hat_t_plus_1 = alpha * train[-1] + (1 - alpha) * y_hat_test_list[t]
            y_hat_test_list.append(y_hat_t_plus_1)
        y_hat_test_list.pop(0)

        return y_hat_train_list, y_hat_test_list

    @ staticmethod
    def compute_des(train, test, alpha, beta):

        """
        Compute double exponential smoothing over the train prices
            and use bootstrapping to predict prices after the train period
        :param train: list of stock prices in the train time frame
        :param test: list of stock prices in the test time frame
        :param alpha: smoothing factor for the level
        :param beta: smoothing factor for the trend
        """

        # initialize prediction at t=0 and smooth train time series
        level_t0 = train[0]
        level_t_minus_1 = level_t0
        trend_t0 = train[1] - train[0]
        trend_t_minus_1 = trend_t0
        y_hat_train_list = [train[0], train[1]]
        for t in range(1, len(train) - 1, 1):
            level_t = alpha * train[t] + (1 - alpha) * y_hat_train_list[t]
            trend_t = beta * (level_t - level_t_minus_1) + (1 - beta) * trend_t_minus_1
            y_hat_plus_1 = level_t + trend_t
            y_hat_train_list.append(y_hat_plus_1)
            level_t_minus_1 = level_t
            trend_t_minus_1 = trend_t

        # bootstrapping forecast
        y_hat_test_list = [level_t_minus_1 + trend_t_minus_1]
        for t in range(0, len(test) - 1, 1):
            level_t = alpha * train[-1] + (1 - alpha) * y_hat_test_list[t]
            trend_t = beta * (level_t - level_t_minus_1) + (1 - beta) * trend_t_minus_1
            y_hat_plus_1 = level_t + trend_t
            y_hat_test_list.append(y_hat_plus_1)
            level_t_minus_1 = level_t
            trend_t_minus_1 = trend_t

        return y_hat_train_list, y_hat_test_list

    @staticmethod
    def compute_forecast_errors(x, y):
        error_analyzer = ErrorAnalyzer(original=x, forecast=y)
        print('RMSE:', error_analyzer.get_rmse())
        print('MAE:', error_analyzer.get_mae())
        print('MAPE:', error_analyzer.get_mape())
