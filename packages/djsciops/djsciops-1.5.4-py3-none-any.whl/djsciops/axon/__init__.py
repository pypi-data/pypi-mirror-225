import pathlib
import os
import boto3.s3.transfer
import tqdm
import re
from typing import Union
from djsciops import utils as djsciops_utils
from djsciops import settings as djsciops_settings
import collections.abc
import logging
from djsciops.log import log, TqdmToLogger
from datetime import datetime, timedelta
import time

_PERMIT_REGEX_DEFAULT = r".*"
_IGNORE_REGEX_DEFAULT = r"no-match^"
_DEFAULT_UPLOAD_MAPPING_RULES = ...
_DEFAULT_UPLOAD_MAPPING_INTERVAL = 60 * 60 * 6
_DEFAULT_UPLOAD_MAPPING_DURATION = None


def upload_continuously(
    session,
    s3_bucket: str,
    upload_mapping_config,
    boto3_config: dict = None,
    rules=_DEFAULT_UPLOAD_MAPPING_RULES,
    interval=_DEFAULT_UPLOAD_MAPPING_INTERVAL,
    duration=_DEFAULT_UPLOAD_MAPPING_DURATION,
    one_off=False,
):
    def _upload_single():
        source, destination = _generate_upload_mapping(
            upload_mapping_config=upload_mapping_config, rules=rules
        )
        upload_files(
            session=session,
            s3_bucket=s3_bucket,
            source=source,
            destination=destination,
            boto3_config=boto3_config,
        )

    if one_off:
        _upload_single()
    else:
        start_time = datetime.now()
        while (
            (datetime.now() <= start_time + timedelta(seconds=duration))
            if duration
            else True
        ):
            time.sleep(interval - time.time() % interval)
            _upload_single()


def _generate_upload_mapping(upload_mapping_config: dict, rules: list) -> tuple:
    rules = (
        upload_mapping_config["rules"]
        if rules is ...
        else [
            r
            for user_rule in rules
            for r in upload_mapping_config["rules"]
            if user_rule == r["name"]
        ]
    )
    upload_mapping = {
        pathlib.Path(path): pathlib.PurePosixPath(rule["destination_directory"])
        / pattern["destination_format"].format(**match.groupdict())
        for rule in list(reversed(rules))
        for pattern in list(reversed((rule["patterns"])))
        for path in pathlib.Path(rule["source_directory"]).glob("**/*")
        if (match := re.match(pattern["match_regex"], str(path)))
    }

    return list(upload_mapping), list(upload_mapping.values())


def _resolve_upload_mapping(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
    *,
    permit_regex=_PERMIT_REGEX_DEFAULT,
    ignore_regex=_IGNORE_REGEX_DEFAULT,
) -> tuple:
    if (
        isinstance(source, list)
        and isinstance(destination, list)
        and len(source) == len(destination)
    ):
        log.debug("Upload mapping provided.")
        # expect file_paths to be list of Path, object_paths to be list of PurePosixPath
        file_paths, object_paths = (source, destination)
        existing_objects = {
            pathlib.PurePosixPath(op.key)
            for op in session.s3.Bucket(s3_bucket).objects.filter(
                Prefix=os.path.commonprefix(object_paths)
            )
        }
        results = tuple(
            zip(
                *(
                    (fp, op)
                    for fp, op in zip(file_paths, object_paths)
                    if (
                        op not in existing_objects
                        and re.match(permit_regex, fp.as_posix())
                        and not re.match(ignore_regex, fp.as_posix())
                    )
                )
            )
        )
        if not results:
            file_paths, object_paths = (None, None)
        else:
            file_paths, object_paths = results
    else:
        # modes: file -> directory, directory -> directory
        assert destination[-1] == "/", "Must point to a directory in object store."
        source = pathlib.Path(source).resolve()
        # recursively list files that are not hidden or directories
        file_paths = {
            relative_fp
            for fp in source.rglob("*")
            if (
                fp.is_file()
                and not fp.name.startswith(".")
                and re.match(
                    permit_regex,
                    (
                        relative_fp := pathlib.PurePosixPath(fp.relative_to(source))
                    ).as_posix(),
                )
                and not re.match(ignore_regex, relative_fp.as_posix())
            )
        }
        file_paths = file_paths or set(
            [pathlib.PurePosixPath(source.name)]
            if re.match(permit_regex, source.name)
            and not re.match(ignore_regex, source.name)
            else []
        )  # if specified a single file
        # recursively list objects
        existing_objects = {
            pathlib.PurePosixPath(op.key.replace(destination, ""))
            for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=destination)
        }
        # exclude objects that exist and verify that new objects are present
        file_paths = file_paths - existing_objects
        log.debug(f"file_paths: {file_paths}")
        if not file_paths:
            return [], []
        object_paths = [pathlib.PurePosixPath(destination, fp) for fp in file_paths]
        file_paths = [
            pathlib.Path(source if source.is_dir() else source.parent, fp)
            for fp in file_paths
        ]

    return file_paths, object_paths


