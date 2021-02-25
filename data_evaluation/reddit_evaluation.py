import os
import json
import multiprocessing
from configurations.global_config import GlobalConfig


class RedditEvaluator:

    def __init__(self):
        self.reddit_dicts_list = os.listdir('../data/reddit_dicts')
        with open('../data/company_names_dict.json', 'r') as file:
            self.company_names_dict = json.load(file)

        # create directory and delete old files
        os.makedirs('../data/reddit_evaluation_dicts', exist_ok=True)
        for file in os.listdir('../data/reddit_evaluation_dicts'):
            os.remove(os.path.join('../data/reddit_evaluation_dicts', file))

    def count_company_ticker_occurrences(self):

        # load list of company tickers
        company_ticker_list = ['$'+symbol for symbol in list(self.company_names_dict.keys())]

        # create argument list for multiprocessing worker
        arg_list = [(reddit_dict, company_ticker_list) for reddit_dict in self.reddit_dicts_list]

        # start multiprocessing
        with multiprocessing.Pool(GlobalConfig.NUM_CPUS) as mp:
            mp.starmap(self.count_company_ticker_occurrences_worker, arg_list)

    def count_company_name_occurrences(self):
        pass

    @classmethod
    def count_company_ticker_occurrences_worker(cls, reddit_dict_name, company_ticker_list):

        # load reddit_dict
        with open('../data/reddit_dicts/' + reddit_dict_name, 'r') as file:
            reddit_dict = json.load(file)

        # create count dictionary
        count_dict = dict()

        # iterate over each ticker
        for idx, ticker in enumerate(company_ticker_list):
            if idx % 1000 == 0:
                print('Searching for ticker with index ' + str(idx) + ' out of around 7000...')

            # add ticker to count dictionary
            count_dict.update({ticker: 0})

            # iterate over each reddit
            for _, reddit_post_value in reddit_dict.items():
                reddit_title = reddit_post_value.get(GlobalConfig.REDDIT_POST_TITLE_STR)
                reddit_text = reddit_post_value.get(GlobalConfig.REDDIT_POST_TEXT_STR)
                if (' ' + ticker + ' ' in reddit_title) or (' ' + ticker + ' ' in reddit_text):
                    count_dict[ticker] = count_dict.get(ticker) + 1

                # iterate over each comment of the respective reddit
                reddit_comment_dict = reddit_post_value.get(GlobalConfig.REDDIT_POST_COMMENTS_STR)
                for _, reddit_comment_value in reddit_comment_dict.items():
                    reddit_comment = reddit_comment_value.get(GlobalConfig.REDDIT_COMMENT_TEXT_STR)
                    if ' ' + ticker + ' ' in reddit_comment:
                        count_dict[ticker] = count_dict.get(ticker) + 1

        # store created dictionaries in reddit_evaluation_dicts
        with open('../data/reddit_evaluation_dicts/'+reddit_dict_name[:-22]+'_evaluation.json', 'w') as file:
            json.dump(count_dict, file)
