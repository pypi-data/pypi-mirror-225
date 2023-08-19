# hubmap-sdk

---
A Python interface to the various HuBMAP web services

### Overview

The hubmap sdk is a client library that allows for easy integration of the API's associated with HuBMAP. 

### Using hubmap-sdk

The hubmap-sdk library is available through PyPi via the command:

```bash
pip3 install hubmap-sdk
```
hubmap-sdk requirements can be found [here](requirements.txt)

## Documentation
Documentation and examples can be found here

* [hubmapsdk](https://software.docs.hubmapconsortium.org/sdk/hubmapsdk.html)
* [entitysdk](https://software.docs.hubmapconsortium.org/sdk/entitysdk.html)
* [searchsdk](https://software.docs.hubmapconsortium.org/sdk/searchsdk.html)

### Building and Publishing hubmap-sdk

<a href="https://pypi.org/project/setuptools/">SetupTools</a> and <a href="https://pypi.org/project/wheel/">Wheel</a> is required to build the sdk distribution. <a href="https://pypi.org/project/twine/">Twine</a> is required to publish to Pypi

Build the distribution directory with: 

```bash
python3 setup.py sdist bdist_wheel
```

from within the python-sdk project directory

To publish, from inside the project directory, run:

```bash
twine upload dist/*
```

A prompt to enter login information to the hubmap Pypi account will appear


### Files 

This code contains:

**collection.py** Contains the Collection class. This is used for creation and modification of Collection objects.

**dataset.py** Contains the Dataset class. This is used for creation and modification of Dataset objects.

**donor.py** Contains the Donor class. This is used for creation and modification of Donor objects.

**entity.py** Contains the Entity class. This is the base class for the Donor, Dataset, Upload, Collection, and Sample classes

**entitysdk.py** This file contains the primary methods used to interface with the Entity Api. These methods are part of the EntitySdk class. An instance of this class is needed to use the various methods in this class. For a detailed breakdown of the various methods within entitysdk.py, visit <a href="https://api.docs.hubmapconsortium.org">api.docs.hubmapconsortium.org</a>  

**sample.py** Contains the Sample class. This is used for creation and modification of Sample objects.

**sdk_helper.py** This helper function contains various functions used frequently throughout the sdk. These include make_entity() and make_request()

**searchsdk.py** This file contains the primary methods used to interface with the Search Api. These methods are part of the EntitySdk class. An instance of this class is needed to use the various methods in this class. For a detailed breakdown of the various methods within searchsdk.py, visit <a href="https://api.docs.hubmapconsortium.org">api.docs.hubmapconsortium.org</a>  

**upload.py** Contains the Upload class. This is used for creation and modification of Upload objects.
