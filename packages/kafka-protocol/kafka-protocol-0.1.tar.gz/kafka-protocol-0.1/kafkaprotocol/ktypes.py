import struct
from io import BytesIO


class Type:
    pass


class PrimitiveType(Type):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._struct = struct.Struct(cls._format)
        cls._pack = cls._struct.pack
        cls._unpack = cls._struct.unpack
        cls._size = cls._struct.size

    @classmethod
    def pack(cls, value) -> bytes:
        return cls._pack(value)

    @classmethod
    def unpack(cls, bytesio: BytesIO):
        return cls._unpack(bytesio.read(cls._size))[0]


class BOOL(PrimitiveType):
    _format = ">?"


class INT8(PrimitiveType):
    _format = ">b"


class INT16(PrimitiveType):
    _format = ">h"


class UINT16(PrimitiveType):
    _format = ">H"


class INT32(PrimitiveType):
    _format = ">i"


class INT64(PrimitiveType):
    _format = ">q"


class FLOAT32(PrimitiveType):
    _format = ">f"


class FLOAT64(PrimitiveType):
    _format = ">d"


class UUID(PrimitiveType):
    _format = "bbbbbbbbbbbbbbbb"


class NULLABLE_BYTES(Type):
    @classmethod
    def pack(cls, value):
        if value is None:
            return INT16.pack(-1)
        return INT16.pack(len(value)) + value

    @classmethod
    def unpack(cls, bytesio):
        length = INT16.unpack(bytesio)
        if length == -1:
            return None
        value = bytesio.read(length)
        if len(value) != length:
            raise ValueError("Data too short")
        return value


class NULLABLE_STRING(NULLABLE_BYTES):
    @classmethod
    def pack(cls, value):
        return super().pack(value and value.encode("utf-8") or value)

    @classmethod
    def unpack(cls, bytesio):
        value = super().unpack(bytesio)
        return value and value.decode("utf-8") or value


class BYTES(NULLABLE_BYTES):
    @classmethod
    def pack(cls, value):
        if value is None:
            raise ValueError("NULL (None) value not allowed")

        return super().pack(value)

    @classmethod
    def unpack(cls, bytesio):
        value = super().unpack(bytesio)
        if value is None:
            raise ValueError("NULL (None) value not allowed")
        return value


class STRING(NULLABLE_STRING):
    @classmethod
    def pack(cls, value):
        if value is None:
            raise ValueError("NULL (None) value not allowed")

        return super().pack(value)

    @classmethod
    def unpack(cls, bytesio):
        value = super().unpack(bytesio)
        if value is None:
            raise ValueError("NULL (None) value not allowed")
        return value


class VARINT(PrimitiveType):
    _format = ">B"

    @classmethod
    def pack(cls, value):
        value &= 0xFFFFFFFF
        result = b""
        while (value & 0xFFFFFF80) != 0:
            b = (value & 0x7F) | 0x80
            result += cls._pack(b)
            value >>= 7
        result += cls._pack(value)
        return result

    @classmethod
    def unpack(cls, bytesio):
        value, i = 0, 0
        while True:
            b = cls._unpack(bytesio.read(cls._size))[0]
            if not (b & 0x80):
                break
            value |= (b & 0x7F) << i
            i += 7
        value |= b << i
        value &= 0xFFFFFFFF
        return (value ^ 0x80000000) - 0x80000000


class COMPACT_NULLABLE_BYTES(Type):
    @classmethod
    def pack(cls, value):
        if value is None:
            return VARINT.pack(-1)
        return VARINT.pack(len(value) + 1) + value

    @classmethod
    def unpack(cls, bytesio):
        length = VARINT.unpack(bytesio)
        if length == -1:
            return None
        length -= 1  # N+1 is given as VARINT
        value = bytesio.read(length)
        if len(value) != length:
            raise ValueError("Data short")
        return value


class COMPACT_NULLABLE_STRING(COMPACT_NULLABLE_BYTES):
    @classmethod
    def pack(cls, value):
        return super().pack(value and value.encode("utf-8") or value)

    @classmethod
    def unpack(cls, bytesio):
        value = super().unpack(bytesio)
        return value and value.decode("utf-8") or value


