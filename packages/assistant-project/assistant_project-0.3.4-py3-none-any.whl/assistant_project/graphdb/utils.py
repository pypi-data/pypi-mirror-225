def get_options_from_type(format_type):
    """
    Get Options for OntoRefine upload based on format_type. format_type has to be supported by GraphDB
    (Currently only 'text/json' and 'text/line-based/*sv' implemented)
    """
    if format_type == 'text/json':
        options = {
            'recordPath': ["_"],
            'limit': -1,
            'trimStrings': False,
            'guessCellValueTypes': False,
            'storeEmptyStrings': False,
            'includeFileSources': False
        }
    elif format_type == 'text/line-based/*sv':
        options = {
            'separator': "\\t",
            'encoding': 'UTF-8',
            'ignoreLines': -1,
            'headerLines': 1,
            'skipDataLines': 0,
            'limit': -1,
            'storeBlankRows': False,
            'storeBlankCellsAsNulls': True,
            'trimStrings': True,
            'quoteCharacter': '"'
        }
    else:
        print("This format is not yet implemented or not supported")
        return None
    return options
