#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: opsgenielib.py
#
# Copyright 2023 Yorick Hoorneman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for opsgenielib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import json
import logging
import urllib.parse
from datetime import datetime, timedelta

import pytz
from requests import Session

from opsgenielib.opsgenielibexceptions import InvalidApiKey, NoAlertPolicyFound

__author__ = '''Yorick Hoorneman <yhoorneman@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''21-03-2023'''
__copyright__ = '''Copyright 2023, Yorick Hoorneman'''
__credits__ = ["Yorick Hoorneman"]
__license__ = '''MIT'''
__maintainer__ = '''Yorick Hoorneman'''
__email__ = '''<yhoorneman@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''opsgenielib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Team:
    """Models the team."""

    def __init__(self, server, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._server = server
        self._data = data

    @property
    def id(self):  # pylint: disable=invalid-name, missing-docstring
        return self._data.get('data', {}).get('id', {})

    @property
    def description(self):  # pylint: disable=missing-docstring
        return self._data.get('data', {}).get('description', {})

    @property
    def name(self):  # pylint: disable=missing-docstring
        return self._data.get('data', {}).get('name', {})

    @property
    def members(self):  # pylint: disable=missing-docstring
        return self._data.get('data', {}).get('members', {})

    def __str__(self):
        return (f'Team name: {self.name}\n'
                f'ID: {self.id}\n'
                f'Description: {self.description}\n\n')

    def serialize(self):  # pylint: disable=missing-docstring
        return json.dumps(self._data)

    @property
    def integrations(self):
        """Listing integration based on teamnames. Returns the json."""
        url = f'{self._server._base_url}/v2/integrations?teamName={self.name}'  # pylint: disable=protected-access
        self._logger.debug('Making a call to "%s"', url)
        response = self._server._session.get(url)  # pylint: disable=protected-access
        if not response.ok:
            self._logger.error('Request failed %s', response.status_code)
            response.raise_for_status()
        return [Integration(self, integration) for integration in response.json().get('data', {})]

class Policy:

    def __init__(self, server, data):
        self._server = server
        self._data = data

    @property
    def id(self):  # pylint: disable=invalid-name, missing-docstring
        return self._data.get('id')

class AlertPolicy(Policy):
    """Models the Alert Policy."""

    def __init__(self, server, data):
        super().__init__(server, data)
    
    @property
    def continue_after(self):  # pylint: disable=invalid-name, missing-docstring
        return self._data.get('continue')

    @property
    def name(self):  # pylint: disable=missing-docstring
        return self._data.get('name')

    @property
    def type(self):  # pylint: disable=missing-docstring
        return self._data.get('type')

    @property
    def order(self):  # pylint: disable=missing-docstring
        return self._data.get('order')
    
    @property
    def enabled(self):  # pylint: disable=missing-docstring
        return self._data.get('enabled')
    
    @property
    def policy_description(self):  # pylint: disable=missing-docstring
        return self._data.get('policyDescription')

    @property
    def tags(self):  # pylint: disable=missing-docstring
        return self._data.get('tags')
    
    @property
    def responders(self):  # pylint: disable=missing-docstring
        return self._data.get('responders')

    @property
    def filter(self):  # pylint: disable=missing-docstring
        return self._data.get('policyDescription')
    
    @property
    def actions(self):  # pylint: disable=missing-docstring
        return self._data.get('actions')
    
    @property
    def details(self):  # pylint: disable=missing-docstring
        return self._data.get('details')
    
class MaintenancePolicy(Policy):
    """Models the Maintenance Policy."""

    def __init__(self, server, data):
        super().__init__(server, data)

    @property
    def status(self):  # pylint: disable=missing-docstring
        return self._data.get('status')

    @property
    def description(self):  # pylint: disable=missing-docstring
        return self._data.get('description')
    
    @property
    def time(self):  # pylint: disable=missing-docstring
        return self._data.get('time')

class Integration:
    """Models the integration."""

    def __init__(self, server, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._server = server
        self._data = data

    @property
    def id(self):  # pylint: disable=invalid-name, missing-docstring
        return self._data.get('id')

    @property
    def type(self):  # pylint: disable=missing-docstring
        return self._data.get('type')

    @property
    def name(self):  # pylint: disable=missing-docstring
        return self._data.get('name')

    @property
    def team_id(self):  # pylint: disable=missing-docstring
        return self._data.get('teamId')

    @property
    def enabled(self):  # pylint: disable=missing-docstring
        return self._data.get('enabled')

    def __str__(self):
        return (f'ID: {self.id}\n'
                f'Type: {self.type}\n'
                f'Name: {self.name}\n'
                f'Team ID: {self.team_id}\n'
                f'Enabled: {self.enabled}\n\n')

    def serialize(self):  # pylint: disable=missing-docstring
        return json.dumps(self._data)

class Heartbeat:

    def __init__(self, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self.parse_data = self._parse_data(data)
        self._data = self.parse_data

    def _parse_data(self, data):
        if not isinstance(data, dict):
            self._logger.error(f'Invalid data received: {data}')
            data = {}
        return data

    @property
    def name(self):
        return self._data.get('name')

    @property
    def description(self):
        return self._data.get('description')
    
    @property
    def interval(self):
        return self._data.get('interval')
    
    @property
    def enabled(self):
        return self._data.get('enabled')
    
    @property
    def intervalUnit(self):
        return self._data.get('intervalUnit')

    @property
    def intervalUnit(self):
        return self._data.get('intervalUnit')

    @property
    def expired(self):
        return self._data.get('expired')

    @property
    def ownerTeam(self):
        return self._data.get('ownerTeam')

    @property
    def lastPingTime(self):
        return self._data.get('lastPingTime')
    
    @property
    def alertMessage(self):
        return self._data.get('alertMessage')

    @property
    def alertTags(self):
        return self._data.get('alertTags')
    
    @property
    def alertPriority(self):
        return self._data.get('alertPriority')

class User:

    def __init__(self, opsgenie_instance, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self.opsgenie_instance = opsgenie_instance
        self.parse_data = self._parse_data(data)
        self._data = self.parse_data
        self._teams = None
        self._notification_rules = None
        self._contacts = None

    def _parse_data(self, data):
        if not isinstance(data, dict):
            self._logger.error(f'Invalid data received: {data}')
            data = {}
        return data

    @property
    def id(self):
        return self._data.get('id')
    
    @property
    def blocked(self):
        return self._data.get('blocked')

    @property
    def verified(self):
        return self._data.get('verified')
    
    @property
    def username(self):
        return self._data.get('username')
    
    @property
    def full_name(self):
        return self._data.get('fullName')

    @property
    def role(self):
        return self._data.get('role')

    @property
    def created_at(self):
        return self._data.get('createdAt')
    
    @property
    def user_contacts(self):
        return self._data.get('userContacts')

    @property
    def teams(self):
        if not self._teams:
            response = self.opsgenie_instance.get_user_teams(self.username)
            self._teams = response.json().get('data', {})
        return self._teams

    @property
    def notification_rules(self):
        if not self._notification_rules:
            response = self.opsgenie_instance.get_user_notification_rules(self.username)
            self._notification_rules = response.json().get('data', {})
        return [NotificationRule(self.opsgenie_instance, self.username, notification_rule) for notification_rule in self._notification_rules if notification_rule]

    @property
    def contacts(self):
        if not self._contacts:
            response = self.opsgenie_instance.get_user_contacts(self.username)
            self._contacts = response.json().get('data', {})
        return [Contacts(self.opsgenie_instance, contact_method) for contact_method in self._contacts]

class Contacts:

    def __init__(self, opsgenie_instance, data) -> None:
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self.opsgenie_instance = opsgenie_instance
        self.parse_data = self._parse_data(data)
        self._data = self.parse_data

    def _parse_data(self, data):
        if not isinstance(data, dict):
            self._logger.error(f'Invalid data received: {data}')
            data = {}
        return data
    
    @property
    def id(self):
        return self._data.get('id')

    @property
    def method(self):
        return self._data.get('method')

    @property
    def to(self):
        return self._data.get('to')
    
    @property
    def status(self):
        return self._data.get('status', {}).get('enabled')
    
    @property
    def applyOrder(self):
        return self._data.get('applyOrder')


class NotificationRule:

    def __init__(self, opsgenie_instance, username, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self.opsgenie_instance = opsgenie_instance
        self.username = username
        self.parse_data = self._parse_data(data)
        self._data = self.parse_data
        self._notification_steps = None

    def _parse_data(self, data):
        if not isinstance(data, dict):
            self._logger.error(f'Invalid data received: {data}')
            data = {}
        return data
    
    @property
    def id(self):
        return self._data.get('id')
    
    @property
    def name(self):
        return self._data.get('name')

    @property
    def action_type(self):
        return self._data.get('actionType')
    
    @property
    def order(self):
        return self._data.get('order')
    
    @property
    def notification_time(self):
        return self._data.get('notificationTime')

    @property
    def steps(self):
        return self._data.get('steps')

    @property
    def enabled(self):
        return self._data.get('enabled')
    
    def _get_notification_steps(self):
        if not self._notification_steps:
            response = self.opsgenie_instance.get_user_notification_rule_steps(self.username, self.id)
            self._notification_steps = response.json().get('data', {})
        return [NotificationRuleStep(self.opsgenie_instance, notification_rule) for notification_rule in self._notification_steps if notification_rule]

    @property
    def notification_steps(self):
        return self._get_notification_steps()


class NotificationRuleStep:

    def __init__(self, opsgenie_instance, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self.opsgenie_instance = opsgenie_instance
        self.parse_data = data
        self._data = self.parse_data
        self._notification_rule_steps = None

    def _parse_data(self, data):
        if not isinstance(data, dict):
            self._logger.error(f'Invalid data received: {data}')
            data = {}
        return data
    
    @property
    def parent(self):
        return self._data.get('_parent', {})
    
    @property
    def id(self):
        return self._data.get('id')

    @property
    def send_after(self):
        return self._data.get('sendAfter')

    @property
    def contact(self):
        return self._data.get('contact')

    @property
    def enabled(self):
        return self._data.get('enabled')    


class Opsgenie:  # pylint: disable=too-many-public-methods, too-many-instance-attributes
    """Main code for the library.

    Functions are based on the endpoints defined in the docs:
        https://docs.opsgenie.com/docs/api-overview
    """

    def __init__(self, api_key, url='https://api.opsgenie.com'):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._base_url = url
        self._session = self._authenticate(api_key)
        self._maintenance_url = f'{self._base_url}/v1/maintenance'
        self._heartbeats_url = f'{self._base_url}/v2/heartbeats'
        self._alerts_url = f'{self._base_url}/v2/alerts'
        self._policies_url = f'{self._base_url}/v2/policies'
        self._integrations_url = f'{self._base_url}/v2/integrations'
        self._teams_url = f'{self._base_url}/v2/teams'
        self._escalations_url = f'{self._base_url}/v2/escalations'
        self._schedules_url = f'{self._base_url}/v2/schedules'
        self._logs_url = f'{self._base_url}/v2/logs'
        self._users_url = f'{self._base_url}/v2/users'

    def _authenticate(self, api_key):
        session = Session()
        session.headers.update({'Authorization': f'GenieKey {api_key}',
                                'Content-Type': 'application/json'})
        url = f'{self._base_url}/v1/maintenance'
        response = session.get(url)
        if not response.ok:
            raise InvalidApiKey(response.text)
        return session

    def get_maintenance(self, id_):
        """Returns the json of a maintenance policy. The id of policy is required.

        Args:
            id_: The Id of the maintenance policy

        Returns:
            All attributes are under 'Data'.

        """
        url = f'{self._maintenance_url}/{id_}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def delete_maintenance(self, maintenance_id):
        """Deletes a maintenance policy. Returns the json The id of policy is required."""
        for id_ in maintenance_id:
            url = f'{self._maintenance_url}/{id_}'
            self._logger.debug('Making a call to "%s"', url)
            response = self._session.delete(url)
            response.raise_for_status()
        return response

    def set_maintenance_schedule(self,  # pylint: disable=too-many-arguments
                                 team_id,
                                 start_date,
                                 end_date,
                                 rules_type,
                                 description,
                                 state,
                                 rules_id):
        """Creation of a maintenance policy for a specified schedule. Returns the json."""
        url = f'{self._base_url}/v1/maintenance'
        payload = {
            "teamId": team_id,
            "description": description,
            "time": {
                "type": "schedule",
                "startDate": start_date,
                "endDate": end_date
            },
            "rules": [
                {
                    "state": state,
                    "entity": {
                        "id": rules_id,
                        "type": rules_type
                    }
                }
            ]
        }
        all_rules = []
        for id_ in rules_id:
            entry = {'entity': {'id': id_, 'type': f'{rules_type}'}, 'state': f'{state}'}
            all_rules.append(entry)
        payload['rules'] = all_rules
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Request failed %s', response.status_code)
            response.raise_for_status()
        return response

    def set_maintenance_hours_by_name(self,  # pylint: disable=too-many-arguments, too-many-locals
                              team_id,
                              hours,
                              rule_type,
                              description,
                              state,
                              policy_name):
        policy = self.get_alert_policy_by_name(policy_name, team_id)
        return self.set_maintenance_hours(team_id, hours, rule_type, description, state, policy.id)

    def set_maintenance_hours(self,  # pylint: disable=too-many-arguments, too-many-locals
                              team_id,
                              hours,
                              rules_type,
                              description,
                              state,
                              rules_id):
        """Creation of a maintenance policy for a X amount of hours from now. Returns the json."""
        utc_start_time = datetime.now().astimezone(pytz.utc)
        utc_end_date = utc_start_time + timedelta(hours=hours)
        start_date = utc_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_date = utc_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        url = f'{self._base_url}/v1/maintenance'
        payload = {
            "teamId": f"{team_id}",
            "description": f"{description}",
            "time": {
                "type": "schedule",
                "startDate": f"{start_date}",
                "endDate": f"{end_date}"
            },
            "rules": [
                {
                    "state": f"{state}",
                    "entity": {
                        "id": f"{rules_id}",
                        "type": f"{rules_type}"
                    }
                }
            ]
        }
        if isinstance(rules_id, (tuple, list)):
            all_rules = []
            for id_ in rules_id:
                entry = {'entity': {'id': id_, 'type': f'{rules_type}'}, 'state': f'{state}'}
                all_rules.append(entry)
            payload['rules'] = all_rules
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        return MaintenancePolicy(self, response.json().get('data', {}))

    def list_maintenance(self, non_expired=False, past=False):
        """Listing maintenance policies. Returns the json."""
        params = []
        if non_expired:
            params.append(('type', 'non-expired'))
        if past:
            params.append(('type', 'past'))
        url = f'{self._maintenance_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return [MaintenancePolicy(self, policy) for policy in response.json().get('data', {})]

    def cancel_maintenance(self, maintenance_id):
        """Cancel a maintenance policy. ID of the maintenance policy is mandatory."""
        url = f"{self._maintenance_url}/{maintenance_id}/cancel"
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url)
        response.raise_for_status()
        return response.json()

    def count_alerts_by_query(self, query):
        """Counting alerts based on a search query. Example: alerts query --query "teams=project9"."""
        search_query = urllib.parse.quote_plus(query)
        url = f'{self._alerts_url}/count?query={search_query}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def create_alert(self, message, alias='', description='', responders=[], visible_to=[], actions=[], tags=[], details={}, entity='', priority=None):
        payload = {
                    "message": message,
                    "alias": alias,
                    "description": description,
                    "responders": responders,
                    "visibleTo": visible_to,
                    "actions": actions,
                    "tags": tags,
                    "details": details,
                    "entity": entity,
                    "priority": priority
                }
        url = self._alerts_url
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_alert_by_id(self, id_):
        """Returns json of a specified alert. The id of an alert is required."""
        url = f'{self._alerts_url}/{id_}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def acknowledge_alerts(self, id_):
        """POST request to acknowledge an alert."""
        url = f'{self._alerts_url}/{id_}/acknowledge'
        self._logger.debug('Making a call to "%s"', url)
        payload = '{}'
        response = self._session.post(url, data=payload)
        response.raise_for_status()
        return response.json()

    def list_alerts_by_team(self, team_name, limit):
        """Listing x amount of alerts. The name of the team and the limit of alerts are required."""
        url = f'{self._alerts_url}?limit={limit}&query=teams:{team_name}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def list_users(self, limit=100):
        """Listing users in Opsgenie."""
        url = f'{self._users_url}?limit={limit}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        results = response.json().get('data', {})
        while "next" in response.json()['paging']:
            url = response.json()['paging']['next']
            self._logger.debug('Making a call to "%s"', url)
            response = self._session.get(url)
            results += response.json().get('data', {})
        return [User(self, user) for user in results if user]

    def query_alerts(self, query, limit=2000):
        """Listing alerts based on a search query. Example: alerts query --query "teams=project9"."""
        search_query = urllib.parse.quote_plus(query)
        url = f'{self._alerts_url}?limit=100&query={search_query}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        results = response.json()['data']
        if not response.json()['data']:
            return results
        while "next" in response.json()['paging']:
            if limit == 0 or not len(results) >= limit:
                url = response.json()['paging']['next']
                self._logger.debug('Making a call to "%s"', url)
                response = self._session.get(url)
                results += response.json()['data']
            else:
                break
        return results

    def close_alerts(self, id_):
        """Closing alerts based on a provided ID."""
        url = f'{self._alerts_url}/{id_}/close'
        payload = {}
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def delete_alert_policy(self, alert_id, team_id):
        """POST request to delete an alert policy. The id of the policy is required."""
        for id_ in alert_id:
            url = f'{self._policies_url}/{id_}?teamId={team_id}'
            self._logger.debug('Making a call to "%s"', url)
            response = self._session.delete(url)
            response.raise_for_status()
        return response.json()

    def create_alert_policy(self, name, filter_condition, policy_description, team_id, enabled=False):  # pylint: disable=too-many-arguments
        """POST request to create an alert policy with simplified logic."""
        payload = {
            "type": "alert",
            "name": f"{name}",
            "enabled": f"{enabled}",
            "description": f"{policy_description}",
            "filter": {
                "type": "match-any-condition",
                "conditions": [
                    {
                        "field": "description",
                        "operation": "matches",
                        "expectedValue": f"{filter_condition}"
                    },
                    {
                        "field": "extra-properties",
                        "key": "host",
                        "operation": "matches",
                        "expectedValue": f"{filter_condition}"
                    }
                ]
            },
            "message": "{{message}}",
            "tags": ["Filtered"]
        }
        url = f'{self._policies_url}/?teamId={team_id}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_alert_policy(self, id_, team_id):
        """Returns the json of an alert policy. The id of policy is required."""
        url = f'{self._policies_url}/{id_}'
        parameters = {'teamId': team_id}
        self._logger.debug('Making a call to "%s", with parameters "%s"', url, parameters)
        response = self._session.get(url, params=parameters)
        response.raise_for_status()
        return AlertPolicy(self, response.json().get('data', {}))
        
    def get_alert_policy_by_name(self, policy_name, team_id):
        alert_policy = [policy for policy in self.list_alert_policy(team_id) if policy.name.lower() == policy_name.lower()]
        if not alert_policy:
            raise NoAlertPolicyFound
        return next(iter(alert_policy))

    def list_alert_policy(self, team_id):
        """Listing all alert policies. Specify the team id."""
        url = f'{self._policies_url}/alert?teamId={team_id}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return [AlertPolicy(self, policy) for policy in response.json().get('data', {})]

    def list_integrations_by_team_name(self, team_name):
        """Listing integration based on teamnames. Returns the json."""
        url = f'{self._integrations_url}?teamName={team_name}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def list_integrations_by_team_id(self, team_id):
        """Listing integrations based on team id. Returns the json."""
        url = f'{self._integrations_url}?teamId={team_id}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def list_integrations(self):
        """Listing integrations for all teams (if the api key used has permissions). Returns the json."""
        url = f'{self._integrations_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    @property
    def integrations(self):
        """Listing all integrations."""
        url = f'{self._integrations_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return [Integration(self, data) for data in response.json().get('data')]

    def get_integration_actions(self, id_):
        """Get information about the actions (create/close/acknowledge) side of the integration."""
        url = f'{self._integrations_url}/{id_}/actions'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def create_integration_action(self, id_, type_, name, alias, order, user, filter_condition_match_type, filter_conditions, source, message, description, entity, tags, extra_properties, responders=None, note=''):
        """Create an alert action (create/close/acknowledge) for an existing integration."""
        url = f'{self._integrations_url}/{id_}/actions'
        payload = {
            "type": type_,
            "name": name,
            "order": order,
            "filter": {
                "conditionMatchType": filter_condition_match_type,
                "conditions": filter_conditions
            },
            "user": user,
            "note": note,
            "alias": alias,
            "source": source,
            "message": message,
            "description": description,
            "entity": entity,
            "appendAttachments": True,
            "alertActions": [],
            "ignoreAlertActionsFromPayload": False,
            "ignoreRespondersFromPayload": False,
            "ignoreTeamsFromPayload": False,
            "tags": tags,
            "ignoreTagsFromPayload": False,
            "extraProperties": extra_properties,
            "ignoreExtraPropertiesFromPayload": False
        }
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        return response.json()

    def get_integration_by_id(self, id_):
        """Get information about an integration based on the ID of the integration."""
        url = f'{self._integrations_url}/{id_}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def create_heartbeat(self, name, description, interval_unit, interval, alert_message, alert_priority, alert_tags, owner_team, enabled=True):
        """Add Heartbeat request is used to define heartbeats in Opsgenie.."""
        if interval_unit not in ["minutes", "hours", "days"]:
            return False
        url = self._heartbeats_url
        payload = {
            "name" : name,
            "description": description,
            "intervalUnit" : interval_unit,
            "interval" : interval,
            "enabled" : enabled,
            "ownerTeam": {
                "name": owner_team
            },
            "alertMessage": alert_message,
            "alertPriority": alert_priority,
            "alertTags": [alert_tags]
        }
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        return response.json()

    def ping_heartbeat(self, heart_beat_name):
        """Ping a heartbeat integration."""
        url = f'{self._heartbeats_url}/{heart_beat_name}/ping'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url)
        response.raise_for_status()
        return response.json()

    def get_heartbeat(self, heart_beat_name):
        """Get information about a heartbeat integration."""
        url = f'{self._heartbeats_url}/{heart_beat_name}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return Heartbeat(response.json().get('data',{}))

    def list_heartbeats(self):
        """Listing all heartbeat integrations (results based on the permissions of the api key)."""
        url = f'{self._heartbeats_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return [Heartbeat(heartbeat) for heartbeat in response.json().get('data',{}).get('heartbeats')]

    def enable_heartbeat(self, heart_beat_name):
        """Enable a heartbeat integration."""
        url = f'{self._heartbeats_url}/{heart_beat_name}/enable'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url)
        response.raise_for_status()
        return response.json()

    def disable_heartbeat(self, heart_beat_name):
        """Disable a heartbeat integration."""
        url = f'{self._heartbeats_url}/{heart_beat_name}/disable'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url)
        response.raise_for_status()
        return response.json()

    def get_team_by_id(self, id_):
        """Get information about a team based on team id."""
        url = f'{self._teams_url}/{id_}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return Team(self, response.json())

    def get_team_by_name(self, team_name):
        """Get information about a team based on teamname."""
        url = f'{self._teams_url}/{team_name}?identifierType=name'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return Team(self, response.json())

    def list_teams(self):
        """Listing all team names and their ID's."""
        url = f'{self._teams_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return [Team(self, data) for data in response.json().get('data')]

    def get_team(self, team_name):
        """Getting Opsgenie team based on team name."""
        url = f'{self._teams_url}/TeamName?identifierType={team_name}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return [Team(self, data) for data in response.json().get('data')]

    def get_team_logs_by_id(self, id_):
        """Get the log of changes made within the opsgenie team, based on team id."""
        url = f'{self._teams_url}/{id_}/logs?order=desc'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_team_logs_by_name(self, team_name):
        """Get the log of changes made within the opsgenie team, based on teamname."""
        url = f'{self._teams_url}/{team_name}/logs?identifierType=name&order=desc'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    @property
    def teams(self):
        """Listing all teams."""
        url = f'{self._teams_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return [Team(self, data) for data in response.json().get('data')]

    def get_routing_rules_by_id(self, id_):
        """Get the routing rules for an opsgenie team, based on team id."""
        url = f'{self._teams_url}/{id_}/routing-rules'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_routing_rules_by_name(self, team_name):
        """Get the routing rules for an opsgenie team, based on teamname."""
        url = f'{self._teams_url}/{team_name}/routing-rules?teamIdentifierType=name'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_escalations_by_id(self, id_):
        """Get the escalations schema for an opsgenie team, based on team id."""
        url = f'{self._escalations_url}/{id_}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_escalations_by_name(self, team_name):
        """Get the escalations schema for an opsgenie team, based on teamname."""
        url = f'{self._escalations_url}/{team_name}?identifierType=name'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def list_escalations(self):
        """Listing all escalations schedules."""
        url = f'{self._escalations_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_schedules_by_id(self, id_):
        """Get the on-call schedules for an opsgenie team, based on team id."""
        url = f'{self._schedules_url}/{id_}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_schedules_by_name(self, team_name):
        """Get the on-call schedules for an opsgenie team, based on teamname."""
        url = f'{self._schedules_url}/{team_name}?identifierType=name'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def list_schedules(self):
        """Listing all on-call schedules (results based on the permissions of the api key)."""
        url = f'{self._schedules_url}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def list_schedule_timeline_by_team_name(self, team_name, expand="base", interval=1, interval_unit="days"):
        """Listing the timeline of on-call users for a schedule."""
        url = f'{self._schedules_url}/{team_name}/timeline?identifierType=name'
        parameters = {'expand': expand}
        parameters.update({'interval': interval})
        parameters.update({'intervalUnit': interval_unit})
        self._logger.debug('Making a call to "%s", with parameters "%s"', url, parameters)
        response = self._session.get(url, params=parameters)
        response.raise_for_status()
        return response.json()

    def enable_policy(self, policy_id, team_id):
        """Enabling the alert or notification policy, based on the id of the policy."""
        for id_ in policy_id:
            url = f'{self._policies_url}/{id_}/enable'
            parameters = {'teamId': team_id}
            self._logger.debug('Making a call to "%s", with parameters "%s"', url, parameters)
            response = self._session.post(url, params=parameters)
            response.raise_for_status()
        return response.json()

    def disable_policy(self, policy_id, team_id):
        """Disabling the alert or notification policy, based on the id of the policy."""
        for id_ in policy_id:
            url = f'{self._policies_url}/{id_}/disable'
            parameters = {'teamId': team_id}
            self._logger.debug('Making a call to "%s", with parameters "%s"', url, parameters)
            response = self._session.post(url, params=parameters)
            response.raise_for_status()
        return response.json()

    def get_notification_policy(self, id_, team_id):
        """Returns the json of a notification policy. The id of policy is required."""
        url = f'{self._policies_url}/{id_}'
        parameters = {'teamId': team_id}
        self._logger.debug('Making a call to "%s", with parameters "%s"', url, parameters)
        response = self._session.get(url, params=parameters)
        response.raise_for_status()
        return response.json()

    def delete_notification_policy(self, notification_id, team_id):
        """POST request to delete a notification policy. Returns the json The id of policy is required."""
        for id_ in notification_id:
            url = f'{self._policies_url}/{id_}?teamId={team_id}'
            self._logger.debug('Making a call to "%s"', url)
            response = self._session.delete(url)
            response.raise_for_status()
        return response

    def list_notification_policy(self, team_id):
        """Listing all notification policies. Specify the team id."""
        url = f'{self._policies_url}/notification?teamId={team_id}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_users_on_call(self):
        """Returns the teams including the user who is on-call (results based on the permissions of the api key)."""
        url = f'{self._schedules_url}/on-calls'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_logs_filenames(self, marker, limit):
        """
        Returns the list of log files available for download.

        To fetch all the log files, get the marker in response and
        use it in the next request until the data field in response is empty.
        """
        url = f'{self._logs_url}/list/{marker}?limit={limit}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_logs_download_link(self, file_name):
        """Generate a link that is valid for 5 minutes to download a given log file."""
        url = f'{self._logs_url}/download/{file_name}'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def set_override_for_hours(self, team_name, user, hours):
        """
        Overrides the on-call user of an opsgenie team, based on the team id.

        Note: Start and End date format example: 2019-03-15T14:34:09Z.
        opsgenie uses UTC, time entered might be different.
        """
        utc_start_time = datetime.now().astimezone(pytz.utc)
        utc_end_date = utc_start_time + timedelta(hours=hours)
        start_date = utc_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_date = utc_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        url = f'{self._schedules_url}/{team_name}/overrides?scheduleIdentifierType=name'
        payload = {
            "user": {
                "type": "user",
                "username": f"{user}"
            },
            "startDate": f"{start_date}",
            "endDate": f"{end_date}"
        }
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        return response

    def set_override_scheduled(self, team_name, start_date, end_date, user):
        """
        Overrides the on-call user of an opsgenie team, based on the team name.

        Note: Start and End date format example: 2019-03-15T14:34:09Z.
        opsgenie uses UTC, time entered might be different.
        """
        url = f'{self._schedules_url}/{team_name}/overrides?scheduleIdentifierType=name'
        payload = {
            "user": {
                "type": "user",
                "username": f"{user}"
            },
            "startDate": f"{start_date}",
            "endDate": f"{end_date}"
        }
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        return response

    def get_user_contacts(self, username):
        url = f'https://api.opsgenie.com/v2/users/{username}/contacts'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response
    
    def get_user_teams(self, username):
        url = f'https://api.opsgenie.com/v2/users/{username}/teams'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response

    def partial_update_contact(self, username, contact_id, method, value, status=True):
        url = f"https://api.opsgenie.com/v2/users/{username}/contacts/{contact_id}"
        self._logger.debug('Making a call to "%s"', url)
        data = {
            "method": method,
            "to": value,
            "status": {
                "enabled": status
            }
        }
        response = self._session.patch(url, data=data)
        response.raise_for_status()
        return response
    
    def create_user_contact(self, username, method, value, status=True):
        url = f"https://api.opsgenie.com/v2/users/{username}/contacts"
        self._logger.debug('Making a call to "%s"', url)
        data = {
            "method": method,
            "to": value
        }
        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response

    def get_user_notification_rules(self, username):
        url = f'https://api.opsgenie.com/v2/users/{username}/notification-rules'
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response

    def get_user_notification_rule_steps(self, username, rule_id):
        url = f"https://api.opsgenie.com/v2/users/{username}/notification-rules/{rule_id}/steps"
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response

    def get_user_notification_rule_step(self, username, rule_id, step_id):
        url = f"https://api.opsgenie.com/v2/users/{username}/notification-rules/{rule_id}/steps/{step_id}"
        self._logger.debug('Making a call to "%s"', url)
        response = self._session.get(url)
        response.raise_for_status()
        return response