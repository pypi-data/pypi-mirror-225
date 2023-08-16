# PyDbJson

`pydbjson` is a simple Python library for managing JSON-based databases.

## Table of Contents

- [Installation](#installation)
- [Description](#Description)
- [Usage](#usage)

## Installation

You can install `pydbjson` using pip:
```python
pip install pydbjson
```


## Description

`pydbjson` provides a convenient way to interact with JSON-based databases in Python. It allows you to load data from a JSON file, insert, retrieve, delete, and find documents, and save the data back to the file.

## Usage

### Importing the library

```python
from pydbjson.pydbjson import pydbjson
```

### Creating an instance of pydbjson

```python
db = pydbjson("database.json")
```

Create an instance of the `pydbjson` class by providing the filename or path of the JSON database file.

### Inserting a document

```python
document = {"name": "John", "age": 30}
key = db.insert_one(document)
```

Insert a document into the database. The `insert_one` method returns the key of the inserted document.

### Find a document

```python
document = {"name": "John"}
found_document = db.find_one(document)
```

Find a document from the database based on the provided data.

### Deleting a document

```python
db.delete_one(found_document)
```

Delete a document from the database based on the data.