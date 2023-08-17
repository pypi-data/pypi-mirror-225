from . import schemas


def mouse_record_to_dynamodb_record(mouse_record: schemas.MouseRecord) -> dict:
    return {
        'id': {'S': mouse_record.id},
        'labtracks_id': {'S': mouse_record.labtracks_id},
        'age': {'N': str(mouse_record.age)},
        'state': {'S': mouse_record.state},
        'status': {'N': str(mouse_record.status)},
        'created_at': {'N': str(mouse_record.created_at)},
        'updated_at': {'N': str(mouse_record.updated_at)},
    }

    