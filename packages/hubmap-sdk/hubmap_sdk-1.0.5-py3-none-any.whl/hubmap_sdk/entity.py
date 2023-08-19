class Entity:

    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def get_uuid(self):
        return self.uuid
