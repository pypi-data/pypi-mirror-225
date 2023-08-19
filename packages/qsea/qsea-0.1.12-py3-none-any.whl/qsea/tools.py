#!/usr/bin/env python
# coding: utf-8

# In[2]:


# beta-версия к публикации

import json
import pandas as pd
import datetime as dt
import logging


# In[5]:


# version 0.1.22-07-11
# just a shortcut to query Qlik Sense Engine Api; 
# json_query - query text; 
# attempts - maximum number of attempts;

def Query(json_query, attempts = 1):
    ws.send(json.dumps(json_query))
    i = 1
    while i <= attempts:
        try: 
            result = ws.recv()
            return json.loads(result)
        except Exception as E:
            ErrorText = str(E)
            logging.error('Unknown Error, attempt %s of %s; %s', i, attempts, ErrorText)
        i += 1
    return 'Query: Unknown Error: ' + ErrorText

# Query({
#         "handle": -1,
#         "method": "GetActiveDoc",
#         "params": [],
#         "outKey": -1,
#         "id": 1
#         })


# In[6]:


# version 0.1.22-07-11
# returns App GUID by its name

def GetAppID(AppName):
    rawAppList = Query({
        "handle": -1,
        "method": "GetDocList",
        "params": [],
        "outKey": -1,
        "id": 1
        })
    
    for app in rawAppList['result']['qDocList']:
        if app['qDocName'] == AppName:
            return app['qDocId']
    
# GetAppID('MyAppName')


# In[7]:


# version 0.1.22-07-11
# opens the app (by name or ID) and returns its handle

def OpenDoc(AppName = '', AppID = ''):
    if AppName == '' and AppID == '':
        logging.error('AppName or AppID not specified')
        return 0
    
    if AppName != '':
        AppID = GetAppID(AppName)

    zu = Query({
    "handle": -1,
    "method": "OpenDoc",
    "params": [AppID],
    "outKey": -1,
    "id": 1
    })

    return zu['result']['qReturn']['qHandle']
    
# AppHandle = OpenDoc('MyAppName')


# In[8]:


# version 0.1.22-07-08
# Returns object properties by its handle; just a shortcut

def GetProperties(handle):
    return Query({
      "jsonrpc": "2.0",
      "id": 4,
      "method": "GetProperties",
      "handle": handle,
      "params": []
    })


# In[9]:


# version 0.1.22-07-08
# Sets object properties by its handle and set query; just a shortcut

def SetProperties(handle, query):
    zu = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "SetProperties",
              "handle": handle,
              "params": [
                query
                ]
            })
    return zu


# In[10]:


# version 0.1.22-07-08
# Returns object layout by its handle; just a shortcut

def GetLayout(handle):
    return Query({
      "jsonrpc": "2.0",
      "id": 4,
      "method": "GetLayout",
      "handle": handle,
      "params": []
    })


# In[11]:


# version 0.1.22-07-08
# returns a handle of any object by its ID

def GetObjectHandle(appHandle, ObjectId):
    return Query({
      "jsonrpc": "2.0",
      "id": 4,
      "method": "GetObject",
      "handle": appHandle,
      "params": [
        ObjectId
      ]
    })['result']['qReturn']['qHandle']


# In[12]:


# version 0.1.22-07-08
# returns dataframe with all apps

def GetAppList():

    zu = Query({
        "handle": -1,
        "method": "GetDocList",
        "params": [],
        "outKey": -1,
        "id": 1
        })
    
    df = pd.json_normalize(zu['result']['qDocList'])
    return df


# In[13]:


# version 0.1.22-07-08
# returns dataframe with app variables

def GetVarPandas(appHandle):
    # get handle of VariableList
    zu = Query({
          "jsonrpc": "2.0",
          "id": 2,
          "method": "CreateSessionObject",
          "handle": appHandle,
          "params": [
            {
              "qInfo": {
                "qId": "VL01",
                "qType": "VariableList"
              },      
              "qVariableListDef": {
                "qType": "variable"
              }
            }
          ]
        }
    )
    listHandle = zu['result']['qReturn']['qHandle']
    return pd.json_normalize(GetLayout(listHandle)['result']['qLayout']['qVariableList']['qItems'])

# zu = GetVarList(1)


# In[14]:


# version 0.1.22-07-08
# returns dataframe with app master measures

def GetMsPandas(appHandle):
    # get handle of MeasureList
    zu = Query({
          "jsonrpc": "2.0",
          "id": 2,
          "method": "CreateSessionObject",
          "handle": appHandle,
          "params": [
            {
              "qInfo": {
                "qId": "ML01",
                "qType": "MeasureList"
              },      
              "qMeasureListDef": {
                "qType": "measure",
                "qData": {
                    "title": "/title",
                    "tags": "/tags",
                    "measure": "/qMeasure"
                    }
              }
            }
          ]
        }
    )
    listHandle = zu['result']['qReturn']['qHandle']
    return pd.json_normalize(GetLayout(listHandle)['result']['qLayout']['qMeasureList']['qItems'])

# zu = GetMsList(1)


# In[15]:


# version 0.1.22-07-08
# returns dataframe with app sheets

def GetSheetPandas(appHandle):
    # get handle of SessionLists
    zu = Query({
      "jsonrpc": "2.0",
      "id": 2,
      "method": "CreateSessionObject",
      "handle": appHandle,
      "params": [
        {
          "qInfo": {
            "qId": "",
            "qType": "SessionLists"
          },
          "qAppObjectListDef": {
            "qType": "sheet",
            "qData": {
              "id": "/qInfo/qId"
            }
          }
        }
      ]
    })
    
    listHandle = zu['result']['qReturn']['qHandle']
    return pd.json_normalize(GetLayout(listHandle)['result']['qLayout']['qAppObjectList']['qItems'])

# zu = GetSheetList(1)


# In[16]:


# version 0.1.22-07-08
# returns dataframe with app fields

