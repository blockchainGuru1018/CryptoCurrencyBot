from rest_framework import serializers
from bitcoin_arbitrage.models import Exchange


class ActionSerialier(serializers.Serializer):
    action = serializers.CharField(required=True)

    def clean_action(self, value):
        if value not in ["start", "stop"]:
            raise serializers.ValidationError()
        return value


def serialize_change(exchange):
    return {
        "name": exchange.name,
        "currency_pair": exchange.currency_pair,
        "last_ask_price": exchange.last_ask_price,
        "last_bid_price": exchange.last_bid_price
    }
