# %%

import json
import requests
#Set the base URL and ITEM_ID
BASE_URL = 'https://api.figshare.com/v2'

#%%

ITEM_ID = 24986532
#Retrieve public metadata from the endpoint
s=requests.get(BASE_URL + '/articles/' + str(ITEM_ID))
#Load the metadata as JSON
metadata=json.loads(s.text)
#View the metadata
print(json.dumps(metadata, indent=2))


# %%

# TODO: stáhněte všechna data

# %%

%matplotlib inline
from ufit.lab import *

# set a template, so that data can be referenced by number only
set_datatemplate('%06d')
# read one dataset from a file, with given X and Y columns
data = read_data(84905, 'QL', 'CNTS')

data.plot()
show()

# %%


# TODO - vytvořte model pro data
# viz https://pythonhosted.org/ufit/models.html

model = Background() + ???

# fit the model, then print and plot the result
result = model.fit(data)
result.printout()
result.plot()
show()
# %%


# TODO: vytvořte hezčí graf

