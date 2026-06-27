from scipy.stats import randint,uniform

LIGHTGM_PARAMS={
    'n_estimators': [100, 300, 500, 1000],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'num_leaves': [15, 31, 50, 100],
    'max_depth': [-1, 5, 10, 20],
    'min_child_samples': [10, 20, 50],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'reg_alpha': [0, 0.1, 1],
    'reg_lambda': [0, 0.1, 1]
}


RANDOM_SEARCH_PARAMS = {
    'n_iter' : 5,
    'cv' : 2,
    'n_jobs':-1,
    'verbose' :2,
    'random_state' : 42,
    'scoring' : 'accuracy'
}

