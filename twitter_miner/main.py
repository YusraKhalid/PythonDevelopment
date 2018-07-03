__author__ = 'abdul'

import argparse
import sys
import twitter_reader


def check_arg(args=None):
    """
    Takes arguments as input
    """
    parser = argparse.ArgumentParser(description='Twitter mining script')
    parser.add_argument('-s', '--string',
                        help='String to search for tweets',
                        required='True',
                        type=str,
                        default='Fifa 2018')
    parser.add_argument('-n', '--number',
                        help='Number of tweets to collect',
                        type=int,
                        default='5')
    results = parser.parse_args(args)
    return (results.string,
            results.number)

if __name__ == '__main__':
    string, count = check_arg(sys.argv[1:]) # Receive arguments

    try:
        tweet_reader = twitter_reader.TwitterReader()
        searched_tweets = tweet_reader.read_tweets(string, count) # Start mining
        for tweet in searched_tweets:
            tweet.print()
            print("------")
    except ValueError as v:
        print(format(v))