def GetFieldPandas(appHandle):
    # GetTablesAndKeys
    zu = Query({
      "jsonrpc": "2.0",
      "id": 1,
      "method": "GetTablesAndKeys",
      "handle": appHandle,
      "params": [
        {
          "qcx": 1000,
          "qcy": 1000
        },
        {
          "qcx": 0,
          "qcy": 0
        },
        30,
        True,
        False
      ]
    })
    
    
    df = pd.json_normalize(zu['result']['qtr'])
    qFields = df['qFields'].explode().apply(pd.Series)
    qFields.rename(columns={col:f'qFields.{col}' for col in qFields.columns}, inplace=True)
    cols = [col for col in df.columns if col not in ['qFields.records']]
    pdf = df[cols].join(qFields)
    
    return pdf

# zu = GetFieldList(1)


# In[17]:


# version 0.1.22-09-13
# returns dataframe with app dimensions

def GetDimPandas(appHandle):
    # get handle of DimensionList
    zu = Query({
          "jsonrpc": "2.0",
          "id": 2,
          "method": "CreateSessionObject",
          "handle": 1,
          "params": [
            {
              "qInfo": {
                "qId": "ML01",
                "qType": "DimensionList"
              },      
              "qDimensionListDef": {
                "qType": "dimension",
                "qData": {
                    "title": "/title",
                    "tags": "/tags",
                    "dimension": "/qDimension"
                    }
              }
            }
          ]
        }
    )

    listHandle = zu['result']['qReturn']['qHandle']
    return pd.json_normalize(GetLayout(listHandle)['result']['qLayout']['qDimensionList']['qItems'])

# zu = GetDimPandas(1)


# In[18]:


# version 0.1.22-08-07
# returns dataframe with objects on the sheet by its handle

def GetSheetObjectsPandas(SheetHandle):
    # раскладка листа
    SheetLayout = GetLayout(SheetHandle)
    odf = pd.json_normalize(GetLayout(SheetHandle)['result']['qLayout']['cells'])
    return odf


# In[19]:


# version 0.1.22-08-07
# returns dataframe with measures used in object by its handle

def GetObjectMeasuresPandas(ObjectHandle):
    gl = Query({
      "jsonrpc": "2.0",
      "id": 4,
      "method": "GetProperties",
      "handle": ObjectHandle,
      "params": []
    })

    odf = pd.json_normalize(gl['result']['qProp']['qHyperCubeDef']['qMeasures'])
    return odf


# In[20]:


# version 0.1.22-08-07
# returns dataframe with dimensions used in object by its handle

def GetObjectDimensionsPandas(ObjectHandle):
    gl = Query({
      "jsonrpc": "2.0",
      "id": 4,
      "method": "GetProperties",
      "handle": ObjectHandle,
      "params": []
    })

    odf = pd.json_normalize(gl['result']['qProp']['qHyperCubeDef']['qDimensions'])
    return odf


# In[21]:


# version 0.1.22-11-10
# the class, representing the application

class App:
    
    def __init__(self, appName):
        self.handle = OpenDoc(appName)
        self.name = appName
        self.variables = AppChildren(self, 'variables')
        self.measures = AppChildren(self, 'measures')
        self.sheets = AppChildren(self, 'sheets')
        self.fields = AppChildren(self, 'fields')
        self.dimensions = AppChildren(self, 'dimensions')
    
    def save(self):
        Query({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "DoSave",
            "handle": self.handle,
            "params": []
        })


# In[22]:


# version 0.1.22-11-10
# the class, representing variables of the application
# member of App.variables collection

class Variable:
    def __init__(self, parent, varName):
        self.name = varName
        self.handle = 0
        self.appHandle = 0
        self.parent = parent

        self.id = ''
        self.definition = ''
        self.description = ''
        self.createdDate = dt.datetime(year=1901, month=1, day=1)
        self.modifiedDate = dt.datetime(year=1901, month=1, day=1)
        self.scriptCreated = ''
        
        
    def getHandle(self):
        self.handle = Query({
          "jsonrpc": "2.0",
          "id": 4,
          "method": "GetVariableById",
          "handle": self.appHandle,
          "params": [self.id]
        })['result']['qReturn']['qHandle']
        return self.handle
    
    def update(self, definition = '', description = ''):
        self.getHandle()

        # changing only nonempty values
        if definition == '': 
            if str(self.definition) == 'nan': definition = '""'
            else: definition = '"' + str(self.definition) + '"'
        else: definition = '"' + definition + '"'
        if description == '':
            if str(self.description) == 'nan': description = '""'
            else: description = '"' + str(self.description) + '"'
        else: description = '"' + description + '"'
        
        zu = Query({
          "jsonrpc": "2.0",
          "id": 2,
          "method": "ApplyPatches",
          "handle": self.handle,
          "params": [
            [
              {
                "qPath": "/qDefinition",
                "qOp": "replace",
                "qValue": definition
              },
              {
                "qPath": "/qComment",
                "qOp": "replace",
                "qValue": description
              }
            ]
          ]
        })
        
        # if success, changes the properties of a variable object
        try:
            if len(zu['change']) > 0:
                self.definition = definition
                self.description = description
        except: 1

        return zu
    
    def delete(self):
        zu = Query({
              "jsonrpc": "2.0",
              "id": 10,
              "method": "DestroyVariableById",
              "handle": self.appHandle,
              "params": [
                self.id
              ]
            })
        
        # delete value from variables collection
        if zu['result']['qSuccess']:
            logging.info('Variable deleted: %s', self.name)
            if self.scriptCreated:
                logging.warning('Deleting the script-generated variable will not affect the state of the app after data reload: %s', self.name)
            del self.parent[self.name]
        else: logging.error('Failed to delete variable: %s', self.name)
        
        return zu
        
    def rename(self, newName):
        #since there is no explicit method to rename a variable in Qlik Sense, just create a new one and delete an old one
        parent = self.parent
        tdef = self.definition
        tdesc = self.description
        if str(tdesc) == 'nan': tdesc = ''
        parent.add(newName, tdef, tdesc)
        self.delete()


# In[23]:


# version 0.1.22-11-10
# the class, representing fields of the application
# member of App.fields collection

class Field:
    def __init__(self, fieldName):
        self.name = fieldName
        self.handle = 0
        self.appHandle = 0
        
        self.tableName = ''
        self.informationDensity, self.nNonNulls, self.nRows, self.subsetRatio = 0, 0, 0, 0
        self.nTotalDistinctValues, self.nPresentDistinctValues = 0, 0
        self.keyType, self.tags = '', ''


# In[24]:


