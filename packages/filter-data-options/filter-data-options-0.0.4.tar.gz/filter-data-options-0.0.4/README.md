# streamlit-custom-component

Streamlit component that allows you to display or not particular data selected

## Installation instructions

```sh
pip install filter-data-options
```

## Usage instructions

```python
import streamlit as st

from filter_data_options import filter_data_options

variables:
- data (list of dictionaries), 
- legendData (list of dictionaries), 
- showLegend (boolean),
- styles (dictionary or dictionaries), 
- submitBtnName (string - name of submit button), 
- deleteBtnName (string - name of delete all btn), 
- key (unique identified for component)

value = filter_data_options(**variables)

st.write(value)
```