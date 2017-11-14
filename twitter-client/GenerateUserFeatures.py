import os
import psycopg2 as psyco
from psycopg2 import extras
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import SqlStatements
from datetime import datetime
from numpy import long

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PROPERTIES_FILE = 'twitter-client.properties'
properties = dict(line.strip().split('=') for line in open(ROOT_DIR + '/' + PROPERTIES_FILE))

conn = psyco.connect(dbname="cs_776", user="system", password="system", host="localhost")


def run(batchSize, numOfThreads):
    while True:
        curs = conn.cursor()
        try:
            curs.execute(SqlStatements.GEN_FEATURES_FOR_USERS_SELECT)
        except Exception as e:
            print("Unable to select users to process. Exception: {}".format(e))
            return

        usersToProcess = curs.fetchmany(batchSize)

        if not usersToProcess:
            print("Features generated for all users, quitting")
            return
        curs.close()

        completionCounter = 0
        totalNumber = len(usersToProcess)
        with ThreadPoolExecutor(max_workers=numOfThreads) as executor:
            futures = [executor.submit(generateFeatures, userId) for userId in usersToProcess]

            for future in as_completed(futures):
                try:
                    futureResult = future.result()

                    if futureResult:
                        completionCounter += 1
                except Exception as e:
                    print("Exception occurred while retrieving results.\nException: {}".format(e))

        print("{} users successfully processed out of {}".format(completionCounter, totalNumber))

    return


def generateFeatures(userId):
    with conn:
        try:
            # get user data
            userFeatures = generateUserFeatures(conn, userId)

            usertTweetFeatures = generateTweetFeatures(conn, userId)

            data = {'user_id': userId}
            data.update(userFeatures)
            data.update(usertTweetFeatures)

            sql = SqlStatements.UPDATE_USER_FEATURES
            result = True
        except Exception as e:
            data = {'user_id': userId,
                    'process_error': str(e)}
            sql = SqlStatements.UPDATE_USER_FEATURES_ERROR
            result = False

        with conn.cursor() as curs:
            SqlStatements.modifyData(conn, curs, sql, data)

    return result


def generateUserFeatures(connection, userId):
    readCursor = connection.cursor(cursor_factory=extras.NamedTupleCursor)
    readCursor.execute(SqlStatements.SELECT_USER_DATA, {'user_id': userId})

    userData = readCursor.fetchone()

    readCursor.close()

    userFeatures = {}

    # is user genuine
    userFeatures['is_genuine'] = userData.is_user_genuine

    # registration age
    regAge = (datetime.now() - userData.timestamp).days
    userFeatures['user_age'] = regAge

    # statuses count on day
    userFeatures['user_status_count'] = userData.statuses_count

    # number of followers
    userFeatures['user_num_followers'] = userData.followers_count

    # number of friends
    userFeatures['user_num_friends'] = userData.friends_count

    # is user verified
    userFeatures['user_verified'] = userData.verified

    # has description?
    description = userData.description
    userFeatures['user_has_description'] = True if description and description != 'NULL' else False

    # has url?
    url = userData.url
    userFeatures['user_has_url'] = True if url and url != 'NULL' else False

    return userFeatures


def generateTweetFeatures(connection, userId):
    readCursor = connection.cursor(cursor_factory=extras.NamedTupleCursor)

    readCursor.execute(SqlStatements.SELECT_TWEET_TEXT_FEATURES, {'user_id': userId})
    tweetFeaturesFromSql = readCursor.fetchone()

    # todo: need to handle case of user with no tweets...all tweet-based features 0?
    # easy to do: just set the default to be 0 for the column (excluding the user tweets)
    # TODO: LOOK FOR OTHER ERROR SCENARIOS: when using records, what if the record isn't there?

    readCursor.execute(SqlStatements.SELECT_MOST_COMMONLY_TWEETED_HOUR, {'user_id': userId})
    mostCommonlyTweetedHour = readCursor.fetchone()

    readCursor.execute(SqlStatements.SELECT_TWEET_COUNT_BY_DAY, {'user_id': userId})
    tweetCountByDay = readCursor.fetchall()

    readCursor.execute(SqlStatements.SELECT_NUM_TWEETS_MULTIPLE_QUEST_EXCLAM, {'user_id': userId})
    tweetCountMultiQuestAndExclam = readCursor.fetchone()

    readCursor.close()

    userTweetFeatures = {}

    # average number of characters
    userTweetFeatures['avg_length_chars'] = int(tweetFeaturesFromSql.avg_length_char)

    # average number of words
    userTweetFeatures['avg_length_words'] = int(tweetFeaturesFromSql.avg_length_words)

    totalNumTweets = int(tweetFeaturesFromSql.total_count)

    # fraction containing question marks
    fractQuestionMarks = int(tweetFeaturesFromSql.num_question_marks) / totalNumTweets
    userTweetFeatures['fract_contains_question'] = fractQuestionMarks

    # fraction containing exclamation marks
    fractionExclamMarks = int(tweetFeaturesFromSql.num_exclam_marks) / totalNumTweets
    userTweetFeatures['fract_contains_exclamation'] = fractionExclamMarks

    # fraction containing multiple exclamation or question marks
    numOfTweetsWithMultiQuestAndExclam = int(tweetCountMultiQuestAndExclam.tweet_count)
    userTweetFeatures['fract_contains_multiple_quest_exlam'] = numOfTweetsWithMultiQuestAndExclam / totalNumTweets

    # fraction containing urls
    fractionUrls = int(tweetFeaturesFromSql.num_containing_urls) / totalNumTweets
    userTweetFeatures['fract_contains_urls'] = fractionUrls

    # average number of urls
    userTweetFeatures['avg_number_of_urls'] = long(tweetFeaturesFromSql.avg_num_urls)

    # fraction containing user mentions
    fractContainsUserMention = int(tweetFeaturesFromSql.num_containing_mentions) / totalNumTweets
    userTweetFeatures['fract_contains_user_mention'] = fractContainsUserMention

    # fraction containing hashtags
    userTweetFeatures['fract_contains_hashtag'] = int(tweetFeaturesFromSql.num_containing_hashtags) / totalNumTweets

    # fraction retweeted
    userTweetFeatures['fract_retweeted'] = int(tweetFeaturesFromSql.num_retweeted) / totalNumTweets

    # most commonly tweeted hour
    userTweetFeatures['most_commonly_tweeted_hour'] = int(mostCommonlyTweetedHour.tweet_hour)

    # tweet count by day
    countByDayPrefix = 'num_tweets_day_'
    for days in SqlStatements.DAY_OF_WEEK_POSTGRES_MAPPING.values():
        userTweetFeatures[countByDayPrefix + days] = 0

    for countByDay in tweetCountByDay:
        userTweetFeatures[countByDayPrefix +
                          SqlStatements.DAY_OF_WEEK_POSTGRES_MAPPING[countByDay.tweet_day]] = int(countByDay.num_tweets)

    return userTweetFeatures


run(5, 5)
