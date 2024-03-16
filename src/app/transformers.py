from typing import List


def bundle(records: List[dict], bundle_col_key: str, keys_to_include: List[str]):
    bundled_records = {}
    for record in records:
        bundle_col_value = record[bundle_col_key]
        bundled_record = {key: record[key] for key in keys_to_include}
        if bundle_col_value in bundled_records:
            bundled_records[bundle_col_value]['results'].append(bundled_record)
        else:
            bundled_records[bundle_col_value] = {'url': bundle_col_value, 'results': [bundled_record]}
    return list(bundled_records.values())
