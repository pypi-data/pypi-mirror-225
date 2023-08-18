from __future__ import annotations

import python_graphql_client
import logging
from typing import Dict, List
import pendulum
from sumatra_client.auth import CognitoJwtAuth
from sumatra_client.config import CONFIG
from sumatra_client.base import BaseClient

logger = logging.getLogger("sumatra.cli")


class AdminClient(BaseClient):
    """
    Admin Client to connect to Sumatra GraphQL API as an instance administrator.
    Not creatable if you are not logged in as an admin user.

    __Humans:__ First, log in via the CLI: `sumatra login`
    """

    def __init__(self):
        super().__init__(
            client=python_graphql_client.GraphqlClient(
                auth=CognitoJwtAuth("_new"), endpoint=CONFIG.console_graphql_url
            ),
        )
        if not self._is_admin():
            raise ValueError(
                "Unable to create an AdminClient when not logged in as an instance admin."
            )

    def _is_admin(self) -> bool:
        logger.debug("Fetching currentUser")
        query = """
        query CurrentUser {
            currentUser {
                admin
            }
        }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["currentUser"]["admin"]

    def upgrade_tenant(self, tenant: str) -> None:
        """
        Upgrade tenant to paid tier.

        Arguments:
            tenant: The slug of the tenant to upgrade.
        """
        query = """
            mutation UpgradeTenant($id: String!) {
                upgradeTenant(id: $id) {
                    id
                }
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={"id": self._tenant_id_from_slug(tenant)},
            headers={"x-sumatra-tenant": tenant},
        )

    def downgrade_tenant(self, tenant: str) -> None:
        """
        Downgrade tenant to free tier.

        Arguments:
            tenant: The slug of the tenant to downgrade.
        """
        query = """
            mutation DowngradeTenant($id: String!) {
                downgradeTenant(id: $id) {
                    id
                }
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={"id": self._tenant_id_from_slug(tenant)},
            headers={"x-sumatra-tenant": tenant},
        )

    def set_quota(self, tenant: str, monthly_events: int) -> None:
        """
        Set quota for tenant.
        """
        query = """
            mutation SetQuota($id: String!, $monthlyEvents: Int!) {
                updateTenant(id: $id, monthlyEvents: $monthlyEvents) {
                    id
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={
                "id": self._tenant_id_from_slug(tenant),
                "monthlyEvents": monthly_events,
            },
            headers={"x-sumatra-tenant": tenant},
        )

    def list_users(self) -> List[str]:
        """
        List all users on instance.
        """
        query = """
            query ListUsers {
                users(first: 60) {
                    nodes {
                        username
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query)

        return [user["username"] for user in ret["data"]["users"]["nodes"]]

    def get_user(self, username: str) -> Dict[str, str]:
        """
        Get metadata for user.
        """
        query = """
            query User($username: String!) {
                user(username: $username) {
                    username
                    email
                    admin
                    status
                    sso
                }
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={
                "username": username,
            },
        )

        return ret["data"]["user"]

    def _tenant_id_from_slug(self, slug: str) -> str:
        query = """
            query TenantIDFromSlug($slug: String!) {
                tenantIdFromSlug(slug: $slug)
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={
                "slug": slug,
            },
        )

        id = ret["data"]["tenantIdFromSlug"]
        if not id:
            raise ValueError(f"Unknown slug {slug}")
        return id

    def list_tenants(self) -> None:
        """
        List all tenants on instance.
        """
        query = """
                query ListTenants {
                    tenants {
                        nodes {
                            key
                        }
                    }
                }
            """

        ret = self._execute_graphql(query=query)

        return [tenant["key"] for tenant in ret["data"]["tenants"]["nodes"]]

    def set_user_role(self, email: str, tenant: str, role: str) -> Dict:
        """
        Set user role for tenant. Adds the user to the tenant if they are not already a member.
        """
        tenant = self._tenant_id_from_slug(tenant)
        query = """
            mutation SetUserRole($email: String!, $tenant: String!, $role: String!) {
                setUserRoleInTenant(email: $email, tenant: $tenant, role: $role) {
                    email
                    role
                    createdAt
		            updatedAt
		            creator
		            tenantSlug
                }
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={
                "email": email,
                "tenant": tenant,
                "role": role,
            },
        )

        d = ret["data"]["setUserRoleInTenant"]
        return {
            "email": d["email"],
            "role": d["role"],
            "create_ts": pendulum.parse(d["createdAt"]),
            "update_ts": pendulum.parse(d["updatedAt"]),
            "creator": d["creator"],
            "tenant": d["tenantSlug"],
        }

    def remove_user_from_tenant(self, email: str, tenant: str) -> Dict:
        """
        Remove the user from a tenant.
        """
        tenant = self._tenant_id_from_slug(tenant)
        query = """
            mutation RemoveUserFromTenant($email: String!, $tenant: String!) {
                removeUserFromTenant(email: $email, tenant: $tenant) {
                    email
                    role
                    createdAt
		            updatedAt
		            creator
		            tenantSlug
                }
            }
        """

        ret = self._execute_graphql(
            query=query,
            variables={
                "email": email,
                "tenant": tenant,
            },
        )

        d = ret["data"]["removeUserFromTenant"]
        return {
            "email": d["email"],
            "role": d["role"],
            "create_ts": pendulum.parse(d["createdAt"]),
            "update_ts": pendulum.parse(d["updatedAt"]),
            "creator": d["creator"],
            "tenant": d["tenantSlug"],
        }
