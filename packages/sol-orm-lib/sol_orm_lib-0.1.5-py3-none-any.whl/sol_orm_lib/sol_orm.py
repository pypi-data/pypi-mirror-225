import os
import sys
import urllib.parse

import requests
from loguru import logger

from .models import *

logger.remove()
logger.add(sys.stdout, colorize=True, 
           format="<le>[{time:DD-MM-YYYY HH:mm:ss}]</le> <lvl>[{level}]: {message}</lvl>", 
           level="INFO")


class SolORM:
    """Interface with the SOL database API.

    This class provides methods to interact with the SOL database API for adding, retrieving, and managing various entities.

    Attributes:
        add_paths (dict): A dictionary mapping entity classes to their corresponding API paths for adding entities.
        get_paths (dict): A dictionary mapping entity classes to their corresponding API paths for retrieving entities.
        util_paths (dict): A dictionary mapping utility methods to their corresponding API paths.

    Methods:
        __init__: Initialize the SolORM instance.
        add_entity: Add an entity to the database.
        get_entity: Retrieve an entity from the database by its ID.
        get_last_entity: Retrieve the last N entities of a certain type.
        get_since_entity: Retrieve entities of a certain type since a specified timestamp.
        util_create_TIC_TACs: Create TICs and TACs for a specified number of years.
    """
    # Add Methods
    add_paths = {
        TIC.__name__: "TICs/add",
        TAC.__name__: "TACs/add",
        SpotPublishedTIC.__name__: "SpotPublishedTICs/add",
        SpotEstimatedTIC.__name__: "SpotEstimatedTICs/add",
        ReceivedForecast.__name__: "ReceivedForecasts/add",
        SAMParameter.__name__: "SAMParameters/add",
        OptimizationParameter.__name__: "OptimizationParameters/add",
        MeasuredWeather.__name__:"MeasuredWeathers/add",
        MeasuredWeatherTIC.__name__: "MeasuredWeatherTICs/add"
    }

    add_range_paths = {
        SpotEstimatedTIC.__name__: "SpotEstimatedTICs/addRange"
    }

    # Get Methods
    get_paths = {
        TIC.__name__: "TICs",
        TAC.__name__: "TACs",
        SpotPublishedTIC.__name__: "SpotPublishedTICs",
        SpotEstimatedTIC.__name__: "SpotEstimatedTICs",
        ReceivedForecast.__name__ : "ReceivedForecasts",
        SAMParameter.__name__: "SAMParameters",
        OptimizationParameter.__name__: "OptimizationParameters",
        MeasuredWeather.__name__:"MeasuredWeathers",
        MeasuredWeatherTIC.__name__: "MeasuredWeatherTICs"
    }

    # Util Methods
    util_paths = {
        'CreateTICsAndTACs': "Utilities/CreateTICsAndTACs"
    }

    def __init__(self, base_url=None, debug=False, verify_ssl=True):
        """Initialize the SolORM instance.

        Args:
            base_url (str, optional): The base URL of the SOL database API. If not provided, it's fetched from the DB_API_URL environment variable.
            debug (bool, optional): Enable debugging mode for logging. Default is False.
            verify_ssl (bool, optional): Verify SSL certificates when making requests. Default is True.
        """
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = os.getenv("DB_API_URL")
            if self.base_url is None:
                raise ValueError("DB_API_URL environment variable not set")
            
        if debug:
            logger.remove()
            logger.add(sys.stdout, colorize=True, 
                       format="<le>[{time:DD-MM-YYYY HH:mm:ss}]</le> <lvl>[{level}]: {message}</lvl>", 
                       level="DEBUG")
            
        self.session = self._create_session(verify_ssl)
        
    def _create_session(self, verify_ssl):
        session = requests.Session()
        session.headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        session.verify = verify_ssl
        return session
    
    def _get_url(self, path):
        return urllib.parse.urljoin(self.base_url, path)
    
    def add_entity(self, entity):
        """Add an entity to the database.

        Args:
            entity: An instance of an entity class (e.g., TIC, TAC, etc.) to be added.

        Returns:
            dict: The JSON response from the API.

        Raises:
            HTTPError: If the request fails or the response status code is not 201 (Created).
        """
        endpoint = self._get_url(self.add_paths[entity.__class__.__name__])
        response = self.session.post(endpoint, json=entity.dict(exclude_none=True))

        if response.status_code == 201:
            logger.debug("Request successful")
            return response.json()
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
        
    def add_range_entity(self, entity_list: list):
        if entity_list.count == 0:
            raise Exception(f"This method can only be used with not empty lists")
        
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        response = requests.post(
            self.get_url(
                self.add_range_paths[entity_list[0].__class__.__name__]),
                json.dumps([x.dict(exclude_none=True) for x in entity_list]), headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 201:
            logger.debug("Request successful")
            return json.loads(response.text)
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
    
    def get_entity(self, entity_name, id, id2=None):
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        endpoint = self.get_url(self.get_paths[entity_name]) + "/" + str(id) + ("/" + str(id2) if id2 is not None else "")        
        response = requests.get(endpoint, headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 200:
            logger.debug("Request successful")
            return response.json()
        else:
            logger.debug(response.text)
            response.raise_for_status()
    
    def get_last_entity(self, entity_name, number=1):
        """Retrieve the last N entities of a certain type.

        Args:
            entity_name (str): The name of the entity type.
            number (int, optional): The number of entities to retrieve. Default is 1.

        Returns:
            dict: The JSON response containing the retrieved entities.

        Raises:
            HTTPError: If the request fails or the response status code is not 200 (OK).
        """
        endpoint = self._get_url(self.get_paths[entity_name]) + "/getLast/" + str(number)
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            logger.debug("Request successful")
            return response.json()
        else:
            logger.debug(response.text)
            response.raise_for_status()
    
    def get_since_entity(self, entity_name, since, number=10):
        """Retrieve entities of a certain type since a specified timestamp.

        Args:
            entity_name (str): The name of the entity type.
            since (int): The timestamp since which to retrieve entities.
            number (int, optional): The number of entities to retrieve. Default is 10.

        Returns:
            dict: The JSON response containing the retrieved entities.

        Raises:
            HTTPError: If the request fails or the response status code is not 200 (OK).
        """
        endpoint = self._get_url(self.get_paths[entity_name]) + "/getSince/" + str(since) + "/" + str(number)
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            logger.debug("Request successful")
            return response.json()
        else:
            logger.debug(response.text)
            response.raise_for_status()
        
    def util_create_TIC_TACs(self, years=1):
        """
        Create TICs and TACs for a specified number of years.

        Args:
            years (int, optional): The number of years for which to create TICs and TACs. Default is 1.

        Returns:
            dict: The JSON response from the API.

        Raises:
            HTTPError: If the request fails or the response status code is not 201 (Created).
        """
        endpoint = self._get_url(self.util_paths["CreateTICsAndTACs"])
        response = self.session.post(endpoint, json={"years": years})
        
        if response.status_code == 201:
            logger.debug("Request successful")
            return response.json()
        else:
            logger.debug(response.text)
            response.raise_for_status()
    