# version 0.1.22-11-10
# the class, representing master measures of the application
# member of App.measures collection

class Measure:
    def __init__(self, parent, msName):
        self.name = msName
        self.handle = 0
        self.appHandle = 0
        self.parent = parent
        
        self.id, self.definition, self.description, self.label, self.labelExpression = '', '', '', '', ''
        self.formatType, self.formatNDec, self.formatUseThou, self.formatDec, self.formatThou = '', -1, -1, '', ''
        self.createdDate, self.modifiedDate = dt.datetime(year=1901, month=1, day=1), dt.datetime(year=1901, month=1, day=1)
        
        
    def getHandle(self):
        self.handle = Query({
          "jsonrpc": "2.0",
          "id": 4,
          "method": "GetMeasure",
          "handle": self.appHandle,
          "params": [self.id]
        })['result']['qReturn']['qHandle']
        return self.handle
    
    def update(self, definition = '', label = '', labelExpression = '', formatType = '',                formatNDec = -1, formatUseThou = -1, formatDec = '', formatThou = ''):
        self.getHandle()

        # check if old values exist; leave old values if new values are empty
        def gn(x, y):
            if type(y) == str:
                if y == '': 
                    if str(x) == 'nan': return ''
                    else: return str(x)
                else: return str(y)
            else:
                if y == -1: 
                    if str(x) == 'nan': return 0
                    else: return int(x)
                else: return int(y)
            
        definition, label, labelExpression, formatType, formatNDec, formatUseThou, formatDec, formatThou =             gn(self.definition, definition),             gn(self.label, label),             gn(self.labelExpression, labelExpression),             gn(self.formatType, formatType),             gn(self.formatNDec, formatNDec),             gn(self.formatUseThou, formatUseThou),             gn(self.formatDec, formatDec),             gn(self.formatThou, formatThou)
        
        t = {
          "jsonrpc": "2.0",
          "id": 2,
          "method": "SetProperties",
          "handle": self.handle,
          "params": [
            {
              "qInfo": {
                "qId": self.id,
                "qType": "measure"
              },
              "qMeasure": {
                  "qLabel": label,
                  "qDef": definition,
                  "qExpressions": [],
                  "qActiveExpression": 0,
                  "qLabelExpression": labelExpression,
                  "qNumFormat": {
                    "qType": formatType,
                    "qnDec": formatNDec,
                    "qUseThou": formatUseThou,
                    "qFmt": "#\xa0##0",
                    "qDec": formatDec,
                    "qThou": formatThou
                  }
                },
                "qMetaDef": {'title': self.name}
            }
          ]
        }
        zu = Query(t)
        
        # прописать, что заменяем только в случае успеха
        try:
            if len(zu['change']) > 0:
                self.definition = definition
                self.label = label
                self.labelExpression = labelExpression
                self.formatType = formatType
                self.formatNDec = formatNDec
                self.formatUseThou = formatUseThou
                self.formatDec = formatDec
                self.formatThou = formatThou
        except: 1
        
        return zu
    
    def delete(self):
        zu = Query({
              "jsonrpc": "2.0",
              "id": 10,
              "method": "DestroyMeasure",
              "handle": self.appHandle,
              "params": [
                self.id
              ]
            })
        
        # delete value from variables collection
        if zu['result']['qSuccess']:
            logging.info ('Measure deleted: %s', self.name)
            del self.parent[self.name]
        else: logging.error('Failed to delete measure: %s', self.name)
        
        return zu
    
    
    def rename(self, name):
        self.getHandle()

        t = {
          "jsonrpc": "2.0",
          "id": 2,
          "method": "SetProperties",
          "handle": self.handle,
          "params": [
            {
              "qInfo": {
                "qId": self.id,
                "qType": "measure"
              },
                "qMetaDef": {'title': name}
            }
          ]
        }
        zu = Query(t)
        
        # прописать, что заменяем только в случае успеха
        self.name = name
        
        return zu


# In[25]:


# version 0.1.22-11-10
# the class, representing master dimensions of the application
# member of App.dimensions collection

class Dimension:
    def __init__(self, parent, dimName):
        self.name = dimName
        self.handle = 0
        self.appHandle = 0
        self.parent = parent
        
        self.id, self.definition = '', ''
        self.createdDate, self.modifiedDate = dt.datetime(year=1901, month=1, day=1), dt.datetime(year=1901, month=1, day=1)
        
        
    def getHandle(self):
        self.handle = Query({
          "jsonrpc": "2.0",
          "id": 4,
          "method": "GetDimension",
          "handle": self.appHandle,
          "params": [self.id]
        })['result']['qReturn']['qHandle']
        return self.handle
    
#     def update(self, definition = '', label = '', labelExpression = '', formatType = '', \
#                formatNDec = '', formatUseThou = '', formatDec = '', formatThou = ''):
#         self.getHandle()

#         # проверяем, есть ли старые значения; если новых значений нет, то оставляем старые
#         def gn(x, y):
#             if y == '': 
#                 if str(x) == 'nan': return ''
#                 else: return str(x)
#             else: return str(y)
            
#         # аналогично для числовых полей
#         def fn(x, y):
#             if y == -1: 
#                 if str(x) == 'nan': return 0
#                 else: return x
#             else: return y

#         definition, label, labelExpression, formatType, formatNDec, formatUseThou, formatDec, formatThou = \
#             gn(self.definition, definition), \
#             gn(self.label, label), \
#             gn(self.labelExpression, labelExpression), \
#             gn(self.formatType, formatType), \
#             fn(self.formatNDec, formatNDec), \
#             fn(self.formatUseThou, formatUseThou), \
#             gn(self.formatDec, formatDec), \
#             gn(self.formatThou, formatThou)

#         #print(definition, '\n', label, '\n', labelExpression, '\n', formatType, '\n' \
# #             , formatNDec, '\n', formatUseThou, '\n', formatDec, '\n', formatThou)

