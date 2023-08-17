import requests
import logging
import json

from .model import (StatusType, DataDomeRequest, OperationType,
                    DataDomeResponse, ResponseStatus, DataDomeResponseError,
                    ResponseAction, DdEncoder)


class DataDome:
    """ DataDome Fraud Protection instance
    
    Attributes:
        key: Your Fraud API Key
        timeout: A timeout threshold in milliseconds
        endpoint: The endpoint to call for the fraud protection API
        logger: The logger to get DataDome information
    """
    def __init__(
        self,
        key,
        timeout=1500,
        endpoint="https://account-api.datadome.co",
        logger=logging.getLogger(),
    ):
        """Inits DataDome Fraud instance with the given parameters"""
        self.key = key
        self.timeout = timeout
        if not endpoint.lower().startswith("https://") and "://" not in endpoint:
            self.endpoint = "https://" + endpoint
        else:
            self.endpoint = endpoint
        self.logger = logger
        self.request_headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "x-api-key": key,
        }

    @staticmethod
    def build_payload(request, event):
        return event.merge_with(DataDomeRequest(request))

    def send_request(
        self,
        operation,
        request,
        event,
    ):
        url = self.endpoint + "/v1/" + operation.value + "/" + event.action.value
        payload = self.build_payload(request, event)
        payloadjson = json.dumps(payload, cls=DdEncoder)
        self.logger.debug(f"url: {url}")
        self.logger.debug(f"body: {payloadjson}")
        response = requests.post(url, data=payloadjson,
                                 headers=self.request_headers, timeout=5)
        return response

            
    def validate(self, request, event):
        """Validates the request given the event information"""
        if (event.status == StatusType.UNDEFINED):
            event.status = StatusType.SUCCEEDED
        dd_response = DataDomeResponse(action=ResponseAction.ALLOW)
        try:
            api_response = self.send_request(OperationType.VALIDATE, request, event)
            if api_response.status_code == requests.codes.ok:
                dd_response.update_with_api_response(json.loads(api_response.text))
            elif api_response.status_code == requests.codes.bad:
                dd_response = DataDomeResponseError(json.loads(api_response.text),
                                                    action=ResponseAction.ALLOW)
                self.logger.error("Invalid request made to DataDome Fraud API: "+ str(dd_response)) # noqa: E501
            else:
                dd_response = DataDomeResponseError()
                self.logger.error("Error on DataDome Fraud API response: "+ str(dd_response)) # noqa: E501                   
        except requests.exceptions.Timeout:
            dd_response = DataDomeResponseError({"message": "Request timed out"},
                                                status=ResponseStatus.TIMEOUT,
                                                action=ResponseAction.ALLOW)
            self.logger.error("Call to DataDome Fraud API timed out")
        
        return dd_response
    
    def collect(self, request, event):
        """Collects data on the request given the event information"""
        if (event.status == StatusType.UNDEFINED):
            event.status = StatusType.FAILED
        dd_response = DataDomeResponse()
        try:
            api_response = self.send_request(OperationType.COLLECT, request, event)
            if api_response.status_code == requests.codes.created:
                dd_response.status = ResponseStatus.OK
            elif (api_response.status_code == requests.codes.bad):
                dd_response = DataDomeResponseError(json.loads(api_response.text))
                self.logger.error("Invalid request made to DataDome Fraud API: "+ str(dd_response)) # noqa: E501
            else:
                dd_response = DataDomeResponseError()
                self.logger.error("Error on DataDome Fraud API response: "+ str(dd_response)) # noqa: E501
        except requests.exceptions.Timeout:
            dd_response = DataDomeResponseError({"message": "Request timed out"}, 
                                                status=ResponseStatus.TIMEOUT)
            self.logger.error("Call to DataDome Fraud API timed out")
            
        return dd_response
