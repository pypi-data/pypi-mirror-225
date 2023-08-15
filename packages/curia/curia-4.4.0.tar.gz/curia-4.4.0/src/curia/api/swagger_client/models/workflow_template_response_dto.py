# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 3.9.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class WorkflowTemplateResponseDto(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float',
        'name': 'str',
        'description': 'str',
        'parameters': 'WorkflowTemplateParameters',
        'definition': 'WorkflowTemplateDefinition',
        'organization_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version',
        'name': 'name',
        'description': 'description',
        'parameters': 'parameters',
        'definition': 'definition',
        'organization_id': 'organizationId'
    }

    def __init__(self, id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None, name=None, description=None, parameters=None, definition=None, organization_id=None):  # noqa: E501
        """WorkflowTemplateResponseDto - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self._name = None
        self._description = None
        self._parameters = None
        self._definition = None
        self._organization_id = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if version is not None:
            self.version = version
        self.name = name
        if description is not None:
            self.description = description
        if parameters is not None:
            self.parameters = parameters
        self.definition = definition
        self.organization_id = organization_id

    @property
    def id(self):
        """Gets the id of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The id of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this WorkflowTemplateResponseDto.


        :param id: The id of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The last_updated_by of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this WorkflowTemplateResponseDto.


        :param last_updated_by: The last_updated_by of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The created_by of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowTemplateResponseDto.


        :param created_by: The created_by of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The created_at of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this WorkflowTemplateResponseDto.


        :param created_at: The created_at of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The updated_at of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this WorkflowTemplateResponseDto.


        :param updated_at: The updated_at of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The archived_at of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this WorkflowTemplateResponseDto.


        :param archived_at: The archived_at of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The version of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this WorkflowTemplateResponseDto.


        :param version: The version of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: float
        """

        self._version = version

    @property
    def name(self):
        """Gets the name of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The name of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this WorkflowTemplateResponseDto.


        :param name: The name of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The description of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this WorkflowTemplateResponseDto.


        :param description: The description of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def parameters(self):
        """Gets the parameters of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The parameters of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: WorkflowTemplateParameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this WorkflowTemplateResponseDto.


        :param parameters: The parameters of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: WorkflowTemplateParameters
        """

        self._parameters = parameters

    @property
    def definition(self):
        """Gets the definition of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The definition of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: WorkflowTemplateDefinition
        """
        return self._definition

    @definition.setter
    def definition(self, definition):
        """Sets the definition of this WorkflowTemplateResponseDto.


        :param definition: The definition of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: WorkflowTemplateDefinition
        """
        if definition is None:
            raise ValueError("Invalid value for `definition`, must not be `None`")  # noqa: E501

        self._definition = definition

    @property
    def organization_id(self):
        """Gets the organization_id of this WorkflowTemplateResponseDto.  # noqa: E501


        :return: The organization_id of this WorkflowTemplateResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this WorkflowTemplateResponseDto.


        :param organization_id: The organization_id of this WorkflowTemplateResponseDto.  # noqa: E501
        :type: str
        """
        if organization_id is None:
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(WorkflowTemplateResponseDto, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, WorkflowTemplateResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
