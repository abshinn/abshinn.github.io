---
layout: post
comments: true
title:  "Grid Searching in all the Right Places"
date:   2014-06-08 00:00:00
categories: python sklearn
---

In this last week at the Zipfian Academy, I came across a pretty awesome snippet of code. We have been doing a lot of machine learning in the last few weeks and my work-flow up to last week could be described as a seemingly infinite loop of training on data and tweaking parameters.

### Grid Searching with Scikit Learn

One solution to the inefficient tweak/train work-flow is a grid search. Although feature selection and preliminary exploration of parameter space is still necessary, I will no longer be endlessly tweaking parameters. As it turns out, [Scikit Learn](http://scikit-learn.org/) has created a very elegant way to run its models and parameters [k-fold](http://en.wikipedia.org/wiki/Cross-validation_(statistics)) times in a search grid with [`sklearn.grid_search.GridSearchCV`](http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html).

But before I run the grid search, I need to import all the necessary tools and load in the data. The data needs to be of type `numpy.ndarray`. Personally, I like to do all of my feature scrubbing in another function, which I will call `get_data()` in this case.

```python
from pprint import pprint
from datetime import datetime as dt

from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

X, y = get_data() # user-defined
```

Both `pprint` and `datetime` will be useful for displaying the results of the search. In this example I am using [`sklearn.metrics.roc_auc_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html) - a ROC area-under-the-curve metric with which to compare model runs. 

### Setting up the models and their parameters

To set up the grid search, you can select models by instantiating a [`Pipeline`](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) object, and select parameters by defining a dictionary with keys as `"model__kwarg"` and values as tuples.

Additionally, in order to prepare the data for training I will use [`sklearn.cross_validation.train_test_split`](http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html) to split the data into train and test numpy arrays.

```python
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
```

### Running the search

Next, initialize `GridSearchCV` with a few keyword parameters. `n_jobs` may seem like an innocuous little keyword, but looks are deceiving. `n_jobs = -1` allows you to parallelize your grid search using all of the cores on your machine. Alternatively, you can set `n_jobs` to `-2` to use all but one of your machine's cores - think of it as an index to a list of the cores on your system.

Also note that multi-processing requires grid search to run in a `"__main__"` protected block.

```python
if __name__ == "__main__":
    # initialize grid search
    grid_search = GridSearchCV(pipeline, parameters, n_jobs = -1, verbose = 1, scoring = "roc_auc")
 
    print("\nPerforming grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = dt.now()
    grid_search.fit(xtrain, ytrain)
    print("done in {}\n".format(dt.now - t0))
```

### Well, what now?

Conveniently, `GridSearchCV` stores the best score within the `best_score_` instance attribute, and their respective parameters within the `best_estimator_` attribute. They could be accessed and sent to `stdout` like so:

```python
    print("\nBest score: {:0.3f}".format(grid_search.best_score_))
    print("\nBest parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t{}: {}".format(param_name, best_parameters[param_name]))
```

#### Re-fit

And that's it. Pretty neat, right?

One final note, if you want to make predictions with the optimal parameters set `refit = True` within the `GridSearchCV` instantiation to re-fit the best estimator with the entire data set.

Happy grid searching!
