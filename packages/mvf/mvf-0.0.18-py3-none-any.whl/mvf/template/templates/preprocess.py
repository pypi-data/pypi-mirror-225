# ---
# jupyter:
#   kernelspec:
{% if python -%}
#     display_name: Python 3
#     language: python
#     name: python3
{% else -%}
#     display_name: R
#     language: R
#     name: ir
{% endif %}# ---

# %%
# Imports
{% if python -%}
import pandas
import feather
{% else -%}
library(arrow)
{% endif %}

# %% tags=["parameters"]
# Do not edit this cell
{% if python -%}
upstream = None
product = None
input_features = []
target_features = []

print(f'Input features are: {input_features}')
print(f'Target features are: {target_features}')
{% else -%}
upstream = NULL
product = NULL
input_features = list()
target_features = list()

print('Input features:')
print(unlist(input_features))
print('Target features:')
print(unlist(target_features))
{% endif %}

# %% [markdown]
# Write code to fetch and preprocess data here.
#
# Ensure you split data into 2 {% if python -%}pandas.DataFrame{% else -%}R data.frame{% endif %} objects:
#
# * **X** - input features
# * **y** - target features

# %%
# Save data for next process
{% if python -%}
feather.write_dataframe(X, product['X_data'])
feather.write_dataframe(y, product['y_data'])
{% else -%}
write_feather(X, product[['X_data']])
write_feather(y, product[['y_data']])
{% endif %}