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

class InterventionDefinition(object):
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
        'person_set': 'PersonSet',
        'model_populations': 'list[ModelPopulation]',
        'population_id': 'str',
        'population': 'Population',
        'dataset_id': 'str',
        'dataset': 'Dataset',
        'created_at': 'datetime',
        'created_by': 'str',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'last_updated_by': 'str',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'person_set': 'personSet',
        'model_populations': 'modelPopulations',
        'population_id': 'populationId',
        'population': 'population',
        'dataset_id': 'datasetId',
        'dataset': 'dataset',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'last_updated_by': 'lastUpdatedBy',
        'version': 'version'
    }

    def __init__(self, id=None, person_set=None, model_populations=None, population_id=None, population=None, dataset_id=None, dataset=None, created_at=None, created_by=None, updated_at=None, archived_at=None, last_updated_by=None, version=None):  # noqa: E501
        """InterventionDefinition - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._person_set = None
        self._model_populations = None
        self._population_id = None
        self._population = None
        self._dataset_id = None
        self._dataset = None
        self._created_at = None
        self._created_by = None
        self._updated_at = None
        self._archived_at = None
        self._last_updated_by = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if person_set is not None:
            self.person_set = person_set
        if model_populations is not None:
            self.model_populations = model_populations
        if population_id is not None:
            self.population_id = population_id
        if population is not None:
            self.population = population
        if dataset_id is not None:
            self.dataset_id = dataset_id
        if dataset is not None:
            self.dataset = dataset
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this InterventionDefinition.  # noqa: E501


        :return: The id of this InterventionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InterventionDefinition.


        :param id: The id of this InterventionDefinition.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def person_set(self):
        """Gets the person_set of this InterventionDefinition.  # noqa: E501


        :return: The person_set of this InterventionDefinition.  # noqa: E501
        :rtype: PersonSet
        """
        return self._person_set

    @person_set.setter
    def person_set(self, person_set):
        """Sets the person_set of this InterventionDefinition.


        :param person_set: The person_set of this InterventionDefinition.  # noqa: E501
        :type: PersonSet
        """

        self._person_set = person_set

    @property
    def model_populations(self):
        """Gets the model_populations of this InterventionDefinition.  # noqa: E501


        :return: The model_populations of this InterventionDefinition.  # noqa: E501
        :rtype: list[ModelPopulation]
        """
        return self._model_populations

    @model_populations.setter
    def model_populations(self, model_populations):
        """Sets the model_populations of this InterventionDefinition.


        :param model_populations: The model_populations of this InterventionDefinition.  # noqa: E501
        :type: list[ModelPopulation]
        """

        self._model_populations = model_populations

    @property
    def population_id(self):
        """Gets the population_id of this InterventionDefinition.  # noqa: E501


        :return: The population_id of this InterventionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._population_id

    @population_id.setter
    def population_id(self, population_id):
        """Sets the population_id of this InterventionDefinition.


        :param population_id: The population_id of this InterventionDefinition.  # noqa: E501
        :type: str
        """

        self._population_id = population_id

    @property
    def population(self):
        """Gets the population of this InterventionDefinition.  # noqa: E501


        :return: The population of this InterventionDefinition.  # noqa: E501
        :rtype: Population
        """
        return self._population

    @population.setter
    def population(self, population):
        """Sets the population of this InterventionDefinition.


        :param population: The population of this InterventionDefinition.  # noqa: E501
        :type: Population
        """

        self._population = population

    @property
    def dataset_id(self):
        """Gets the dataset_id of this InterventionDefinition.  # noqa: E501


        :return: The dataset_id of this InterventionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this InterventionDefinition.


        :param dataset_id: The dataset_id of this InterventionDefinition.  # noqa: E501
        :type: str
        """

        self._dataset_id = dataset_id

    @property
    def dataset(self):
        """Gets the dataset of this InterventionDefinition.  # noqa: E501


        :return: The dataset of this InterventionDefinition.  # noqa: E501
        :rtype: Dataset
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this InterventionDefinition.


        :param dataset: The dataset of this InterventionDefinition.  # noqa: E501
        :type: Dataset
        """

        self._dataset = dataset

    @property
    def created_at(self):
        """Gets the created_at of this InterventionDefinition.  # noqa: E501


        :return: The created_at of this InterventionDefinition.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InterventionDefinition.


        :param created_at: The created_at of this InterventionDefinition.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this InterventionDefinition.  # noqa: E501


        :return: The created_by of this InterventionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this InterventionDefinition.


        :param created_by: The created_by of this InterventionDefinition.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_at(self):
        """Gets the updated_at of this InterventionDefinition.  # noqa: E501


        :return: The updated_at of this InterventionDefinition.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this InterventionDefinition.


        :param updated_at: The updated_at of this InterventionDefinition.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this InterventionDefinition.  # noqa: E501


        :return: The archived_at of this InterventionDefinition.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this InterventionDefinition.


        :param archived_at: The archived_at of this InterventionDefinition.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this InterventionDefinition.  # noqa: E501


        :return: The last_updated_by of this InterventionDefinition.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this InterventionDefinition.


        :param last_updated_by: The last_updated_by of this InterventionDefinition.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def version(self):
        """Gets the version of this InterventionDefinition.  # noqa: E501


        :return: The version of this InterventionDefinition.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this InterventionDefinition.


        :param version: The version of this InterventionDefinition.  # noqa: E501
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
        if issubclass(InterventionDefinition, dict):
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
        if not isinstance(other, InterventionDefinition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
