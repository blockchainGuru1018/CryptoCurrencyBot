import json
import requests as req


class CryptoHooperHandler(object):
    endpoints = {
        'auth': ' https://www.cryptohopper.com/oauth2/authorize',
        'token': 'https://www.cryptohopper.com/oauth2/token',
        'api_root': 'https://api.cryptohopper.com/v1/',
    }

    def __init__(self, api_key, api_secret, **kwargs):
        self.api_key = api_key
        self.api_secret = api_secret
        self._token = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def authorize(self):
        """
        Authorizes the app to access to the API resources.
        params required:

        client_id     : The app key of your application.
        response_type : The response type should contain the text: code.
        redirect_uri  : The redirect URL where users will be redirected to after the Oauth process.
        state         : Extra parameter to recognise requests on the application side.
                        Will be returned to the redirect URL. (optional).
        scope         : A comma separated list of scopes, for example: read,notifications,manage,trade.

        :return: token authorization or raises Exception.
        """
        params = {
            'client_id': self.api_key,
            'response_type': 'application/JSON',
            'scope': ['read', 'notification', 'manage', 'trade']
        }
        response = req.get(self.endpoints['auth'], params)
        if response.status_code != 200:
            raise Exception(
                f"Authentication error {response.status_code} - {response.reason}"
            ) from None
        self.token = response.json()['code']
        return self.token

    def _listing_items(self, url, **kwargs):
        """
        generic method for listing items
        that doesn't require params
        :param url:
        :return:
        """
        data = {key: value for key, value in kwargs.items()}
        response = req.get(url, headers={'access-token': self.token}, params=data)
        if response.status_code != 200:
            raise Exception(
                f"ListingGenericError {response.status_code} - {response.reason}"
            ) from None
        return response.json()

    def _delete_item(self, url, **kwargs):
        """
        generic delete implementation
        :param url: str
        :param template_id: int
        :return: json
        """
        result = {'success': False}
        response = req.delete(url, headers={'access-token': self.token}, kwargs=kwargs)
        if response.status_code != 200:
            raise Exception(
                f"GenericDeleteError {response.status_code} - {response.reason}"
            ) from None
        result.update({'success': True, 'status': response.status_code})
        return json.dumps(result)

    def _create_item(self, url, data):
        """
        generic create method
        :param url: str: where to send the data to
        :param data: data to insert
        :return: json
        """
        result = {'success': False}
        response = req.post(url, data=data, headers={'access-token': self.token})
        if response.status_code != 200:
            raise Exception(
                f"CreateGenericError {response.status_code} - {response.reason}"
            ) from None
        result.update({'success': True, 'status': response.status_code})
        return json.dumps(result)

    def _post(self, url, data):
        """
        generic post method for those post requests
        :param url: str: where to send the data to
        :param data: data to insert
        :return: json
        """
        result = {'success': False}
        response = req.post(url, data=data, headers={'access-token': self.token})
        if response.status_code != 200:
            raise Exception(
                f"GenericPostError {response.status_code} - {response.reason}"
            ) from None
        result.update({'success': True, 'status': response.status_code})
        return json.dumps(result)

    def _put(self, url, data):
        """
        generic put method for those post requests
        :param url: str: where to send the data to
        :param data: data to insert
        :return: json
        """
        result = {'success': False}
        response = req.put(url, data=data, headers={'access-token': self.token})
        if response.status_code != 200:
            raise Exception(
                f"GenericPutError {response.status_code} - {response.reason}"
            ) from None
        result.update({'success': True, 'status': response.status_code})
        return json.dumps(result)

    def _get_item(self, url, **kwargs):
        """
        generic method for getting an item
        :param url: str
        :param kwargs: params for the get request
        :return:
        """
        response = req.get(url, headers={'access-token': self.token}, params=kwargs)
        return response.json()

    def change_token(self):
        """
        :return: token or raises AttributeError
        """
        params = {
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'response_type': 'application/JSON',
            'code': self.token
        }
        response = req.get(self.endpoints['auth'], params)
        if response.status_code != 200:
            raise Exception(
                f"Change token error {response.status_code} - {response.reason}"
            ) from None
        self.token = response.json()['code']
        return self.token

    def list_hoopers(self):
        """
        loads all of the hoopers of the client provided
        """
        url = '{0}hopper'.format(self.endpoints['api_root'])
        return self._listing_items(url)

    def get_hooper(self, hopper_id):
        """
        Gets a single hooper
        :param hopper_id: int
        """
        url = '{0}hopper/{1}'.format(self.endpoints['api_root'], hopper_id)
        return self._get_item(url)

    def create_hooper(self, hooper_data):
        """
        Creates a single hopper.
        Raises Exception
        """
        url = '{0}hopper'.format(self.endpoints['api_root'])
        return self._create_item(url, hooper_data)

    def list_hopper_config_pools(self, hopper_id):
        """
        loads all configurations for the given hooper
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/config/pools"
        return self._listing_items(url)

    def get_base_hopper_config(self, hopper_id):
        """
        gets the basic configuration for the hopper
        :param hopper_id: int
        :return: json
        """
        url = '{0}hopper/{1}/config'.format(self.endpoints['api_root'], hopper_id)
        return self._get_item(url)

    def update_base_hopper_config(self, hopper_id, config_data):
        """
        updates the base configuration for the hopper
        :param hopper_id: int
        :param config_data: dict data related to the config
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/config"
        return self._put(url, config_data)

    def get_hopper_config_pool(self, hopper_id, config_pool_id):
        """
        gets the specific config pool for the given hopper
        :param config_pool_id: int
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/config/pool/{config_pool_id}"
        return self._get_item(url)

    def create_hopper_config_pool(self, hopper_id, config_pool_data):
        """
        loads all configurations for the given hooper
        :param hopper_id: int
        :param config_pool_data: dict containing all data for the config pool
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/config/pool"
        return self._create_item(url, config_pool_data)

    def update_hopper_config_pool(self, hopper_id, config_pool_id, config_pool_data):
        """
        updates the hopper configuration pool for the hopper provided
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/config/pool/{config_pool_id}"
        return self._put(url, config_pool_data)

    def delete_hopper_config_pool(self, hopper_id, config_pool_id):
        """
        removes the given config pool for the given hopper
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/config/pool/{config_pool_id}"
        return self._delete_item(url)

    def create_hooper_template(self, hooper, template_data):
        """
        creates a hooper template
        :param hooper_data: dict containing
         all values required for the hooper template
        :return: JSON
        """
        url = f"{self.endpoints['api_root']}hopper/{hooper.id}/template/save"
        return self._create_item(url, template_data)

    def list_templates(self, basic=False) -> json:
        """
        lists all of the existing templates available
        :param basic: bool: whether you want the basic templates or generic
        :return: JSON object
        """
        url = f"{self.endpoints['api_root']}template" if not basic else  f"{self.endpoints['api_root']}template/basic"
        return self._listing_items(url)

    def list_template_exchange(self, exchange):
        """
        get all list of templates for the exchange
        :param exchange: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}template/basic/{exchange}"
        return self._listing_items(url)

    def list_template_market(self):
        """
        lists all template markets for the given user
        or in this case the API
        :return: json
        """
        url = f"{self.endpoints['api_root']}template/basic/{exchange}"
        return self._listing_items(url)

    def list_market_signals(self):
        """
        lists all of the market signals available
        to the API
        :return: json
        """
        url = f"{self.endpoints['api_root']}market/signals"
        return self._listing_items(url)

    def get_signal(self, signal_id):
        """
        loads the given signal
        :param signal_id: int
        :return: JSON
        """
        url = f"{self.endpoints['api_root']}market/signals/{signal_id}"
        return self._get_item(url)

    def list_hopper_trade_history(self, hopper_id):
        """
        lists all of the history when it comes to the hopper
        history
        :param hopper_id:int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/trade"
        return self._listing_items(url)

    def hopper_trade_history_details(self, hopper_id, trade_id):
        """
        gets the details for the given trade beloging to the hopper
        :param hopper_id:int
        :param trade_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/trade/{trade_id}"
        return self._get_item(url)

    def view_hopper_logs(self, hopper_id):
        """
        gets all of the hopper's log related to
        the actions of it
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}/hopper/{hopper_id}/output"
        return self._get_item(url)

    def get_hopper_position(self, hopper_id):
        """
        gets the current position of your hopper
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}/hopper/{hopper_id}/position"
        return self._get_item(url)

    def list_hopper_position_holds(self, hopper_id):
        """
        Lists all position holds for the given hopper
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/position/hold"
        return self._listing_items(url)

    def hold_hopper_position(self, hopper_id, position_id):
        """
        sets a hold on the position/positions for the given hopper
        :param hopper_id: int
        :param position_id: int or a list of integers
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/position/hold"
        data = {'position_id': position_id}
        return self._post(url, data)

    def remove_hopper_positons(self, hopper_id):
        """
        removes all positions for the given hopper
        :param hopper_id:
        :return:
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/position"
        return self._delete_item(url)

    def remove_hopper_position(self, hopper_id, position_id):
        """
        removes a single position for the given hopper
        :param hopper_id:
        :return:
        """
        url = f"{self.endpoints['api_root']}hopper/{hopper_id}/position/{position_id}"
        return self._delete_item(url)

    def hopper_positions_sell(self, hopper_id, position_id):
        """
        sets a hold on the position/positions for the given hopper
        :param hopper_id: int
        :param position_id: int or a list of integers
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/position/sell"
        data = {'position_id': position_id}
        return self._post(url, data)

    def hopper_position_sell(self, hopper_id, position_id):
        """
        sets a hold on the position for the given hopper
        :param hopper_id: int
        :param position_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/position/sell/{position_id}"
        return self._post(url, data={})

    def set_hopper_take_profit(self, hopper_id, position_id, percentage_profit):
        """
        sets a flag for the given hopper to take profit
        at the given value when this one is reached in all positions
        :param hopper_id: int
        :param position_id: int or a list of integers
        :param percentage_profit: int or a list of integers
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/position/settakeprofit"
        data = {'position_id': position_id, 'percentage_profit': percentage_profit}
        return self._post(url, data)

    def list_hopper_orders(self, hopper_id):
        """
        gets all of the existing orders for the given hopper
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/orders"
        return self._listing_items(url)

    def get_hopper_order(self, hopper_id, order_id):
        """
        get the selected order for the given hopper
        :param hopper_id: int
        :param order_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/order/{order_id}"
        return self._get_item(url)

    def create_hooper_order(self, hopper_id, order_data):
        """
        creates an order for the given hopper
        :param hopper_id: int
        :param order_data: dict: all fields required for the order
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/order"
        return self._create_item(url, order_data)

    def cancel_order(self, hopper_id, order_id):
        """
        cancels the open order provided for the hopper
        :param hopper_id: int
        :param order_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/order/{order_id}"
        return self._delete_item(url)

    def cancel_hopper_orders(self, hopper_id):
        """
        cancels all of the existing orders for the given hopper
        :param hopper_id: int
        :return: json
        """
        url = f"{self.endpoints['api_root']}hooper/{hopper_id}/order/all"
        return self._delete_item(url)