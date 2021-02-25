# Stock Selection
A stock selection project based on ticker mentions in social media.

# Setup
Set up a file called *local_config.py* in the configurations
directory that has the following structure:

```
import os

class LocalConfig:

    # CPU count
    NUM_CPUS = os.cpu_count() - 2

    # Reddit credentials
    REDDIT_CLIENT_ID = 'XXX'
    REDDIT_CLIENT_SECRET = 'XXX'
    REDDIT_USERNAME = 'XXX'
    REDDIT_PASSWORD = 'XXX'
    REDDIT_USER_AGENT = 'XXX'

    # Twitter credentials
    TWITTER_CONSUMER_KEY = 'XXX'
    TWITTER_CONSUMER_SECRET = 'XXX'
    TWITTER_ACCESS_TOKEN = 'XXX'
    TWITTER_ACCESS_TOKEN_SECRET = 'XXX'
```
A Reddit account as well as a Twitter account are needed
so that the required credentials can be generated.
