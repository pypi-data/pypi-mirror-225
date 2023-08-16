import argparse
import sys
import yaml
from djsciops import __version__ as version
from djsciops import authentication as djsciops_authentication
from djsciops import axon as djsciops_axon
from djsciops import settings as djsciops_settings
from djsciops.axon import speed_audit as djsciops_speed_audit


def djsciops(args: list = None):
    """
    Primary console interface for djsciops's shell utilities.

    :param args: List of arguments to be passed in, defaults to reading stdin
    :type args: list, optional
    """
    from djsciops.log import log

    parser = argparse.ArgumentParser(
        prog="djsciops", description="DataJoint SciOps console interface."
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"djsciops {version}"
    )
    command = parser.add_subparsers(dest="command")

    axon = command.add_parser("axon", description="Manage object store data.")
    axon_subcommand = axon.add_subparsers(dest="subcommand")

    axon_upload_agent = axon_subcommand.add_parser(
        "upload-agent",
        description="Upload objects in the background.",
    )
    axon_upload_agent_optional_named = axon_upload_agent.add_argument_group(
        "optional named arguments"
    )
    axon_upload_agent_optional_named.add_argument(
        "--one-off",
        action="store_true",
        dest="one_off",
        help="Upload mapping rules only once.",
    )
    axon_upload_agent_optional_named.add_argument(
        "rules",
        type=str,
        nargs="*",
        default=djsciops_axon._DEFAULT_UPLOAD_MAPPING_RULES,
        help="List of specific rules and check order to perform upload. Defaults to using all rules.",
    )
    axon_upload_agent_optional_named.add_argument(
        "-i",
        "--interval",
        type=int,
        default=djsciops_axon._DEFAULT_UPLOAD_MAPPING_INTERVAL,
        required=False,
        help="Time between every upload in seconds. Default to 21,600 (6 hours).",
    )
    axon_upload_agent_optional_named.add_argument(
        "-d",
        "--duration",
        type=int,
        default=djsciops_axon._DEFAULT_UPLOAD_MAPPING_DURATION,
        required=False,
        help="Stop uploading after a certain amount of time. Default to uploading indefinitely.",
    )

    axon_upload = axon_subcommand.add_parser(
        "upload", description="Copy objects by uploading to object store."
    )
    axon_upload_required_named = axon_upload.add_argument_group(
        "required named arguments"
    )
    axon_upload_required_named.add_argument(
        "source",
        type=str,
        help="Source file or directory on client.",
    )
    axon_upload_required_named.add_argument(
        "destination",
        type=str,
        help="Target directory in object store.",
    )
    axon_upload_optional_named = axon_upload.add_argument_group(
        "optional named arguments"
    )
    axon_upload_optional_named.add_argument(
        "-p",
        "--permit-regex",
        type=str,
        default=djsciops_axon._PERMIT_REGEX_DEFAULT,
        required=False,
        dest="permit_regex",
        help="Regular expression pattern to permit file(s) for uploading (default - all files permitted).",
    )
    axon_upload_optional_named.add_argument(
        "-i",
        "--ignore-regex",
        type=str,
        default=djsciops_axon._IGNORE_REGEX_DEFAULT,
        required=False,
        dest="ignore_regex",
        help="Regular expression pattern to ignore file(s) for uploading (default - no files ignored).",
    )

    axon_download = axon_subcommand.add_parser(
        "download", description="Download objects from object store."
    )
    axon_download_required_named = axon_download.add_argument_group(
        "required named arguments"
    )
    axon_download_required_named.add_argument(
        "source",
        type=str,
        help="Source file or directory in object store.",
    )
    axon_download_required_named.add_argument(
        "destination",
        type=str,
        help="Target directory on client.",
    )

    axon_download_optional_named = axon_download.add_argument_group(
        "optional named arguments"
    )
    axon_download_optional_named.add_argument(
        "-p",
        "--permit-regex",
        type=str,
        default=djsciops_axon._PERMIT_REGEX_DEFAULT,
        required=False,
        dest="permit_regex",
        help="Regular expression pattern to permit file(s) for downloading (default - all files permitted).",
    )
    axon_download_optional_named.add_argument(
        "-i",
        "--ignore-regex",
        type=str,
        default=djsciops_axon._IGNORE_REGEX_DEFAULT,
        required=False,
        dest="ignore_regex",
        help="Regular expression pattern to ignore file(s) for downloading (default - no files ignored).",
    )

    axon_speed_audit = axon_subcommand.add_parser(
        "speed-audit",
        description="Compare the speed of axon to the speed of the network.",
    )

    axon_speed_audit_optional_named = axon_speed_audit.add_argument_group(
        "optional named arguments"
    )
    axon_speed_audit_optional_named.add_argument(
        "-s",
        "--file-size",
        type=int,
        default=djsciops_speed_audit._DEFAULT_FILE_SIZE,
        required=False,
        dest="file_size",
        help=f"File size in MiB of generated file used during test. Defaults to {djsciops_speed_audit._DEFAULT_FILE_SIZE}.",
    )
    axon_speed_audit_optional_named.add_argument(
        "-d",
        "--down-limit",
        type=int,
        default=djsciops_speed_audit._DEFAULT_DOWN_LIMIT,
        required=False,
        dest="down_limit",
        help="Expected download bandwidth in Mbps. Defaults to skipping comparison.",
    )
    axon_speed_audit_optional_named.add_argument(
        "-u",
        "--up-limit",
        type=int,
        default=djsciops_speed_audit._DEFAULT_UP_LIMIT,
        required=False,
        dest="up_limit",
        help="Expected upload bandwidth in Mbps. Defaults to skipping comparison.",
    )

    axon_speed_audit_optional_named.add_argument(
        "-p",
        "--path",
        type=str,
        default=djsciops_speed_audit._DEFAULT_PATH,
        required=False,
        dest="path",
        help="Audit from a specific directory. Defaults to using local temporary directory.",
    )

    config = command.add_parser("config", description="View or modify djsciops config")

    config_optional_named = config.add_argument_group("optional named arguments")
    config_optional_named.add_argument(
        "key", type=str, nargs="?", default=None, help="Configuration key."
    )
    config_optional_named.add_argument(
        "value", type=str, nargs="?", default=None, help="New configuration value."
    )
    kwargs = vars(parser.parse_args(args if sys.argv[1:] else ["-h"]))
    djsciops_config = djsciops_settings.get_config()
    if kwargs["command"] == "axon":
        if kwargs["subcommand"] == "upload-agent":
            djsciops_axon.upload_continuously(
                one_off=kwargs["one_off"],
                session=djsciops_authentication.Session(
                    aws_account_id=djsciops_config["aws"]["account_id"],
                    s3_role=djsciops_config["s3"]["role"],
                    auth_client_id=djsciops_config["djauth"]["client_id"],
                    **(
                        {"auth_client_secret": c["client_secret"]}
                        if "client_secret" in (c := djsciops_config["djauth"])
                        else {}
                    ),
                ),
                upload_mapping_config=djsciops_config["axon"]["upload"],
                s3_bucket=djsciops_config["s3"]["bucket"],
                boto3_config=djsciops_config["boto3"],
                rules=kwargs["rules"],
                interval=kwargs["interval"],
                duration=kwargs["duration"],
            )
        elif kwargs["subcommand"] == "upload":
            djsciops_axon.upload_files(
                session=djsciops_authentication.Session(
                    aws_account_id=djsciops_config["aws"]["account_id"],
                    s3_role=djsciops_config["s3"]["role"],
                    auth_client_id=djsciops_config["djauth"]["client_id"],
                    **(
                        {"auth_client_secret": c["client_secret"]}
                        if "client_secret" in (c := djsciops_config["djauth"])
                        else {}
                    ),
                ),
                s3_bucket=djsciops_config["s3"]["bucket"],
                source=kwargs["source"],
                destination=kwargs["destination"],
                boto3_config=djsciops_config["boto3"],
                permit_regex=kwargs["permit_regex"],
                ignore_regex=kwargs["ignore_regex"],
            )
        elif kwargs["subcommand"] == "download":
            djsciops_axon.download_files(
                session=djsciops_authentication.Session(
                    aws_account_id=djsciops_config["aws"]["account_id"],
                    s3_role=djsciops_config["s3"]["role"],
                    auth_client_id=djsciops_config["djauth"]["client_id"],
                    **(
                        {"auth_client_secret": c["client_secret"]}
                        if "client_secret" in (c := djsciops_config["djauth"])
                        else {}
                    ),
                ),
                s3_bucket=djsciops_config["s3"]["bucket"],
                source=kwargs["source"],
                destination=kwargs["destination"],
                boto3_config=djsciops_config["boto3"],
                permit_regex=kwargs["permit_regex"],
                ignore_regex=kwargs["ignore_regex"],
            )
        elif kwargs["subcommand"] == "speed-audit":
            djsciops_speed_audit.speed_audit(
                **dict(
                    {k: v for k, v in kwargs.items() if "command" not in k},
                    aws_account_id=djsciops_config["aws"]["account_id"],
                    s3_bucket=djsciops_config["s3"]["bucket"],
                    region="us-east-2",
                    boto3_config=djsciops_config["boto3"],
                )
            )
    elif kwargs["command"] == "config":

        def _recursive_index(key, config_obj, mode="get"):
            if "." not in key:
                if mode == "get":
                    return config_obj[key]
                elif mode == "set":
                    return key, config_obj
            config_keys = key.split(".")
            return _recursive_index(
                ".".join(config_keys[1:]), config_obj[config_keys[0]], mode=mode
            )

        def _cast_input(s, key):
            if s.lower() == "true":
                return True
            elif s.lower() == "false":
                return False
            elif not s.isnumeric() or key == "aws.account_id":
                return s
            else:
                try:
                    return int(s)
                except ValueError:
                    return float(s)

        if kwargs["key"] and not kwargs["value"]:
            log.info(
                yaml.dump(_recursive_index(kwargs["key"], djsciops_config)),
                extra={"disable_format": True},
            )

        elif kwargs["key"] and kwargs["value"]:
            curr_key, curr_object = _recursive_index(
                kwargs["key"], djsciops_config, mode="set"
            )
            curr_object[curr_key] = _cast_input(kwargs["value"], kwargs["key"])
            config_directory = djsciops_settings.appdirs.user_data_dir(
                appauthor="datajoint", appname="djsciops"
            )
            djsciops_settings.save_config(yaml.dump(djsciops_config), config_directory)

        else:
            log.info(yaml.dump(djsciops_config), extra={"disable_format": True})
    raise SystemExit


if __name__ == "__main__":
    djsciops()
