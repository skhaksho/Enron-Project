import sys
import cPickle
import matplotlib.pyplot as plt
import numpy as np
#sys.path.append("C:\\Users\\Sam\\Desktop\\CMPT732\\spark-1.6.2-bin-hadoop2.6\\python")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

### Load the dictionary containing the dataset
data_dict = cPickle.load(open("C:\\Users\\Sam\\Desktop\\CMPT732\\project\\gitup\\final_project_dataset.pkl","r") )

# Preparing all features and data to test.

features_to_test = ['poi',
                    'bonus',
                    'salary',
                    'deferral_payments',
                    'deferred_income',
                    'director_fees',
                    'exercised_stock_options',
                    'expenses',
                    'total_payments',
                    'total_stock_value',
                    'from_messages',
                    'from_poi_to_this_person',
                    'from_this_person_to_poi',
                    'loan_advances',
                    'long_term_incentive',
                    'other',
                    'restricted_stock',
                    'restricted_stock_deferred',
                    'salary',
                    'shared_receipt_with_poi',
                    'to_messages'
                   ]
data_to_test = featureFormat(data_dict, features_to_test)
print(data_to_test.shape)
import pandas as pd
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 0)

def to_pandas(data_dict):
    df = pd.DataFrame(data_dict)
    df = df.convert_objects(convert_numeric=True)
    df = df.transpose()
    df.reset_index(level=0, inplace=True)
    
    columns = list(df.columns)
    columns[0] = 'name'
    df.columns = columns
    return(df)
df = to_pandas(data_dict)
df.to_csv('dataset.csv')
#print ', '.join(df.keys())
heads = df.head(5)
#print(heads)

#%pylab inline

# data_to_test = featureFormat(data_dict_updated, features_to_test)
# fig = plt.figure(figsize=(15, 30))

# for idx, feature in enumerate(features_to_test):
    # ax = plt.subplot(7,3, idx+1)
    # plt.title(feature)
    # plt.xticks(rotation='vertical')
    # plt.subplots_adjust(hspace=.6) 
    # ax.hist(data_to_test[:,idx])
	
random = 13
import copy

my_dataset = copy.deepcopy(data_dict)

from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import MinMaxScaler

combined_features = FeatureUnion([
        ('scale', MinMaxScaler())
    ])

estimators = [
    ('features', combined_features),
    ('classify', DecisionTreeClassifier(random_state=random))
]

pclf = Pipeline(estimators)

test_classifier(pclf, data_dict_updated, features_to_test)

features_to_test_no_aggregates = [
    'poi',
    'bonus',
    'salary',
    'deferral_payments',
    'deferred_income',
    'director_fees',
    'exercised_stock_options',
    'expenses',
    'from_messages',
    'from_poi_to_this_person',
    'from_this_person_to_poi',
    'loan_advances',
    'long_term_incentive',
    'other',
    'restricted_stock',
    'restricted_stock_deferred',
    'salary',
    'shared_receipt_with_poi',
    'to_messages'
]

combined_features = FeatureUnion([
        ('scale', MinMaxScaler())
    ])

estimators = [
    ('features', combined_features),
    ('classify', DecisionTreeClassifier(random_state=random))
]

pclf = Pipeline(estimators)

test_classifier(pclf, data_dict_updated, features_to_test_no_aggregates)

