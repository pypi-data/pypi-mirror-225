import pysnooper

from kaya_module_sdk.sdk import (
    KInt, KFloat, KString, KList, KDict, KSet, KTuple, KBool, KTimeSeries,
)


def data_type_map() -> dict:
    k_map = {
        int: KInt,
        float: KFloat,
        str: KString,
        bool: KBool,
        set: KSet,
        tuple: KTuple,
        list: KList,
        dict: KDict,
    }
    return k_map

#@pysnooper.snoop()
def serializer(*args, **kwargs) -> (list, dict):
    serialized_args, serialized_kwargs, supported_types = [], {}, data_type_map()
    inverse_supported_types = {v: k for k, v in supported_types.items()}
    for arg in args:
        arg_type = type(arg)
        if arg_type in inverse_supported_types:
            serialized_args.append(arg)
            continue
        if arg_type not in supported_types:
            continue
        elif arg_type is list \
                and KTimeSeries.is_list_of_tuples_with_two_elements(arg):
            type_casted_value = KTimeSeries(arg)
        else:
            type_casted_value = supported_types[arg_type](arg)
        serialized_args.append(type_casted_value)
    for kwarg in kwargs:
        kwarg_type = type(kwarg)
        if kwarg_type in inverse_supported_types:
            serialized_kwargs.append(kwarg)
            continue
        if kwarg_type not in supported_types:
            continue
        elif kwarg_type is list \
                and KTimeSeries.is_list_of_tuples_with_two_elements(kwargs[kwarg]):
            type_casted_value = {kwarg: KTimeSeries(kwargs[kwarg])}
        else:
            type_casted_value = {kwarg: supported_types[kwarg_type](kwargs[kwarg])}
        serialized_kwargs.update(type_casted_value)
    serialized_args = [str(item) for item in serialized_args]
    serialized_kwargs = {str(k): str(v) for k, v in serialized_kwargs.items()}
    return serialized_args, serialized_kwargs

