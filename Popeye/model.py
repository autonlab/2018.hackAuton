from sklearn.neural_network import MLPClassifier
import csv
import numpy as np
from sklearn.metrics import classification_report,confusion_matrix
from textblob import TextBlob


### This model only input the profile and semantic features of troll profiles
### Profiles and semantic features of real accounts has to be appended to the X (input vector) and Y (output vector {0 for fake accounts and 1 for real accounts})

### Input of profile features from csv file
inputprofilecsv="introllprof.csv"
read2=csv.reader(open(inputprofilecsv,newline=""),delimiter=",")
i=0
X=[]
for row2 in read2:
	i+=1
	if i==1:
		continue
	else:
		row2=np.array(row2)
		inp2 = row2.astype(np.float)
		inp2=list(inp2)
		X.append(inp2)

### Input of tweet semantic feature from csv file
inputtweetscsv="introlltweets.csv"
read=csv.reader(open(inputtweetscsv,newline=""),delimiter=",")
j=0
for row in read:
	j=j+1
	if j==126:
		break
	else:
		moditags=["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN",
		"NNS","NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM",
		"TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"]
		tagcount=np.zeros(37,dtype=float)
		tagcoutn=list(tagcount)
		str=TextBlob(row[0])
		t=str.tags
		sent=str.sentiment.polarity
		for i in t:
			ind=moditags.index(i[1])
			tagcount[ind]=tagcount[ind]+1
		tagcount[36]=sent
		tagcount=list(tagcount)
		e=0
		while e!=37:
			X[j-1].append(tagcount[e])
			e=e+1


# X=[[0.0,0.0],[1.0,1.0]]
Y=np.zeros(j-1)
# Y=np.random.randint(2, size=i-1)
# Y=np.random.randint(2, size=2)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(30,30), random_state=1)
print(clf.fit(X,Y))


