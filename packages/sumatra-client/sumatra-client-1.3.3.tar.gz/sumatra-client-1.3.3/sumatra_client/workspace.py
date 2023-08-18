import python_graphql_client
import pandas as pd
from logging import getLogger
from typing import Optional
from sumatra_client.auth import CognitoJwtAuth
from sumatra_client.config import CONFIG
from sumatra_client.base import BaseClient

logger = getLogger("sumatra.config")


class WorkspaceClient(BaseClient):
    """
    Client to manage workspaces.

    __Humans:__ First, log in via the CLI: `sumatra login`

    __Bots:__ Sorry, no bots allowed

    """

    def __init__(self):
        """
        Create connection object.
        """
        super().__init__(
            client=python_graphql_client.GraphqlClient(
                auth=CognitoJwtAuth("_new"), endpoint=CONFIG.console_graphql_url
            ),
        )

    def get_workspaces(self) -> pd.DataFrame:
        """
        Return workspaces, along with metadata, that the current user has access to

        Returns:
            Dataframe of workspace metadata
        """
        logger.debug("Fetching workspaces")
        query = """
            query CurrentUser($after: String) {
                currentUser {
                    availableRoles(first: 100, after: $after) {
                        nodes {
                            tenant
                            tenantSlug
                            tenantName
                            role
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        """

        variables = {"after": None}
        has_next_page = True
        rows = []
        while has_next_page:
            ret = self._execute_graphql(
                query=query,
                variables=variables,
            )

            for workspace in ret["data"]["currentUser"]["availableRoles"]["nodes"]:
                rows.append(
                    {
                        "workspace": workspace["tenantSlug"],
                        "nickname": workspace["tenantName"],
                        "role": workspace["role"],
                        "tenant_id": workspace["tenant"],
                    }
                )
            has_next_page = ret["data"]["currentUser"]["availableRoles"]["pageInfo"]["hasNextPage"]
            variables["after"] = ret["data"]["currentUser"]["availableRoles"]["pageInfo"]["endCursor"]
        return (
            pd.DataFrame(rows, columns=["workspace", "nickname", "role", "tenant_id"])
            .set_index("workspace")
            .sort_index()
        )

    def create_workspace(self, workspace: str, nickname: Optional[str] = None) -> str:
        """
        Create a new workspace.

        Arguments:
            workspace: Desired slug of the new workspace. Must consist only of letters, numbers, '-', and '_'. If this slug is taken, a random one will be generated instead, which may be changed later.
            nickname: A human readable name for the new workspace. If not provided, the workspace slug will be used.

        Returns:
            name (slug) of newly created workspace
        """

        query = """
            mutation CreateWorkspace($name: String!, $slug: String!) {
                createTenant(name: $name, slug: $slug) {
                    slug
                }
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={"name": nickname or workspace, "slug": workspace},
        )

        return ret["data"]["createTenant"]["slug"]

    def delete_workspace(self, workspace: str) -> None:
        """
        Deletes the workspace and all associated data. You must be an owner of the workspace to delete it.

        Warning: This action is not reversible!

        Arguments:
            workspace: Slug of the workspace to delete.
        """

        query = """
            mutation DeleteWorkspace {
                deleteTenant {
                    id
                }
            }
        """

        try:
            ret = self._execute_graphql(
                query=query,
                headers={"x-sumatra-tenant": workspace},
            )
        except RuntimeError as e:
            if str(e) == "Schema is not configured for mutations":
                raise ValueError(f"Workspace '{workspace}' not found.")

    def _old_tenant(self) -> str:
        logger.debug("Fetching tenant the old-fashioned way")
        query = """
            query Tenant {
                tenant {
                    key
                }
            }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["tenant"]["key"]
