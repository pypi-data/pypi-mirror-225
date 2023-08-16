import pathlib
import tempfile
import time
from datetime import datetime
import speedtest
from djsciops import authentication
from djsciops import axon
from djsciops.log import log
from djsciops import settings as djsciops_settings
from minio import Minio
from minio.credentials import WebIdentityProvider

_DEFAULT_FILE_SIZE = 256
_DEFAULT_UP_LIMIT = None
_DEFAULT_DOWN_LIMIT = None
_DEFAULT_PATH = None


def speed_audit(
    aws_account_id: str,
    s3_bucket: str,
    region: str,
    boto3_config: dict,
    file_size: int = _DEFAULT_FILE_SIZE,
    up_limit: int = _DEFAULT_UP_LIMIT,
    down_limit: int = _DEFAULT_DOWN_LIMIT,
    path: str = _DEFAULT_PATH,
):
    def perform_network_test(description: str, downloads: list, uploads: list) -> tuple:
        log.info(f"Starting {description} network test...")
        return downloads + [st.download() / 10**6], uploads + [st.upload() / 10**6]

    def time_it(function):
        start_time = time.time()
        function()
        return time.time() - start_time

    def display(direction, unit, network, s3, axon, bandwidth=None):
        custom_round = lambda x: x if isinstance(x, str) else round(x, 2)
        constant = 100 / bandwidth if bandwidth else 1
        network_string = (
            f"Network: {custom_round(network*constant)} {unit}, " if network else ""
        )
        log.info(
            f"{direction} => {network_string}S3: {custom_round(s3*constant)} {unit}, Axon: {custom_round(axon*constant)} {unit}"
        )

    log.info("Initializing test...")
    session_data = {
        "aws_account_id": aws_account_id,
        "s3_role": "axon_speed_audit",
        "auth_client_id": "axon-speed-audit",
        "auth_client_secret": "axon-speed-audit",
    }
    s3_directory = pathlib.PurePosixPath("test/axon/speed-audit")
    name = "speed-audit-{size}{suffix}.tmp"
    remote_path = s3_directory / name.format(
        size=file_size, suffix=f"-{int(datetime.utcnow().timestamp())}"
    )
    local_path = pathlib.Path(path or f"{tempfile.gettempdir()}/axon") / name.format(
        size=file_size, suffix=""
    )
    log.debug(f"local_path: {local_path}")
    if not path:
        local_path.parent.mkdir(parents=True, exist_ok=True)
    byte_length = file_size * 1024**2
    if local_path.is_file():
        log.debug("Found test file. Skipping generating file.")
    else:
        log.debug(f"Generating {file_size} MiB file...")
        with open(local_path, "wb") as f:
            f.seek(byte_length - 1)
            f.write(("\0").encode())
    session = authentication.Session(**session_data)
    provider = WebIdentityProvider(
        jwt_provider_func=lambda: {"access_token": session.bearer_token},
        sts_endpoint="https://sts.amazonaws.com:443",
        role_arn=f"arn:aws:iam::{session_data['aws_account_id']}:role/{session_data['s3_role']}",
    )
    client = Minio(
        endpoint="s3-accelerate.amazonaws.com:443", region=region, credentials=provider
    )
    download, upload = ([], [])
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        enable_network_test = True
    except speedtest.ConfigRetrievalError:
        log.warning("Network speed test temporarily unavailable!")
        enable_network_test = False
    # Run tests
    if enable_network_test:
        download, upload = perform_network_test("first", download, upload)
    log.info("Running axon upload test...")
    axon_up_time = time_it(
        lambda: axon.upload_files(
            session, s3_bucket, [local_path], [remote_path], boto3_config
        )
    )
    log.info("Running S3 upload test...")
    s3_up_time = time_it(
        lambda: client.fput_object(s3_bucket, str(remote_path), str(local_path))
    )
    local_path.unlink()
    if enable_network_test:
        download, upload = perform_network_test("second", download, upload)
    log.info("Starting S3 download test...")
    s3_down_time = time_it(
        lambda: client.fget_object(s3_bucket, str(remote_path), str(local_path))
    )
    log.info("Starting axon download test...")
    axon_down_time = time_it(
        lambda: axon.download_files(
            session, s3_bucket, [remote_path], [local_path], boto3_config
        )
    )
    if enable_network_test:
        download, upload = perform_network_test("final", download, upload)
    # Summarize results
    net_up_speed = sum(upload) / len(upload) if enable_network_test else None
    net_down_speed = sum(download) / len(download) if enable_network_test else None
    s3_up_speed = byte_length * 8 / 10**6 / s3_up_time
    s3_down_speed = byte_length * 8 / 10**6 / s3_down_time
    axon_up_speed = byte_length * 8 / 10**6 / axon_up_time
    axon_down_speed = byte_length * 8 / 10**6 / axon_down_time
    if up_limit:
        display("Upload", "%", net_up_speed, s3_up_speed, axon_up_speed, up_limit)
    if down_limit:
        display(
            "Download", "%", net_down_speed, s3_down_speed, axon_down_speed, down_limit
        )
    display("Upload", "Mbps", net_up_speed, s3_up_speed, axon_up_speed)
    display("Download", "Mbps", net_down_speed, s3_down_speed, axon_down_speed)
