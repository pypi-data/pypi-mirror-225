## Title

QSEA refers to the Qlik Sense Engine API. 

## Description

QSEA intends to automate most basic operations with Qlik Sense Enterprise apps in a pythonic way.
With QSEA you can quickly view and edit variables, master measures and dimensions, as well as main sheet objects. For example, you can replace variables in all master measures of your app in one line

```python
for ms in App.measures: ms.update(definition = replace(ms.definition, '$(var1)', '$(var2)'))
```
or quickly move all measures from one app to another:

```python
for ms in App1.measures: App2.measures.add(name = ms.name, definition = ms.definition)
```

```python
Installation

pip install qsea
```

## Getting started

QSEA uses Qlik Sense Engine API via the Qlik Sense Proxy Service as a main tool, so you'll need correct API credetentials to start working with QSEA. Please refer to following links for help.

https://help.qlik.com/en-US/sense-developer/May2023/Subsystems/EngineAPI/Content/Sense_EngineAPI/GettingStarted/connecting-to-engine-api.htm

https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Admin/mc-generate-api-keys.htm


Your credetentials should look something like this
```python
header_user = {'Authorization': 'Bearer <Very long API KEY>'}
qlik_url = "wss://server.domain.com[/virtual proxy]/app/"
```

Now we can connect to the Qlik Server:
```python
conn = qsea.Connection(header_user, qlik_url)
```

Let's create an App object which is a representation of the application in Qlik Sense.
```python
app = qsea.App(conn, 'MyAppName')
```

By default the App class object is almost empty. Use load() function to make use of it:
```python
app.load()
```

Now all variables, master measuers and dimensions are uploaded to our App object. We can access them by their name:
```python
var = app.variables['MyVar']
var.definition
```

```python
ms = app.measures['MyMeasure']
ms.label_expression
```

or overview their properties via pandas dataframe:
```python
app.dimensions.df
```

Let's create a new measure:
```python
app.measures.add(name = 'MyMeasure', definition = 'sum(Sales)')
```

or update a variable:
```python
var.update(definition = 'sum(Sales)')
```

Save the app in order for changes to reflect in the real Qlik Sense application 
```python
app.save()
```

Let's copy the set of master dimensions in a new app:
```python
source_app = qsea.App(conn, 'Source AppName')
target_app = qsea.App(conn, 'Target AppName')
source_app.load()
target_app.load()

for dim in source_app.dimensions:
    if dim.name not in [target_dim.name for target_dim in target_app.dimensions]: target_app.dimensions.add (name = dim.name, definition = dim.definition)

target_app.save()
```

For unknown reasons, on certain instances of Qlik Sense, changes in the App can not be seen in the Qlik Sense interface. The usual workaround is to make a new copy of the Application (via QMC or Hub). Usually all changes can be seen in the copy.

Note that as it stands, only basic properties, such as names, definitions and a couple of others can be accesed via qsea module.

Most of read-only operations (such as loading apps) can be performed on published apps. However, it is recommnded to modify objects only in unpublished apps.

Besides master measures, master dimensions and variables, tables and charts in the App can be also uploaded.

```python
app.load()
sh = app.sheets['MySheet']
sh.load()
for obj in sh.objects:
    for ms on obj.measures:
        print(ms.definition)
```

Good luck!

### App class
The class, representing the Qlik Sense application. This is the main object to work with. The class is empty when created; run the load() function to make use of it.

#### load()
Loads data from the Qlik Sense application into an App object.

Args:
* depth (int): depth of loading
    - 1 - app + variables, measures, sheets, fields, dimensions (default value)
    - 2 - everything from 1 + sheet objects (tables, sharts etc.)
    - 3 - everything from 2 + object dimensions and measures

Different levels can be useful while working with large apps for which full load can be time-consuming.
Only dimensions and measures from standard Qlik Sense charts are uploaded. Uploading dimensions from filter panes is currently not supported.

```
App.load(level = 3)
```

#### save()
You have to save the App object for the changes to be reflected in the Qlik Sense Application. Note that it is recommnded to modify objects only in unpublished apps.
```
App.save()
```

#### reload_data()
Starts the script of reloading data into the Qlik Sense Application.
```
App.reload_data()
```

#### children
app.load(level = 1) creates several objects of AppChildren class

### AppChildren class
The class contains collections of master objects in the Qlik Sense Application:
* app.variables: a collection of Variable class objects, representing the variables of the Qlik Sense application
* app.measures: a collection of Measure class objects, representing the master measures of the Qlik Sense application
* app.dimensions: a collection of Dimension class objects, representing the master dimensions of the Qlik Sense application
* app.sheets: a collection of Sheet class objects, representing the sheets of the Qlik Sense application 
* app.fields: a collection of Field class objects, representing the fields of the Qlik Sense application