def _resolve_download_mapping(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
    *,
    permit_regex=_PERMIT_REGEX_DEFAULT,
    ignore_regex=_IGNORE_REGEX_DEFAULT,
) -> tuple:
    if (
        isinstance(source, list)
        and isinstance(destination, list)
        and len(source) == len(destination)
    ):
        log.debug("Download mapping provided.")
        # expect file_paths to be list of Path, object_paths to be list of PurePosixPath
        object_paths, file_paths = (source, destination)
        existing_files = {
            fp
            for fp in pathlib.Path(os.path.commonprefix(file_paths)).glob("**/*")
            if fp.is_file()
        }
        file_paths, object_paths = tuple(
            zip(
                *(
                    (fp, op)
                    for fp, op in zip(file_paths, object_paths)
                    if (
                        fp not in existing_files
                        and re.match(permit_regex, op.as_posix())
                        and not re.match(ignore_regex, op.as_posix())
                    )
                )
            )
        )

    else:
        # modes: file -> directory, directory -> directory
        assert destination[-1] == (
            "/" if os.name == "posix" else "\\"
        ), "Must point to a local directory"
        destination = pathlib.Path(destination).resolve()
        log.debug(f"destination: {destination}")
        # recursively list objects
        object_root = s.parent if (s := pathlib.PurePosixPath(source)).suffix else s
        object_paths = {
            relative_op
            for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=source)
            if (
                re.match(
                    permit_regex,
                    (
                        relative_op := pathlib.PurePosixPath(op.key).relative_to(
                            object_root
                        )
                    ).as_posix(),
                )
                and not re.match(ignore_regex, relative_op.as_posix())
            )
        }
        log.debug(f"object_paths: {object_paths}")
        # recursively list files that are not hidden or directories
        existing_objects = {
            fp.relative_to(destination)
            for fp in destination.rglob("*")
            if not fp.is_dir() and not str(fp.name).startswith(".")
        }
        log.debug(f"existing_objects: {existing_objects}")
        existing_objects = (
            {pathlib.PurePosixPath(_) for _ in existing_objects}
            if existing_objects
            else {pathlib.PurePosixPath(destination.name)}
        )  # if specified a single file
        # exclude objects that exist and verify that new objects are present
        object_paths = object_paths - existing_objects
        if not object_paths:
            return [], []
        file_paths = [pathlib.Path(destination, op) for op in object_paths]
        log.debug(f"file_paths: {file_paths}")
        object_paths = [pathlib.PurePosixPath(object_root, op) for op in object_paths]

    return object_paths, file_paths


def list_files(
    session,
    s3_bucket: str,
    s3_prefix: str,
    *,
    permit_regex=_PERMIT_REGEX_DEFAULT,
    ignore_regex=_IGNORE_REGEX_DEFAULT,
    include_contents_hash=False,
    as_tree=True,
):
    objects = [
        dict(
            key=op.key,
            _size=op.size,
            _contents_hash=op.Object().metadata["contents_hash"]
            if include_contents_hash
            else None,
        )
        for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=s3_prefix)
        if (
            re.match(permit_regex, op.key.replace(s3_prefix, ""))
            and not re.match(ignore_regex, op.key.replace(s3_prefix, ""))
        )
    ]
    objects = sorted(objects, key=lambda o: o["key"])

    if not as_tree:
        return objects

    tree = {}
    for o in objects:
        node = tree  # local node
        levels = o["key"].split("/")
        for level in levels:
            node = node.setdefault(level, dict())
            node["_size"] = (
                o["_size"] + node["_size"] if "_size" in node else o["_size"]
            )

    def update(d):
        for k, v in d.items():
            if isinstance(v, collections.abc.Mapping) and len(v) > 1:
                if k not in ("_size"):
                    _ = d[k].pop("_size")
                    d[k] = update(d.get(k, {}))
            else:
                d[k] = None
        return d

    return update(tree)


