import json
import uuid

import httpx

from shinami_python_sdk import logger
from shinami_python_sdk.exceptions import (
    ShinamiInvalidApiTokenException,
    ShinamiWalletException,
    ShinamiWalletExistsException,
    ShinamiWalletNotFoundException,
)
from shinami_python_sdk.models import JsonRpcResponse, ShinamiWallet


def _is_error(r: dict) -> bool:
    return True if "error" in r else False


class ShinamiIawClient:
    """
    API wrapper for the Shinami IAW API.
    """

    def __init__(
        self,
        api_token: str,
        api_url: str = "https://api.shinami.com",
    ) -> None:
        self.api_token = api_token
        self.api_url = api_url

    ###################
    # SESSION METHODS #
    ###################

    async def create_session(
        self,
        secret: str,
        full_response: bool = False,
    ) -> dict | str:
        """
        Create a Shinami session with the given secret.

        Args:
            secret (str): The secret to use to create the session.
            full_response (bool, optional): Whether to return the full response or just the session token. Defaults to False.

        Returns:
            str: The session token.
        """
        r = await self._make_post_request(
            f"{self.api_url}/key/v1",
            "shinami_key_createSession",
            [secret],
        )

        if r.error is not None:
            raise Exception(r.error)

        return r if full_response else r.result

    ##################
    # WALLET METHODS #
    ##################

    async def create_wallet(
        self,
        wallet_id: str,
        session_token: str,
        full_response: bool = False,
    ) -> ShinamiWallet:
        """
        Create a Shinami wallet with the given wallet ID and session token.

        Args:
            wallet_id (str): An ID to associate with the wallet.
            session_token (str): The session token to use to create the wallet.
            full_response (bool, optional): Whether to return the full response or just the wallet ID. Defaults to False.
        """
        logger.info(f"Creating wallet with session token: {session_token}")
        logger.info(f"Creating wallet with ID: {wallet_id}")

        r = await self._make_post_request(
            f"{self.api_url}/wallet/v1",
            "shinami_wal_createWallet",
            [wallet_id, session_token],
        )

        if r.error:
            raise ShinamiWalletException(r.error)

        if full_response:
            return r
        else:
            return r.result

    async def get_wallet(
        self,
        wallet_id: str,
        full_response: bool = False,
    ) -> ShinamiWallet:
        """
        Fetch a Shinami wallet with the given wallet ID.

        Args:
            wallet_id (str): The ID of the wallet to fetch.
            full_response (bool, optional): Whether to return the full response or just the wallet ID. Defaults to False.
        """
        r = await self._make_post_request(
            f"{self.api_url}/wallet/v1",
            "shinami_wal_getWallet",
            [wallet_id],
        )

        if r.error:
            raise ShinamiWalletException(r.error)

        if full_response:
            return r
        else:
            return r.result

    #######################
    # TRANSACTION METHODS #
    #######################

    async def execute_gasless_transaction_block(
        self,
        wallet_id: str,
        session_token: str,
        tx_bytes: str,
        gas_budget: int,
        request_type: str,
    ) -> dict | str:
        """
        Execute a gasless transaction block with the given parameters.

        Args:
            session_token (str): The session token to use to execute the transaction block.
            wallet_id (str): The ID of the wallet to use to execute the transaction block.
            tx_bytes (str): The transaction bytes to use to execute the transaction block.
            gas_budget (int): The gas budget to use to execute the transaction block.
            request_type (str): The request type to use to execute the transaction block.
            full_response (bool, optional): Whether to return the full response or just the transaction ID. Defaults to False.
        """
        r = await self._make_post_request(
            f"{self.api_url}/wallet/v1",
            "shinami_wal_executeGaslessTransactionBlock",
            [
                wallet_id,
                session_token,
                tx_bytes,
                gas_budget,
                request_type,
            ],
        )

        if _is_error(r):
            raise Exception(json.dumps(r["error"]["data"]))
        else:
            return r

    async def _make_post_request(
        self,
        url: str,
        method: str,
        params: list[str],
        id: str | int | None = str(uuid.uuid4()),
    ) -> JsonRpcResponse:
        """
        Make a POST request to the Shinami API.

        Args:
            method (str): The method to call.
            params (list[str]): The parameters to pass to the method.
            id (str | int | None, optional): The ID of the request. Defaults to str(uuid.uuid4()).
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": id,
        }

        logger.info(payload)

        async with httpx.AsyncClient() as client:
            r = await client.post(
                url=url,
                json=payload,
                headers=self._generate_headers(),
            )

            logger.info(r.status_code)
            logger.info(r.json())

            if r.status_code == 401:
                raise ShinamiInvalidApiTokenException(
                    "Ser, your Shinami API token is invalid. Please provide a valid API token and try again."
                )

            r.raise_for_status()

        return JsonRpcResponse(**r.json())

    def _generate_headers(
        self,
    ) -> dict:
        return {
            "X-Api-Key": self.api_token,
            "Content-Type": "application/json",
        }
