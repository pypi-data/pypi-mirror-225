from sklearn.datasets import load_wine
import pandas as pd
import numpy as np
np.set_printoptions(precision=4)
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


wine = load_wine()
X = pd.DataFrame(wine.data, columns=wine.feature_names)
y = pd.Categorical.from_codes(wine.target, wine.target_names)

X.shape

X.head()


df = X.join(pd.Series(y, name='class'))


class_feature_means = pd.DataFrame(columns=wine.target_names)

for c, rows in df.groupby('class'):
    class_feature_means[c] = rows.mean()
class_feature_means



within_class_scatter_matrix = np.zeros((13,13))

for c, rows in df.groupby('class'):
    
    rows = rows.drop(['class'], axis=1)
        
    s = np.zeros((13,13))
    for index, row in rows.iterrows():
        
            x, mc = row.values.reshape(13,1), class_feature_means[c].values.reshape(13,1)        
            s += (x - mc).dot((x - mc).T)
        
    within_class_scatter_matrix += s

