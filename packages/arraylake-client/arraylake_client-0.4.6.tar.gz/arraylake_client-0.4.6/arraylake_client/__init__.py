import importlib.metadata
import os
import warnings

if not os.getenv("ZARR_V3_EXPERIMENTAL_API"):
    warnings.warn("ZARR_V3_EXPERIMENTAL_API must be set before importing the arraylake client")

from arraylake_client.client import AsyncClient, Client
from arraylake_client.config import config

__version__ = importlib.metadata.version("arraylake_client")
