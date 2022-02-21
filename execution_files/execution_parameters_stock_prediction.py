from configurations.global_config import GlobalConfig


class ExecutionParameters:

    # define stock ticker for which predictions shall be made
    TICKER = 'FTK'

    # define time interval for stock data to pull
    TIME_INTERVAL_STR = GlobalConfig.FIVE_MIN_INTERVAL_STR

    # define lag intervals for auto correlation and partial auto correlation
    TIME_INTERVAL_INT = GlobalConfig.FIVE_MIN_INTERVAL_INT

    # define past time in hours that shall be taken into account for predictions
    NUM_PAST_HOURS = 6

    # define number of hours that shall be predicted
    NUM_PREDICT_HOURS = 1

    # how much time in the past should be considered to perform time series analysis
    STOCK_DATA_HORIZON = GlobalConfig.SLICE_LIST_SHORT

    STORE_IN_DB = True
