# JsonDF [Json parser for DataFrane usage]

This package is a package for converting nested Json/Dictionaries/Lists for DataFrame usage

## Download

for latest release
```
pip install JsonDF==1.0.3
```
## Normal Usage

and to use it : 

```python
from JsonDf.Data import Data

data = Data(prefix="your_prefered_prefix_default_is_root", data=YourJson)

data.childs() #for processing the childs of the Json/Dict/List
print(data.rows) #organized dictionary with the data !! Not for DataFrame usage
data.flatten() #for flattening the result for DataFram usage
print(data.rows_flatten) #flatten the data for DataFrame usage
```

## Json type usage

In Json type you have the ability to parse Json/Dict in the sameway it parsed in JQuery, in addition to the ability to make objects automatically from json/dict

### create Json

to use it : 

```python
from Json.utils.Json import Json

some_json = {
  'keys' : {
    "another_key": "some_value",  
    },
}

json = Json(json=some_json, name=any_name)
json.objectify()
print(json)
print(json.keys)
print(json.keys.another_key)
```

### insert and update values in Json

you can add values inside the Json as you want,
use the insert method

```python
json.insert(name='name', value='value')
```

keep in mind that you add in the base level,
which mean that if you have two Jsons inside each other, and you want to add in the secod Json,
you need to access it first to add in it.
I'll try to fix this problem later.

NOTE : you can update values in Json by using the same insert method if the name is already exist.

### delete values totally

you can totally delete keys and its values from the Json using the delete method, in this case the name and its value
will be deleted

```python
json = Json(name='json_name', json={'key': 'value'})
json.delete('key')
print(json')

#  output :
#  {}
#  empty because the 'key' key and it's values is deleted
```
you've to know that when you delete a key, it's deleted the Json object it self not from the original template it has started with,
so if the edits was made in the json was new and was made by JsonDf, deleting it will delete it with no coming back.

### dumping values from keys

you can dump values from keys and make the key equals to empty value depends on its type, by using the `dump()` method

```python
json = Json(name='json_name', json={'key': 'value'})
json.dump('key')
print(json')

#  output :
#  {'key': ''}
#  empty because the 'key' key and it's values is deleted
```
the type of the value is determined with the same type that it was with in the Json Object, to change it you've to update it
with the `insert()` method after the `objectify()` other wise it will still with the same type.

feel free to contribute in this project.

cheers.
