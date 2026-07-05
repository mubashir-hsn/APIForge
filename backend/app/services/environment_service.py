import re


def replace_variables(
    value,
    variables: dict
):

    if not value:
        return value

    # Replace variables like {{BASE_URL}}
    pattern = r"\{\{(.*?)\}\}"

    matches = re.findall(pattern, value)

    for match in matches:

        variable_name = match.strip()

        variable_value = variables.get(
            variable_name
        )

        if variable_value:

            value = value.replace(
                f"{{{{{variable_name}}}}}",
                str(variable_value)
            )

    return value