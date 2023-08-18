import requests
import requests.packages
import logging
from typing import List, Dict
from exceptions import DiscuitAPIException
from json import JSONDecodeError
from models import Result, Post, Posts

class RestAdapter:
    def __init__(self, hostname: str = 'discuit.net/api', ssl_verify: bool = True,
                 logger: logging.Logger = None):
        """Constructor for RestAdapater

        Args:
            hostname (str): Defaults to, discuit.net/api
            api_key (str, optional): string used for auth. current unused. Defaults to ''.
            ssl_verify (bool, optional): if having SSL/TLS cert validation issues, can turn off with False. Defaults to True.
            logger (logging.Logger, optional): If app has a logger, pass itr here. Defaults to None.
        """
        self.url = "https://{}/".format(hostname)
        # save to private member variables
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)

        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """Helper func for POST/GET/DELETE methods for returning data from requests.

        Args:
            http_method (str): The method used
            endpoint (str): The endpoint desired to hit
            ep_params (Dict, optional): Any parameters required for the data. Defaults to None.
            data (Dict, optional): Used for POST methods. Defaults to None.

        Raises:
            DiscuitAPIException: Request failed.
            DiscuitAPIException: Bad JSON response.
            DiscuitAPIException: Bad status code.

        Returns:
            Result: Instance of results model. 
        """

        full_url = self.url + endpoint
        # will be required for auth down the line
        headers = {}

        log_line_pre = f"method={http_method}, url={full_url}. params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, messaage={}"))

        # Log HTTP params and perform HTTP request, catching and re-raising execeptions.
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, 
                                        headers=headers, params=ep_params, json=data)
        
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DiscuitAPIException("Request Failed") from e

        # deserialise JSON output to pytho nobject, or return failed on exe
        try:
            data = response.json()

        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise DiscuitAPIException("Bad JSON response") from e

        # if status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200

        if is_success: # okay 
            # return a result object
            
            return Result(response.status_code, message=response.reason, data=data)
    
        raise DiscuitAPIException(f"{response.status_code} :  {response.reason}")


    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """Performs a GET request to the specified endpoint with given parameters.

        Args:
            endpoint (str): The endpoint to reach after /api. (e.g., posts, users)
            ep_params (Dict, optional): Parameters for the request. Defaults to None.

        Returns:
            Result: Result object.
        """
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)
    
    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """Performs a POST reqeuest to the given endpoint, with params and data.

        Args:
            endpoint (str): The endpoint to reach after /api. (e.g., posts, users)
            ep_params (Dict, optional): Parameters for the request.. Defaults to None.
            data (Dict, optional): Data to post. Defaults to None.

        Returns:
            Result: Result object.
        """
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
    
    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
    
    def fetch_data(self, url:str) -> bytes:
        #GET URL 
        http_method = 'GET'
        try:
            log_line = f"method={http_method}, url={url}"
            self._logger.debug(msg=log_line)
            response = requests.request(method=http_method, url=url, verify=self._ssl_verify)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DiscuitAPIException(str(e)) from e
        
        # If status_code in 200-299 range, return byte stream, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)
        if not is_success:
            raise DiscuitAPIException(response.reason)
        return response.content