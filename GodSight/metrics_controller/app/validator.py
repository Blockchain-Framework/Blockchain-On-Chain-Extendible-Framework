from app.handler import query_all_general_models, check_field_name_exists


def validate_json_structure(formula, formula_type):
    # Define the expected keys for both formats
    expected_keys_aggregation = {'name', 'column', 'function'}
    expected_keys_arithmetic = {'name', 'operation', 'operands'}
    valid_functions = ['sum', 'avg', 'min', 'max']  # Example valid functions
    valid_operations = ['addition', 'subtraction', 'multiplication', 'division']

    # Basic checks for key presence based on formula type
    if 'aggregations' not in formula or 'final_answer' not in formula:
        return False, "Missing 'aggregations' or 'final_answer' in formula."

    # Check for unexpected keys in the root of the formula
    expected_root_keys = {'aggregations', 'final_answer', 'arithmetic'} if formula_type == 'Format 2' else {
        'aggregations', 'final_answer'}
    unexpected_keys = set(formula.keys()) - expected_root_keys
    if unexpected_keys:
        return False, f"Unexpected keys in formula: {', '.join(unexpected_keys)}."

    # Validate 'aggregations' structure
    for aggregation in formula['aggregations']:
        # Check for required keys and unexpected keys
        if not all(key in aggregation for key in expected_keys_aggregation):
            return False, "One or more 'aggregations' items are missing required keys."
        if not set(aggregation.keys()).issubset(expected_keys_aggregation):
            return False, f"Unexpected keys in 'aggregations': {', '.join(set(aggregation.keys()) - expected_keys_aggregation)}."
        # Validate values are strings
        if not all(isinstance(aggregation[key], str) for key in expected_keys_aggregation):
            return False, "All values in 'aggregations' must be strings."
        # Validate function is one of the valid functions
        if aggregation['function'] not in valid_functions:
            return False, f"Invalid function '{aggregation['function']}' in 'aggregations'. Valid functions are: {', '.join(valid_functions)}."

    # Validate 'arithmetic' structure for Format 2
    if formula_type == 'Format 2':
        defined_names = [agg['name'] for agg in formula['aggregations']]
        for arithmetic in formula.get('arithmetic', []):
            # Check for required and unexpected keys
            if not all(key in arithmetic for key in expected_keys_arithmetic):
                return False, "One or more 'arithmetic' items are missing required keys."
            if not set(arithmetic.keys()).issubset(expected_keys_arithmetic):
                return False, f"Unexpected keys in 'arithmetic': {', '.join(set(arithmetic.keys()) - expected_keys_arithmetic)}."
            # Validate values are appropriate types
            if not isinstance(arithmetic['name'], str) or not isinstance(arithmetic['operation'], str) or not all(
                    isinstance(operand, str) for operand in arithmetic['operands']):
                return False, "All values in 'arithmetic' must be strings."
            # Validate operation is one of the valid operations
            if arithmetic['operation'] not in valid_operations:
                return False, f"Invalid operation '{arithmetic['operation']}' in 'arithmetic'. Valid operations are: {', '.join(valid_operations)}."

        # Check if 'final_answer' refers to a defined variable and is a string
        if formula['final_answer'] not in defined_names or not isinstance(formula['final_answer'], str):
            return False, "'final_answer' refers to an undefined variable or is not a string."

    return True, ""


def validate_columns_existence_and_type(formula, formula_type, blockchain, sub_chain):

    # Validate columns in 'aggregations'
    for aggregation in formula['aggregations']:
        column_name = aggregation['column']
        column_detail = check_field_name_exists(column_name)
        if column_detail is None:
            return False, f"Column '{column_name}' does not exist for blockchain {blockchain} and sub-chain {sub_chain}."
        if column_detail.data_type != 'numerical':
            return False, f"Column '{column_name}' is not suitable for numerical operations."

    # Additional validation for 'arithmetic' in Format 2
    if formula_type == 'Format 2':
        defined_variables = [agg['name'] for agg in formula['aggregations']]
        # Ensure arithmetic operations use previously defined variables
        for operation in formula.get('arithmetic', []):
            # Check if operands are defined
            for operand in operation['operands']:
                if operand not in defined_variables:
                    return False, f"Operand '{operand}' in arithmetic operation '{operation['name']}' is not defined."
            defined_variables.append(operation['name'])  # Add the result of this operation as a defined variable

        # Validate 'final_answer' references a defined variable
        if formula['final_answer'] not in defined_variables:
            return False, f"The final answer '{formula['final_answer']}' is not defined in the formula."

        # Additional check: Ensure the operations are in valid order
        if not validate_arithmetic_order(formula['arithmetic'], defined_variables):
            return False, "Arithmetic operations are not in a valid order."

    return True, ""


def validate_arithmetic_order(arithmetic_operations, defined_variables):
    """
    Validates that arithmetic operations are defined in an order that ensures
    all operands are defined before being used in an operation.
    """
    # This function assumes that defined_variables initially contains only names from aggregations
    for operation in arithmetic_operations:
        if all(operand in defined_variables for operand in operation['operands']):
            # If all operands are already defined, the operation is in a valid order
            defined_variables.append(operation['name'])
        else:
            # If any operand is not yet defined, the order is invalid
            return False
    return True