#         t = {
#           "jsonrpc": "2.0",
#           "id": 2,
#           "method": "SetProperties",
#           "handle": self.handle,
#           "params": [
#             {
#               "qInfo": {
#                 "qId": self.id,
#                 "qType": "measure"
#               },
#               "qMeasure": {
#                   "qLabel": label,
#                   "qDef": definition,
#                   "qExpressions": [],
#                   "qActiveExpression": 0,
#                   "qLabelExpression": labelExpression,
#                   "qNumFormat": {
#                     "qType": formatType,
#                     "qnDec": formatNDec,
#                     "qUseThou": formatUseThou,
#                     "qFmt": "#\xa0##0",
#                     "qDec": formatDec,
#                     "qThou": formatThou
#                   }
#                 },
#                 "qMetaDef": {'title': self.name}
#             }
#           ]
#         }
#         zu = Query(t)
        
#         # прописать, что заменяем только в случае успеха
#         self.definition = definition
#         self.label = label
#         self.labelExpression = labelExpression
#         self.formatType = formatType
#         self.formatNDec = formatNDec
#         self.formatUseThou = formatUseThou
#         self.formatDec = formatDec
#         self.formatThou = formatThou
        
#         return zu
    
    def delete(self):
        zu = Query({
              "jsonrpc": "2.0",
              "id": 10,
              "method": "DestroyDimension",
              "handle": self.appHandle,
              "params": [
                self.id
              ]
            })
        
#         # delete value from variables collection
#         if zu['result']['qSuccess']:
#             print ('Measure deleted: ', self.name)
#             del self.parent[self.name]
#         else: print ('Failed to delete measure: ', self.name)
        
#         return zu
    
    
#     def rename(self, name):
#         self.getHandle()

#         t = {
#           "jsonrpc": "2.0",
#           "id": 2,
#           "method": "SetProperties",
#           "handle": self.handle,
#           "params": [
#             {
#               "qInfo": {
#                 "qId": self.id,
#                 "qType": "measure"
#               },
#                 "qMetaDef": {'title': name}
#             }
#           ]
#         }
#         zu = Query(t)
        
#         # прописать, что заменяем только в случае успеха
#         self.name = name
        
#         return zu


# In[26]:


# version 0.1.22-11-10

class ChildrenIterator:
    def __init__(self, children):
        self.children = children.children
        self._keys = list(children.children.keys())
        self._index = 0
        self._class_size = len(children.children)
        
    def __next__(self):
        if self._index < self._class_size:
            result = self.children[self._keys[self._index]]
            self._index +=1
            return result
        raise StopIteration


# In[27]:


# version 0.1.22-11-10
# the class, representing different collections of app objects, like master measures or dimensions

