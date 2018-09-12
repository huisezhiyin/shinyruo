from rest_framework import serializers


class DatetimeField(serializers.Field):
    def to_representation(self, value):
        # 序列化 value为 datetime.datetime
        if not value:
            return None
        return f"{value.year}-{value.month}-{value.day} {value.hour}:{value.minute}:{value.second}"

    def to_internal_value(self, data):
        # 反序列化 此处为预留操作
        return super(DatetimeField, self).to_internal_value(data)
