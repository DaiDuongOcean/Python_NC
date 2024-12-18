CATEGORIES = {
    "Personal": "Personal",
    "Work": "Work",
    "Education": "Education",
    "Creative": "Creative",
    "Organization": "Organization",
    "Reference": "Reference",
    "Finance": "Finance",
    "Health": "Health"
}

PRIORITY = {
    "High": "High",
    "Medium": "Medium",
    "Low": "Low"
}

STATUS = {
    "Uncomplete": "Uncomplete",
    "Completed": "Completed"
}

TABLE_COLUMNS = [
    {
        'name': "Id",
        'width': 10
    },
{
        'name': "Name",
        'width': 120
    },
{
        'name': "Description",
        'width': 140
    },
{
        'name': "Category",
        'width': 50
    },
{
        'name': "Date",
        'width': 40
    },
{
        'name': "Time",
        'width': 20
    },
{
        'name': "Priority",
        'width': 30
    },
{
        'name': "Image",
        'width': 100
    },
{
        'name': "Status",
        'width': 50
    },
]

def get_cols():
    return [col for col in TABLE_COLUMNS]

def get_col_index_by_name(col_name):
    if col_name in [col['name'] for col in get_cols()]:
        for index in range(len(TABLE_COLUMNS)):
            if TABLE_COLUMNS[index]['name'] == col_name:
                return index
    return -1

def convert_from_list_to_dict(list_val):
    dict = {}
    cols_name = [col['name'].lower() for col in get_cols()]
    for index in range(len(cols_name)):
        dict[f"{cols_name[index]}"] = list_val[index]
    return dict