You can access the main information in pandas dataframe about each group of objects via .df:
```python 
app.variables.df
``` 
#### add()
Use `add()` function to add new variables, master measures or master dimensions to the app. 

Args:
* name (str): Name of the object to be created.
* definition (str): Definition of the object to be created.
* description (str, optional): Description of the object to be created. Defaults to ''.
* label (str, optional): Label of the object to be created. Defaults to ''.
* label_expression (str, optional): Label expression of the object to be created. Defaults to ''.
* format_type (str, optional): Format type of the object to be created. Defaults to 'U'.
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec (int, optional): Number of decimals of the object to be created. Defaults to 10.
* format_use_thou (int, optional): Use thousands separator of the object to be created. Defaults to 0.
* format_dec (str, optional): Decimal separator of the object to be created. Defaults to ','.
* format_thou (str, optional): Thousands separator of the object to be created. Defaults to ''.

Returns: True if the object was created successfully, False otherwise.
Only parametres applicable to the certain class will be used
```
App.variables.add(name = 'MyVar', definition = 'sum(Sales)')
App.measures.add(name = 'MyFunc', definition = 'sum(Sales)', format_type = 'F')
App.dimensions.add(name = 'MyDim', definition = 'Customer')
```

### Variable class
The class, representing variables of the application. Member of the App.variables collection.
You can call the exact variable via it's name or iterate them
```
var = app.variables['MyVar']
print(var.definition)

for var in app.variables:
    if var.definition == 'sum(Sales)': var.update(name = 'varSales')
```
#### variable properties
* name: that's the name of the variable you generally use in the Qlik Sense interface
* definition: the formula behind the variable
* description: the description of the variable
* auxiliary
    - handle: the internal handle of the object in Qlik Sense Engine API; can be  used to access the variable via `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the variable
    - parent: App-children object; you can access the App class object like this `var.parent.parent`
    - created_date: creation date of the variable, as stored in Qlik Sense
    - modified_date: date of the last modification of the variable, as stored in Qlik Sense
    - script_created: True if the variable is created via the application load script, False if not

#### update()
Updates the variable on the Qlik Sense Server

Args:
* definition (str): new definition of the variable (leave None to keep the old value)
* description (str): new description of the variable (leave None to keep the old value)

Returns:
    True if the variable was updated successfully, False otherwise
```
var = app.variables['MyVar']
var.update(definition = 'sum(Sales)')
app.save()
```

#### delete()
Deletes the variable from the Qlik Sense Server

Returns:
    True if the variable was deleted successfully, False otherwise

```
var = app.variables['MyVar']
var.delete()
app.save()
```

#### rename()
Renames the variable on the Qlik Sense Server. Since there is no direct method to rename the variable, it basically deletes the variable with the old name, and creates a new one, with the new name.

Returns:
    True if the variable is renamed succesfully, False otherwise

```
var = app.variables['MyVar']
var.rename('MyVarNewName')
app.save()
```

### Measure class
The class, representing master measures of the application. Member of the App.measures collection.
You can call the exact measure via it's name or iterate them
```
ms = app.measures['MyMeasure']
print(ms.definition)

for ms in app.measures:
    if ms.definition == 'sum(Sales)': ms.update(name = 'Sales')
```
#### measure properties
* name: that's the name of the measure you generally use in the Qlik Sense interface
* definition: the formula behind the measure
* description: the description of the measure
* label: the label of the measure, as it appears in charts
* label_expression: the label expression of the measure
* format_type: Format type of the object
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec: Number of decimals of the object
* format_use_thou: Use thousands separator of the object
* format_dec: Decimal separator of the object
* format_thou: Thousands separator of the object
* auxiliary
    - handle: the internal handle of the object in Qlik Sense Engine API; can be used to access the measure via `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the measure
    - parent: AppChildren object; you can access the App class object like this `ms.parent.parent`
    - created_date: creation date of the measure, as stored in Qlik Sense
    - modified_date: date of the last modification of the measure, as stored in Qlik Sense

#### update()
Updates the measure on the Qlik Sense Server

Args: 
* definition (str, optional): The definition of the measure
* description (str, optional): the description of the measure
* label (str, optional): the label of the measure, as it appears in charts
* label_expression (str, optional): the label expression of the measure
* format_type (str, optional): Format type of the object to be created. Defaults to 'U'.
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec (int, optional): Number of decimals of the object to be created. Defaults to 10.
* format_use_thou (int, optional): Use thousands separator of the object to be created. Defaults to 0.
* format_dec (str, optional): Decimal separator of the object to be created. Defaults to ','.
* format_thou (str, optional): Thousands separator of the object to be created. Defaults to ''.

