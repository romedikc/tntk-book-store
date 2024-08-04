from datetime import datetime


def to_dict(model):
    def serialize_value(value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    return {column.name: serialize_value(getattr(model, column.name)) for column in model.__table__.columns}
