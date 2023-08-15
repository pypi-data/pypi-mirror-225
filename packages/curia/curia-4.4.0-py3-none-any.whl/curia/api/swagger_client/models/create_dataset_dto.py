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

class CreateDatasetDto(object):
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
        'type': 'object',
        'model_type': 'str',
        'outcome_type': 'object',
        'treatment_type': 'object',
        'location': 'str',
        'snowflake_location': 'str',
        'file_content_type': 'str',
        'file_size': 'str',
        'file_type': 'str',
        'row_count': 'str',
        'column_count': 'float',
        'status': 'str',
        'is_downloadable': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'tags': 'tags',
        'type': 'type',
        'model_type': 'modelType',
        'outcome_type': 'outcomeType',
        'treatment_type': 'treatmentType',
        'location': 'location',
        'snowflake_location': 'snowflakeLocation',
        'file_content_type': 'fileContentType',
        'file_size': 'fileSize',
        'file_type': 'fileType',
        'row_count': 'rowCount',
        'column_count': 'columnCount',
        'status': 'status',
        'is_downloadable': 'isDownloadable'
    }

    def __init__(self, name=None, description=None, tags=None, type=None, model_type=None, outcome_type=None, treatment_type=None, location=None, snowflake_location=None, file_content_type=None, file_size=None, file_type=None, row_count=None, column_count=None, status=None, is_downloadable=None):  # noqa: E501
        """CreateDatasetDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._tags = None
        self._type = None
        self._model_type = None
        self._outcome_type = None
        self._treatment_type = None
        self._location = None
        self._snowflake_location = None
        self._file_content_type = None
        self._file_size = None
        self._file_type = None
        self._row_count = None
        self._column_count = None
        self._status = None
        self._is_downloadable = None
        self.discriminator = None
        self.name = name
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        self.type = type
        if model_type is not None:
            self.model_type = model_type
        if outcome_type is not None:
            self.outcome_type = outcome_type
        if treatment_type is not None:
            self.treatment_type = treatment_type
        if location is not None:
            self.location = location
        if snowflake_location is not None:
            self.snowflake_location = snowflake_location
        if file_content_type is not None:
            self.file_content_type = file_content_type
        if file_size is not None:
            self.file_size = file_size
        if file_type is not None:
            self.file_type = file_type
        if row_count is not None:
            self.row_count = row_count
        if column_count is not None:
            self.column_count = column_count
        if status is not None:
            self.status = status
        if is_downloadable is not None:
            self.is_downloadable = is_downloadable

    @property
    def name(self):
        """Gets the name of this CreateDatasetDto.  # noqa: E501


        :return: The name of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateDatasetDto.


        :param name: The name of this CreateDatasetDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this CreateDatasetDto.  # noqa: E501


        :return: The description of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateDatasetDto.


        :param description: The description of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def tags(self):
        """Gets the tags of this CreateDatasetDto.  # noqa: E501


        :return: The tags of this CreateDatasetDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateDatasetDto.


        :param tags: The tags of this CreateDatasetDto.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def type(self):
        """Gets the type of this CreateDatasetDto.  # noqa: E501


        :return: The type of this CreateDatasetDto.  # noqa: E501
        :rtype: object
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateDatasetDto.


        :param type: The type of this CreateDatasetDto.  # noqa: E501
        :type: object
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def model_type(self):
        """Gets the model_type of this CreateDatasetDto.  # noqa: E501


        :return: The model_type of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """Sets the model_type of this CreateDatasetDto.


        :param model_type: The model_type of this CreateDatasetDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["risk", "impactability"]  # noqa: E501
        if model_type not in allowed_values:
            raise ValueError(
                "Invalid value for `model_type` ({0}), must be one of {1}"  # noqa: E501
                .format(model_type, allowed_values)
            )

        self._model_type = model_type

    @property
    def outcome_type(self):
        """Gets the outcome_type of this CreateDatasetDto.  # noqa: E501


        :return: The outcome_type of this CreateDatasetDto.  # noqa: E501
        :rtype: object
        """
        return self._outcome_type

    @outcome_type.setter
    def outcome_type(self, outcome_type):
        """Sets the outcome_type of this CreateDatasetDto.


        :param outcome_type: The outcome_type of this CreateDatasetDto.  # noqa: E501
        :type: object
        """

        self._outcome_type = outcome_type

    @property
    def treatment_type(self):
        """Gets the treatment_type of this CreateDatasetDto.  # noqa: E501


        :return: The treatment_type of this CreateDatasetDto.  # noqa: E501
        :rtype: object
        """
        return self._treatment_type

    @treatment_type.setter
    def treatment_type(self, treatment_type):
        """Sets the treatment_type of this CreateDatasetDto.


        :param treatment_type: The treatment_type of this CreateDatasetDto.  # noqa: E501
        :type: object
        """

        self._treatment_type = treatment_type

    @property
    def location(self):
        """Gets the location of this CreateDatasetDto.  # noqa: E501


        :return: The location of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this CreateDatasetDto.


        :param location: The location of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def snowflake_location(self):
        """Gets the snowflake_location of this CreateDatasetDto.  # noqa: E501


        :return: The snowflake_location of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._snowflake_location

    @snowflake_location.setter
    def snowflake_location(self, snowflake_location):
        """Sets the snowflake_location of this CreateDatasetDto.


        :param snowflake_location: The snowflake_location of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._snowflake_location = snowflake_location

    @property
    def file_content_type(self):
        """Gets the file_content_type of this CreateDatasetDto.  # noqa: E501


        :return: The file_content_type of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._file_content_type

    @file_content_type.setter
    def file_content_type(self, file_content_type):
        """Sets the file_content_type of this CreateDatasetDto.


        :param file_content_type: The file_content_type of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._file_content_type = file_content_type

    @property
    def file_size(self):
        """Gets the file_size of this CreateDatasetDto.  # noqa: E501


        :return: The file_size of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._file_size

    @file_size.setter
    def file_size(self, file_size):
        """Sets the file_size of this CreateDatasetDto.


        :param file_size: The file_size of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._file_size = file_size

    @property
    def file_type(self):
        """Gets the file_type of this CreateDatasetDto.  # noqa: E501


        :return: The file_type of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        """Sets the file_type of this CreateDatasetDto.


        :param file_type: The file_type of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._file_type = file_type

    @property
    def row_count(self):
        """Gets the row_count of this CreateDatasetDto.  # noqa: E501


        :return: The row_count of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._row_count

    @row_count.setter
    def row_count(self, row_count):
        """Sets the row_count of this CreateDatasetDto.


        :param row_count: The row_count of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._row_count = row_count

    @property
    def column_count(self):
        """Gets the column_count of this CreateDatasetDto.  # noqa: E501


        :return: The column_count of this CreateDatasetDto.  # noqa: E501
        :rtype: float
        """
        return self._column_count

    @column_count.setter
    def column_count(self, column_count):
        """Sets the column_count of this CreateDatasetDto.


        :param column_count: The column_count of this CreateDatasetDto.  # noqa: E501
        :type: float
        """

        self._column_count = column_count

    @property
    def status(self):
        """Gets the status of this CreateDatasetDto.  # noqa: E501


        :return: The status of this CreateDatasetDto.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CreateDatasetDto.


        :param status: The status of this CreateDatasetDto.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def is_downloadable(self):
        """Gets the is_downloadable of this CreateDatasetDto.  # noqa: E501


        :return: The is_downloadable of this CreateDatasetDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_downloadable

    @is_downloadable.setter
    def is_downloadable(self, is_downloadable):
        """Sets the is_downloadable of this CreateDatasetDto.


        :param is_downloadable: The is_downloadable of this CreateDatasetDto.  # noqa: E501
        :type: bool
        """

        self._is_downloadable = is_downloadable

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
        if issubclass(CreateDatasetDto, dict):
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
        if not isinstance(other, CreateDatasetDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
