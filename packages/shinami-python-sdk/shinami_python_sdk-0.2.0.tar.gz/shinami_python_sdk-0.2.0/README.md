# Shinami Python SDK

This package is an asynchronous API wrapper for the [Shinami In-App Wallet (IAW) API](https://docs.shinami.com/reference/in-app-wallet-api).

Currently, this SDK supports the IAW methods below.

* shinami_key_createSession
* shinami_wal_createWallet
* shinami_wal_executeGaslessTransactionBlock
* shinami_wal_getWallet

## How to Install

```
pip install shinami-python-sdk
```

## How to Use

```
import asyncio
import os

from shinami_python_sdk.iaw import ShinamiIawClient

# Set Shinami API key.
SHINAMI_IAW_API_TOKEN = os.environ["SHINAMI_IAW_API_KEY"]

# Initialize IAW API client.
shinami_iaw_client = ShinamiIawClient(SHINAMI_IAW_API_KEY)

# Create a session_token.
session_token = asyncio.run(shinami_iaw_client.create_session("NOT_A_SECURE_SECRET"))

# Create a wallet.
wallet = asyncio.run(shinami_iaw_client.create_wallet("walletid123", session_token))
```