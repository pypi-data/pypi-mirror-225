# Python Library for the EU ASSISTANT Project

## Library Description

This library contains the following sublibraries:
1. [**graphdb**](#graphdb)
2. [**production_system**](#production-system)
3. [**dict_wrapper**](#dict-wrapper)

### GraphDB
Enables using the Rest API for 
[OntoText GraphDB](https://www.ontotext.com/products/graphdb/) 
to Up-/Download files to
and from the selected graph inside a repository. 

With OntoRefine you can upload a file and map the keywords, preprocessing the data for uploading it to a graph.


### Production System

Enables reading ProductionSystem file from GraphDB and turning it into valid json format.


### Dict Wrapper

Allows to read every key-value pair and return list/dict based on custom config.

---
## Change History

**0.3.4**:
- Fix error where list isn't returned when it is not in top level dictionary.

**0.3.3**:
- Bug fixes

**0.3.2**:
- FIX: relative import of *json_wapper*
- Add condition to return correct value if two keys are identical in different subdirectories

**0.3.1**:
- Add method to get identifier from cfg_file based on name for *json_wrapper*

**0.3**:
- Create new sublibrary *json_wrapper*

**0.2**:
- Create new sublibrary *production_system*
- Remove prints from *graphdb*

**0.1.1**:
- Update graphdb download

**0.1**:
- Create library
- Create new sublibrary *graphdb*

---
For more information about the project go to the [ASSISTANT Homepage](https://assistant-project.eu).

