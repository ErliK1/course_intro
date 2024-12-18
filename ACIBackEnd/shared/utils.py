def get_error_message(message, *args):
    return message.format(*args)

def check_ids_part_of_db(list_of_ids, model_class):
    try:
        map(lambda x: model_class.objects.get(id=x), list_of_ids)
        result = True
    except Exception:
        result = False
    finally:
        return result



