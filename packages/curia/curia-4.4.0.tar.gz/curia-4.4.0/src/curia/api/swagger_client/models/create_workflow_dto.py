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

class CreateWorkflowDto(object):
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
        'name': 'str',
        'description': 'str',
        'tags': 'list[str]',
        'template_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'tags': 'tags',
        'template_id': 'templateId'
    }

    def __init__(self, name=None, description=None, tags=None, template_id=None):  # noqa: E501
        """CreateWorkflowDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._tags = None
        self._template_id = None
        self.discriminator = None
        self.name = name
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        self.template_id = template_id

    @property
    def name(self):
        """Gets the name of this CreateWorkflowDto.  # noqa: E501


        :return: The name of this CreateWorkflowDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateWorkflowDto.


        :param name: The name of this CreateWorkflowDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this CreateWorkflowDto.  # noqa: E501


        :return: The description of this CreateWorkflowDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateWorkflowDto.


        :param description: The description of this CreateWorkflowDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def tags(self):
        """Gets the tags of this CreateWorkflowDto.  # noqa: E501


        :return: The tags of this CreateWorkflowDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateWorkflowDto.


        :param tags: The tags of this CreateWorkflowDto.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def template_id(self):
        """Gets the template_id of this CreateWorkflowDto.  # noqa: E501


        :return: The template_id of this CreateWorkflowDto.  # noqa: E501
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this CreateWorkflowDto.


        :param template_id: The template_id of this CreateWorkflowDto.  # noqa: E501
        :type: str
        """
        if template_id is None:
            raise ValueError("Invalid value for `template_id`, must not be `None`")  # noqa: E501

        self._template_id = template_id

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
        if issubclass(CreateWorkflowDto, dict):
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
        if not isinstance(other, CreateWorkflowDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
