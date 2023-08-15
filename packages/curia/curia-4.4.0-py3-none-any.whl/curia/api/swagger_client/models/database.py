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

class Database(object):
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
        'name': 'str',
        'description': 'str',
        'location': 'str',
        'last_synced_at': 'datetime',
        'organization_id': 'str',
        'organization': 'Organization',
        'tables': 'list[DataTable]',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'location': 'location',
        'last_synced_at': 'lastSyncedAt',
        'organization_id': 'organizationId',
        'organization': 'organization',
        'tables': 'tables',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, description=None, location=None, last_synced_at=None, organization_id=None, organization=None, tables=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """Database - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._description = None
        self._location = None
        self._last_synced_at = None
        self._organization_id = None
        self._organization = None
        self._tables = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        self.id = id
        self.name = name
        if description is not None:
            self.description = description
        if location is not None:
            self.location = location
        if last_synced_at is not None:
            self.last_synced_at = last_synced_at
        self.organization_id = organization_id
        if organization is not None:
            self.organization = organization
        if tables is not None:
            self.tables = tables
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

    @property
    def id(self):
        """Gets the id of this Database.  # noqa: E501


        :return: The id of this Database.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Database.


        :param id: The id of this Database.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Database.  # noqa: E501


        :return: The name of this Database.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Database.


        :param name: The name of this Database.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Database.  # noqa: E501


        :return: The description of this Database.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Database.


        :param description: The description of this Database.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def location(self):
        """Gets the location of this Database.  # noqa: E501


        :return: The location of this Database.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this Database.


        :param location: The location of this Database.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def last_synced_at(self):
        """Gets the last_synced_at of this Database.  # noqa: E501


        :return: The last_synced_at of this Database.  # noqa: E501
        :rtype: datetime
        """
        return self._last_synced_at

    @last_synced_at.setter
    def last_synced_at(self, last_synced_at):
        """Sets the last_synced_at of this Database.


        :param last_synced_at: The last_synced_at of this Database.  # noqa: E501
        :type: datetime
        """

        self._last_synced_at = last_synced_at

    @property
    def organization_id(self):
        """Gets the organization_id of this Database.  # noqa: E501


        :return: The organization_id of this Database.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this Database.


        :param organization_id: The organization_id of this Database.  # noqa: E501
        :type: str
        """
        if organization_id is None:
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def organization(self):
        """Gets the organization of this Database.  # noqa: E501


        :return: The organization of this Database.  # noqa: E501
        :rtype: Organization
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this Database.


        :param organization: The organization of this Database.  # noqa: E501
        :type: Organization
        """

        self._organization = organization

    @property
    def tables(self):
        """Gets the tables of this Database.  # noqa: E501


        :return: The tables of this Database.  # noqa: E501
        :rtype: list[DataTable]
        """
        return self._tables

    @tables.setter
    def tables(self, tables):
        """Sets the tables of this Database.


        :param tables: The tables of this Database.  # noqa: E501
        :type: list[DataTable]
        """

        self._tables = tables

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this Database.  # noqa: E501


        :return: The last_updated_by of this Database.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this Database.


        :param last_updated_by: The last_updated_by of this Database.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this Database.  # noqa: E501


        :return: The created_by of this Database.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Database.


        :param created_by: The created_by of this Database.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this Database.  # noqa: E501


        :return: The created_at of this Database.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Database.


        :param created_at: The created_at of this Database.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Database.  # noqa: E501


        :return: The updated_at of this Database.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Database.


        :param updated_at: The updated_at of this Database.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this Database.  # noqa: E501


        :return: The archived_at of this Database.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this Database.


        :param archived_at: The archived_at of this Database.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this Database.  # noqa: E501


        :return: The version of this Database.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Database.


        :param version: The version of this Database.  # noqa: E501
        :type: float
        """

        self._version = version

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
        if issubclass(Database, dict):
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
        if not isinstance(other, Database):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
