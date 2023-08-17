import uuid
import json
from .api_dto import ApiDto


class TwinRegistration(ApiDto):
    """
    Registration of a Digital Twin on a solution Template.

    :ivar twin_registration_id: UUID of the registration
    :ivar twin_id: UUID of registered Digital Twin
    :ivar template_id: UUID of the solution template.
    :ivar properties: list of Properties { name , datapoint, float, integer, string }

    A property must contains a name and the hardwareId of the datapoint or the value corresponding to the right type.
    """

    def __init__(self, twin_registration_id=None, twin_id=None, template_id=None, properties=None):
        if twin_registration_id is None:
            self.twin_registration_id = uuid.uuid4()
        else:
            self.twin_registration_id = twin_registration_id
        self.twin_id = twin_id
        self.template_id = template_id
        if properties is None:
            properties = []
        self.properties = properties
        self.createdById = None
        self.createdDate = None
        self.updatedById = None
        self.updatedDate = None

    def api_id(self) -> str:
        """
        Id of the TwinRegistrations (twin_registration_id)

        :return: string formatted UUID of the template.
        """
        return str(self.twin_registration_id).upper()

    def endpoint(self) -> str:
        """
        Name of the endpoints used to manipulate templates.
        :return: Endpoint name.
        """
        return "TwinRegistration"

    def from_json(self, obj):
        """
        Load the Registration entity from a dictionary.

        :param obj: Dict version of the Registration.
        """
        if "id" in obj.keys():
            self.twin_registration_id = uuid.UUID(obj["id"])
        if "twinId" in obj.keys() and obj["twinId"] is not None:
            self.twin_id = obj["twinId"]
        if "templateId" in obj.keys() and obj["templateId"] is not None:
            self.template_id = obj["templateId"]
        if "properties" in obj.keys() and obj["properties"] is not None:
            if isinstance(obj["properties"], str):
                self.properties = json.loads(obj["properties"])
            else:
                self.properties = obj["properties"]
        if "createdById" in obj.keys() and obj["createdById"] is not None:
            self.createdById = obj["createdById"]
        if "createdDate" in obj.keys() and obj["createdDate"] is not None:
            self.createdDate = obj["createdDate"]
        if "updatedById" in obj.keys() and obj["updatedById"] is not None:
            self.updatedById = obj["updatedById"]
        if "updatedDate" in obj.keys() and obj["updatedDate"] is not None:
            self.updatedDate = obj["updatedDate"]

    def to_json(self):
        """
        Convert the registration to a dictionary compatible to JSON format.

        :return: dictionary representation of the Registration object.
        """
        obj = {
            "id": str(self.twin_registration_id)
        }
        if self.twin_id is not None:
            obj["twinId"] = str(self.twin_id)
        if self.template_id is not None:
            obj["templateId"] = str(self.template_id)
        if self.properties is not None:
            obj["properties"] = json.dumps(self.properties)
        if self.createdById is not None:
            obj["createdById"] = str(self.createdById)
        if self.createdDate is not None:
            obj["createdDate"] = str(self.createdDate)
        if self.updatedById is not None:
            obj["updatedById"] = str(self.updatedById)
        if self.updatedDate is not None:
            obj["updatedDate"] = str(self.updatedDate)
        return obj

    def get_value(self, name: str, p_type: str):
        """
        get value of a property based on name and type.
        :param name: name of property.
        :param p_type: type of property.
        :return: value.
        """
        if self.properties is None:
            raise ValueError('there is no property on your registration.')

        if name is None or p_type is None:
            raise ValueError('please set a name or a p_type')

        for r_property in self.properties:
            if r_property is None:
                raise ValueError('a registration property cannot be None.')

            if "name" in r_property and r_property["name"] is not None and r_property["name"] == name:
                if p_type not in r_property:
                    raise ValueError(f'requested type is not set on the property {name}')
                return r_property[p_type]

        raise ValueError(f'property {name} of type {p_type} not found in the registration')
