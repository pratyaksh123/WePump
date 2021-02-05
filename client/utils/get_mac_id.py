import uuid


def get_mac():
    return (hex(uuid.getnode()))
