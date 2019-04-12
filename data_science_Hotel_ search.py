import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import sklearn
import seaborn as sns
import re
from collections import Counter
%matplotlib inline
# Import and initiate a vectorizer.
from sklearn.feature_extraction.text import CountVectorizer
# Import a random forest model.
from sklearn.ensemble import RandomForestClassifier

# Import the Data Set.
data = pd.read_csv('https://github.com/Thinkful-Ed/data-201-resources/raw/master/hotel-reviews.csv')

# Perform some basic cleaning and character removal.

# Make everything lower case.
data['reviews.text'] = data['reviews.text'].str.lower()

# Remove non-text characters.
data['reviews.text'] = data['reviews.text'].str.replace(r'\.|\!|\?|\'|,|-|\(|\)', "",)

# Fill in black reviews with '' rather than Null (which would give us errors).
data['reviews.text'] = data['reviews.text'].fillna('')

​
# The max features is how many words we want to allow us to create columns for.
vectorizer = CountVectorizer(max_features=5000)

# Vectorize our reviews to transform sentences into volumns.
X = vectorizer.fit_transform(data['reviews.text'])

# And then put all of that in a table.
bag_of_words = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())

# Rename some columns for clarity.
data.rename(columns={'address': 'hotel_address', 'city': 'hotel_city',
                     'country':'hotel_country', 'name':'hotel_name'},
            inplace=True)

# Join our bag of words back to our initial hotel data.
full_df = data.join(bag_of_words)

# X is our words.
X = bag_of_words

# Y is our hotel name (the outcome we care about).
Y_hotel = data['hotel_name']


# Import a random forest model.
rfc = RandomForestClassifier()

# Fit that random forest model to our data.
rfc.fit(X,Y_hotel)

RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=10, n_jobs=1, oob_score=False, random_state=None,
            verbose=0, warm_start=False)


# If you want to run a different test review, start from here.

# Write your own dream vacation review here...
test_review = ['''
    I loved the beach and the sunshine and the clean and modern room.
    ''']

# Convert your test review into a vector.
X_test = vectorizer.transform(test_review).toarray()

# Match your review.
prediction = rfc.predict(X_test)[0]

# Return the essential information about your match.
data[data['hotel_name'] == prediction][['hotel_name', 'hotel_address', 
                                        'hotel_city', 'hotel_country']].head(1)