Returns: 
    True if the measure was updated successfully, False otherwise

```
ms = app.measures['MyMeasure']
ms.update(definition = 'sum(Sales)', label = 'Total Sales', format_type = 'F')
app.save()
```

#### delete()
Deletes the measure from the Qlik Sense Server

Returns:
    True if the measure was deleted successfully, False otherwise

```
ms = app.measures['MyMeasure']
ms.delete()
app.save()
```

#### rename()
Renames the measure on the Qlik Sense Server.

Returns:
    True if the measure is renamed succesfully, False otherwise

```
ms = app.measures['MyMeasure']
ms.rename('MyMeasureNewName')
app.save()
```

### Dimension class
The class, representing master dimensions of the application. Member of the App.dimensions collection.
You can call the exact dimension via it's name or iterate them.
Note that hierarchical dimensions are not yet supported.

```
dim = app.dimensions['MyDimension']
print(dim.definition)

for dim in app.dimensions:
    if dim.definition == '[Customer]': dim.update(name = 'Customer_dimension')
```

#### dimension properties
* name: that's the name of the dimension you generally use in the Qlik Sense interface
* definition: the formula behind the dimension
* label: the label of the dimension, as it appears in charts
* auxiliary
    - handle: the internal handle of the object in Qlik Sense Engine API; can be used to access the dimension via `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the dimension
    - parent: AppChildren object; you can access the App class object like this `dim.parent.parent`
    - created_date: creation date of the dimension, as stored in Qlik Sense
    - modified_date: date of the last modification of the dimension, as stored in Qlik Sense

#### update()
Updates the dimension on the Qlik Sense Server

Args: 
* definition (str, optional): The definition of the dimension
* label (str, optional): the label of the dimension, as it appears in charts

Returns: 
    True if the dimension was updated successfully, False otherwise

```
dim = app.dimensions['MyDimension']
dim.update(definition = 'Customer', label = 'Customer_dimension')
app.save()
```

#### delete()
Deletes the dimension from the Qlik Sense Server

Returns:
    True if the dimension was deleted successfully, False otherwise

```
dim = app.dimensions['MyDimension']
dim.delete()
app.save()
```

#### rename()
Renames the dimension on the Qlik Sense Server.

Returns:
    True if the dimension is renamed succesfully, False otherwise

```
dim = app.dimensions['MyDimension']
dim.rename('MyDimensionNewName')
app.save()
```

### Sheet class
The class, representing the sheets of the application. Member of the App.sheets collection.
You can access the objects on the sheets, such as charts and tables, via Sheet class object.

```
for sh in app.sheets:
    print(sh.name)
```

#### sheet properties
* name: that's the name of the measure you generally use in the Qlik Sense interface
* description: the description of the measure
* auxiliary
    - handle: the internal handle of the object in Qlik Sense Engine API; can be used to access the measure via `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the measure
    - parent: AppChildren object; you can access the App class object like this `ms.parent.parent`
    - created_date: creation date of the measure, as stored in Qlik Sense
    - modified_date: date of the last modification of the measure, as stored in Qlik Sense
    - published: True if the list is published, False if not
    - approved: True if the list is approved, False if not
    - owner_id: GUID of the owner of the sheet
    - owner_name: name of the owner of the sheet

#### load()
Loads objects from the sheet in a Qlik Sense application into a Sheet object

```
sh = App.sheets['MySheet']
sh.load()

for obj in sh.objects:
    print(obj.type)
```


### Field class
The class, representing the fields of the application. Member of the App.fields collection.
You can only use the class for information purposes; now changes can be made with fields via QSEA.

```
for fld in app.fields:
    print(field.table_name, field.name)
```

#### field properties
* name: name if the field, as it appears in the model
* table_name: the name of the table, containing field
* information_density, non_nulls, rows_count, subset_ratio, distinct_values_count, present_distinct_values, key_type, tags: properties of the fields as the can be found in the data model
* auxiliary
    - handle
    - app_handle


### Object class 
The class, representing the objects on the sheet, such as charts and tables. Member of the SheetChildren collection

