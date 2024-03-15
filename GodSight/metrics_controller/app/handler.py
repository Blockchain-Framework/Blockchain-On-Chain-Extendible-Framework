from .models import GeneralModel


def query_all_general_models():
    all_entries = GeneralModel.objects.all()
    return all_entries


def check_field_name_exists(field_name_to_check):
    exists = GeneralModel.objects.filter(field_name=field_name_to_check).exists()
    if exists:
        entry = GeneralModel.objects.get(field_name=field_name_to_check)
        return entry
    else:
        return None
