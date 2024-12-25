# Session 11
### [👉 Watch the session recordings]()

### [👉 Slides]()

## Goals 🎯

## Questions

### Vincent Reynard Satyadharma
Based on your experience, how do you establish the baseline performance for you initial models?

Especially for difficult problem like this, I feel like we need to convince the client that our model's performance is justified.

### Jayant Sharma
Is it a good practice to subclass the original model class like XGBRegressor when defining your model class XGBRegressor. This way we might not need to define all functions, right?

Please try it, and let me know.
https://en.wikipedia.org/wiki/Composition_over_inheritance


### Jayant Sharma
so for each trial, the objective will be calculated for all the n_splits times, right? Cant we use a holdout validation (normal validation) data instead of cross validation?