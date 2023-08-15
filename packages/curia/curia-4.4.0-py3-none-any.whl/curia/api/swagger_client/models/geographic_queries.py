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

class GeographicQueries(object):
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
        'outcome_count_by_zip_query': 'str',
        'outcome_count_by_state_query': 'str',
        'cohort_count_by_zip_query': 'str',
        'cohort_count_by_state_query': 'str',
        'intervention_count_by_zip_query': 'str',
        'intervention_count_by_state_query': 'str'
    }

    attribute_map = {
        'outcome_count_by_zip_query': 'outcomeCountByZipQuery',
        'outcome_count_by_state_query': 'outcomeCountByStateQuery',
        'cohort_count_by_zip_query': 'cohortCountByZipQuery',
        'cohort_count_by_state_query': 'cohortCountByStateQuery',
        'intervention_count_by_zip_query': 'interventionCountByZipQuery',
        'intervention_count_by_state_query': 'interventionCountByStateQuery'
    }

    def __init__(self, outcome_count_by_zip_query=None, outcome_count_by_state_query=None, cohort_count_by_zip_query=None, cohort_count_by_state_query=None, intervention_count_by_zip_query=None, intervention_count_by_state_query=None):  # noqa: E501
        """GeographicQueries - a model defined in Swagger"""  # noqa: E501
        self._outcome_count_by_zip_query = None
        self._outcome_count_by_state_query = None
        self._cohort_count_by_zip_query = None
        self._cohort_count_by_state_query = None
        self._intervention_count_by_zip_query = None
        self._intervention_count_by_state_query = None
        self.discriminator = None
        if outcome_count_by_zip_query is not None:
            self.outcome_count_by_zip_query = outcome_count_by_zip_query
        if outcome_count_by_state_query is not None:
            self.outcome_count_by_state_query = outcome_count_by_state_query
        if cohort_count_by_zip_query is not None:
            self.cohort_count_by_zip_query = cohort_count_by_zip_query
        if cohort_count_by_state_query is not None:
            self.cohort_count_by_state_query = cohort_count_by_state_query
        if intervention_count_by_zip_query is not None:
            self.intervention_count_by_zip_query = intervention_count_by_zip_query
        if intervention_count_by_state_query is not None:
            self.intervention_count_by_state_query = intervention_count_by_state_query

    @property
    def outcome_count_by_zip_query(self):
        """Gets the outcome_count_by_zip_query of this GeographicQueries.  # noqa: E501


        :return: The outcome_count_by_zip_query of this GeographicQueries.  # noqa: E501
        :rtype: str
        """
        return self._outcome_count_by_zip_query

    @outcome_count_by_zip_query.setter
    def outcome_count_by_zip_query(self, outcome_count_by_zip_query):
        """Sets the outcome_count_by_zip_query of this GeographicQueries.


        :param outcome_count_by_zip_query: The outcome_count_by_zip_query of this GeographicQueries.  # noqa: E501
        :type: str
        """

        self._outcome_count_by_zip_query = outcome_count_by_zip_query

    @property
    def outcome_count_by_state_query(self):
        """Gets the outcome_count_by_state_query of this GeographicQueries.  # noqa: E501


        :return: The outcome_count_by_state_query of this GeographicQueries.  # noqa: E501
        :rtype: str
        """
        return self._outcome_count_by_state_query

    @outcome_count_by_state_query.setter
    def outcome_count_by_state_query(self, outcome_count_by_state_query):
        """Sets the outcome_count_by_state_query of this GeographicQueries.


        :param outcome_count_by_state_query: The outcome_count_by_state_query of this GeographicQueries.  # noqa: E501
        :type: str
        """

        self._outcome_count_by_state_query = outcome_count_by_state_query

    @property
    def cohort_count_by_zip_query(self):
        """Gets the cohort_count_by_zip_query of this GeographicQueries.  # noqa: E501


        :return: The cohort_count_by_zip_query of this GeographicQueries.  # noqa: E501
        :rtype: str
        """
        return self._cohort_count_by_zip_query

    @cohort_count_by_zip_query.setter
    def cohort_count_by_zip_query(self, cohort_count_by_zip_query):
        """Sets the cohort_count_by_zip_query of this GeographicQueries.


        :param cohort_count_by_zip_query: The cohort_count_by_zip_query of this GeographicQueries.  # noqa: E501
        :type: str
        """

        self._cohort_count_by_zip_query = cohort_count_by_zip_query

    @property
    def cohort_count_by_state_query(self):
        """Gets the cohort_count_by_state_query of this GeographicQueries.  # noqa: E501


        :return: The cohort_count_by_state_query of this GeographicQueries.  # noqa: E501
        :rtype: str
        """
        return self._cohort_count_by_state_query

    @cohort_count_by_state_query.setter
    def cohort_count_by_state_query(self, cohort_count_by_state_query):
        """Sets the cohort_count_by_state_query of this GeographicQueries.


        :param cohort_count_by_state_query: The cohort_count_by_state_query of this GeographicQueries.  # noqa: E501
        :type: str
        """

        self._cohort_count_by_state_query = cohort_count_by_state_query

    @property
    def intervention_count_by_zip_query(self):
        """Gets the intervention_count_by_zip_query of this GeographicQueries.  # noqa: E501


        :return: The intervention_count_by_zip_query of this GeographicQueries.  # noqa: E501
        :rtype: str
        """
        return self._intervention_count_by_zip_query

    @intervention_count_by_zip_query.setter
    def intervention_count_by_zip_query(self, intervention_count_by_zip_query):
        """Sets the intervention_count_by_zip_query of this GeographicQueries.


        :param intervention_count_by_zip_query: The intervention_count_by_zip_query of this GeographicQueries.  # noqa: E501
        :type: str
        """

        self._intervention_count_by_zip_query = intervention_count_by_zip_query

    @property
    def intervention_count_by_state_query(self):
        """Gets the intervention_count_by_state_query of this GeographicQueries.  # noqa: E501


        :return: The intervention_count_by_state_query of this GeographicQueries.  # noqa: E501
        :rtype: str
        """
        return self._intervention_count_by_state_query

    @intervention_count_by_state_query.setter
    def intervention_count_by_state_query(self, intervention_count_by_state_query):
        """Sets the intervention_count_by_state_query of this GeographicQueries.


        :param intervention_count_by_state_query: The intervention_count_by_state_query of this GeographicQueries.  # noqa: E501
        :type: str
        """

        self._intervention_count_by_state_query = intervention_count_by_state_query

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
        if issubclass(GeographicQueries, dict):
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
        if not isinstance(other, GeographicQueries):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
