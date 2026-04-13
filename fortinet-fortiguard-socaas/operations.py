"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import json
from .forticloud_auth import SOCaaS, check
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('fortinet-fortiguard-socaas')

def get_alert_list(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/alert"
    return co.make_rest_call(endpoint, 'GET')

def get_alert_uuid(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/alert/" + params.get('alertuuid')
    return co.make_rest_call(endpoint, 'GET')

def update_alert_status(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/alert/" + params.get('alertuuid')
    param_data = {
        "status": params.get('status')
    }
    if params.get('closure_notes') is not None:
        param_data['closure_notes'] = params.get('closure_notes')
    payload = {
        "param": {
            "data": param_data
        }
    }        
    return co.make_rest_call(endpoint, 'POST', data=json.dumps(payload))

def get_alert_list_clientuuid(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/alert/client/" + params.get('clientuuid')
    return co.make_rest_call(endpoint, 'GET')

def get_comment_list(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/comment"
    query_params = {}
    query_params['module'] = params.get('module')
    query_params['uuid'] = params.get('uuid')
    return co.make_rest_call(endpoint, 'GET', params=query_params)

def create_comment(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/comment"
    param_data = {
        "content": params.get('comment'),
        "related": params.get('module'),
        "related_uuid": params.get('uuid')
    }
    if params.get('tag') is not None:
        param_data['tag'] = params.get('tag')
    else:
        param_data['tag'] = ""

    payload = {
        "param": {
            "data": param_data
        }
    }
    return co.make_rest_call(endpoint, 'POST', data=json.dumps(payload))

def download_attachment_and_report(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/file"
    query_params = {}
    query_params['module'] = params.get('module')
    query_params['file-portal-uuid'] = params.get('file-portal-uuid')
    return co.make_rest_call(endpoint, 'GET', params=query_params)

def get_list_service_request(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/service-request"
    return co.make_rest_call(endpoint, 'GET')

def create_service_request(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/service-request"
    param_data = params.get('data')
    param_data['type'] = params.get('type')
    param_data['notification'] = params.get('notification')
    param_data['title'] = params.get('title')
    
    payload = {
        "param": {
            "data": param_data
        }
    }
    return co.make_rest_call(endpoint, 'POST', data=json.dumps(payload))

def get_details_service_request(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/service-request/" + params.get('service_request_uuid')
    return co.make_rest_call(endpoint, 'GET')

def get_client_service_request(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/service-request/client/" + params.get('clientuuid')
    return co.make_rest_call(endpoint, 'GET')

def get_list_reports(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/report"
    return co.make_rest_call(endpoint, 'GET')

def get_list_reports_client(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/report/client/" + params.get('clientuuid')
    return co.make_rest_call(endpoint, 'GET')

def get_client_list(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/client"
    return co.make_rest_call(endpoint, 'GET')

def get_preonboarding_info(config, params=None):
    co = SOCaaS(config)
    endpoint = "/socaasAPI/v1/mssp-onboarding-info"
    return co.make_rest_call(endpoint, 'GET')

def generic_api_call(config, params):
    try:
        method = params.get('method')
        endpoint = params.get('endpoint')
        data = params.get('data')

        co = SOCaaS(config)

        if data and isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise ConnectorError("Invalid JSON in 'data' parameter")

        return co.make_rest_call(endpoint, method, data=json.dumps(data) if data else None)
    except Exception as err:
        logger.exception(f"{str(err)}")
        raise ConnectorError(f"{str(err)}")

def _check_health(config):
    try:
        return check(config)
    except Exception as err:
        logger.exception(f"{str(err)}")
        raise ConnectorError(f"{str(err)}")


operations = {
    'get_alert_list': get_alert_list,
	'get_alert_uuid': get_alert_uuid,
	'get_alert_list_clientuuid': get_alert_list_clientuuid,
    'update_alert_status': update_alert_status,
    "get_comment_list": get_comment_list,
    "create_comment": create_comment,
    "download_attachment_and_report": download_attachment_and_report,
    "get_list_service_request": get_list_service_request,
    "create_service_request": create_service_request,
    "get_details_service_request": get_details_service_request,
    "get_client_service_request": get_client_service_request,
    "get_list_reports": get_list_reports,
    "get_list_reports_client": get_list_reports_client,
    "get_client_list": get_client_list,
    "get_preonboarding_info": get_preonboarding_info,
    "generic_api_call": generic_api_call
}
