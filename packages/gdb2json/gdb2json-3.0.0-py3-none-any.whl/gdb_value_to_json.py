import gdb
import json

DEBUG = False

if DEBUG:
    def print_debug(msg):
        print_debug(msg)
else:
    def print_debug(msg):
        pass

OBJ_TYPE_NEEDS_RECURSIVE_CALL = [
    gdb.TYPE_CODE_STRUCT,
    gdb.TYPE_CODE_UNION,
    gdb.TYPE_CODE_ARRAY
]


def gdb_value_to_json_obj(gdb_value: gdb.Value,
                          obj_to_fill,
                          key_for_primitive_value=None):
    """
    Obj to fill can be a dict or a list
    """

    obj_value_code = gdb_value.type.strip_typedefs().code

    # If the object is a struct, union, array... recursively process its data
    if obj_value_code in OBJ_TYPE_NEEDS_RECURSIVE_CALL:
        if type(obj_to_fill) is dict:
            gdb_value_to_dict(gdb_value, obj_to_fill)
        elif type(obj_to_fill) is list:
            item = {}
            gdb_value_to_dict(gdb_value, item)
            obj_to_fill.append(item)

    # Primitive type (int, char, enum, etc) push it to the obj_to_fill
    else:
        if type(obj_to_fill) is dict:
            if key_for_primitive_value is None:
                raise Exception("key_for_primitive_value is None")
            obj_to_fill[key_for_primitive_value] = gdb_value_to_value(
                gdb_value)
        elif type(obj_to_fill) is list:
            obj_to_fill.append(gdb_value_to_value(gdb_value))
        else:
            raise Exception("obj_to_fill is not a dict or a list")

    print_debug("Returning data: {}".format(json.dumps(obj_to_fill, indent=4)))


def gdb_value_to_value(gdb_value: gdb.Value):
    """
    Sets given value in the given dict under the given key

    :param gdb_value: gdb.Value to be returned
    """

    gdb_value_type_code = gdb_value.type.strip_typedefs().code

    if gdb_value_type_code in OBJ_TYPE_NEEDS_RECURSIVE_CALL:
        raise Exception("obj_value_to_value called on a non primitive type")

    if gdb_value_type_code == gdb.TYPE_CODE_INT:
        return hex(int(gdb_value))
    else:
        return str(gdb_value)


def gdb_value_to_dict(gdb_value: gdb.Value, data: dict):
    """
    Recursive function to convert gdb C struct/union/array to python
    dict or list

    :param gdb_value: gdb.Value
    :param data: dict or list to be filled
    :return: None
    """

    gdb_value_type_code = gdb_value.type.strip_typedefs().code

    print_debug("-- struct_type: {} code: {}".format(gdb_value.type,
                                                     gdb_value.type.code))

    if gdb_value_type_code not in OBJ_TYPE_NEEDS_RECURSIVE_CALL:
        raise Exception("obj_value_to_dict called on a primitive type")

    # Recursively extract data from nested structs/unions/arrays

    for field in gdb_value.type.fields():
        field_name = field.name
        field_value = gdb_value[field_name]
        field_type = field_value.type.strip_typedefs()
        field_type_code = field_type.code

        print_debug("---- subfield_name: {}"
                    " type_raw: {} {}"
                    "type_: {} {} ".format(
                        field_name,
                        field.type,
                        field.type.code,
                        field_type, field_type.code))

        if field_type_code == gdb.TYPE_CODE_STRUCT \
                or field_type_code == gdb.TYPE_CODE_UNION:
            print_debug("Creating struct under data [{}]".format(field_name))

            # If the field is a nested struct, recursively extract its data
            struct_data = {}
            gdb_value_to_dict(field_value, struct_data)
            if field_type_code == gdb.TYPE_CODE_STRUCT:
                key_ = field_name + "::struct"
            else:  # gdb.TYPE_CODE_UNION
                key_ = field_name + "::union"
            data[key_] = struct_data

        elif field_type_code == gdb.TYPE_CODE_ARRAY:
            print_debug("Creating array under data [{}]".format(field_name))
            # Initialize it as a list
            key_ = field_name + "::array"
            data[key_] = []

            # For each item in the array, recursively extract its data
            for i in range(field_type.range()[1]):
                gdb_value_to_json_obj(field_value[i], data[key_])

        else:
            print_debug("Creating primitive under [{}]".format(field_name))
            data[field_name] = gdb_value_to_value(field_value)