def upload_files(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
    boto3_config: dict = None,
    *,
    permit_regex=_PERMIT_REGEX_DEFAULT,
    ignore_regex=_IGNORE_REGEX_DEFAULT,
):
    """
    Args:
        session: An instance of authentication.Session to access S3 resources
        s3_bucket: Name of the S3 bucket
        source: Source file or directory on client.
        destination: Target directory in object store.
        permit_regex: Regular expression pattern to permit file(s) for uploading (default - all files permitted)
        ignore_regex: Regular expression pattern to ignore file(s) for uploading (default - no files ignored)
    """
    if not boto3_config:
        boto3_config = djsciops_settings.get_config()["boto3"]

    file_paths, object_paths = _resolve_upload_mapping(
        session=session,
        s3_bucket=s3_bucket,
        source=source,
        destination=destination,
        permit_regex=permit_regex,
        ignore_regex=ignore_regex,
    )
    if not file_paths or not object_paths:
        log.warning("All upload-permitted files already exist in object store.")
        return
    log.debug("Starting upload")
    with tqdm.tqdm(
        total=sum(os.stat(fp).st_size for fp in file_paths),
        unit="B",
        unit_scale=True,
        desc="",
        mininterval=5,
        file=TqdmToLogger(log, level=logging.INFO),
    ) as pbar:
        for fp, op in zip(file_paths, object_paths):
            log.info(f"{fp}->{op}")
            ## hash metadata
            contents_hash = djsciops_utils.uuid_from_file(fp)
            log.debug(f"contents_hash.hex: {contents_hash.hex}")
            ## upload
            session.s3.Bucket(s3_bucket).upload_file(
                Filename=str(fp),
                Key=str(op),
                Config=boto3.s3.transfer.TransferConfig(**boto3_config),
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
                ExtraArgs={"Metadata": {"contents_hash": contents_hash.hex}},
            )


def download_files(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
    boto3_config: dict = None,
    *,
    permit_regex=_PERMIT_REGEX_DEFAULT,
    ignore_regex=_IGNORE_REGEX_DEFAULT,
):
    """

    Args:
        session: An instance of authentication.Session to access S3 resources
        s3_bucket: Name of the S3 bucket
        source: Source file or directory in object store.
        destination: Target directory on client.
        permit_regex: Regular expression pattern to permit file(s) for downloading (default - all files permitted)
        ignore_regex: Regular expression pattern to ignore file(s) for downloading (default - no files ignored)
    """

    if not boto3_config:
        boto3_config = djsciops_settings.get_config()["boto3"]

    object_paths, file_paths = _resolve_download_mapping(
        session=session,
        s3_bucket=s3_bucket,
        source=source,
        destination=destination,
        permit_regex=permit_regex,
        ignore_regex=ignore_regex,
    )
    if not file_paths or not object_paths:
        log.warning("All download-permitted files already exist locally.")
        return
    log.debug("Starting download")
    with tqdm.tqdm(
        total=sum(
            session.s3.Object(s3_bucket, str(op)).content_length for op in object_paths
        ),
        unit="B",
        unit_scale=True,
        desc="",
        mininterval=5,
        file=TqdmToLogger(log, level=logging.INFO),
    ) as pbar:
        for op, fp in zip(object_paths, file_paths):
            log.info(f"{op}->{fp}")
            # check if dir exists
            if not os.path.exists(os.path.dirname(fp)):
                os.makedirs(os.path.dirname(fp))
            ## download
            session.s3.Bucket(s3_bucket).download_file(
                Key=str(op),
                Filename=str(fp),
                Config=boto3.s3.transfer.TransferConfig(**boto3_config),
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
            )