class AppChildren():
    def __init__(self, parent, _type):
        self.children = {}
        self.count = 0
        self.parent = parent
        self.appHandle = parent.handle
        self._type = _type
        
    def __getitem__(self, childName):
        if self._type == 'variables':
            if self.count == 0:
                self.df = GetVarPandas(self.appHandle)
                for varName in self.df['qName']:
                    var = Variable(self, varName)
                    var.appHandle = self.appHandle
                    
                    row = self.df[self.df['qName'] == varName].iloc[0]
                    var.id = row['qInfo.qId']
                    var.definition = row['qDefinition']
                    var.description = row['qDescription']
                    var.scriptCreated = row['qIsScriptCreated']
                    if str(var.scriptCreated) == 'nan': var.scriptCreated = False

                    self[varName] = var
                    self.count += 1
        
        if self._type == 'measures':
            if self.count == 0:
                self.df = GetMsPandas(self.appHandle)
                for msName in self.df['qMeta.title']:
                    ms = Measure(self, msName)
                    ms.appHandle = self.appHandle

                    row = self.df[self.df['qMeta.title'] == msName].iloc[0]
                    ms.id = row['qInfo.qId']
                    ms.definition = row['qData.measure.qDef']
                    ms.label = row['qData.measure.qLabel']
                    ms.labelExpression = row['qData.measure.qLabelExpression']
                    ms.format = row['qData.measure.qNumFormat.qFmt']
                    ms.formatType = row['qData.measure.qNumFormat.qType']
                    ms.formatNDec = row['qData.measure.qNumFormat.qnDec']
                    ms.formatUseThou = row['qData.measure.qNumFormat.qUseThou']
                    ms.formatDec = row['qData.measure.qNumFormat.qDec']
                    ms.formatThou = row['qData.measure.qNumFormat.qThou']
                    ms.createdDate = dt.datetime.strptime(row['qMeta.createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    ms.modifiedDate = dt.datetime.strptime(row['qMeta.modifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

                    self[msName] = ms
                    self.count += 1
                        
        if self._type == 'sheets':
            if self.count == 0:
                self.df = GetSheetPandas(self.appHandle)
                for shName in self.df['qMeta.title']:
                    sh = Sheet(self, shName)
                    sh.appHandle = self.appHandle
                    
                    row = self.df[self.df['qMeta.title'] == shName].iloc[0]
                    sh.id = row['qInfo.qId']
                    sh.description = row['qMeta.description']
                    sh.createdDate = dt.datetime.strptime(row['qMeta.createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    sh.modifiedDate = dt.datetime.strptime(row['qMeta.modifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    sh.published = row['qMeta.published']
                    sh.approved = row['qMeta.approved']
                    sh.ownerId = row['qMeta.owner.id']
                    sh.ownerName = row['qMeta.owner.name']

                    self[shName] = sh
                    self.count += 1
                    
        if self._type == 'fields':
            if self.count == 0:
                self.df = GetFieldPandas(self.appHandle)
                for fName in self.df['qFields.qName']:
                    f = Field(fName)
                    f.appHandle = self.appHandle
                    
                    row = self.df[self.df['qFields.qName'] == fName].iloc[0]
                    f.tableName = row['qName']
                    f.informationDensity = row['qFields.qInformationDensity']
                    f.nNonNulls = row['qFields.qnNonNulls']
                    f.nRows = row['qFields.qnRows']
                    f.subsetRatio = row['qFields.qSubsetRatio']
                    f.nTotalDistinctValues = row['qFields.qnTotalDistinctValues']
                    f.nPresentDistinctValues = row['qFields.qnPresentDistinctValues']
                    f.keyType = row['qFields.qKeyType']
                    f.tags = row['qFields.qTags']

                    self[fName] = f
                    self.count += 1
                    
        if self._type == 'dimensions':
            if self.count == 0:
                self.df = GetDimPandas(self.appHandle)
                for dimName in self.df['qMeta.title']:
                    dim = Dimension(self, dimName)
                    dim.appHandle = self.appHandle

                    row = self.df[self.df['qMeta.title'] == dimName].iloc[0]
                    dim.id = row['qInfo.qId']
                    #dim.definition = row['qData.measure.qDef']   добавить
                    dim.createdDate = dt.datetime.strptime(row['qMeta.createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    dim.modifiedDate = dt.datetime.strptime(row['qMeta.modifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

                    self[dimName] = dim
                    self.count += 1
                    
        
        return self.children[childName]
    
    def __setitem__(self, childName, var):
          self.children[childName] = var
            
    def __delitem__(cls, childName):
        del cls.children[childName]
        cls.count -= 1
            
    def __iter__(self):
        # initializing collection if empty
        if self.count == 0:
            try: zvb = self['']
            except: 1
        return ChildrenIterator(self)
    
    def load(self):
        try: zu = self['']
        except: 1
    
    def add(self, name, definition, description = '', label = '', labelExpression = '', formatType = 'U',                formatNDec = 10, formatUseThou = 0, formatDec = ',', formatThou = ''):
        if self._type == 'variables':
            zu = Query({
                "jsonrpc": "2.0",
                "id": 4,
                "method": "CreateVariableEx",
                "handle": self.appHandle,
                "params": [
                    {
                        "qInfo": {
                            "qType": "variable"
                        },
                    "qName": name,
                    "qComment": description,
                    "qDefinition": definition
                    }
                ]
            })
            
            try:
                if zu['error']['parameter'] == 'Variable already exists':
                    logging.error('Variable already exists: %s', name)
                    return zu
            except: 1
            
            var = Variable(self, name)
            var.appHandle = self.appHandle

            # renew variables data from app
            # переписать тут, не запрашивать весь список, а запросить только данные по конкретной переменной
            self.df = GetVarPandas(self.appHandle)
            row = self.df[self.df['qName'] == name].iloc[0]
            var.id = row['qInfo.qId']
            var.definition = row['qDefinition']
            var.description = row['qDescription']
            var.scriptCreated = row['qIsScriptCreated']
            if str(var.scriptCreated) == 'nan': var.scriptCreated = False

            self[name] = var
            self.count += 1
            logging.info('Variable created: %s', name)
            return zu
        
        if self._type == 'measures':
            t = {
                "handle": self.appHandle,
                "method": "CreateMeasure",
                "params": {
                    "qProp": {
                        "qInfo": {
                            "qType": "measure"
                        },
                        "qMeasure": {
                            "qLabel": label,
                            "isCustomFormatted": True,
                            "numFormatFromTemplate": False,
                            "qNumFormat": {
                                                "qType": formatType,
                                                "qnDec": formatNDec,
                                                'qUseThou': formatUseThou,
                                                "qDec": formatDec,
                                                'qThou': formatThou
                                                      },
                            "qLabelExpression": labelExpression,
                            "qDef": definition,
                            "qGrouping": 0,
                            "qExpressions": [
                                ""
                            ],
                            "qActiveExpression": 0
                        },
                        "qMetaDef": {
                            "title": name,
                            "description": description
                                            }
                    }
                }
            }
            logging.debug(t)
            zu = Query(t)
            
            try:
                if zu['result']['qReturn']['qHandle'] > 0:
                    ms = Measure(self, name)
                    ms.appHandle = self.appHandle

                    # renew measures data from app
                    # to refine: query date for exact variable instead of the whole list
                    row = self.df[self.df['qMeta.title'] == msName].iloc[0]
                    ms.id = row['qInfo.qId']
                    ms.definition = row['qData.measure.qDef']
                    ms.label = row['qData.measure.qLabel']
                    ms.labelExpression = row['qData.measure.qLabelExpression']
                    ms.format = row['qData.measure.qNumFormat.qFmt']
                    ms.formatType = row['qData.measure.qNumFormat.qType']
                    ms.formatNDec = row['qData.measure.qNumFormat.qnDec']
                    ms.formatUseThou = row['qData.measure.qNumFormat.qUseThou']
                    ms.formatDec = row['qData.measure.qNumFormat.qDec']
                    ms.formatThou = row['qData.measure.qNumFormat.qThou']
                    ms.createdDate = dt.datetime.strptime(row['qMeta.createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    ms.modifiedDate = dt.datetime.strptime(row['qMeta.modifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

                    self[msName] = ms
                    self.count += 1
                    logging.info('Measure created: %s', name)
                else: logging.error('Failed to create measure: %s', name)
            except: logging.error('Failed to create measure: %s', name)
            return zu


# In[28]:


# version 0.1.22-11-10
# the class, representing sheets of the application
# member of App.sheets collection

class Sheet:
    def __init__(self, parent, sheetName):
        self.name = sheetName
        self.handle = 0
        self.parent = parent
        self.appHandle = parent.appHandle
        
        self.id = ''
        self.description = ''
        self.createdDate = dt.datetime(year=1901, month=1, day=1)
        self.modifiedDate = dt.datetime(year=1901, month=1, day=1)
        self.published = ''
        self.approved = ''
        self.ownerId = ''
        self.ownerName = ''
        
        self.objects = SheetChildren(self)
        
    def getHandle(self):
        self.handle = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "GetObject",
              "handle": self.appHandle,
              "params": [
                self.id
              ]
            })['result']['qReturn']['qHandle']
        return self.handle
        
        


# In[29]:


# version 0.1.22-11-10
# the class, representing collection of objects on the sheet

class SheetChildren():
    def __init__(self, parent):
        self.children = {}
        self.count = 0
        self.sheetHandle = 0
        self.appHandle = parent.appHandle
        self.parent = parent
        self.parentId = parent.id
        
        
    def __getitem__(self, childName):
        if self.count == 0:
            self.sheetHandle = self.parent.getHandle()
            self.df = GetSheetObjectsPandas(self.sheetHandle)
            for objName in self.df['name']:
                obj = Object(self, objName)
                obj.sheetHandle = self.sheetHandle

                row = self.df[self.df['name'] == objName].iloc[0]
                obj.id = objName
                obj.type = row['type']
                obj.col = row['col']
                obj.row = row['row']
                obj.colspan = row['colspan']
                obj.rowspan = row['rowspan']
                obj.boundsY = row['bounds.y']
                obj.boundsX = row['bounds.x']
                obj.boundsWidth = row['bounds.width']
                obj.boundsHeight = row['bounds.height']

                self[objName] = obj
                self.count += 1
        
        return self.children[childName]
    
    def __setitem__(self, childName, var):
          self.children[childName] = var
            
    def __delitem__(cls, childName):
        del cls.children[childName]
        cls.count -= 1
            
    def __iter__(self):
        # initializing collection if empty
        if self.count == 0:
            try: zvb = self['']
            except: 1
        return ChildrenIterator(self)
    
    def load(self):
        try: zu = self['']
        except: 1
    


# In[30]:


# version 0.1.22-11-10
# the class, representing objects on the sheet, member of SheetChildren collection

class Object:
    def __init__(self, parent, objName):
        self.name = objName
        self.handle = 0
        self.parent = parent
        self.appHandle = parent.appHandle
        self.sheetHandle = parent.sheetHandle
        
        
        self.type = ''
        self.col, self.row, self.colspan, self.rowspan, self.boundsY,                 self.boundsX, self.boundsWidth, self.boundsHeight = 0, 0, 0, 0, 0, 0, 0, 0
        
        self.dimensions = ObjectChildren(self, 'objectDimensions')
        self.measures = ObjectChildren(self, 'objectMeasures')
        
    def getHandle(self):
        logging.debug('self.id: %s, self.appHandle: %s', self.id, self.appHandle)
        self.handle = Query({
          "jsonrpc": "2.0",
          "id": 4,
          "method": "GetObject",
          "handle": self.appHandle,
          "params": [self.id]
        })['result']['qReturn']['qHandle']
        return self.handle
    


# In[31]:


# version 0.1.22-11-10
# the class, representing dimensions, used in object on the sheet

class ObjectDimension():
    def __init__(self, parent, dimName):
        self.name = dimName
        self.appHandle = 0
        self.parent = parent
        self.object = parent.parent
        self.index = -1
        
        logger.debug(type(self.object))
        
        self.id, self.libraryId, self.definition, self.label, self.calcCondition = '', '', '', '', ''
        
    def update(self, definition = '', label = '', labelExpression = '', calcCondition = ''):
        self.object.getHandle()

        # check if new values exists; if not, leave old values without change
        def gn(x, y):
            if y == '': 
                if str(x) == 'nan': return ''
                else: return str(x)
            else: return str(y)
            
        # check if new values exists; if not, leave old values without change
        def fn(x, y):
            if y == -1: 
                if str(x) == 'nan': return 0
                else: return x
            else: return y

        definition, label, labelExpression, calcCondition =             gn(self.definition, definition),             gn(self.label, label),             gn(self.labelExpression, labelExpression),             gn(self.calcCondition, calcCondition)

        # receiving properties of parent object
        t = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "GetProperties",
              "handle": self.object.handle,
              "params": []
            })['result']['qProp']
               
        # changing properties json
        t['qHyperCubeDef']['qDimensions'][self.index]['qDef']['qFieldDefs'] = definition
        t['qHyperCubeDef']['qDimensions'][self.index]['qDef']['qFieldLabels'] = label
        t['qHyperCubeDef']['qDimensions'][self.index]['qDef']['qLabelExpression'] = labelExpression
        t['qHyperCubeDef']['qDimensions'][self.index]['qCalcCondition']['qCond']['qv'] = calcCondition
               
        # setting new properties
        zu = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "SetProperties",
              "handle": 4,
              "params": [
                t
                ]
            })
        
        # to refine: change dataframe only in case of success
        self.definition = definition
        self.label = label
        self.labelExpression = labelExpression
        self.calcCondition = calcCondition
        
        return zu
    
    def delete(self):
        self.object.getHandle()

        # receiving properties of parent object
        t = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "GetProperties",
              "handle": self.object.handle,
              "params": []
            })['result']['qProp']
               
        # deleting item properties json
        t['qHyperCubeDef']['qDimensions'].pop(self.index)
        t['qHyperCubeDef']['qInterColumnSortOrder'].remove(max(t['qHyperCubeDef']['qInterColumnSortOrder']))
        t['qHyperCubeDef']['qColumnOrder'].remove(max(t['qHyperCubeDef']['qColumnOrder']))
        t['qHyperCubeDef']['columnOrder'].remove(max(t['qHyperCubeDef']['columnOrder']))
        t['qHyperCubeDef']['columnWidths'].pop(self.index)   # здесь  неправильно - не ясно какую колонку на самом деле мы удаляем
        
        # setting new properties
        zu = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "SetProperties",
              "handle": self.object.handle,
              "params": [
                t
                ]
            })
        
        # delete value from variables collection
        
        if 'change' in zu:
            logger.info('Dimension deleted: %s', self.name)
            del self.parent[self.name]
        else: logger.error('Failed to delete dimension: %s', self.name)
        
        return zu


