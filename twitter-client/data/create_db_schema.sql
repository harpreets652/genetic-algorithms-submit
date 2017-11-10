\connect cs_776;

CREATE SCHEMA TSS_DEV
  AUTHORIZATION system;

\echo 'Creating USERS table IN TSS_DEV'
CREATE TABLE TSS_DEV.USERS (
  user_id                            BIGINT PRIMARY KEY,
  name                               CHAR(255) DEFAULT NULL,
  screen_name                        CHAR(255) DEFAULT NULL,
  statuses_count                     INTEGER   DEFAULT NULL,
  followers_count                    INTEGER   DEFAULT NULL,
  friends_count                      INTEGER   DEFAULT NULL,
  favourites_count                   INTEGER   DEFAULT NULL,
  listed_count                       SMALLINT  DEFAULT NULL,
  url                                TEXT      DEFAULT NULL,
  lang                               CHAR(25)  DEFAULT NULL,
  time_zone                          CHAR(100) DEFAULT NULL,
  location                           CHAR(255) DEFAULT NULL,
  default_profile                    BOOLEAN   DEFAULT FALSE,
  default_profile_image              BOOLEAN   DEFAULT FALSE,
  geo_enabled                        BOOLEAN   DEFAULT FALSE,
  profile_image_url                  TEXT      DEFAULT NULL,
  profile_banner_url                 TEXT      DEFAULT NULL,
  profile_use_background_image       BOOLEAN   DEFAULT FALSE,
  profile_background_image_url_https TEXT      DEFAULT NULL,
  profile_text_color                 CHAR(50)  DEFAULT NULL,
  profile_image_url_https            TEXT      DEFAULT NULL,
  profile_sidebar_border_color       CHAR(50)  DEFAULT NULL,
  profile_background_tile            BOOLEAN   DEFAULT FALSE,
  profile_sidebar_fill_color         CHAR(50)  DEFAULT NULL,
  profile_background_image_url       TEXT      DEFAULT NULL,
  profile_background_color           CHAR(50)  DEFAULT NULL,
  profile_link_color                 CHAR(50)  DEFAULT NULL,
  utc_offset                         INTEGER   DEFAULT NULL,
  is_translator                      BOOLEAN   DEFAULT FALSE,
  follow_request_sent                TEXT      DEFAULT NULL,
  protected                          BOOLEAN   DEFAULT FALSE,
  verified                           BOOLEAN   DEFAULT FALSE,
  notifications                      TEXT      DEFAULT NULL,
  description                        TEXT      DEFAULT NULL,
  contributors_enabled               BOOLEAN   DEFAULT FALSE,
  following                          TEXT      DEFAULT NULL,
  created_at                         TEXT      DEFAULT NULL,
  timestamp                          TIMESTAMP DEFAULT NULL,
  crawled_at                         TIMESTAMP DEFAULT NULL,
  updated                            TIMESTAMP DEFAULT NULL,
  is_user_genuine                    BOOLEAN   DEFAULT FALSE
);


\echo 'Creating TWEETS table IN TSS_DEV'
CREATE TABLE TSS_DEV.TWEETS (
  tweet_id                BIGINT PRIMARY KEY,
  user_id_fk              BIGINT REFERENCES TSS_DEV.USERS,
  tweet_text              CHAR(255) DEFAULT NULL,
  source                  TEXT      DEFAULT NULL,
  truncated               BOOLEAN   DEFAULT FALSE,
  in_reply_to_status_id   BIGINT    DEFAULT NULL,
  in_reply_to_user_id     BIGINT    DEFAULT NULL,
  retweeted_status_id     BIGINT    DEFAULT NULL,
  in_reply_to_screen_name CHAR(255) DEFAULT NULL,
  geo                     TEXT      DEFAULT NULL,
  place                   CHAR(500) DEFAULT NULL,
  contributors            TEXT      DEFAULT NULL,
  retweet_count           INTEGER   DEFAULT NULL,
  reply_count             INTEGER   DEFAULT NULL,
  favorite_count          INTEGER   DEFAULT NULL,
  favorited               BOOLEAN   DEFAULT FALSE,
  retweeted               BOOLEAN   DEFAULT FALSE,
  possibly_sensitive      BOOLEAN   DEFAULT FALSE,
  num_hashtags            SMALLINT  DEFAULT NULL,
  num_urls                SMALLINT  DEFAULT NULL,
  num_mentions            SMALLINT  DEFAULT NULL,
  created_at              TEXT      DEFAULT NULL,
  timestamp               TIMESTAMP DEFAULT NULL,
  crawled_at              TIMESTAMP DEFAULT NULL,
  updated                 TIMESTAMP DEFAULT NULL
);


\echo 'Creating USERS_FEATURES table IN TSS_DEV'
CREATE TABLE TSS_DEV.USERS_FEATURES (
  user_id                             BIGINT PRIMARY KEY,
  is_user_genuine                     BOOLEAN  DEFAULT FALSE,
  avg_length_chars                    SMALLINT DEFAULT NULL,
  avg_length_words                    SMALLINT DEFAULT NULL,
  fract_contains_question             DECIMAL  DEFAULT NULL,
  fract_contains_exclamation          DECIMAL  DEFAULT NULL,
  fract_contains_multiple_quest_exlam DECIMAL  DEFAULT NULL,
  fract_contains_emoticon_frown       DECIMAL  DEFAULT NULL,
  fract_contains_emoticion_smile      DECIMAL  DEFAULT NULL,
  fract_contains_pronoun_first_p      DECIMAL  DEFAULT NULL,
  fract_contains_pronoun_second_p     DECIMAL  DEFAULT NULL,
  fract_contains_pronoun_third_p      DECIMAL  DEFAULT NULL,
  fract_contains_urls                 DECIMAL  DEFAULT NULL,
  avg_number_of_urls                  DECIMAL  DEFAULT NULL,
  contains_urls_top_100               BOOLEAN  DEFAULT FALSE,
  fract_contains_user_mention         DECIMAL  DEFAULT NULL,
  fract_contains_hashtag              DECIMAL  DEFAULT NULL,
  fract_contains_stock_sym            DECIMAL  DEFAULT NULL,
  fract_retweeted                     DECIMAL  DEFAULT NULL,
  most_commonly_tweeted_day           CHAR(4)  DEFAULT NULL,
  most_commonly_tweeted_hour          SMALLINT DEFAULT NULL,
  avg_sentiment_pos_words             DECIMAL  DEFAULT NULL,
  avg_sentiment_neg_words             DECIMAL  DEFAULT NULL,
  avg_sentiment_score                 DECIMAL  DEFAULT NULL,
  user_age                            SMALLINT DEFAULT NULL,
  user_status_count                   INTEGER  DEFAULT NULL,
  user_num_followers                  INTEGER  DEFAULT NULL,
  user_num_friends                    INTEGER  DEFAULT NULL,
  user_verified                       BOOLEAN  DEFAULT NULL,
  user_has_description                BOOLEAN  DEFAULT NULL,
  user_has_url                        BOOLEAN  DEFAULT NULL,
  process_error                       TEXT     DEFAULT NULL
);