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

class UpdateWorkflowExecutionSpecDto(object):
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
        'execution_id': 'str',
        'parameters': 'WorkflowTemplateParameters',
        'definition': 'WorkflowTemplateDefinition'
    }

    attribute_map = {
        'execution_id': 'executionId',
        'parameters': 'parameters',
        'definition': 'definition'
    }

    def __init__(self, execution_id=None, parameters=None, definition=None):  # noqa: E501
        """UpdateWorkflowExecutionSpecDto - a model defined in Swagger"""  # noqa: E501
        self._execution_id = None
        self._parameters = None
        self._definition = None
        self.discriminator = None
        if execution_id is not None:
            self.execution_id = execution_id
        if parameters is not None:
            self.parameters = parameters
        if definition is not None:
            self.definition = definition

    @property
    def execution_id(self):
        """Gets the execution_id of this UpdateWorkflowExecutionSpecDto.  # noqa: E501


        :return: The execution_id of this UpdateWorkflowExecutionSpecDto.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this UpdateWorkflowExecutionSpecDto.


        :param execution_id: The execution_id of this UpdateWorkflowExecutionSpecDto.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def parameters(self):
        """Gets the parameters of this UpdateWorkflowExecutionSpecDto.  # noqa: E501


        :return: The parameters of this UpdateWorkflowExecutionSpecDto.  # noqa: E501
        :rtype: WorkflowTemplateParameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this UpdateWorkflowExecutionSpecDto.


        :param parameters: The parameters of this UpdateWorkflowExecutionSpecDto.  # noqa: E501
        :type: WorkflowTemplateParameters
        """

        self._parameters = parameters

    @property
    def definition(self):
        """Gets the definition of this UpdateWorkflowExecutionSpecDto.  # noqa: E501


        :return: The definition of this UpdateWorkflowExecutionSpecDto.  # noqa: E501
        :rtype: WorkflowTemplateDefinition
        """
        return self._definition

    @definition.setter
    def definition(self, definition):
        """Sets the definition of this UpdateWorkflowExecutionSpecDto.


        :param definition: The definition of this UpdateWorkflowExecutionSpecDto.  # noqa: E501
        :type: WorkflowTemplateDefinition
        """

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
        if issubclass(UpdateWorkflowExecutionSpecDto, dict):
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
        if not isinstance(other, UpdateWorkflowExecutionSpecDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
