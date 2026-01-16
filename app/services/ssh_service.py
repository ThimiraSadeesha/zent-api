import paramiko
from typing import Optional
import logging
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

logger = logging.getLogger(__name__)

def ssh_connect(host: str, username: str, password: Optional[str] = None, port: int = 22, key: Optional[str] = None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key:
            pkey = paramiko.RSAKey.from_private_key_file(key)
            client.connect(hostname=host, username=username, pkey=pkey, port=port, timeout=10)
        else:
            client.connect(hostname=host, username=username, password=password, port=port, timeout=10)

        logger.info(f"✅ SSH login successful: {username}@{host}:{port}")
        return client

    except Exception as e:
        logger.error(f"❌ SSH login failed: {username}@{host}:{port} | {str(e)}")
        return None
