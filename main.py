from asyncio.exceptions import TimeoutError
from gql.transport.exceptions import TransportServerError, TransportQueryError
from graphql.error.graphql_error import GraphQLError
from lib.ghostwriter import GhostwriterClient
from lib.logging import Logger
from lib.nessus import NessusFileParser
from lib.settings import settings
import sys


def add_findings_to_gw(gw_findings):

    logger = Logger()

    try:
        gw_client = GhostwriterClient()

        response = gw_client.authenticate()
        logger.info(
            f"Authenticated as {response['whoami']['username']}",
            extra={"response": response},
        )

        for finding in gw_findings:
            response = gw_client.execute(
                finding.query,
                variable_values=finding.variable_values,
                serialize_variables=True,
            )
            logger.info(
                f"Added finding: {finding.title}",
                extra={"response": response},
            )

    except GraphQLError as e:
        logger.error(f"GraphQL error: {e}")
    except TimeoutError as e:
        logger.error(f"GraphQL transport query timed out: {e}")
    except TransportQueryError as e:
        logger.error(f"GraphQL transport query error: {e}")
    except TransportServerError as e:
        logger.error(f"GraphQL transport server error: {e}")


def parse_nessus_reports():
    parser = NessusFileParser()
    parser.read_findings()
    return parser.get_gw_findings()


def main():

    if settings.debug.print_settings:
        print(settings)
        sys.exit()

    findings = parse_nessus_reports()
    add_findings_to_gw(findings)


if __name__ == "__main__":
    main()