class COMPACT_STRING(COMPACT_NULLABLE_STRING):
    @classmethod
    def pack(cls, value):
        if value is None:
            raise ValueError("NULL (None) value not allowed")

        return super().pack(value)

    @classmethod
    def unpack(cls, bytesio):
        value = super().unpack(bytesio)
        if value is None:
            raise ValueError("NULL (None) value not allowed")
        return value


class COMPACT_BYTES(COMPACT_NULLABLE_BYTES):
    @classmethod
    def pack(cls, value):
        if value is None:
            raise ValueError("NULL (None) value not allowed")

        return super().pack(value)

    @classmethod
    def unpack(cls, bytesio):
        value = super().unpack(bytesio)
        if value is None:
            raise ValueError("NULL (None) value not allowed")
        return value


class TAG_BUFFER(Type):
    @classmethod
    def pack(cls, items):
        if items is None:
            raise ValueError("NULL value (None) not allowed")
        result = []
        for key, value in items.items():
            result.append(VARINT.pack(key) + VARINT.pack(len(value)) + value)
        return VARINT.pack(len(result)) + b"".join(result)

    @classmethod
    def unpack(cls, bytesio):
        length = VARINT.unpack(bytesio)
        tags = {}
        for _ in range(length):
            tag = VARINT.unpack(bytesio)
            value_len = VARINT.unpack(bytesio)
            value = bytesio.read(value_len)
            tags[tag] = value
        return tags


RECORDS = BYTES


class ARRAY(Type):
    def __init__(self, *args, **kwargs):
        self._fields = []
        if args:
            self._item = args[0]
        else:
            self._item = type("ARRAY.Structure", (Structure,), kwargs)

    def pack(self, items):
        if items is None:
            return INT32.pack(-1)
        result = []
        for item in items:
            if not isinstance(item, Structure):
                if isinstance(item, tuple):
                    item = self._item(*item)
                elif isinstance(item, dict):
                    item = self._item(**item)
            result.append(self._item.pack(item))
        return b"".join([INT32.pack(len(result))] + result)

    def unpack(self, bytesio):
        length = INT32.unpack(bytesio)
        if length == -1:
            return None
        return [self._item.unpack(bytesio) for _ in range(length)]


class COMPACT_ARRAY(Type):
    def __init__(self, *args, **kwargs):
        self._fields = []
        if args:
            self._item = args[0]
        else:
            self._item = type("COMPACT_ARRAY.Structure", (Structure,), kwargs)

    def pack(self, items):
        if items is None:
            return VARINT.pack(-1)
        result = []
        for item in items:
            if not isinstance(item, Structure):
                if isinstance(item, tuple):
                    item = self._item(*item)
                elif isinstance(item, dict):
                    item = self._item(**item)
            result.append(self._item.pack(item))
        return b"".join([VARINT.pack(len(result) + 1)] + result)

    def unpack(self, bytesio):
        length = VARINT.unpack(bytesio)
        if length == -1:
            return None
        length -= 1  # length N+1 is given
        return [self._item.unpack(bytesio) for _ in range(length)]


class Structure:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._fields = []
        for name, value in cls.__dict__.items():
            if (
                isinstance(value, Type)
                or (type(value) is type and issubclass(value, Type))
                or (type(value) is type and issubclass(value, Structure))
            ):
                cls._fields.append((name, value))
                setattr(cls, name, None)

    def __init__(self, *args, **kwargs):
        for (name, _), value in zip(self._fields, args):
            setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        return repr({name: getattr(self, name, None) for name, _ in self._fields})

    @classmethod
    def pack(cls, value):
        result = []
        for name, t in cls._fields:
            result.append(t.pack(getattr(value, name, None)))
        return b"".join(result)

    @classmethod
    def unpack(cls, bytesio):
        result = []
        for name, t in cls._fields:
            result.append(t.unpack(bytesio))
        return cls(*result)


class RequestHeader0(Structure):
    request_api_key = INT16
    request_api_version = INT16
    correlation_id = INT32


class RequestHeader1(Structure):
    request_api_key = INT16
    request_api_version = INT16
    correlation_id = INT32
    client_id = NULLABLE_STRING


class RequestHeader2(Structure):
    request_api_key = INT16
    request_api_version = INT16
    correlation_id = INT32
    client_id = NULLABLE_STRING
    _tagged_fields = TAG_BUFFER


class ResponseHeader0(Structure):
    correlation_id = INT32


class ResponseHeader1(Structure):
    correlation_id = INT32
    _tagged_fields = TAG_BUFFER
