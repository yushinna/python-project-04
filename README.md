# Store Inventory
## Description
A console application that allows you to easily interact with data for a store's inventory.
The data needs to be cleaned from the CSV before it is to be persisted in the database. All interactions with the records should use ORM methods for viewing records, creating records, and exporting a new CSV backup.

## Requirements
Activate the virtual environment by running the following command in your terminal.

If using Mac/Linux:
```
source ./env/bin/activate
```
If using Windows:
```
.\env\Scripts\activate
```

Install the project requirements from the provided requirements.txt file by running the following command in your terminal:
```
pip install -r requirements.txt
```

## Usage
Run the application so you can connect to the database, load the CSV products data into the created table, and make menu choices and interact with the application.
```
python app.py
```