#### object properties
* type: type of the object; 'piechart' or 'pivot-table', for instance
* col, row, colspan, rowspan, bounds_y, bounds_x, bounds_width, bounds_height: parameters referring to the location of an object on the sheet
* auxiliary
    - handle: the internal handle of the object in Qlik Sense Engine API; can be  used to access the object via `query()` function
    - sheet_handle: handle of the parent sheet
    - sheet: the Sheet object, on which the object itself is located
    - id: Qlik Sense internal id of the object
    - parent: SheetChildren object

#### load()
Loads measures and dimensions of the object in a Qlik Sense application into a Object class object

```
sh = App.sheets['MySheet']
sh.load()

for obj in sh.objects:
    if obj.type == 'piechart': 
        obj.load()
        print(obj.dimensions.count)
```

### ObjectChildren class
The class contains collections of measures and dimensions in the object on the sheet:
* object.measures: a collection of ObjectMeasure class objects, representing the measures in the object on the sheet
* object.dimensions: a collection of ObjectDimension class objects, representing the dimensions in the object on the sheet

You can access the main information in pandas dataframe via .df:
```python
App.sheets['MySheet'].objects['object_id'].measures.df
```

Adding measures and dimensions to app objects is not supported yet


### ObjectMeasure class
The class, representing measures of the object on the sheet. Member of the object.measures collection. Since there can be no specific name for the measure in the object, the internal Qlik id is used instead of the name; thus you can either iterate measures, or call them by internal Qlik id:
```python
ms = obj.measures['measure_id']
print(ms.definition)

for ms in obj.measures:
    if ms.definition == 'sum(Sales)': ms.update(definition = 'sum(Incomes)')
```

#### ObjectMeasure properties
* name: internal Qlik id of the measure
* definition: the formula behind the measure
* label: the label of the measure, as it appears in the charts
* label_expression: the label expression of the measure
* calc_condition: calculation condition for the measure
* library_id: in case if master measure used, refers to its id
* format_type: Format type of the object
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec: Number of decimals of the object
* format_use_thou: Use thousands separator of the object
* format_dec: Decimal separator of the object
* format_thou: Thousands separator of the object
* auxiliary
    - app_handle: the handle of the parent App object
    - parent: ObjectChildren object
    - object: you can access the Object class object like this `ms.object`
    
        

#### update()
Updates the measure in the object in the sheet

Args: 
* definition (str, optional): The definition of the measure
* label (str, optional): the label of the measure, as it appears in charts
* label_expression (str, optional): the label expression of the measure
* calc_condition (str, optional): calculation condition for the measure
* library_id (str, optional): if of the master measure
* format_type (str, optional): Format type of the object to be created. Defaults to 'U'.
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_use_thou (int, optional): Use thousands separator of the object to be created. Defaults to 0.
* format_dec (str, optional): Decimal separator of the object to be created. Defaults to ','.
* format_thou (str, optional): Thousands separator of the object to be created. Defaults to ''.

Returns: 
    True if the measure was updated successfully, False otherwise

```
ms = obj.measures['measure_id']
ms.update(definition = 'sum(Sales)', label = 'Total Sales', format_type = 'F')
app.save()
```

#### delete()
Deletes the measure from the object on the sheet

Returns:
    True if the measure was deleted successfully, False otherwise

```
ms = obj.measures['measure_id']
ms.delete()
app.save()
```

### ObhectDimension class
The class, representing dimensions of the object on the sheet. Member of the object.dimensions collection.
Since there can be no specific name for the dimension in the object, the internal Qlik id is used instead of the name; thus you can either iterate dimensions, or call them by internal Qlik id:
```python
dim = obj.measures['dimension_id']
print(dim.definition)

for dim in obj.dimensions:
    if dim.definition == '[Customer]': dim.update(definition = '[Supplier]')
```

Note that hierarchical dimensions are not yet supported.

#### ObjectDimension properties
* name: internal Qlik id of the dimension
* definition: the formula behind the dimension
* label: the label of the dimension, as it appears in the charts
* auxiliary
    - app_handle: the handle of the parent App object
    - parent: ObjectChildren object
    - object: you can access the Object class object like this `dim.object`

#### update()
Updates the dimension in the object in the sheet

Args: 
* definition (str, optional): The definition of the dimension
* label (str, optional): the label of the dimension, as it appears in charts
* calc_condition (str, optional): calculation condition for the dimension

Returns: 
    True if the dimension was updated successfully, False otherwise

```
dim = obj.dimensions['dimension_id']
dim.update(definition = 'Customer', label = 'Customer_dimension')
app.save()
```

#### delete()
Deletes the dimension from the Qlik Sense Server

Returns:
    True if the dimension was deleted successfully, False otherwise

```
dim = app.dimensions['dimension_id']
dim.delete()
app.save()
```