



def calculate_amount_unlocked(transaction):
    amountUnlocked = transaction.get('amountUnlocked', [])
    
    amount_unlocked = {}
    
    for amount in amountUnlocked:
        if int(amount['denomination']) != 0:
            unlocked_value = int(amount['amount']) / int(amount['denomination'])
        else:
            unlocked_value = int(amount['amount'])

        if amount['name'] in amount_unlocked:
            amount_unlocked[amount['name']] += unlocked_value
        else:
            amount_unlocked[amount['name']] = unlocked_value

    return amount_unlocked

def calculate_amount_created(transaction):
    amountCreated = transaction.get('amountCreated', [])

    amount_created = {}
    
    for amount in amountCreated:
        if int(amount['denomination']) != 0:
            created_value = int(amount['amount']) / int(amount['denomination'])
        else:
            created_value = int(amount['amount'])

        if amount['name'] in amount_created:
            amount_created[amount['name']] += created_value
        else:
            amount_created[amount['name']] = created_value

    return amount_created