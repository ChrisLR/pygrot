import json


class NetworkComm(object):
    def __init__(self, x, y, z, mess):
        self.x = x
        self.y = y
        self.z = z
        self.mess = mess


def serialize(instance):
    return json.dumps(instance, cls=NetCommEncoder)


def deserialize(json_str):
    return json.loads(json_str, object_hook=HOOK)


class NetCommEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NetworkComm):
            return {"NetworkComm":{"mess": obj.mess, "x": obj.x, "y": obj.y, "z": obj.z}}
            # Let the base class default method raise the TypeError

        return json.JSONEncoder.default(self, obj)


def HOOK(dat_data):
    comm = dat_data.get("NetworkComm")
    if comm is None:
        return dat_data
    return NetworkComm(**comm)


if __name__ == '__main__':
    comm = NetworkComm(1,2,3,"kek")
    json_str = serialize(comm)
    back_comm = deserialize(json_str)
    print(back_comm)
