from typing import Any, Dict, List, Optional


def ensure_patient_in_group(patient_key: str, group_externally_exposable_id: str) -> Dict[str, Any]:

    return {
        'integration_type': 'Group',
        'integration_source': 'SDK',
        'handling_options': {
            'respond_async': True
        },
        'integration_payload': {
            'externally_exposable_id': group_externally_exposable_id,
            'group_type': 'patientgroup',
            'members': {
                'mode': 'appendOrRemove',
                'entries': [{
                    'uuid': patient_key,
                }]
            }
        }
    }


def ensure_patient_not_in_group(patient_key: str, group_externally_exposable_id: str) -> Dict[str, Any]:

    return {
        'integration_type': 'Group',
        'integration_source': 'SDK',
        'handling_options': {
            'respond_async': True
        },
        'integration_payload': {
            'externally_exposable_id': group_externally_exposable_id,
            'group_type': 'patientgroup',
            'members': {
                'mode': 'appendOrRemove',
                'entries': [{
                    'uuid': patient_key,
                    'inactive': True
                }]
            }
        }
    }


def create_task_payload(patient_key: str,
                        created_by_key: str,
                        status: Optional[str] = "OPEN",
                        title: Optional[str] = None,
                        assignee_identifier: Optional[str] = None,
                        team_identifier: Optional[str] = None,
                        due: Optional[str] = None,
                        created: Optional[str] = None,
                        tag: Optional[str] = None,
                        labels: Optional[List[str]] = None) -> Dict[str, Any]:

    payload_properties = {
                                "title": title,
                                "team_identifier": team_identifier,
                                "created": created,
                                "due": due,
                                "tag": tag,
                                "labels": labels
                             }
    integration_payload = {
                            "creator": {
                                "identifier_type": "key",
                                "identifier": {
                                    "key": created_by_key
                                }
                            },
                            "status": status
                        }
    for prop, value in payload_properties.items():
        if value:
            integration_payload[prop] = value

    if assignee_identifier:
        integration_payload['assignee'] = {
                    'identifier_type': 'key',
                    'identifier': {
                        'key': assignee_identifier
                    }
                }
    return {
            "integration_type": "Task",
            "integration_source": "SDK",
            "handling_options": {
                "respond_async": True
                },
            "patient_identifier": {
                "identifier_type": "key",
                "identifier": {
                    "key": patient_key
                    }
                },
            "integration_payload": integration_payload
            }
