union = Pipeline([
    ('features_union', Pipeline([
        ('text_pipeline', Pipeline([
            ('selector', TextSelector(key=column)),
            ('vectoriser', TfidfVectorizer(stopwords='english')),
            ('select_features', SelectKBest())
        ])),
        ('categorical_pipeline', Pipeline([
            ('selector', DataFrameSelector(key=column)),
            ('one_hot', OneHotEncoder(handle_unknown='ignore')),
            ('select_features', SelectKBest())
        ])),
    ])),
    ('classifier', MODEL())
])
