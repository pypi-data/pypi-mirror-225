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

class CreateOrganizationSettingDto(object):
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
        'models': 'object',
        'min_claim_date': 'datetime',
        'max_claim_date': 'datetime',
        'max_cohort_windows': 'float',
        'pipeline_version': 'str',
        'risk_version': 'str',
        'impactability_version': 'str',
        'primary_database': 'str',
        'features_database': 'str'
    }

    attribute_map = {
        'models': 'models',
        'min_claim_date': 'minClaimDate',
        'max_claim_date': 'maxClaimDate',
        'max_cohort_windows': 'maxCohortWindows',
        'pipeline_version': 'pipelineVersion',
        'risk_version': 'riskVersion',
        'impactability_version': 'impactabilityVersion',
        'primary_database': 'primaryDatabase',
        'features_database': 'featuresDatabase'
    }

    def __init__(self, models=None, min_claim_date=None, max_claim_date=None, max_cohort_windows=None, pipeline_version=None, risk_version=None, impactability_version=None, primary_database=None, features_database=None):  # noqa: E501
        """CreateOrganizationSettingDto - a model defined in Swagger"""  # noqa: E501
        self._models = None
        self._min_claim_date = None
        self._max_claim_date = None
        self._max_cohort_windows = None
        self._pipeline_version = None
        self._risk_version = None
        self._impactability_version = None
        self._primary_database = None
        self._features_database = None
        self.discriminator = None
        if models is not None:
            self.models = models
        if min_claim_date is not None:
            self.min_claim_date = min_claim_date
        if max_claim_date is not None:
            self.max_claim_date = max_claim_date
        self.max_cohort_windows = max_cohort_windows
        if pipeline_version is not None:
            self.pipeline_version = pipeline_version
        if risk_version is not None:
            self.risk_version = risk_version
        if impactability_version is not None:
            self.impactability_version = impactability_version
        if primary_database is not None:
            self.primary_database = primary_database
        if features_database is not None:
            self.features_database = features_database

    @property
    def models(self):
        """Gets the models of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The models of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: object
        """
        return self._models

    @models.setter
    def models(self, models):
        """Sets the models of this CreateOrganizationSettingDto.


        :param models: The models of this CreateOrganizationSettingDto.  # noqa: E501
        :type: object
        """

        self._models = models

    @property
    def min_claim_date(self):
        """Gets the min_claim_date of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The min_claim_date of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: datetime
        """
        return self._min_claim_date

    @min_claim_date.setter
    def min_claim_date(self, min_claim_date):
        """Sets the min_claim_date of this CreateOrganizationSettingDto.


        :param min_claim_date: The min_claim_date of this CreateOrganizationSettingDto.  # noqa: E501
        :type: datetime
        """

        self._min_claim_date = min_claim_date

    @property
    def max_claim_date(self):
        """Gets the max_claim_date of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The max_claim_date of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: datetime
        """
        return self._max_claim_date

    @max_claim_date.setter
    def max_claim_date(self, max_claim_date):
        """Sets the max_claim_date of this CreateOrganizationSettingDto.


        :param max_claim_date: The max_claim_date of this CreateOrganizationSettingDto.  # noqa: E501
        :type: datetime
        """

        self._max_claim_date = max_claim_date

    @property
    def max_cohort_windows(self):
        """Gets the max_cohort_windows of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The max_cohort_windows of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: float
        """
        return self._max_cohort_windows

    @max_cohort_windows.setter
    def max_cohort_windows(self, max_cohort_windows):
        """Sets the max_cohort_windows of this CreateOrganizationSettingDto.


        :param max_cohort_windows: The max_cohort_windows of this CreateOrganizationSettingDto.  # noqa: E501
        :type: float
        """
        if max_cohort_windows is None:
            raise ValueError("Invalid value for `max_cohort_windows`, must not be `None`")  # noqa: E501

        self._max_cohort_windows = max_cohort_windows

    @property
    def pipeline_version(self):
        """Gets the pipeline_version of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The pipeline_version of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_version

    @pipeline_version.setter
    def pipeline_version(self, pipeline_version):
        """Sets the pipeline_version of this CreateOrganizationSettingDto.


        :param pipeline_version: The pipeline_version of this CreateOrganizationSettingDto.  # noqa: E501
        :type: str
        """

        self._pipeline_version = pipeline_version

    @property
    def risk_version(self):
        """Gets the risk_version of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The risk_version of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: str
        """
        return self._risk_version

    @risk_version.setter
    def risk_version(self, risk_version):
        """Sets the risk_version of this CreateOrganizationSettingDto.


        :param risk_version: The risk_version of this CreateOrganizationSettingDto.  # noqa: E501
        :type: str
        """

        self._risk_version = risk_version

    @property
    def impactability_version(self):
        """Gets the impactability_version of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The impactability_version of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: str
        """
        return self._impactability_version

    @impactability_version.setter
    def impactability_version(self, impactability_version):
        """Sets the impactability_version of this CreateOrganizationSettingDto.


        :param impactability_version: The impactability_version of this CreateOrganizationSettingDto.  # noqa: E501
        :type: str
        """

        self._impactability_version = impactability_version

    @property
    def primary_database(self):
        """Gets the primary_database of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The primary_database of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: str
        """
        return self._primary_database

    @primary_database.setter
    def primary_database(self, primary_database):
        """Sets the primary_database of this CreateOrganizationSettingDto.


        :param primary_database: The primary_database of this CreateOrganizationSettingDto.  # noqa: E501
        :type: str
        """

        self._primary_database = primary_database

    @property
    def features_database(self):
        """Gets the features_database of this CreateOrganizationSettingDto.  # noqa: E501


        :return: The features_database of this CreateOrganizationSettingDto.  # noqa: E501
        :rtype: str
        """
        return self._features_database

    @features_database.setter
    def features_database(self, features_database):
        """Sets the features_database of this CreateOrganizationSettingDto.


        :param features_database: The features_database of this CreateOrganizationSettingDto.  # noqa: E501
        :type: str
        """

        self._features_database = features_database

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
        if issubclass(CreateOrganizationSettingDto, dict):
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
        if not isinstance(other, CreateOrganizationSettingDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
