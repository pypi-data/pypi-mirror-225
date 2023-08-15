class MCT_TYPE_ERROR(Exception):
    def __init__(self, obj_name: str, action=None):
        # Note that __main__.MCT_TYPE_ERROR: Type Tempo not approved for MCT database use. will replace __main__ with moduel name on prod use
        self.message = "Type " + str(obj_name) + " is not an MCT approved dataclass.\n"
        super().__init__(self.message)

class MCT_INIT_TABLE_ERROR(Exception):
    def __init__(self, obj_name: str):
        self.message = "This type has not yet been approved"
        super().__init__(self.message)

# this one not currently used
class MCT_UPDATE_ERROR(Exception):
    def __init__(self, obj_name: str):
        self.message = (
            "This object of type "
            + obj_name
            + " cannot be updated because it either has not been initiated or has not been deleted.."
        )
        super().__init__(self.message)


class MCT_INDEX_ERROR(Exception):
    def __init__(self, obj_name: str, action_type: str):
        self.message = (
            "No index found for object of type "
            + obj_name
            + " on action "
            + action_type
            + ". Has the object been inserted yet or deleted already?"
        )
        super().__init__(self.message)


class MCT_DELETED_ERROR(Exception):
    def __init__(self, obj_name: str):
        self.message = (
            "Specified object of type " + obj_name + " has already been deleted."
        )
        super().__init__(self.message)