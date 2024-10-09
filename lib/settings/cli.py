from argparse import ArgumentParser
from lib.types.namespace import Namespace


def get_options():

    parser = ArgumentParser()
    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        "--print-settings",
        action="store_true",
        dest="debug_print_settings",
        help="Print the settings and exit.",
    )
    log_group = parser.add_argument_group("Logging")
    log_group.add_argument(
        "--log-level", dest="logging_level", default=None, help="Set the log level"
    )
    log_group.add_argument(
        "--logfile", dest="logging_log_file", default=None, help="Set the logfile"
    )
    gw_group = parser.add_argument_group("Ghostwriter")
    gw_group.add_argument(
        "--gw-report-id",
        dest="ghostwriter_report_id",
        type=int,
        required=True,
        help="Set the Ghostwriter report ID",
    )
    gw_group.add_argument(
        "--gw-api-token",
        dest="ghostwriter_api_token",
        type=str,
        default=None,
        required=False,
        help="Set the Ghostwriter report ID",
    )
    gw_group.add_argument(
        "--gw-url",
        dest="ghostwriter_url",
        type=str,
        default=None,
        required=False,
        help="Set the Ghostwriter URL",
    )
    gw_group.add_argument(
        "--gw-throttle",
        dest="ghostwriter_throttle",
        type=int,
        default=0,
        help="Set throttle time in seconds between requests to Ghostwriter",
    )
    nessus_group = parser.add_argument_group("Nessus")
    nessus_group.add_argument(
        "--nessus-url",
        dest="nessus_url",
        type=str,
        default=None,
        required=False,
        help="Set the Nessus URL",
    )
    nessus_group.add_argument(
        "--nessus-user",
        dest="nessus_username",
        default=None,
        type=str,
        required=False,
        help="Set the Nessus username",
    )
    nessus_group.add_argument(
        "--nessus-pass",
        dest="nessus_password",
        default=None,
        type=str,
        required=False,
        help="Set the Nessus passname",
    )
    nessus_group.add_argument(
        "--nessus-retrieve",
        dest="nessus_retrieve",
        action="store_true",
        help="Retrieve nessus files from the server prior to parsing",
    )
    nessus_group.add_argument(
        "--nessus-files",
        dest="nessus_files",
        type=str,
        nargs="+",
        default=None,
        help="List of nessus files to parse",
    )
    nessus_group.add_argument(
        "--nessus-dir",
        dest="nessus_directory",
        type=str,
        default=None,
        help="List of nessus files to parse",
    )
    nessus_group.add_argument(
        "--exclude-hosts",
        dest="nessus_exclude_hosts",
        type=str,
        nargs="+",
        default=None,
        help="List of nessus files to parse",
    )
    args = parser.parse_args()

    options = {}
    for key, val in args.__dict__.items():

        if val is None:
            continue

        section, param_name = key.split("_", 1)
        options[section] = {**options.get(section, {}), param_name: val}

    return Namespace.from_dict(options)
