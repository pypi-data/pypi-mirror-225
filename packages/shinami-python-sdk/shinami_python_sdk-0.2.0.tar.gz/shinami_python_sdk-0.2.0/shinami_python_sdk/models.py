from typing import Optional

from pydantic import BaseModel


class JsonRpcResponse(BaseModel):
    jsonrpc: str
    result: Optional[dict | str] = None
    error: Optional["JsonRpcResponseError"] = None
    id: Optional[str | int]


class JsonRpcResponseError(BaseModel):
    code: int
    message: str
    data: Optional[dict | str] = None


JsonRpcResponse.update_forward_refs()


class ShinamiWallet(BaseModel):
    id: str
    address: str
