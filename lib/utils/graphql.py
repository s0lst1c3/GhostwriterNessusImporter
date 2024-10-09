from gql import gql


def create_whoami_query():

    return gql(
        """
        query Whoami {
            whoami {
                username role expires
            }
        }
        """
    )
