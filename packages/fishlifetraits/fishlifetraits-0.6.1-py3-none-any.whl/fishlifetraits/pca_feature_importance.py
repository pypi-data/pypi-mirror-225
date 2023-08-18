
from operator import le
import numpy as np
import pandas as pd
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


plt.rcParams["figure.figsize"] = (10,10)

# iris = datasets.load_iris()
# ## prota processing
# prota_drop = ['group', 'rank', 'au_test']

# prota_features = pd.read_csv('/Users/ulises/Desktop/GOL/software/GGpy/proofs_ggi/prota/features_prota_original.tsv',sep='\t')
# prota_labels = pd.read_csv('/Users/ulises/Desktop/GOL/software/GGpy/proofs_ggi/prota/joined_out_ggi_1024exons.tax_prop80_TreeId.tsv', sep = '\t')

# prota_labels_c = (prota_labels[prota_labels['rank'] == 1]
#                     .rename(columns={'alignment': 'aln_base'})
#                     .drop(prota_drop, 1)
#                     .reset_index().drop(['index'], 1))

# iris = prota_features.merge(prota_labels_c, on = 'aln_base')
## prota

## flatfishes
iris = pd.read_csv('/Users/ulises/Desktop/GOL/software/GGpy/proofs_ggi/postRaxmlBug/flatfishes/two_hypo_ASTRAL-ML/raxml_noRaxmlBug_7_h1_h2_features_hypos.csv', sep = ',')
## flatfishes

drop_columns = [
            'Group', 'aln_base', 
            'SymPval', 'MarPval', 
            'IntPval'
        ]

for c in drop_columns:
    try:
        iris = iris.drop( c, 1 )
    except KeyError:
        pass

# ## flatfishes
iris = iris[ (iris['hypothesis']  == 1) |  (iris['hypothesis']  == 2)]
# ## flatfishes

## prota
# iris = iris[ (iris['tree_id']  == 1) |  (iris['tree_id']  == 2)]
## prota

X0  = iris.drop('hypothesis', axis=1)
labels = X0.columns

y = iris['hypothesis']

# X = iris.data
# y = iris.target
#In general a good idea is to scale the data
scaler = StandardScaler()
scaler.fit(X0)
X=scaler.transform(X0)

pca = PCA()
x_new = pca.fit_transform(X)

def myplot(score,coeff,labels=None):
    xs = score[:,0]
    ys = score[:,1]
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    plt.scatter( xs * scalex, ys * scaley, c = y )
    for i in range(n):
        plt.arrow( 0, 0, coeff[i,0], coeff[i,1], color = 'r', alpha = 0.5 )
        if labels is None:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("PC{}".format(1))
    plt.ylabel("PC{}".format(2))
    plt.grid()

#Call the function. Use only the 2 PCs.

myplot(x_new[:,0:2],np.transpose(pca.components_[0:2, :]), labels=labels)
plt.savefig('/Users/ulises/Desktop/ABL/ecomunch/flat_fishes.png', dpi = 130)
plt.close()
# plt.show()

pc_ratios = pca.explained_variance_ratio_


pcs = []
seen = []
pc_index = 0
for marr in abs( pca.components_ ):
    tmp_label = labels[np.argmax(marr)]
    if not (tmp_label in seen):
        percentage = pc_ratios[pc_index]*100
        pc_label = "PC %s (%.3f %%)" % (pc_index + 1, percentage)
        pcs.append((pc_label, tmp_label))
    
    pc_index += 1


