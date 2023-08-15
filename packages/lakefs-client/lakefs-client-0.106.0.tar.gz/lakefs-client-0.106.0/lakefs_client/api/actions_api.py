"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from lakefs_client.api_client import ApiClient, Endpoint as _Endpoint
from lakefs_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from lakefs_client.model.action_run import ActionRun
from lakefs_client.model.action_run_list import ActionRunList
from lakefs_client.model.error import Error
from lakefs_client.model.hook_run_list import HookRunList


class ActionsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.get_run_endpoint = _Endpoint(
            settings={
                'response_type': (ActionRun,),
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/repositories/{repository}/actions/runs/{run_id}',
                'operation_id': 'get_run',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'repository',
                    'run_id',
                ],
                'required': [
                    'repository',
                    'run_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'repository':
                        (str,),
                    'run_id':
                        (str,),
                },
                'attribute_map': {
                    'repository': 'repository',
                    'run_id': 'run_id',
                },
                'location_map': {
                    'repository': 'path',
                    'run_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.get_run_hook_output_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/repositories/{repository}/actions/runs/{run_id}/hooks/{hook_run_id}/output',
                'operation_id': 'get_run_hook_output',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'repository',
                    'run_id',
                    'hook_run_id',
                ],
                'required': [
                    'repository',
                    'run_id',
                    'hook_run_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'repository':
                        (str,),
                    'run_id':
                        (str,),
                    'hook_run_id':
                        (str,),
                },
                'attribute_map': {
                    'repository': 'repository',
                    'run_id': 'run_id',
                    'hook_run_id': 'hook_run_id',
                },
                'location_map': {
                    'repository': 'path',
                    'run_id': 'path',
                    'hook_run_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/octet-stream',
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.list_repository_runs_endpoint = _Endpoint(
            settings={
                'response_type': (ActionRunList,),
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/repositories/{repository}/actions/runs',
                'operation_id': 'list_repository_runs',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'repository',
                    'after',
                    'amount',
                    'branch',
                    'commit',
                ],
                'required': [
                    'repository',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'amount',
                ]
            },
            root_map={
                'validations': {
                    ('amount',): {

                        'inclusive_maximum': 1000,
                        'inclusive_minimum': -1,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'repository':
                        (str,),
                    'after':
                        (str,),
                    'amount':
                        (int,),
                    'branch':
                        (str,),
                    'commit':
                        (str,),
                },
                'attribute_map': {
                    'repository': 'repository',
                    'after': 'after',
                    'amount': 'amount',
                    'branch': 'branch',
                    'commit': 'commit',
                },
                'location_map': {
                    'repository': 'path',
                    'after': 'query',
                    'amount': 'query',
                    'branch': 'query',
                    'commit': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.list_run_hooks_endpoint = _Endpoint(
            settings={
                'response_type': (HookRunList,),
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/repositories/{repository}/actions/runs/{run_id}/hooks',
                'operation_id': 'list_run_hooks',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'repository',
                    'run_id',
                    'after',
                    'amount',
                ],
                'required': [
                    'repository',
                    'run_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'amount',
                ]
            },
            root_map={
                'validations': {
                    ('amount',): {

                        'inclusive_maximum': 1000,
                        'inclusive_minimum': -1,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'repository':
                        (str,),
                    'run_id':
                        (str,),
                    'after':
                        (str,),
                    'amount':
                        (int,),
                },
                'attribute_map': {
                    'repository': 'repository',
                    'run_id': 'run_id',
                    'after': 'after',
                    'amount': 'amount',
                },
                'location_map': {
                    'repository': 'path',
                    'run_id': 'path',
                    'after': 'query',
                    'amount': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def get_run(
        self,
        repository,
        run_id,
        **kwargs
    ):
        """get a run  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_run(repository, run_id, async_req=True)
        >>> result = thread.get()

        Args:
            repository (str):
            run_id (str):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ActionRun
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['repository'] = \
            repository
        kwargs['run_id'] = \
            run_id
        return self.get_run_endpoint.call_with_http_info(**kwargs)

    def get_run_hook_output(
        self,
        repository,
        run_id,
        hook_run_id,
        **kwargs
    ):
        """get run hook output  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_run_hook_output(repository, run_id, hook_run_id, async_req=True)
        >>> result = thread.get()

        Args:
            repository (str):
            run_id (str):
            hook_run_id (str):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            file_type
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['repository'] = \
            repository
        kwargs['run_id'] = \
            run_id
        kwargs['hook_run_id'] = \
            hook_run_id
        return self.get_run_hook_output_endpoint.call_with_http_info(**kwargs)

    def list_repository_runs(
        self,
        repository,
        **kwargs
    ):
        """list runs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_repository_runs(repository, async_req=True)
        >>> result = thread.get()

        Args:
            repository (str):

        Keyword Args:
            after (str): return items after this value. [optional]
            amount (int): how many items to return. [optional] if omitted the server will use the default value of 100
            branch (str): [optional]
            commit (str): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ActionRunList
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['repository'] = \
            repository
        return self.list_repository_runs_endpoint.call_with_http_info(**kwargs)

    def list_run_hooks(
        self,
        repository,
        run_id,
        **kwargs
    ):
        """list run hooks  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_run_hooks(repository, run_id, async_req=True)
        >>> result = thread.get()

        Args:
            repository (str):
            run_id (str):

        Keyword Args:
            after (str): return items after this value. [optional]
            amount (int): how many items to return. [optional] if omitted the server will use the default value of 100
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            HookRunList
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['repository'] = \
            repository
        kwargs['run_id'] = \
            run_id
        return self.list_run_hooks_endpoint.call_with_http_info(**kwargs)

