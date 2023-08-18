import re
from typing import List, Tuple


def build_query(query_params: List[Tuple]):
    result = {}

    if len(query_params) == 0:
        return result

    fields = []
    sort = {}
    pagination = {}
    filters = {}

    for item in query_params:
        param = item[0]
        value = item[1]

        if (len(value) != 0):
            if (param == "fields"):
                fields.extend(value.split(","))
            elif (param == "sort"):
                if value[0] == "-":
                    sort[value[1:]] = "DESC"
                else:
                    sort[value] = "ASC"
            elif (param == "page"):
                pagination["page"] = process_page_value(value)
            elif (param == "limit"):
                pagination["limit"] = process_limit_value(value)
            else:
                if (value.find(",") != -1):
                    value_temp = {}
                    value_temp["$or"] = [process_filter_value(item) for item in value.split(",")]
                    filters[param] = value_temp
                elif (value.find(";") != -1):
                    value_temp = {}
                    value_temp["$and"] = [process_filter_value(item) for item in value.split(";")]
                    filters[param] = value_temp
                else:
                    filters[param] = process_filter_value(value)

    if (len(fields)):
        result["fields"] = fields
    if (len(sort)):
        result["sort"] = sort
    if (len(pagination)):
        result["pagination"] = pagination
    if (len(filters)):
        result["filters"] = filters

    return result


def process_page_value(value):
    return int(value) if value.isdigit() else 1


def process_limit_value(value):
    return int(value) if value.isdigit() else 100


def process_filter_value(value):
    if (value.startswith("*") or value.endswith("*")):
        return build_regex(value)
    elif (value.find(":") != -1):
        return build_comparison_operator(value)
    return value


def build_regex(value):
    value = re.sub(r"\*{2,}", "*", value)
    value = re.sub(r"\+", "\+", value)
    value = add_accent_regex(value)

    result = {}

    if (not value.startswith("*") and value.endswith("*")):
        result["$regex"] = "^{}".format(value.replace("*", ""))
    elif (value.startswith("*") and not value.endswith("*")):
        result["$regex"] = "{}$".format(value.replace("*", ""))
    else:
        result["$regex"] = value.replace("*", "")

    return result


def add_accent_regex(value):
    return value.replace("a", "[a,á,à,ä,â,ã]") \
        .replace("A", "[A,Á,À,Ä,Â,Ã]") \
        .replace("e", "[e,é,ë,ê]") \
        .replace("E", "[E,É,Ë,Ê]") \
        .replace("i", "[i,í,ï]") \
        .replace("I", "[I,Í,Ï]") \
        .replace("o", "[o,ó,ò,ö,ô]") \
        .replace("O", "[O,Ó,Ò,Ö,Ô]") \
        .replace("u", "[u,ú,ù,ü]") \
        .replace("U", "[U,Ú,Ù,Ü]")


def build_comparison_operator(value):
    if (value.startswith("gte:")):
        return {"$gte": value[4:]}
    elif (value.startswith("gt:")):
        return {"$gt": value[3:]}
    elif (value.startswith("lte:")):
        return {"$lte": value[4:]}
    elif (value.startswith("lt:")):
        return {"$lt": value[3:]}
    elif (value.startswith("ne:")):
        return {"$ne": value[3:]}

    return value
