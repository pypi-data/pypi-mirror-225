from typing import List


def filters_to_claims(filters: List[str]):
    result = []
    for value in filters:
        if value:
            [table, column, *value] = value.split(':')
            result.append({'tableName': table,
                           'columnName': column,
                           'value': ':'.join(value)})
    return result
