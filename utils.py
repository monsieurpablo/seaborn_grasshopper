import io
import pandas as pd


def clean_dict_datatype(a_dict: dict) -> dict:
    """Hops only accepts one datatype per input.
    We force the str datatype at input (convert if necessary),
    then convert back to either integer, float, bool or string"""

    for key_index in a_dict.keys():
        for elem in range(len(a_dict[key_index])):
            current_elem = a_dict[key_index][elem]

            if str(current_elem).isdigit():
                a_dict[key_index][elem] = int(current_elem)
            elif current_elem.replace('.', '', 1).isdigit() and current_elem.count('.') < 2:
                a_dict[key_index][elem] = float(current_elem)
            elif current_elem == "True":    # Implicit conversion sometimes fails...
                a_dict[key_index][elem] = True
            elif current_elem == "False":
                a_dict[key_index][elem] = False
            else:
                a_dict[key_index][elem] = str(current_elem)
    return a_dict


def temp_rename_dict(a_dict: dict) -> dict:
    """remove the {} of the paths (that are the keys of the dictionary)"""
    new_dict = {}
    for key in a_dict.keys():
        new_dict[str(key)[1:-1]] = a_dict[key]
    return new_dict


def list_key_path(a_dict) -> list:
    """create a list of all the elements that make a key, and for all the keys"""
    temp_list = []
    for key in a_dict.keys():
        for path in range(len(key.split(";"))):
            temp_list.append(key.split(";")[path])
    return temp_list


def sub_lister(a_list, num) -> list:
    """partition the previously created list, depending of the branch level of the datatree"""
    return [a_list[i:i + num] for i in range(0, len(a_list), num)]


def label_dict(nested_list: list, label: list) -> dict:
    """create a dictionary for each path labels"""
    yolo_dict = {}
    for sub_list_index in range(len(nested_list)):
        key = label[sub_list_index]
        yolo_dict[key] = [label[sub_list_index] + "_" + item for item in nested_list[sub_list_index]]
    return yolo_dict


def dicts_for_datatypes(a_dict: dict, datatypes: list) -> list:
    """create a list of dictionaries, where each datatypes gets a list of values from another dictionary"""
    name_dict = []
    for i in range(len(datatypes)):
        name_dict.append({datatypes[i]: [x[i] for x in a_dict.values()]})
    return name_dict


def dict_merger(a_dict, list_of_dicts) -> dict:
    """merge dictionaries together"""
    for i in list_of_dicts:
        a_dict.update(i)
    return a_dict


def fix_one_item_list(a_df, data_type):
    """Fixes weird behaviour where some items are a one item list"""
    counter = 0
    for item in a_df[data_type]:
        if isinstance(item, list):
            a_df[data_type][counter] = item[0]
        counter += 1
    return a_df


def csv_to_df(df1):
    """load df from a csv, with special line-terminator"""
    buffer = io.StringIO(df1)
    loaded_df1 = pd.read_csv(filepath_or_buffer=buffer, skipinitialspace=True, lineterminator='@')
    return loaded_df1
