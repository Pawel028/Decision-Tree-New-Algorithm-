The Data_Tree_BinaryDepvar class is designed to create a decision tree, allowing users to customize the splitting decision metric using the metric_string variable. This class operates on a Pandas dataframe, with the dependent variable specified by depvar and the set of variables to be used for decision-making defined by usable_vars.

Parameters
depvar: Specifies the dependent variable in the dataset.
usable_vars: List of variables to be used for decision-making.
min_size_to_split: Minimum size of nodes to trigger splitting.
metric_string: A user-defined metric string for decision-making, utilizing the Pandas dataframe mat.

Ensure that your data is in the form of a Pandas dataframe for compatibility.

Feel free to explore and customize the class based on your specific use case!
