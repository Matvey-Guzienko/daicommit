from .tokenCount import token_count

def merge_diffs(arr: list[str], max_string_length: int) -> list[str]:
    merged_arr = []
    current_item = arr[0]

    for item in arr[1:]:
        if token_count(current_item + item) <= max_string_length:
            current_item += item
        else:
            merged_arr.append(current_item)
            current_item = item

    merged_arr.append(current_item)

    return merged_arr
