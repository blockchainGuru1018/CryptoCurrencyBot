import os
import nox


locations = ["backend/bitcoin_arbitrage", "backend/crypto_bot"]


@nox.session(python="3.8")
def black(session):
    session.install("black")
    session.run("black", *locations)


