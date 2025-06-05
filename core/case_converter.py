def camel_case_to_snake_case(input: str) -> str:
    result = []
    for c_idx, char in enumerate(input):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            flag = nxt_idx >= len(input) or input[nxt_idx].isupper()
            prev_char = input[c_idx - 1]
            if flag and prev_char.isupper():
                pass
            else:
                result.append("_")
        result.append(char.lower())
    return "".join(result)
