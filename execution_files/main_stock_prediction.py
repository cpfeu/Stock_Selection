from data_pulling import *
from data_evaluation import *
from datetime import datetime
from configurations.global_config import GlobalConfig
from execution_files.execution_parameters_stock_prediction import ExecutionParameters


def main():

    # starting time
    starting_time = datetime.now()
    print(starting_time, ': Program started.')
    print(GlobalConfig.SEPARATION_STR)

    # pull stock data of the most mentioned stock ticker which should be manually defined in the
    # <execution_parameters_stock_prediction> file
    stock_puller = StockPuller(api_key=GlobalConfig.ALPHA_VANTAGE_API_KEY_EXTENDED_HISTORY,
                               ticker=ExecutionParameters.TICKER, interval=ExecutionParameters.TIME_INTERVAL_STR)
    stock_puller.pull_data()

    # predict
    stock_predictor = StockPredictor(ticker=ExecutionParameters.TICKER,
                                     time_interval_str=ExecutionParameters.TIME_INTERVAL_STR,
                                     time_interval_int=ExecutionParameters.TIME_INTERVAL_INT,
                                     num_past_hours=ExecutionParameters.NUM_PAST_HOURS,
                                     num_prediction_hours=ExecutionParameters.NUM_PREDICT_HOURS,
                                     store_in_db=ExecutionParameters.STORE_IN_DB)
    stock_predictor.compute_predictions()
    stock_predictor.visualize_prediction_results()
    stock_predictor.plot_autocorrelation()
    stock_predictor.plot_partial_autocorrelation()

    # ending time
    ending_time = datetime.now()
    print(GlobalConfig.SEPARATION_STR)
    print(ending_time, ': Program finished.')

    # execution length
    print('Program took', ending_time - starting_time, 'to run.')


if __name__ == '__main__':
    main()
