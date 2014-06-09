---
layout: post
comments: true
title:  "Grid Searching in all the Right Places"
date:   2014-06-08 00:00:00
categories: python, sklearn
---

In this last week at the Zipfian Academy, I came across a game-changing snippet of code. We have been doing a lot of machine learning in the last few weeks and my work-flow could be described as a seemingly infinite loop of tweaking parameters and training on my data. There is a better way.

### Grid Searching with Scikit Learn

```python
from pprint import pprint
from datetime import datetime as dt

from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

X, y = get_data() # user-defined

if __name__ == "__main__":
    pipeline = Pipeline([
        #( 'clf', LogisticRegression()),
        ('kNN', KNeighborsClassifier()),
    ])

    parameters = {
        #'clf__C': (1, 10),
        #'clf__penalty': ('l1', 'l2'),
        'kNN__n_neighbors': (5, 10, 30),
    }
  
    # split data into train and test set
    xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size = .10, random_state = 1)

    # initialize grid search
    grid_search = GridSearchCV(pipeline, parameters, n_jobs = -1, verbose = 1, scoring = "roc_auc")

    print("\nPerforming grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = dt.now()
    grid_search.fit(xtrain, ytrain)
    print("done in {}\n".format(dt.now - t0))

    print("\nBest score: {:0.3f}".format(grid_search.best_score_))
    print("\nBest parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t{}: {}".format(param_name, best_parameters[param_name]))
```
