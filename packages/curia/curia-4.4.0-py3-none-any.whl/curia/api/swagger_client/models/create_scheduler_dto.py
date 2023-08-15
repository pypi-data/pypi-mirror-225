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

class CreateSchedulerDto(object):
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
        'type': 'str',
        'workflow_id': 'str',
        'schedule': 'str',
        'parameters': 'WorkflowTemplateParameters',
        'job_key': 'str',
        'last_run_at': 'datetime',
        'next_run_at': 'datetime',
        'is_paused': 'object'
    }

    attribute_map = {
        'type': 'type',
        'workflow_id': 'workflowId',
        'schedule': 'schedule',
        'parameters': 'parameters',
        'job_key': 'jobKey',
        'last_run_at': 'lastRunAt',
        'next_run_at': 'nextRunAt',
        'is_paused': 'isPaused'
    }

    def __init__(self, type=None, workflow_id=None, schedule=None, parameters=None, job_key=None, last_run_at=None, next_run_at=None, is_paused=None):  # noqa: E501
        """CreateSchedulerDto - a model defined in Swagger"""  # noqa: E501
        self._type = None
        self._workflow_id = None
        self._schedule = None
        self._parameters = None
        self._job_key = None
        self._last_run_at = None
        self._next_run_at = None
        self._is_paused = None
        self.discriminator = None
        self.type = type
        self.workflow_id = workflow_id
        self.schedule = schedule
        if parameters is not None:
            self.parameters = parameters
        if job_key is not None:
            self.job_key = job_key
        if last_run_at is not None:
            self.last_run_at = last_run_at
        if next_run_at is not None:
            self.next_run_at = next_run_at
        self.is_paused = is_paused

    @property
    def type(self):
        """Gets the type of this CreateSchedulerDto.  # noqa: E501


        :return: The type of this CreateSchedulerDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateSchedulerDto.


        :param type: The type of this CreateSchedulerDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["Cron", "OneTime"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def workflow_id(self):
        """Gets the workflow_id of this CreateSchedulerDto.  # noqa: E501


        :return: The workflow_id of this CreateSchedulerDto.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this CreateSchedulerDto.


        :param workflow_id: The workflow_id of this CreateSchedulerDto.  # noqa: E501
        :type: str
        """
        if workflow_id is None:
            raise ValueError("Invalid value for `workflow_id`, must not be `None`")  # noqa: E501

        self._workflow_id = workflow_id

    @property
    def schedule(self):
        """Gets the schedule of this CreateSchedulerDto.  # noqa: E501


        :return: The schedule of this CreateSchedulerDto.  # noqa: E501
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this CreateSchedulerDto.


        :param schedule: The schedule of this CreateSchedulerDto.  # noqa: E501
        :type: str
        """
        if schedule is None:
            raise ValueError("Invalid value for `schedule`, must not be `None`")  # noqa: E501

        self._schedule = schedule

    @property
    def parameters(self):
        """Gets the parameters of this CreateSchedulerDto.  # noqa: E501


        :return: The parameters of this CreateSchedulerDto.  # noqa: E501
        :rtype: WorkflowTemplateParameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this CreateSchedulerDto.


        :param parameters: The parameters of this CreateSchedulerDto.  # noqa: E501
        :type: WorkflowTemplateParameters
        """

        self._parameters = parameters

    @property
    def job_key(self):
        """Gets the job_key of this CreateSchedulerDto.  # noqa: E501


        :return: The job_key of this CreateSchedulerDto.  # noqa: E501
        :rtype: str
        """
        return self._job_key

    @job_key.setter
    def job_key(self, job_key):
        """Sets the job_key of this CreateSchedulerDto.


        :param job_key: The job_key of this CreateSchedulerDto.  # noqa: E501
        :type: str
        """

        self._job_key = job_key

    @property
    def last_run_at(self):
        """Gets the last_run_at of this CreateSchedulerDto.  # noqa: E501


        :return: The last_run_at of this CreateSchedulerDto.  # noqa: E501
        :rtype: datetime
        """
        return self._last_run_at

    @last_run_at.setter
    def last_run_at(self, last_run_at):
        """Sets the last_run_at of this CreateSchedulerDto.


        :param last_run_at: The last_run_at of this CreateSchedulerDto.  # noqa: E501
        :type: datetime
        """

        self._last_run_at = last_run_at

    @property
    def next_run_at(self):
        """Gets the next_run_at of this CreateSchedulerDto.  # noqa: E501


        :return: The next_run_at of this CreateSchedulerDto.  # noqa: E501
        :rtype: datetime
        """
        return self._next_run_at

    @next_run_at.setter
    def next_run_at(self, next_run_at):
        """Sets the next_run_at of this CreateSchedulerDto.


        :param next_run_at: The next_run_at of this CreateSchedulerDto.  # noqa: E501
        :type: datetime
        """

        self._next_run_at = next_run_at

    @property
    def is_paused(self):
        """Gets the is_paused of this CreateSchedulerDto.  # noqa: E501


        :return: The is_paused of this CreateSchedulerDto.  # noqa: E501
        :rtype: object
        """
        return self._is_paused

    @is_paused.setter
    def is_paused(self, is_paused):
        """Sets the is_paused of this CreateSchedulerDto.


        :param is_paused: The is_paused of this CreateSchedulerDto.  # noqa: E501
        :type: object
        """
        if is_paused is None:
            raise ValueError("Invalid value for `is_paused`, must not be `None`")  # noqa: E501

        self._is_paused = is_paused

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
        if issubclass(CreateSchedulerDto, dict):
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
        if not isinstance(other, CreateSchedulerDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