# In[32]:


# version 0.1.22-11-10
# the class, representing measures, used in object on the sheet

class ObjectMeasure():
    def __init__(self, parent, msName):
        self.name = msName
        self.appHandle = 0
        self.parent = parent
        self.object = parent.parent
        self.index = -1
        
        self.id, self.libraryId, self.definition, self.label, self.labelExpression, self.calcCondition = '', '', '', '', '', ''
        self.formatType, self.formatNDec, self.formatUseThou, self.formatDec, self.formatThou = '', -1, -1, '', ''
        
    def update(self, definition = '', label = '', labelExpression = '', calcCondition = '', libraryId = '',              formatType = '', formatNDec = -1, formatUseThou = -1, formatDec = '', formatThou = ''):
        self.object.getHandle()

        # check if new values exists; if not, leave old values without change
        def gn(x, y):
            if y == '': 
                if str(x) == 'nan': return ''
                else: return str(x)
            else: return str(y)
            
        # check if new values exists; if not, leave old values without change
        def fn(x, y):
            if y == -1: 
                if str(x) == 'nan': return 0
                else: return x
            else: return y

        definition, label, labelExpression, calcCondition, libraryId,                     formatType, formatNDec, formatUseThou, formatDec, formatThou =             gn(self.definition, definition),             gn(self.label, label),             gn(self.labelExpression, labelExpression),             gn(self.calcCondition, calcCondition),             gn(self.libraryId, libraryId),             gn(self.formatType, formatType),             fn(self.formatNDec, formatNDec),             fn(self.formatUseThou, formatUseThou),             gn(self.formatDec, formatDec),             gn(self.formatThou, formatThou)

        # receiving properties of parent object
        t = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "GetProperties",
              "handle": self.object.handle,
              "params": []
            })['result']['qProp']
               
        # changing properties json
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qDef'] = definition
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qLabel'] = label
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qLabelExpression'] = labelExpression
        t['qHyperCubeDef']['qMeasures'][self.index]['qCalcCondition']['qCond']['qv'] = calcCondition
        t['qHyperCubeDef']['qMeasures'][self.index]['qLibraryId'] = libraryId
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qNumFormat']['qType'] = formatType
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qNumFormat']['qnDec'] = formatNDec
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qNumFormat']['qUseThou'] = formatUseThou
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qNumFormat']['qDec'] = formatDec
        t['qHyperCubeDef']['qMeasures'][self.index]['qDef']['qNumFormat']['qThou'] = formatThou
        
        
               
        # setting new properties
        zu = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "SetProperties",
              "handle": self.object.handle,
              "params": [
                t
                ]
            })
        
        # to refine: change dataframe only in case of success
        self.definition = definition
        self.label = label
        self.labelExpression = labelExpression
        self.calcCondition = calcCondition
        self.libraryId = libraryId
        self.formatType = formatType
        self.formatNDec = formatNDec
        self.formatUseThou = formatUseThou
        self.formatDec = formatDec
        self.formatThou = formatThou
        
        return zu
    
    
    def delete(self):
        self.object.getHandle()

        # receiving properties of parent object
        t = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "GetProperties",
              "handle": self.object.handle,
              "params": []
            })['result']['qProp']
               
        # deleting item properties json
        t['qHyperCubeDef']['qMeasures'].pop(self.index)
        t['qHyperCubeDef']['qInterColumnSortOrder'].remove(max(t['qHyperCubeDef']['qInterColumnSortOrder']))
        t['qHyperCubeDef']['qColumnOrder'].remove(max(t['qHyperCubeDef']['qColumnOrder']))
        t['qHyperCubeDef']['columnOrder'].remove(max(t['qHyperCubeDef']['columnOrder']))
        t['qHyperCubeDef']['columnWidths'].pop(self.index)   # здесь  неправильно - не ясно какую колонку на самом деле мы удаляем
        
        # setting new properties
        zu = Query({
              "jsonrpc": "2.0",
              "id": 4,
              "method": "SetProperties",
              "handle": self.object.handle,
              "params": [
                t
                ]
            })
        
        # delete value from variables collection
        
        if 'change' in zu:
            logger.info('Measure deleted: %s', self.name)
            del self.parent[self.name]
        else: logger.error('Failed to delete measure: %s', self.name)
        
        return zu


