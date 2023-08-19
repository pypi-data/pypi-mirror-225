import commonbase.completion
import os

base_url = os.getenv("CB_DEV_API_BASE_URL")
if base_url is not None:
    commonbase.completion._API_BASE_URL = base_url  # type: ignore
