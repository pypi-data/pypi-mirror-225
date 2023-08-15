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

class WorkflowExecutionSpecResponseDto(object):
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
        'execution': 'WorkflowExecutionSpecJoinedWorkflowExecutionResponseDto',
        'execution_id': 'str',
        'parameters': 'WorkflowTemplateParameters',
        'definition': 'WorkflowTemplateDefinition'
    }

    attribute_map = {
        'id': 'id',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version',
        'execution': 'execution',
        'execution_id': 'executionId',
        'parameters': 'parameters',
        'definition': 'definition'
    }

    def __init__(self, id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None, execution=None, execution_id=None, parameters=None, definition=None):  # noqa: E501
        """WorkflowExecutionSpecResponseDto - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self._execution = None
        self._execution_id = None
        self._parameters = None
        self._definition = None
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
        if execution is not None:
            self.execution = execution
        self.execution_id = execution_id
        if parameters is not None:
            self.parameters = parameters
        self.definition = definition

    @property
    def id(self):
        """Gets the id of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The id of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this WorkflowExecutionSpecResponseDto.


        :param id: The id of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The last_updated_by of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this WorkflowExecutionSpecResponseDto.


        :param last_updated_by: The last_updated_by of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The created_by of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowExecutionSpecResponseDto.


        :param created_by: The created_by of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The created_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this WorkflowExecutionSpecResponseDto.


        :param created_at: The created_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The updated_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this WorkflowExecutionSpecResponseDto.


        :param updated_at: The updated_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The archived_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this WorkflowExecutionSpecResponseDto.


        :param archived_at: The archived_at of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The version of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this WorkflowExecutionSpecResponseDto.


        :param version: The version of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: float
        """

        self._version = version

    @property
    def execution(self):
        """Gets the execution of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The execution of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: WorkflowExecutionSpecJoinedWorkflowExecutionResponseDto
        """
        return self._execution

    @execution.setter
    def execution(self, execution):
        """Sets the execution of this WorkflowExecutionSpecResponseDto.


        :param execution: The execution of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: WorkflowExecutionSpecJoinedWorkflowExecutionResponseDto
        """

        self._execution = execution

    @property
    def execution_id(self):
        """Gets the execution_id of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The execution_id of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this WorkflowExecutionSpecResponseDto.


        :param execution_id: The execution_id of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: str
        """
        if execution_id is None:
            raise ValueError("Invalid value for `execution_id`, must not be `None`")  # noqa: E501

        self._execution_id = execution_id

    @property
    def parameters(self):
        """Gets the parameters of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The parameters of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: WorkflowTemplateParameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this WorkflowExecutionSpecResponseDto.


        :param parameters: The parameters of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: WorkflowTemplateParameters
        """

        self._parameters = parameters

    @property
    def definition(self):
        """Gets the definition of this WorkflowExecutionSpecResponseDto.  # noqa: E501


        :return: The definition of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :rtype: WorkflowTemplateDefinition
        """
        return self._definition

    @definition.setter
    def definition(self, definition):
        """Sets the definition of this WorkflowExecutionSpecResponseDto.


        :param definition: The definition of this WorkflowExecutionSpecResponseDto.  # noqa: E501
        :type: WorkflowTemplateDefinition
        """
        if definition is None:
            raise ValueError("Invalid value for `definition`, must not be `None`")  # noqa: E501

        self._definition = definition

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
        if issubclass(WorkflowExecutionSpecResponseDto, dict):
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
        if not isinstance(other, WorkflowExecutionSpecResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