# In[33]:


# version 0.1.22-11-10
# the class, representing different collections of sheet objects, like measures or dimensions

class ObjectChildren():
    def __init__(self, parent, _type):
        self.children = {}
        self.count = 0
        self.parent = parent
        self.appHandle = parent.appHandle
        self._type = _type
        
    
    def __getitem__(self, childCaller):
        def clear(row, colName, _type = str):
            if colName in row.index:
                return row[colName]
            else: 
                if _type == str: return ''
                else: return 0

        
        if self._type == 'objectDimensions':
            if self.count == 0:
                logger.debug('self.parent.name: %s', self.parent.name)
                self.parentHandle = self.parent.getHandle()
                logger.debug('parentHandle: %s', self.parentHandle)
                self.df = GetObjectDimensionsPandas(self.parentHandle)
                for dimId in self.df['qDef.cId']:
                    dim = ObjectDimension(self, dimId)
                    dim.appHandle = self.appHandle
                    dim.index = self.count
                    
                    row = self.df[self.df['qDef.cId'] == dimId].iloc[0]
                    dim.id = dimId
                    dim.libraryId = clear(row, 'qLibraryId')
                    dim.definition = clear(row, 'qDef.qFieldDefs')
                    dim.label = clear(row, 'qDef.qFieldLabels')
                    dim.labelExpression = clear(row, 'qDef.qLabelExpression')
                    dim.calcCondition = clear(row, 'qCalcCondition.qCond.qv')

                    self[dimId] = dim
                    self.count += 1


        if self._type == 'objectMeasures':
            def clear(row, colName, _type = str):
                if colName in row.index:
                    return row[colName]
                else: 
                    if _type == str: return ''
                    else: return 0

            if self.count == 0:
                logger.debug('self.parent.name: %s', self.parent.name)
                self.parentHandle = self.parent.getHandle()
                logger.debug('parentHandle: %s', self.parentHandle)
                self.df = GetObjectMeasuresPandas(self.parentHandle)
                for msId in self.df['qDef.cId']:
                    ms = ObjectMeasure(self, msId)
                    ms.appHandle = self.appHandle
                    ms.index = self.count

                    row = self.df[self.df['qDef.cId'] == msId].iloc[0]
                    ms.id = msId
                    ms.libraryId = clear(row, 'qLibraryId')
                    ms.definition = clear(row, 'qDef.qDef')
                    ms.label = clear(row, 'qDef.qLabel')
                    ms.labelExpression = clear(row, 'qDef.qLabelExpression')
                    ms.calcCondition = clear(row, 'qCalcCondition.qCond.qv')
                    ms.formatType = clear(row, 'qDef.qNumFormat.qType')
                    ms.formatNDec = clear(row, 'qDef.qNumFormat.qnDec', int)
                    ms.formatUseThou = clear(row, 'qDef.qNumFormat.qUseThou', int)
                    ms.formatDec = clear(row, 'qDef.qNumFormat.qDec')
                    ms.formatThou = clear(row, 'qDef.qNumFormat.qThou')

                    self[msId] = ms
                    self.count += 1
                        
        if type(childCaller) == str:
            return self.children[childCaller]
        else:
            for ch in self.children.keys():
                logger.debug(self.children[ch].index)
                if self.children[ch].index == childCaller: return self.children[ch]
    
    def __setitem__(self, childCaller, var):
          self.children[childCaller] = var
            
    def __delitem__(cls, childCaller):
        del cls.children[childCaller]
        cls.count -= 1
            
    def __iter__(self):
        # initializing collection if empty
        if self.count == 0:
            try: zvb = self['']
            except: 1
        return ChildrenIterator(self)
    
    def load(self):
        try: zu = self['']
        except: 1
            
    def add(self, definition = '', label = '', labelExpression = '', libraryId = '',              formatType = '', formatNDec = -1, formatUseThou = -1, formatDec = '', formatThou = ''):
        
        self.parent.getHandle()
        if self._type == 'objectDimensions':
            
            # warnings
            if labelExpression != '': logger.warning("labelExpression can't be used with dimensions, field will be ignored")
            if formatType != '': logger.warning("formatType can't be used with dimensions, field will be ignored")
            if formatNDec != -1: logger.warning("formatNDec can't be used with dimensions, field will be ignored")
            if formatUseThou != -1: logger.warning("formatUseThou can't be used with dimensions, field will be ignored")
            if formatDec != '': logger.warning("formatDec can't be used with dimensions, field will be ignored")
            if formatThou != '': logger.warning("formatThou can't be used with dimensions, field will be ignored")

            # receiving properties of parent object
            t = Query({
                  "jsonrpc": "2.0",
                  "id": 4,
                  "method": "GetProperties",
                  "handle": self.parent.handle,
                  "params": []
                })['result']['qProp']
            
            # changing properties json
            # length of dimensions list
            
            if libraryId == '':
                t['qHyperCubeDef']['qDimensions'].append({'qDef': 
                                                      {'qGrouping': 'N', 
                                                       'qFieldDefs': [definition], 
                                                       'qFieldLabels': [label], 
                                                       #'qLabelExpression': [labelExpression],
                                                       'qSortCriterias': [{'qSortByNumeric': 1
                                                                           , 'qSortByAscii': 1
                                                                           , 'qSortByLoadOrder': 1
                                                                           , 'qExpression': {}}], 
                                                       'qNumberPresentations': [], 
                                                       'qActiveField': 0, 
                                                       'autoSort': True, 
                                                       #'cId': 'NbjUkqwer', 
                                                       'othersLabel': 'Другие', 
                                                       'textAlign': {'auto': True, 'align': 'left'}, 
                                                       'representation': {'type': 'text', 
                                                                          'urlPosition': 'dimension', 
                                                                          'urlLabel': '', 'linkUrl': ''}}, 
                                                      'qOtherTotalSpec': {'qOtherMode': 'OTHER_OFF', 
                                                                          'qOtherCounted': {'qv': '10'}, 
                                                                          'qOtherLimit': {'qv': '0'}, 
                                                                          'qOtherLimitMode': 'OTHER_GE_LIMIT', 
                                                                          'qForceBadValueKeeping': True, 
                                                                          'qApplyEvenWhenPossiblyWrongResult': True, 
                                                                          'qOtherSortMode': 'OTHER_SORT_DESCENDING', 
                                                                          'qTotalMode': 'TOTAL_OFF', 
                                                                          'qReferencedExpression': {}}, 
                                                      'qOtherLabel': {'qv': 'Другие'}, 
                                                      'qTotalLabel': {}, 
                                                      'qCalcCond': {}, 
                                                      'qAttributeExpressions': [], 
                                                      'qAttributeDimensions': [], 
                                                      'qCalcCondition': {'qCond': {}, 'qMsg': {}}})
                
            if libraryId != '':
                t['qHyperCubeDef']['qDimensions'].append({'qLibraryId': libraryId,
                                                     'qDef': {'qGrouping': 'N',
                                                      'qFieldDefs': [],
                                                      'qFieldLabels': [],
                                                      'qSortCriterias': [{'qSortByNumeric': 1,
                                                        'qSortByAscii': 1,
                                                        'qSortByLoadOrder': 1,
                                                        'qExpression': {}}],
                                                      'qNumberPresentations': [],
                                                      'qActiveField': 0,
                                                      'autoSort': True,
                                                      #'cId': 'VwGrKh',
                                                      'othersLabel': 'Другие',
                                                      'textAlign': {'auto': True, 'align': 'left'},
                                                      'representation': {'type': 'text',
                                                       'urlPosition': 'dimension',
                                                       'urlLabel': '',
                                                       'linkUrl': ''}},
                                                     'qOtherTotalSpec': {'qOtherMode': 'OTHER_OFF',
                                                      'qOtherCounted': {'qv': '10'},
                                                      'qOtherLimit': {'qv': '0'},
                                                      'qOtherLimitMode': 'OTHER_GE_LIMIT',
                                                      'qForceBadValueKeeping': True,
                                                      'qApplyEvenWhenPossiblyWrongResult': True,
                                                      'qOtherSortMode': 'OTHER_SORT_DESCENDING',
                                                      'qTotalMode': 'TOTAL_OFF',
                                                      'qReferencedExpression': {}},
                                                     'qOtherLabel': {'qv': 'Другие'},
                                                     'qTotalLabel': {},
                                                     'qCalcCond': {},
                                                     'qAttributeExpressions': [],
                                                     'qAttributeDimensions': [],
                                                     'qCalcCondition': {'qCond': {}, 'qMsg': {}}
                                                         })

            t['qHyperCubeDef']['qInterColumnSortOrder'].append(max(t['qHyperCubeDef']['qInterColumnSortOrder']) + 1)
            t['qHyperCubeDef']['qColumnOrder'].append(max(t['qHyperCubeDef']['qColumnOrder']) + 1)
            t['qHyperCubeDef']['columnOrder'].append(max(t['qHyperCubeDef']['columnOrder']) + 1)
            t['qHyperCubeDef']['columnWidths'].append(-1)   # здесь  неправильно - не ясно какую колонку на самом деле мы удаляем

            logger.debug(t)
            
            # setting new properties
            zu = Query({
                  "jsonrpc": "2.0",
                  "id": 4,
                  "method": "SetProperties",
                  "handle": self.parent.handle,
                  "params": [
                    t
                    ]
                })

            # to refine: change dataframe only in case of success
            self.definition = definition
            self.label = label
            self.labelExpression = labelExpression
            #self.calcCondition = calcCondition

            return [t, zu]
            
    


# In[ ]:




