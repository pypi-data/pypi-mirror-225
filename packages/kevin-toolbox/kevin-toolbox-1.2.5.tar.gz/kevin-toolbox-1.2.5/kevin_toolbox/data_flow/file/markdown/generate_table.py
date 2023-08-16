def generate_table(content_s, ordered_keys=None, orientation="vertical"):
    ordered_keys = content_s.keys() if ordered_keys is None else ordered_keys
    assert orientation in ["vertical", "horizontal", "h", "v"]
    min_row_nums = min([len(i) for i in content_s.values()])
    for k in ordered_keys:
        assert len(content_s[k]) == min_row_nums, \
            f'number of rows ({len(content_s[k])}) in column {k} exceeds ' \
            f'the minimum number ({min_row_nums}) of rows in content'

    table = ""
    if orientation in ["vertical", "v"]:
        table += "| " + " | ".join([f'{i}' for i in ordered_keys]) + " |\n"
        table += "| " + " | ".join(["---"] * len(ordered_keys)) + " |\n"
        for row in zip(*[content_s[k] for k in ordered_keys]):
            table += "| " + " | ".join([f'{i}' for i in row]) + " |\n"
    else:
        for i, k in enumerate(ordered_keys):
            row = [f'{k}'] + [f'{i}' for i in content_s[k]]
            table += "| " + " | ".join(row) + " |\n"
            if i == 0:
                table += "| " + " | ".join(["---"] * len(row)) + " |\n"
    return table


if __name__ == '__main__':
    print(generate_table(content_s=dict(a=[1, 2, 3], b=[4, 5, 6]), orientation="h"))
