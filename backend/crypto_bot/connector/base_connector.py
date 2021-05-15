

class BaseConnector(object):

    market_events = []

    def __init__(self):
        self._account_balances = {}  # Dict[asset_name:str, Decimal]
        self._account_available_balances = {}  # Dict[asset_name:str,Decimal]
        # _real_time_balance_update is used to flag whether the
        # connector provides real time balance updates.
        # if not, the available will be calculated based on
        # what happened since snapshot taken.
        self._real_time_balance_update = True
        # If _real_time_balance_update is set to False, Sub classes of this
        # connector class need to set values for _in_flight_orders_snapshot and
        # _in_flight_orders_snapshot_timestamp when the update user balances.
        self._in_flight_orders_snapshot = {}  #Dict[order_id:str, InFlightOrderBase]
        self._in_flight_orders_snapshot_timestamp = 0.0


        @property
        def real_time_balance_update(self):
            return self._real_time_balance_update


        @real_time_balance_update.setter 
        def real_time_balance_update(self, value):
            self._real_time_balance_update = value 

        
        @property 
        def in_flight_order_snapshot(self):
            return self._in_flight_orders_snapshot 


        @in_flight_order_snapshot.setter 
        def in_flight_order_snapshot(self, value):
            self._in_flight_order_snapshot = value 


        @property 
        def in_flight_order_snapshot_timestamp(self):
            return self._in_flight_orders_snapshot_timestamp 


        @in_flight_order_snapshot_timestamp.setter 
        def in_flight_order_snapshot_timestamp(self, value):
            return self._in_flight_order_snapshot_timestamp 


