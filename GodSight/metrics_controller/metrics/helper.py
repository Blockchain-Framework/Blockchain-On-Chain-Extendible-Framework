from .models import TransactionsFeatureMapping, EmittedUtxosFeatureMapping, ConsumedUtxosFeatureMapping


def get_column_details(blockchain, sub_chain):
    """
    Fetches column details from the database for the specified blockchain and sub-chain.
    Returns a dictionary with column names as keys and their types as values.
    """
    column_details = {}

    # Assuming 'type' field contains information if a column is numerical or not
    # Adjust the query if your database schema differs
    mappings = (
        TransactionsFeatureMapping.objects.filter(blockchain=blockchain, sub_chain=sub_chain)
        .union(
            EmittedUtxosFeatureMapping.objects.filter(blockchain=blockchain, sub_chain=sub_chain),
            ConsumedUtxosFeatureMapping.objects.filter(blockchain=blockchain, sub_chain=sub_chain),
            all=True
        )
    )

    for mapping in mappings:
        column_details[mapping.sourceField] = mapping.type

    return column_details
