# ML Boilerplate

This is a collection of tools and modules which can be used in machine learning.

- The first toolbox will be a 'Train, Assess, Predict' object for XGBoost linear regression.
The objective will be to have an object in which a DataFrame can be passed, along with descriptions of the
binary, text, numeric and categorical columns, and the object will be able to:
 -  Train a new model
 -  Produce performance metrics
 -  Make predictions on new data

## CREDIT

The transformers and pipelines in this toolbox are derived from these blog posts from <a href='https://github.com/ramhiser'>John Ramey</a> (awaiting permission confirmation) and <a href='https://github.com/tomderuijter'>Tom De Ruijter</a> (awaiting permission confirmation).

Inspiration:
- <a href='https://ramhiser.com/post/2018-04-16-building-scikit-learn-pipeline-with-pandas-dataframe/'>Ramhiser Blog</a>

- <a href='https://medium.com/bigdatarepublic/integrating-pandas-and-scikit-learn-with-pipelines-f70eb6183696'>Tom De Ruijter Medium article</a>
