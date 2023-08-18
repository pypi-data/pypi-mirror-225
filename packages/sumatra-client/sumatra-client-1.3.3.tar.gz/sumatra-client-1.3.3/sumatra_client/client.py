from __future__ import annotations

import os
import re
import time
import json
import logging
import awswrangler as wr
import boto3
import gzip
import pendulum
import python_graphql_client
import pandas as pd
import requests
import base64
from time import sleep
from datetime import datetime
from typing import Any, Optional, Dict, List, Union, Tuple
from tqdm.auto import tqdm
from requests.auth import AuthBase
from sumatra_client.auth import SDKKeyAuth, CognitoJwtAuth
from sumatra_client.config import CONFIG
from sumatra_client.workspace import WorkspaceClient
from sumatra_client.base import BaseClient

logger = logging.getLogger("sumatra.client")

TENANT_PREFIX = "sumatra_"
DEPS_FILE = "deps.scowl"
TABLE_NAME_REGEXP = re.compile("^[a-z][a-zA-Z0-9_]*$")


def parse_timestamp_columns(df, columns):
    df = df.copy()
    for col in columns:
        times = []
        for t in df[col]:
            ts = "NaT"
            try:
                ts = (
                    pendulum.parse(t)
                    .astimezone(pendulum.timezone("UTC"))
                    .to_iso8601_string()
                )
            except:
                pass
            times.append(ts)
        df[col] = times
        df[col] = pd.to_datetime(df[col], unit="ns")
        if df[col].dt.tz is None:
            df[col] = df[col].dt.tz_localize("UTC")
        df[col] = df[col].dt.tz_convert(CONFIG.timezone)
    return df


def tz_convert_timestamp_columns(df):
    df = df.copy()
    for col in df.columns:
        if hasattr(df[col], "dt"):
            try:
                df[col] = df[col].dt.tz_localize("UTC")
            except:
                pass
            df[col] = df[col].dt.tz_convert(CONFIG.timezone)
    return df


def _load_scowl_files(dir: str) -> Dict[str, str]:
    scowls = {}
    for fname in os.listdir(dir):
        if fname.endswith(".scowl") and fname != DEPS_FILE:
            scowl = open(os.path.join(dir, fname)).read()
            scowls[fname] = scowl
    return scowls


def _splitext(path: str):
    fullext = ""
    while True:
        path, ext = os.path.splitext(path)
        if ext:
            fullext = ext + fullext
        else:
            break
    return os.path.basename(path), fullext


def _humanize_status(status: str):
    """
    Translate server-side status to human-readable, standardized identifier
    """
    standardize = {
        "New": "Processing",
        "Running": "Processing",
        "Offline": "Processing",
        "Online": "Ready",
    }
    if status in standardize:
        return standardize[status]
    return status.title()


class Client(BaseClient):
    """
    Client to connect to Sumatra GraphQL API

    __Humans:__ First, log in via the CLI: `sumatra login`

    __Bots:__ Set the `SUMATRA_INSTANCE` and `SUMATRA_SDK_KEY` environment variables
    """

    def __init__(
        self,
        instance: Optional[str] = None,
        branch: Optional[str] = None,
        workspace: Optional[str] = None,
    ):
        """
        Create connection object.

        Arguments:
            instance: Sumatra instance url, e.g. `yourco.sumatra.ai`. If unspecified, the your config default will be used.
            branch: Set default branch. If unspecified, your config default will be used.
            workspace: Sumatra workspace name to connect to.
        """
        if instance:
            CONFIG.instance = instance
        self._branch = branch or CONFIG.default_branch
        self._workspace_arg = workspace or CONFIG.workspace
        self._workspace = None
        self._workspace_id = None
        if CONFIG.sdk_key:
            logger.info("Connecting via SDK key")
            auth: AuthBase = SDKKeyAuth()
            endpoint = CONFIG.sdk_graphql_url
        else:
            auth = CognitoJwtAuth(self.workspace)
            endpoint = CONFIG.console_graphql_url
        super().__init__(
            client=python_graphql_client.GraphqlClient(
                auth=auth, endpoint=endpoint
            ),
        )

    def _choose_workspace(self) -> Tuple[Optional[str], Optional[str]]:
        if CONFIG.sdk_key:
            sdk_key_workspace, tenant_id = self._get_workspace_from_sdk_key()
            if self._workspace_arg and sdk_key_workspace != self._workspace_arg:
                raise ValueError(
                    f"SDK Key's workspace: '{sdk_key_workspace}' does not match "
                    f"chosen workspace: '{self._workspace_arg}'."
                )
            return sdk_key_workspace, tenant_id
        try:
            workspaces = WorkspaceClient().get_workspaces()
        except RuntimeError:  # TODO: this is a hack to support v1.2.X
            tenant_id = WorkspaceClient()._old_tenant()
            return tenant_id, tenant_id
        if self._workspace_arg:
            if self._workspace_arg not in workspaces.index:
                raise ValueError(
                    f"Workspace '{self._workspace_arg}' not found. "
                    f"Choose one of: {workspaces.index.tolist()}."
                )
            ws = workspaces.loc[self._workspace_arg]
            return ws.name, ws.tenant_id
        if len(workspaces) == 1:
            ws = workspaces.iloc[0]
            return ws.name, ws.tenant_id
        if len(workspaces) > 1:
            raise RuntimeError(
                "Unable to determine workspace. "
                "Specify a workspace or run `sumatra workspace select`."
            )
        raise RuntimeError("No workspaces found. Run `sumatra workspace create` first.")

    def _get_workspace_from_sdk_key(self):
        logger.debug("Fetching workspace from SDK key")
        query = """
            query Workspace {
                workspace {
                    id
                    slug
                }
            }
        """

        ret = self._execute_graphql(query=query)

        d = ret["data"]["workspace"]
        return d["slug"], d["id"]

    @property
    def instance(self) -> str:
        """
        Instance name from client config, e.g. `'yourco.sumatra.ai'`
        """
        return CONFIG.instance

    @property
    def workspace(self) -> Optional[str]:
        """
        User's current workspace slug, e.g. `my-workspace`
        """
        if not self._workspace:
            self._workspace, self._workspace_id = self._choose_workspace()
        return self._workspace

    def _tenant_id(self) -> Optional[str]:
        if not self._workspace_id:
            self._workspace, self._workspace_id = self._choose_workspace()
        return self._workspace_id

    def update_workspace(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        icon: Optional[bytes] = None,
    ) -> Dict:
        """
        Update workspace metadata.

        Arguments:
            name: A human readable name for the new workspace
            slug: Desired slug of the new workspace. Must consist only of letters, numbers, '-', and '_'. If this slug is taken, a random one will be generated instead, which may be changed later.
            icon: Binary encoding of a PNG image to use as the workspace icon. Max size 50kb

        Returns:
            A dict of the updated workspace metadata
        """

        query = """
            mutation UpdateWorkspace($id: String!, $name: String, $slug: String, $icon: String) {
                updateTenant(id: $id, name: $name, slug: $slug, icon: $icon) {
                    id
                    slug
                    name
                }
            }
        """

        if icon:
            icon = base64.b64encode(icon).decode()

        ret = self._execute_graphql(
            query=query,
            variables={
                "id": self._tenant_id(),
                "name": name,
                "slug": slug,
                "icon": icon,
            },
        )

        d = ret["data"]["updateTenant"]
        return {
            "id": d["id"],
            "slug": d["slug"],
            "name": d["name"],
        }

    @property
    def branch(self) -> str:
        """
        Default branch name
        """
        return self._branch

    @branch.setter
    def branch(self, branch: str) -> None:
        self._branch = branch

    def user_email(self) -> str:
        """
        Return the email address of the connected user.

        Returns:
            Email address
        """
        logger.debug("Fetching user")
        query = """
        query CurrentUser {
            currentUser {
                email
            }
        }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["currentUser"]["email"]

    def tenant(self) -> str:
        """
        Return the assigned tenant name for the connected user.
        (DEPRECATED) use .workspace instead

        Returns:
            Tenant name (slug)
        """
        if self.version().startswith("v1.2"):
            return WorkspaceClient()._old_tenant()
        logger.warn(
            "tenant() is deprecated and will be removed in the next release. Use .workspace instead."
        )
        return self.workspace

    def sdk_key(self) -> str:
        """
        Return the SDK key for the connected workspace

        Returns:
            SDK key
        """
        logger.debug("Fetching tenant sdk key")
        query = """
            query SDKKey {
                currentTenant {
                    accessKeys(type: "sdk") {
                        nodes {
                            key
                        }
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["currentTenant"]["accessKeys"]["nodes"][0]["key"]

    def api_key(self) -> str:
        """
        Return the API key for the connected workspace

        Returns:
            API key
        """
        logger.debug("Fetching tenant api key")
        query = """
            query APIKey {
                currentTenant {
                    accessKeys(type: "api") {
                        nodes {
                            key
                        }
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["currentTenant"]["accessKeys"]["nodes"][0]["key"]

    def query_athena(self, sql: str) -> pd.DataFrame:
        """
        Execute a SQL query against the Athena backend and return the
        result as a dataframe.

        Arguments:
            sql: SQL query (e.g. "select * from event_log where event_type='login' limit 10")

        Returns:
            Result of query as a Pandas dataframe
        """
        session = self._get_session()
        tenant = self._tenant_id()
        return wr.athena.read_sql_query(
            boto3_session=session,
            sql=sql,
            database=TENANT_PREFIX + tenant,
            workgroup=TENANT_PREFIX + tenant,
        )

    def get_branch(self, branch: Optional[str] = None) -> Dict:
        """
        Return metadata about the branch.

        Arguments:
            branch: Specify a branch other than the client default.

        Returns:
            Branch metadata
        """
        branch = branch or self._branch
        logger.info(f"Getting branch {branch}")
        query = """
            query BranchScowl($id: String!) { 
              branch(id: $id) { id, hash, events, creator, lastUpdated, error } 
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": branch}, error_prefix=f"error getting branch '{branch}'")

        d = ret["data"]["branch"]
        if not d:
            raise ValueError(f"branch '{branch}' not found")

        row = {
            "name": d["id"],
            "creator": d["creator"],
            "update_ts": d["lastUpdated"],
            "event_types": d["events"],
        }

        if "error" in d and d["error"]:
            row["error"] = d["error"]

        return row

    def clone_branch(self, dest: str, branch: Optional[str] = None) -> None:
        """
        Copy branch to another branch name.

        Arguments:
            dest: Name of branch to be created or overwritten.
            branch: Specify a source branch other than the client default.
        """
        branch = branch or self._branch
        logger.info(f"Cloning branch {branch} to {dest}")
        query = """
            mutation CloneBranch($id: String!, $sourceId: String!) {
                cloneBranch(id: $id, sourceId: $sourceId) { id, creator, lastUpdated, scowl }
              }
        """

        ret = self._execute_graphql(
            query=query, variables={"id": dest, "sourceId": branch}
        )

    def _put_branch_object(
        self, key: str, scowl: str, branch: Optional[str] = None
    ) -> None:
        branch = branch or self._branch
        logger.info(f"Putting branch object {key} to branch {branch}")
        query = """
              mutation PutBranchObject($branchId: String!, $key: String!, $scowl: String!) {
                putBranchObject(branchId: $branchId, key: $key, scowl: $scowl) { key }
              }
        """

        ret = self._execute_graphql(
            query=query, variables={"branchId": branch, "key": key, "scowl": scowl}
        )

    def create_branch_from_scowl(self, scowl: str, branch: Optional[str] = None) -> str:
        """
        Create (or overwrite) branch with single file of scowl source code.

        Arguments:
            scowl: Scowl source code as string.
            branch: Specify a source branch other than the client default.

        Returns:
            Name of branch created
        """

        branch = branch or self._branch
        logger.info(f"Creating branch '{branch}' from scowl")
        try:
            self.delete_branch(branch)
        except:
            pass

        self._put_branch_object("main.scowl", scowl, branch)

        b = self.get_branch(branch)
        if "error" in b:
            raise RuntimeError(b["error"])

        return b["name"]

    def create_branch_from_dir(
        self,
        scowl_dir: Optional[str] = None,
        branch: Optional[str] = None,
        deps_file: Optional[str] = None,
    ) -> str:
        """
        Create (or overwrite) branch with local scowl files.

        Arguments:
            scowl_dir: Path to local .scowl files.
            branch: Specify a source branch other than the client default.
            deps_file: Path to deps file [default: <scowl_dir>/deps.scowl]

        Returns:
            Name of branch created
        """
        scowl_dir = scowl_dir or CONFIG.scowl_dir
        deps_file = deps_file or os.path.join(scowl_dir, DEPS_FILE)
        branch = branch or self._branch
        logger.info(f"Creating branch '{branch}' from dir '{scowl_dir}'")

        try:
            self.delete_branch(branch)
        except:
            pass

        scowls = _load_scowl_files(scowl_dir)
        if os.path.exists(deps_file):
            scowls[DEPS_FILE] = open(deps_file).read()
        if not scowls:
            raise RuntimeError(
                f"Unable to push local dir. '{scowl_dir}' has no .scowl files."
            )

        for key in scowls:
            self._put_branch_object(key, scowls[key], branch)

        b = self.get_branch(branch)
        if "error" in b:
            raise RuntimeError(b["error"])

        return b["name"]

    def publish_dir(
        self, scowl_dir: Optional[str] = None, deps_file: Optional[str] = None
    ) -> None:
        """
        Push local scowl dir to branch and promote to LIVE.

        Arguments:
            scowl_dir: Path to .scowl files. Default: `'.'`
            deps_file: Path to deps file [default: <scowl_dir>/deps.scowl]

        """
        scowl_dir = scowl_dir or CONFIG.scowl_dir
        logger.info(f"Publishing dir '{scowl_dir}' to LIVE.")
        branch = self.create_branch_from_dir(scowl_dir, "main", deps_file)
        self.publish_branch(branch)

    def publish_branch(self, branch: Optional[str] = None) -> None:
        """
        Promote branch to LIVE.

        Arguments:
            branch: Specify a branch other than the client default.
        """
        branch = branch or self._branch
        logger.info(f"Publishing '{branch}' branch to LIVE.")
        query = """
            mutation PublishBranch($id: String!) {
                publish(id: $id) {
                    id
                }
            }
        """
        ret = self._execute_graphql(query=query, variables={"id": branch}, error_prefix=f"Error publishing branch '{branch}'")

    def publish_scowl(self, scowl: str) -> None:
        """
        Push local scowl source to branch and promote to LIVE.

        Arguments:
            scowl: Scowl source code as string.
        """
        logger.info("Publishing scowl to LIVE.")
        branch = self.create_branch_from_scowl(scowl, "main")
        self.publish_branch(branch)

    def diff_branch_with_live(
        self, branch: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Compare branch to LIVE topology and return diff.

        Arguments:
            branch: Specify a source branch other than the client default.

        Returns:
            Events and features added, redefined, and deleted.
        """

        branch = branch or self._branch
        logger.info(f"Diffing '{branch}' branch against LIVE.")
        query = """
            query Branch($id: String!) {
                branch(id: $id) {
                liveDiff {
                    eventsAdded
                    eventsDeleted
                    topologyDiffs {
                        eventType
                        featuresDeleted
                        featuresAdded
                        featuresRedefined
                        featuresDirtied
                    }
                    tableDiffs {
                        id
                        oldVersion
                        newVersion
                    }
                    warnings
                }
              }
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": branch})

        return ret["data"]["branch"]["liveDiff"]

    def get_branches(self) -> pd.DataFrame:
        """
        Return all branches and their metadata.

        Returns:
            Branch metadata.
        """
        logger.debug(f"Getting branches")
        query = """
            query BranchList {
                branches {
                    id
                    events
                    error
                    creator
                    lastUpdated
                }
            }
        """

        ret = self._execute_graphql(query=query, error_prefix="error getting branches")

        rows = []
        for branch in ret["data"]["branches"]:
            row = {
                "name": branch["id"],
                "creator": branch["creator"],
                "update_ts": branch["lastUpdated"],
                "event_types": branch["events"],
            }
            if branch["error"]:
                row["error"] = branch["error"]

            rows.append(row)
        if not rows:
            return pd.DataFrame(columns=["name", "creator", "update_ts", "event_types"])
        df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["update_ts"])
        return df.sort_values(["creator", "update_ts"], ascending=False).set_index(
            "name"
        )

    def get_live_scowl(self) -> str:
        """
        Return scowl source code for LIVE topology as single cleansed string.

        Returns:
            Scowl source code as string.
        """
        query = """
            query LiveScowl {
                liveBranch { scowl }
            }
        """

        ret = self._execute_graphql(query=query)

        scowl = ret["data"]["liveBranch"]["scowl"]
        return scowl

    def delete_branch(self, branch: Optional[str] = None) -> None:
        """
        Delete server-side branch

        Arguments:
            branch: Specify a branch other than the client default.
        """
        branch = branch or self._branch
        logger.info(f"Deleting branch '{branch}'.")
        query = """
            mutation DeleteBranch($id: String!) {
                deleteBranch(id: $id) {
                    id
                }
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": branch}, error_prefix=f"Error deleting branch '{branch}'")

    def save_branch_to_dir(
        self,
        scowl_dir: Optional[str] = None,
        branch: Optional[str] = None,
        deps_file: Optional[str] = None,
    ) -> str:
        """
        Save remote branch scowl files to local dir.

        Arguments:
            scowl_dir: Path to save .scowl files.
            branch: Specify a source branch other than the client default.
            deps_file: Path to deps file [default: <scowl_dir>/deps.scowl]

        Returns:
            Name of branch created
        """
        scowl_dir = scowl_dir or CONFIG.scowl_dir
        branch = branch or self._branch
        deps_file = deps_file or os.path.join(scowl_dir, DEPS_FILE)

        logger.info(f"Fetching objects for branch '{branch}''")

        query = """
            query BranchObjects($id: String!) {
                branch(id: $id) {
                    objects {
                        key
                        scowl
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": branch}, error_prefix=f"error getting branch '{branch}'")

        d = ret["data"]["branch"]
        if not d:
            raise ValueError(f"branch '{branch}' not found")

        logger.info(f"Saving branch '{branch}' to dir '{scowl_dir}'")

        for obj in d["objects"]:
            fname = os.path.join(scowl_dir, obj["key"])
            if obj["key"] == DEPS_FILE:
                fname = deps_file
            with open(fname, "w") as f:
                f.write(obj["scowl"])

        return branch

    def get_inputs_from_feed(
        self,
        start_ts: Optional[Union[pd.Timestamp, str]] = None,
        end_ts: Optional[Union[pd.Timestamp, str]] = None,
        count: Optional[int] = None,
        event_types: Optional[List[str]] = None,
        where: Dict[str, str] = {},
        batch_size: int = 10000,
        ascending: bool = False,
    ) -> List[Dict]:
        """
        Return the raw input events from the Event Feed.

        Fetches events in descending time order from `end_ts`. May specify `count` or `start_ts`, but not both.

        Arguments:
            start_ts: Earliest event timestamp to fetch (local client timezone). If not specified, `count` will be used instead.
            end_ts: Latest event timestamp to fetch (local client timezone) [default: now].
            count: Number of rows to return (if start_ts not specified) [default: 10].
            event_types: Subset of event types to fetch. [default: all]
            where: Dictionary of equality conditions (all must be true for a match), e.g. {"zipcode": "90210", "email_domain": "gmail.com"}.
            batch_size: Maximum number of records to fetch per GraphQL call.
            ascending: Sort results in ascending chronological order instead of descending.

        Returns:
            List of events: [{"_id": , "_type": , "_time": , [inputs...]}] (in descending time order).
        """

        where = [{"key": k, "value": v} for k, v in where.items()]
        if batch_size < 1 or batch_size > 10000:
            raise RuntimeError(f"batch size: {batch_size} is out of range [1,10000]")
        end_ts = end_ts or str(pendulum.now())
        if isinstance(end_ts, pd.Timestamp):
            end_ts = str(end_ts)
        end_ts = pendulum.parse(end_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )

        if event_types is not None:
            event_types = [{"type": t} for t in event_types]

        query = """
        query EventFeed($size: Int!, $end: DateTime!, $eventTypes: [EventSelection], $where: [FeatureFilter]!, $reverse: Boolean!) {
            events {
                feed(
                    from: 0
                    size: $size
                    end: $end
                    types: $eventTypes
                    where: $where
                    reverse: $reverse
                ) {
                id
                type
                time
                input
                }
            }
        }
        """
        if start_ts:
            if count:
                raise RuntimeError("specify only one of: start_ts or count")
            if isinstance(start_ts, pd.Timestamp):
                start_ts = str(start_ts)
            start_ts = pendulum.parse(start_ts, tz=CONFIG.timezone).astimezone(
                pendulum.timezone("UTC")
            )

            rows = []
            done = False
            while not done:
                variables = {
                    "size": batch_size,
                    "end": end_ts.to_iso8601_string(),
                    "where": where,
                    "reverse": ascending,
                }
                if event_types:
                    variables["eventTypes"] = event_types
                ret = self._execute_graphql(
                    query=query,
                    variables=variables,
                )
                new_rows = []
                for event in ret["data"]["events"]["feed"]:
                    event_time = pendulum.parse(event["time"])
                    if event_time < start_ts:
                        done = True
                        break
                    row = {
                        "_id": event["id"],
                        "_type": event["type"],
                        "_time": str(event_time),
                    }
                    row.update(event["input"])
                    new_rows.append(row)
                rows.extend(new_rows)
                if done or not new_rows:
                    break
                end_ts = event_time
            return rows
        else:  # count
            if count is None:
                count = 10
            from_ = 0
            rows = []
            while True:
                size = min(batch_size, count - from_)
                if size <= 0:
                    break
                variables = {
                    "size": size,
                    "end": end_ts.to_iso8601_string(),
                    "where": where,
                    "reverse": ascending,
                }
                if event_types:
                    variables["eventTypes"] = event_types
                ret = self._execute_graphql(
                    query=query,
                    variables=variables,
                )
                new_rows = []
                for event in ret["data"]["events"]["feed"]:
                    event_time = pendulum.parse(event["time"])
                    row = {
                        "_id": event["id"],
                        "_type": event["type"],
                        "_time": str(event_time),
                    }
                    row.update(event["input"])
                    new_rows.append(row)
                rows.extend(new_rows)
                from_ += size
                if from_ >= count:
                    break
                end_ts = event_time
            return rows

    def get_features_from_feed(
        self,
        event_type: str,
        start_ts: Optional[Union[pd.Timestamp, str]] = None,
        end_ts: Optional[Union[pd.Timestamp, str]] = None,
        count: Optional[int] = None,
        where: Dict[str, str] = {},
        batch_size: int = 10000,
        ascending: bool = False,
    ) -> pd.DataFrame:
        """
        For a given event type, return the feature values as they were
        calculated at event time.

        Fetches events in descending time order from `end_ts`. May specify `count` or `start_ts`, but not both.

        Arguments:
            event_type: Event type name.
            start_ts: Earliest event timestamp to fetch (local client timezone). If not specified, `count` will be used instead.
            end_ts: Latest event timestamp to fetch (local client timezone) [default: now].
            count: Number of rows to return (if start_ts not specified) [default: 10].
            where: Dictionary of equality conditions (all must be true for a match), e.g. {"zipcode": "90210", "email_domain": "gmail.com"}.
            batch_size: Maximum number of records to fetch per GraphQL call.
            ascending: Sort results in ascending chronological order instead of descending.

        Returns:
            Dataframe: _id, _time, [features...] (in descending time order).
        """

        where = [{"key": k, "value": v} for k, v in where.items()]
        if batch_size < 1 or batch_size > 10000:
            raise RuntimeError(f"batch size: {batch_size} is out of range [1,10000]")
        end_ts = end_ts or str(pendulum.now())
        if isinstance(end_ts, pd.Timestamp):
            end_ts = str(end_ts)
        end_ts = pendulum.parse(end_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )

        query = """
        query EventFeed($size: Int!, $end: DateTime!, $eventType: String!, $where: [FeatureFilter]!, $reverse: Boolean!) {
            events {
                feed(
                    from: 0
                    size: $size
                    end: $end
                    types: [{ type: $eventType, where: $where }]
                    reverse: $reverse
                ) {
                id
                time
                features
                }
            }
        }
        """
        if start_ts:
            if count:
                raise RuntimeError("specify only one of: start_ts or count")
            if isinstance(start_ts, pd.Timestamp):
                start_ts = str(start_ts)
            start_ts = pendulum.parse(start_ts, tz=CONFIG.timezone).astimezone(
                pendulum.timezone("UTC")
            )

            rows = []
            done = False
            while not done:
                ret = self._execute_graphql(
                    query=query,
                    variables={
                        "size": batch_size,
                        "end": end_ts.to_iso8601_string(),
                        "eventType": event_type,
                        "where": where,
                        "reverse": ascending,
                    },
                )
                new_rows = []
                for event in ret["data"]["events"]["feed"]:
                    event_time = pendulum.parse(event["time"])
                    if event_time < start_ts:
                        done = True
                        break
                    row = {"_id": event["id"], "_time": event_time}
                    row.update(event["features"])
                    new_rows.append(row)
                rows.extend(new_rows)
                if done or not new_rows:
                    break
                end_ts = event_time
            if not rows:
                return pd.DataFrame(columns=["_id", "_time"])
            df = pd.DataFrame(rows)
            df = tz_convert_timestamp_columns(df)
            return df.set_index("_id")
        else:  # count
            if count is None:
                count = 10
            from_ = 0
            rows = []
            while True:
                size = min(batch_size, count - from_)
                if size <= 0:
                    break
                ret = self._execute_graphql(
                    query=query,
                    variables={
                        "size": size,
                        "end": end_ts.to_iso8601_string(),
                        "eventType": event_type,
                        "where": where,
                        "reverse": ascending,
                    },
                )
                new_rows = []
                for event in ret["data"]["events"]["feed"]:
                    event_time = pendulum.parse(event["time"])
                    row = {"_id": event["id"], "_time": event_time}
                    row.update(event["features"])
                    new_rows.append(row)
                rows.extend(new_rows)
                from_ += size
                if from_ >= count:
                    break
                end_ts = event_time
            if not rows:
                return pd.DataFrame(columns=["_id", "_time"])
            df = pd.DataFrame(rows)
            df = tz_convert_timestamp_columns(df)
            return df.set_index("_id")

    def get_live_schema(self) -> Dict[str, Dict[str, str]]:
        """
        Return the feature names and types for every event in the LIVE topology

        Returns:
            Dictionary {'event_name': {'f1': 'int', 'f2': 'bool', ...} ...}
        """
        logger.debug("Getting LIVE schema")
        query = """
            query Topology {
                topology(name: "live") {
                    events {
                        name
                        features {
                            name
                            type
                        }
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query, error_prefix="error getting live schema")

        events = {}
        for event in ret["data"]["topology"]["events"]:
            events[event["name"]] = {f["name"]: f["type"] for f in event["features"]}

        return events

    def _athena_feature_sql(
        self, event_type, start_ts, end_ts, features, include_inputs, where
    ):
        schema = self.get_live_schema()
        if event_type not in schema:
            raise ValueError(f"event '{event_type}' not found in LIVE topology")

        if features is None:
            features = list(schema[event_type].keys())

        for f in features:
            if f not in schema[event_type]:
                raise ValueError(
                    f"feature '{event_type}.{f}' not found in LIVE topology"
                )

        type_map = {
            "int": "int",
            "bool": "boolean",
            "float": "double",
            "string": "varchar",
            "time": "varchar",
        }

        scalar_selector = """, (case when (json_extract_scalar(features, '$.{}') = 'null') then null
            else try_cast(json_extract_scalar(features, '$.{}') AS {}) end) "{}"
            """

        # Athena doesn't support "timestamp with timezone" for format='PARQUET' so leave as strings
        # time_selector = """, (case when (json_extract_scalar(features, '$.{}') = 'null') then null
        #     else from_iso8601_timestamp(json_extract_scalar(features, '$.{}')) end) "{}"
        #     """

        selector = """, json_format(json_extract(features, '$.{}')) "{}"
            """

        json_fields = []
        selectors = []
        for f, t in schema[event_type].items():
            if t in type_map:
                selectors.append(scalar_selector.format(f, f, type_map[t], f))
            # elif t == "time":
            #    selectors.append(time_selector.format(f, f, f))
            else:
                selectors.append(selector.format(f, f))
                if f in features:
                    json_fields.append(f)

        where = f"where {where}" if where else ""
        inputs = ""
        if include_inputs:
            inputs = ', event as "_inputs"'
            json_fields.append("_inputs")

        features = [f'"{feature}"' for feature in features]
        returned = ", ".join(["_id", "_time"] + features)

        query = f"""with tmp as (
            select
            event_id "_id"
            ,event_ts "_time"
            {inputs}
            {"".join(selectors)}
            from
            "event_log"
            where (event_type = '{event_type}')
            and (event_ts between '{start_ts}' and '{end_ts}')
            ) select {returned} from tmp {where}
            """

        logger.debug(query)
        return query, json_fields

    def get_features_from_log(
        self,
        event_type: str,
        start_ts: Optional[Union[pd.Timestamp, str]] = None,
        end_ts: Optional[Union[pd.Timestamp, str]] = None,
        features: Optional[List[str]] = None,
        include_inputs: bool = False,
        where: Optional[str] = None,
        deserialize_json: bool = True,
    ) -> pd.DataFrame:
        """
        For a given event type, fetch the historical values for features, as
        calculated in the LIVE environment.

        Arguments:
            event_type: Event type name.
            start_ts: Earliest event timestamp to fetch (local client timezone). If not specified, will start from beginning of log.
            end_ts: Latest event timestamp to fetch (local client timezone) [default: now].
            features: Subset of features to fetch. [default: all].
            include_inputs: Include request json as "_inputs" column.
            where: SQL clauses (not including "where" keyword), e.g. "col1 is not null"
            deserialize_json: Deserialize complex data types from JSON strings to Python objects.

        Returns:
            Dataframe: _id, _time, [features...] (in ascending time order).
        """
        end_ts = end_ts or str(pendulum.now())
        if isinstance(end_ts, pd.Timestamp):
            end_ts = str(end_ts)
        end_ts = pendulum.parse(end_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )

        start_ts = start_ts or "1971-01-01"
        if isinstance(start_ts, pd.Timestamp):
            start_ts = str(start_ts)
        start_ts = pendulum.parse(start_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )

        where = (where or "").strip()
        if where.lower().startswith("where"):
            raise ValueError("'where' condition should omit the 'where' keyword")
        sql, json_fields = self._athena_feature_sql(
            event_type, start_ts, end_ts, features, include_inputs, where
        )

        df = self.query_athena(sql)
        if deserialize_json:  # TODO: duckdb could probably do this a lot faster
            df = df.assign(
                **{field: df[field].apply(json.loads) for field in json_fields}
            )
        return df.set_index("_id")

    def get_timelines(self) -> pd.DataFrame:
        """
        Return all timelines and their metadata.

        Returns:
            Timeline metadata.
        """

        logger.debug(f"Getting timelines")
        query = """
            query TimelineList {
                timelines { id, createUser, createTime, metadata { start, end, count, events }, source, state, error }
            }
        """
        ret = self._execute_graphql(query)
        rows = []
        for timeline in ret["data"]["timelines"]:
            status = timeline["state"]
            row = {
                "name": timeline["id"],
                "creator": timeline["createUser"],
                "create_ts": timeline["createTime"],
                "event_types": timeline["metadata"]["events"],
                "event_count": timeline["metadata"]["count"],
                "start_ts": timeline["metadata"]["start"]
                if timeline["metadata"]["start"] != "0001-01-01T00:00:00Z"
                else "",
                "end_ts": timeline["metadata"]["end"]
                if timeline["metadata"]["end"] != "0001-01-01T00:00:00Z"
                else "",
                "source": timeline["source"],
                "status": status,
                "error": timeline["error"],
            }
            rows.append(row)
        if not rows:
            return pd.DataFrame(
                columns=[
                    "name",
                    "creator",
                    "create_ts",
                    "event_types",
                    "event_count",
                    "start_ts",
                    "end_ts",
                    "source",
                    "status",
                    "error",
                ]
            )
        df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["create_ts", "start_ts", "end_ts"])
        return df.sort_values(["creator", "create_ts"], ascending=False).set_index(
            "name"
        )

    def get_timeline(self, timeline: str) -> pd.Series:
        """
        Return metadata about the timeline.

        Arguments:
            timeline: Timeline name.

        Returns:
            Timeline metadata.
        """
        logger.debug(f"Getting timeline '{timeline}'")
        timelines = self.get_timelines()
        if timeline in timelines.index:
            return timelines.loc[timeline]
        raise RuntimeError(f"Timeline '{timeline}' not found.")

    def delete_timeline(self, timeline: str) -> None:
        """
        Delete timeline

        Arguments:
            timeline: Timeline name.
        """
        logger.info(f"Deleting timeline '{timeline}'.")
        query = """
            mutation DeleteTimeline($id: String!) {
                deleteTimeline(id: $id) {
                    id
                }
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": timeline})

        return ret["data"]["deleteTimeline"]["id"]

    def infer_schema_from_timeline(self, timeline: str) -> str:
        """
        Attempt to infer the paths and data types of all fields in the timeline's
        input data. Generate the scowl to parse all JSON paths.

        This function helps bootstrap scowl code for new event types, with
        the expectation that most feature names will need to be modified.

        e.g.
        ```
            account_id := $.account.id as int
            purchase_items_0_amount := $.purchase.items[0].amount as float
        ```

        Arguments:
            timeline: Timeline name.

        Returns:
            Scowl source code as string.
        """
        query = """
            query TimelineScowl($id: String!) {
                timeline(id: $id) { id, scowl }
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": timeline})

        return ret["data"]["timeline"]["scowl"]

    def create_timeline_from_s3(
        self,
        timeline: str,
        s3_uri: str,
        time_path: str,
        data_path: str,
        id_path: Optional[str] = None,
        type_path: Optional[str] = None,
        default_type: Optional[str] = None,
    ):
        """
        Create (or overwrite) timeline from a JSON file on S3

        Arguments:
            timeline: Timeline name.
            s3_uri: S3 bucket URI.
            time_path: JSON path where event timestamp is found (e.g. $._time)
            data_path: JSON path where event payload is found (e.g. $)
            id_path: JSON path where event ID is found (e.g. $.event_id)
            type_path: JSON path where event type is found (e.g. $._type)
            default_type: Event type to use in case none found at `type_path`
        """
        query = """
                    mutation SaveTimelineMutation($id: String!, $source: String!, $state: String!, $parameters: [KeyValueInput]!) {
                        saveTimeline(id: $id, source: $source, state: $state, parameters: $parameters) {
                            id
                        }
                    }
                """

        parameters = [
            {"key": "s3_uri", "value": s3_uri},
            {"key": "time_path", "value": time_path},
            {"key": "data_path", "value": data_path},
        ]

        if default_type:
            parameters.append({"key": "default_type", "value": default_type})

        if id_path:
            parameters.append({"key": "id_path", "value": id_path})

        if type_path:
            parameters.append({"key": "type_path", "value": type_path})

        ret = self._execute_graphql(
            query=query,
            variables={
                "id": timeline,
                "source": "s3",
                "state": "processing",
                "parameters": parameters,
            },
        )

        return ret["data"]["saveTimeline"]["id"]

    def create_timeline_from_log(
        self,
        timeline: str,
        start_ts: Union[pd.Timestamp, str],
        end_ts: Union[pd.Timestamp, str],
        event_types: Optional[List[str]] = None,
    ) -> None:
        """
        Create (or overwrite) timeline from the Event Log

        Arguments:
            timeline: Timeline name.
            start_ts: Earliest event timestamp to fetch (local client timezone).
            end_ts: Latest event timestamp to fetch (local client timezone).
            event_types: Event types to include (default: all).
        """

        query = """
            mutation SaveTimeline($id: String!, $parameters: [KeyValueInput]!) {
              saveTimeline(id: $id, source: "athena", state: "processing", parameters: $parameters) {
                id
              }
            }
        """
        if isinstance(start_ts, pd.Timestamp):
            start_ts = str(start_ts)
        if isinstance(end_ts, pd.Timestamp):
            end_ts = str(end_ts)
        start_ts = pendulum.parse(start_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )
        end_ts = pendulum.parse(end_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )
        start_str = start_ts.to_iso8601_string()
        end_str = end_ts.to_iso8601_string()
        parameters = [
            {"key": "start", "value": start_str},
            {"key": "end", "value": end_str},
        ]

        if event_types:
            events = ",".join(event_types)
            parameters.append({"key": "events", "value": events})

        ret = self._execute_graphql(
            query=query, variables={"id": timeline, "parameters": parameters}
        )
        self._wait_for_timeline_processing(timeline)

    def create_timeline_from_dataframes(
        self,
        timeline: str,
        df_dict: Dict[str, pd.DataFrame],
        timestamp_column: Optional[str] = None,
    ) -> None:
        """
        Create (or overwrite) timeline from a collection of DataFrames—one per event type.

        Arguments:
            timeline: Timeline name.
            df_dict: Dictionary from event type name to DataFrame of events.
            timestamp_column: Name of timestamp column, default `_time`. If column not present, current timestamp used for all events.
        """
        jsonl = ""
        for event_type, df in df_dict.items():
            jsonl += self._df_to_jsonl(df, event_type, timestamp_column)
        self.create_timeline_from_jsonl(timeline, jsonl)

    def create_timeline_from_jsonl(self, timeline: str, jsonl: str) -> None:
        """
        Create (or overwrite) timeline from JSON events passed in as a string.

        Arguments:
            timeline: Timeline name.
            jsonl: JSON event data, one JSON dict per line.
        """

        if not jsonl.endswith("\n"):
            jsonl += "\n"
        data = gzip.compress(bytes(jsonl, "utf-8"))
        self._create_timeline_from_jsonl_gz(timeline, data)

    def _create_timeline_from_jsonl_gz(
        self,
        timeline: str,
        data: bytes,
    ) -> None:
        query = """
            mutation SaveTimelineMutation($id: String!,
                                          $filename: String!) {
                saveTimeline(id: $id, source: "file", state: "new") {
                    uploadUrl(name: $filename)
                }
            }
        """

        ret = self._execute_graphql(
            query=query, variables={"id": timeline, "filename": "timeline.jsonl.gz"}
        )

        url = ret["data"]["saveTimeline"]["uploadUrl"]

        http_response = requests.put(url, data=data)
        if http_response.status_code != 200:
            raise RuntimeError(http_response.error)

        query = """
            mutation SaveTimelineMutation($id: String!) {
                saveTimeline(id: $id, source: "file", state: "processing") {
                    id
                }
            }
        """

        ret = self._execute_graphql(query=query, variables={"id": timeline})

        self._wait_for_timeline_processing(timeline)

    def _wait_for_timeline_processing(self, timeline: str) -> None:
        RETRIES = 180
        DELAY = 5.0
        retry_count = 0
        while retry_count < RETRIES:
            tl = self.get_timeline(timeline)
            if tl.status != "processing":
                if tl.status != "materialized":
                    raise RuntimeError(
                        f"unexpected timeline state: {tl.status} error: {tl.error}"
                    )
                return
            time.sleep(DELAY)
            retry_count += 1
        if self.status == "processing":
            raise RuntimeError(f"Timed out after {DELAY * RETRIES} seconds")

    def create_timeline_from_file(self, timeline: str, filename: str) -> None:
        """
        Create (or overwrite) timeline from events stored in a file.

        Supported file types: `.jsonl`, `.jsonl.gz`

        Arguments:
            timeline: Timeline name.
            filename: Name of events file to upload.
        """

        _, ext = _splitext(filename)

        if ext in (".jsonl.gz", ".json.gz"):
            with open(filename, "rb") as f:
                self._create_timeline_from_jsonl_gz(timeline, f.read())
        elif ext in (".jsonl", ".json"):
            with open(filename, "r") as f:
                jsonl = f.read()
                self.create_timeline_from_jsonl(timeline, jsonl)
        else:
            raise RuntimeError(f"Unsupported file extension: {ext}")

    def _df_to_jsonl(self, df, event_type, timestamp_column=None):
        df = df.copy()
        df["_type"] = event_type
        if timestamp_column:
            df.rename(columns={timestamp_column: "_time"}, inplace=True)
        if "_time" not in df.columns:
            df["_time"] = datetime.utcnow()
        df.sort_values("_time", inplace=True)
        jsonl = df.to_json(orient="records", lines=True, date_format="iso")
        if not jsonl.endswith("\n"):
            jsonl += "\n"
        return jsonl

    def get_materialization(self, id: str) -> Materialization:
        return Materialization(self, id)

    def materialize(
        self, timeline: str, branch: Optional[str] = None
    ) -> Materialization:
        """
        Enrich timeline using topology at branch.

        This is the primary function of the SDK.

        Arguments:
            timeline: Timeline name.
            branch: Specify a source branch other than the client default.

        Returns:
            Handle to Materialization job
        """

        return self.materialize_many([timeline], branch)

    def materialize_many(
        self, timelines: List[str], branch: Optional[str] = None
    ) -> Materialization:
        """
        Enrich collection of timelines using topology at branch. Timelines are merged based on timestamp.

        This is the primary function of the SDK.

        Arguments:
            timelines: Timeline names.
            branch: Specify a source branch other than the client default.

        Returns:
            Handle to Materialization job
        """
        branch = branch or self._branch
        query = """
            mutation Materialize($timelines: [String], $branch: String!) {
                materialize(timelines: $timelines, branch: $branch) { id }
            }
        """

        ret = self._execute_graphql(
            query=query, variables={"timelines": timelines, "branch": branch}
        )

        return Materialization(self, ret["data"]["materialize"]["id"])

    def replay(
        self,
        features: List[str],
        start_ts: Union[pd.Timestamp, str],
        end_ts: Union[pd.Timestamp, str],
        extra_timelines: Optional[List[str]] = None,
        branch: Optional[str] = None,
    ) -> Materialization:
        """
        (BETA)
        Recompute historical feature values from LIVE event log on given topology branch.

        This is the primary function of the SDK.

        Arguments:
            features: List of features to materialize, e.g. `['login.email', 'purchase.*']`
            start_ts: Earliest event timestamp to materialize (local client timezone).
            end_ts: Latest event timestamp to materialize (local client timezone).
            extra_timelines: Names of supplemental timelines.
            branch: Specify a source branch other than the client default.

        Returns:
            Handle to Materialization job
        """

        if isinstance(start_ts, pd.Timestamp):
            start_ts = str(start_ts)
        start = pendulum.parse(start_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )
        start = int(start.timestamp())

        if isinstance(end_ts, pd.Timestamp):
            end_ts = str(end_ts)
        end = pendulum.parse(end_ts, tz=CONFIG.timezone).astimezone(
            pendulum.timezone("UTC")
        )
        end = int(end.timestamp())

        live_timeline = f"live_{start}_{end}"
        self.create_timeline_from_log(live_timeline, start_ts, end_ts)

        timelines = (extra_timelines or []) + [live_timeline]
        return self.distributed_materialize_many(
            timelines, features, start_ts, end_ts, branch
        )

    def distributed_materialize_many(
        self,
        timelines: List[str],
        features: List[str] = None,
        start_ts: Optional[Union[pd.Timestamp, str]] = None,
        end_ts: Optional[Union[pd.Timestamp, str]] = None,
        branch: Optional[str] = None,
    ) -> Materialization:
        """
        Enrich collection of timelines using topology at branch. Timelines are merged based on timestamp.

        Arguments:
            timelines: Timeline names.
            branch: Specify a source branch other than the client default.
            start_ts: Earliest event timestamp to materialize (local client timezone).
            end_ts: Latest event timestamp to materialize (local client timezone).
            features: List of features to materialize, e.g. `['login.email', 'purchase.*']`

        Returns:
            Handle to Materialization job
        """

        variables = {
            "timelines": timelines,
            "branch": branch or self._branch,
            "features": features,
        }

        if start_ts:
            if isinstance(start_ts, pd.Timestamp):
                start_ts = str(start_ts)
            start_ts = pendulum.parse(start_ts, tz=CONFIG.timezone).astimezone(
                pendulum.timezone("UTC")
            )
            variables["start"] = start_ts.to_iso8601_string()

        if end_ts:
            if isinstance(end_ts, pd.Timestamp):
                end_ts = str(end_ts)
            end_ts = pendulum.parse(end_ts, tz=CONFIG.timezone).astimezone(
                pendulum.timezone("UTC")
            )
            variables["end"] = end_ts.to_iso8601_string()

        query = """
            mutation DistributedMaterialize($timelines: [String], $branch: String!, $features: [String], $start: DateTime, $end: DateTime) {
                distributedMaterialize(timelines: $timelines, branch: $branch, features: $features, start: $start, end: $end) { id }
            }        
        """

        ret = self._execute_graphql(
            query=query,
            variables=variables,
        )

        return Materialization(self, ret["data"]["distributedMaterialize"]["id"])

    def get_models(self) -> pd.DataFrame:
        """
        Return all models and their metadata.

        Returns:
            Model metadata.
        """
        logger.debug("Getting models")
        query = """
            query ModelList {
                models {
                    nodes {
                        name
                        liveVersion {
                            version
                        }
                        latestVersion {
                            version
                        }
                        updatedAt
                        updatedBy
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query, error_prefix="error getting models")

        rows = []
        for model in ret["data"]["models"]["nodes"]:
            live_version = (
                model["liveVersion"]["version"] if model["liveVersion"] else ""
            )
            row = {
                "name": model["name"],
                "live_version": live_version,
                "latest_version": model["latestVersion"]["version"],
                "update_ts": model["updatedAt"],
                "updated_by": model["updatedBy"],
            }
            rows.append(row)
        if not rows:
            return pd.DataFrame(
                columns=[
                    "name",
                    "latest_version",
                    "live_version",
                    "update_ts",
                    "updated_by",
                ]
            )
        df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["update_ts"])
        return df.sort_values(["update_ts"], ascending=False).set_index("name")

    def get_model_history(self, name: str) -> pd.DataFrame:
        """
        Return list of versions for the given model along with their metadata.

        Arguments:
            name: Model name.

        Returns:
            DataFrame of version metadata.
        """

        query = """
            query ModelVersions($name: String!) {
                model(name: $name) {
                    versions {
                        nodes {
                            version
                            status
                            createdAt
                            creator
                        }
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query, variables={"name": name}, error_prefix=f"error getting versions of model '{name}'")

        rows = []
        for version in ret["data"]["model"]["versions"]["nodes"]:
            row = {
                "version": version["version"],
                "status": _humanize_status(version["status"]),
                "create_ts": version["createdAt"],
                "created_by": version["creator"],
            }
            rows.append(row)
        if not rows:
            df = pd.DataFrame(
                columns=[
                    "version",
                    "status",
                    "create_ts",
                    "created_by",
                ]
            )
        else:
            df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["create_ts"])
        return df.set_index("version")

    def get_model_version(self, name: str, version: str) -> ModelVersion:
        """
        Return handle to a specific model version.

        Arguments:
            name: Model name.
            version: Model version.

        Returns:
            Model version future object.
        """
        return ModelVersion(self, name, version)

    def get_model_schema(self, name: str, version: Optional[str] = None) -> str:
        if version is None:
            try:
                version = self.get_models().loc[name].latest_version
            except KeyError:
                raise RuntimeError(f"model '{name}' not found")
        return self.get_model_version(name, version).schema

    def _get_model_version(self, name: str, version: str) -> Dict[str, Any]:
        query = """
            query GetModelVersion($name: String!, $version: String!) {
                modelVersion(name: $name, version: $version) {
                    status
                    error
                    s3Uri
                    uploadUrl
                    creator
                    createdAt
                    updatedAt
                    size
                    inputSchema
                    outputSchema
                    scowlSnippet
                    metadata
                    comment
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"name": name, "version": version},
        )

        return ret["data"]["modelVersion"]

    def _create_empty_model_version(
        self, model: str, s3_uri: Optional[str] = None, comment: Optional[str] = None
    ) -> tuple[str, str]:
        query = """
            mutation ModelVersionPath($name: String!, $s3Uri: String, $comment: String) {
                createEmptyModelVersion(name: $name, s3Uri: $s3Uri, comment: $comment) {
                    version
                    s3Uri
                    uploadUrl
                }
            }
        """

        variables = {"name": model}
        if s3_uri:
            variables["s3Uri"] = s3_uri
        if comment:
            variables["comment"] = comment
        ret = self._execute_graphql(query=query, variables=variables)

        version = ret["data"]["createEmptyModelVersion"]["version"]
        upload_url = ret["data"]["createEmptyModelVersion"]["uploadUrl"]

        return version, upload_url

    def _load_model_version(self, model: str, version: str) -> None:
        query = """
            mutation LoadModelVersion($name: String!, $version: String!) {
                loadModelVersion(name: $name, version: $version) {
                    status
                    error
                }
            }
        """

        variables = {"name": model, "version": version}
        ret = self._execute_graphql(query=query, variables=variables)

        status = ret["data"]["loadModelVersion"]["status"]
        error = ret["data"]["loadModelVersion"]["error"]
        if status != "Online":
            raise RuntimeError(f"Model status after load was {status}: {error}")

    def create_model_from_pmml(
        self, model: str, filename: str, comment: Optional[str] = None
    ) -> str:
        """
        Create (or overwrite) model from PMML file.

        Arguments:
            model: Model name, e.g. "churn_predictor".
            filename: Local PMML file, e.g. "my_model.xml"
            comment: A comment string to store with the model version. Max 60 characters. Optional

        Returns:
            A `ModelVersion` handle to the upload job.
        """

        with open(filename, "rb") as f:
            version, upload_uri = self._create_empty_model_version(
                model, comment=comment
            )

            files = {"file": (filename, f)}
            http_response = requests.put(upload_uri, files=files)
            if http_response.status_code != 200:
                raise RuntimeError(http_response.error)

        self._load_model_version(model, version)

        return ModelVersion(self, model, version)

    def get_models_openai(self) -> pd.DataFrame:
        """
        Return all OpenAI models and their metadata.

        Returns:
            OpenAI Model metadata.
        """
        logger.debug("Getting openai models")
        query = """
            query OpenAIModelList {
                integration(type: "openai") {
                    type
                    creator
                    createdAt
                    updatedBy
                    updatedAt
                    error
                    status
                    output
                }
            }
        """

        empty = pd.DataFrame(
            columns=[
                "name",
                "owner",
                "type",
            ]
        )
        try:
            ret = self._execute_graphql(query=query)
        except RuntimeError as e:
            if str(e) == "could not find resource 'openai'":
                return empty
            raise

        integration = ret["data"]["integration"]
        if integration["status"] == "Error":
            raise RuntimeError(f"OpenAI integration error: {integration['error']}")

        rows = []
        output = integration.get("output") or {}
        for model in output.get("models", []):
            row = {
                "name": model["id"],
                "owner": model["owner"],
                "type": model["type"],
            }
            rows.append(row)
        if not rows:
            df = empty
        else:
            df = pd.DataFrame(rows)
        return df.set_index("name")

    def get_openai_config(self) -> dict:
        """
        Return the current OpenAI model configuration, if any

        Returns:
            OpenAI Model configuration state.
        """
        logger.debug("Getting openai config")
        query = """
            query OpenAIConfig {
                integration(type: "openai") {
                    creator
                    createdAt
                    updatedBy
                    updatedAt
                    error
                    status
                    config
                }
            }
        """

        try:
            ret = self._execute_graphql(query=query)
        except RuntimeError as e:
            if str(e) == "could not find resource 'openai'":
                return None
            raise

        return ret["data"]["integration"]

    def set_openai_config(self, api_key: str, timeout_ms: int = None, retry_limit: int = None, max_tokens: int = None) -> dict:
        """
        Create or update OpenAI model configuration

        Arguments:
            api_key: OpenAI API key
            timeout_ms: Timeout in milliseconds. Default 5000
            retry_limit: Number of retries to perform on API error. Default 3
            max_tokens: Maximum number of tokens to generate in a single request. Default 8192

        Returns:
            OpenAI Model configuration state.
        """
        logger.debug("Setting openai config")
        if timeout_ms is None:
            timeout_ms = 5000
        if retry_limit is None:
            retry_limit = 3
        if max_tokens is None:
            max_tokens = 8192

        current_config = self.get_openai_config()
        mutation = "createIntegration" if current_config is None else "updateIntegration"

        query = f"""
            mutation OpenAIConfig($config: JSON) {{
                {mutation}(type: "openai", config: $config) {{
                    creator
                    createdAt
                    updatedBy
                    updatedAt
                    error
                    status
                    config
                }}
            }}
        """

        ret = self._execute_graphql(query=query, variables={
            "config": {
                "apiKey": api_key,
                "timeoutMs": timeout_ms,
                "retryLimit": retry_limit,
                "maxTokens": max_tokens,
            }
        })

        return ret["data"][mutation]

    def delete_openai_config(self) -> None:
        """
        Delete the current OpenAI configuration
        """
        logger.debug("Deleting openai config")

        query = """
            mutation DeleteOpenAIConfig {
                deleteIntegration(type: "openai") {
                    type
                }
            }
        """

        self._execute_graphql(query=query)

    def refresh_openai_config(self) -> dict:
        """
        Refresh the OpenAI model list using the existing configuration

        Returns:
            OpenAI Model configuration state.
        """
        logger.debug("Refreshing openai config")

        query = """
            mutation RefreshOpenAI {
                testIntegration(type: "openai") {
                    creator
                    createdAt
                    updatedBy
                    updatedAt
                    error
                    status
                    config
                }
            }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["testIntegration"]

    def version(self) -> str:
        """
        Return the server-side version number.

        Returns:
            Version identifier
        """
        query = """
            query Version {
                version
            }
        """

        ret = self._execute_graphql(query=query)

        return ret["data"]["version"]

    def _get_session(self):
        query = """
                    query TempCredentials {
                        tenant { credentials }
                    }
                """

        ret = self._execute_graphql(query=query)

        creds = ret["data"]["tenant"]["credentials"]

        return boto3.Session(
            aws_access_key_id=creds["AccessKeyID"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
            region_name=CONFIG.aws_region,
        )

    def get_deps(self, live: bool = False) -> str:
        """
        Fetch latest dependencies from server as Scowl source `require` statements.

        Arguments:
            live: Return the LIVE versions of dependencies instead of latest.

        Returns:
            Scowl source code as string.
        """
        if live:
            raise NotImplementedError("option to fetch LIVE deps not yet supported")
        table_entries = []
        model_entries = []
        for _, row in self.get_tables().sort_index().iterrows():
            version = row.latest_version
            table_entries.append(f"  {row.name} {version}")
        for _, row in self.get_models().sort_index().iterrows():
            version = row.latest_version
            model_entries.append(f"  {row.name} {version}")
        final = ""
        if table_entries:
            joined = "\n".join(table_entries)
            final = f"require table (\n{joined}\n)\n"
        if model_entries:
            joined = "\n".join(model_entries)
            final += f"require model (\n{joined}\n)\n"
        return final

    def save_deps(self, live: bool = False, deps_file: Optional[str] = None) -> str:
        """
        Fetch latest dependencies from server and save to file

        Arguments:
            live: Return the LIVE versions of dependencies instead of latest.
            deps_file: Path to save deps file [default: ./deps.scowl]

        Returns:
            Full path to saved dependency file.
        """

        deps = self.get_deps(live)
        deps_file = deps_file or DEPS_FILE
        with open(deps_file, "w") as f:
            f.write(deps + "\n")
        return deps_file

    def resolve_deps_from_file(self, deps_file: Optional[str] = None) -> str:
        """
        Return the resolved resources (i.e. table schemas) from the local `deps.scowl` file.

        Arguments:
            deps_file: Path to deps file [default: ./deps.scowl]

        Returns:
            Resolved resource definitions (table schemas) as scowl code.
        """

        deps_file = deps_file or DEPS_FILE
        try:
            with open(deps_file, "r") as f:
                return self.resolve_deps(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find '{deps_file}'. Try running `sumatra deps update` first."
            )

    def resolve_deps(self, requires: str) -> str:
        """
        Return the resolved resources (i.e. table schemas) from the given requires statements.

        Arguments:
            requires: Scowl requires statement as code blob

        Returns:
            Resolved resource definitions (table schemas) as scowl code.
        """
        query = """
            query Deps($deps: String!) {
                resolveDeps(deps: $deps)
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"deps": requires},
        )

        return ret["data"]["resolveDeps"]

    def get_tables(self) -> pd.DataFrame:
        """
        Return all tables and their metadata.

        Returns:
            Table metadata.
        """
        logger.debug("Getting tables")
        query = """
            query TableList {
                tables {
                    nodes {
                        name
                        liveVersion {
                            version
                        }
                        latestVersion {
                            version
                        }
                        updatedAt
                        updatedBy
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query, error_prefix="error getting tables")

        rows = []
        for table in ret["data"]["tables"]["nodes"]:
            live_version = (
                table["liveVersion"]["version"] if table["liveVersion"] else ""
            )
            row = {
                "name": table["name"],
                "live_version": live_version,
                "latest_version": table["latestVersion"]["version"],
                "update_ts": table["updatedAt"],
                "updated_by": table["updatedBy"],
            }
            rows.append(row)
        if not rows:
            return pd.DataFrame(
                columns=[
                    "name",
                    "latest_version",
                    "live_version",
                    "update_ts",
                    "updated_by",
                ]
            )
        df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["update_ts"])
        return df.sort_values(["update_ts"], ascending=False).set_index("name")

    def get_table_schema(self, name: str, version: Optional[str] = None) -> str:
        if version is None:
            try:
                version = self.get_tables().loc[name].latest_version
            except KeyError:
                raise RuntimeError(f"table '{name}' not found")
        return self.get_table_version(name, version).schema

    def get_table_history(self, name: str) -> pd.DataFrame:
        """
        Return list of versions for the given table along with their metadata.

        Arguments:
            name: Table name.

        Returns:
            DataFrame of version metadata.
        """

        query = """
            query TableVersions($name: String!) {
                table(name: $name) {
                    versions {
                        nodes {
                            version
                            rowCount
                            status
                            createdAt
                            creator
                        }
                    }
                }
            }
        """

        ret = self._execute_graphql(query=query, variables={"name": name}, error_prefix=f"error getting versions of table '{name}'")

        rows = []
        for version in ret["data"]["table"]["versions"]["nodes"]:
            row = {
                "version": version["version"],
                "row_count": version["rowCount"],
                "status": _humanize_status(version["status"]),
                "create_ts": version["createdAt"],
                "created_by": version["creator"],
            }
            rows.append(row)
        if not rows:
            return pd.DataFrame(
                columns=[
                    "version",
                    "row_count",
                    "status",
                    "create_ts",
                    "created_by",
                ]
            )
        df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["create_ts"])
        return df.set_index("version")

    def get_table_version(self, name: str, version: str) -> TableVersion:
        """
        Return handle to a specific table version.

        Arguments:
            name: Table name.
            version: Table version.

        Returns:
            Table version future object.
        """
        return TableVersion(self, name, version)

    def _get_table_version(self, name: str, version: str) -> Dict[str, Any]:
        query = """
            query GetTableVersion($name: String!, $version: String!) {
                tableVersion(name: $name, version: $version) {
                    status
                    error
                    s3Uri
                    creator
                    createdAt
                    updatedAt
                    schema
                    rowCount
                    jobId
                    key
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"name": name, "version": version},
        )
        return ret["data"]["tableVersion"]

    def _create_empty_table_version(
        self, table: str, s3_uri: Optional[str] = None
    ) -> tuple[str, str]:
        query = """
            mutation TableVersionPath($name: String!, $s3Uri: String) {
                createEmptyTableVersion(name: $name, s3Uri: $s3Uri) {
                    version
                    s3Uri
                }
            }
        """

        variables = {"name": table}
        if s3_uri:
            variables["s3Uri"] = s3_uri
        ret = self._execute_graphql(query=query, variables=variables)

        version = ret["data"]["createEmptyTableVersion"]["version"]
        s3_uri = ret["data"]["createEmptyTableVersion"]["s3Uri"]
        return version, s3_uri

    def create_table_from_dataframe(
        self,
        table: str,
        df: pd.DataFrame,
        key_column: str,
        include_index: bool = False,
    ) -> TableVersion:
        """
        Create (or overwrite) table from a DataFrame

        Arguments:
            table: Table name.
            df: DataFrame to upload as table
            key_column: Name of column containing the prmary index for the table
            include_index: Include the DataFrame's index as a column named `index`?

        Returns:
            A `TableVersion` handle to the upload job.
        """
        MAX_ROWS_PER_FILE = 1000000

        if len(df) == 0:
            raise ValueError("non-empty dataframe required for table creation")
        if key_column not in df.columns:
            raise ValueError(
                f"key column '{key_column}' not found in column list: {df.columns.tolist()}"
            )
        if df[key_column].isnull().sum() > 0:
            raise ValueError(
                f"key column {key_column} contained missing or null values"
            )
        if df[key_column].nunique() != len(df):
            raise ValueError(f"key column {key_column} did not contain unique values")

        if not TABLE_NAME_REGEXP.match(table):
            raise ValueError(f"invalid table name '{table}'")
        for column in df.columns:
            if not TABLE_NAME_REGEXP.match(column):
                raise ValueError(f"invalid table field name '{column}'")

        version, s3_uri = self._create_empty_table_version(table)

        session = self._get_session()
        wr.s3.to_parquet(
            boto3_session=session,
            df=df,
            compression="snappy",
            path=s3_uri,
            dataset=True,
            index=include_index,
            bucketing_info=([key_column], (len(df) // MAX_ROWS_PER_FILE + 1)),
            concurrent_partitioning=True,
            pyarrow_additional_kwargs={
                "coerce_timestamps": "ms",
                "allow_truncated_timestamps": True,
                "use_deprecated_int96_timestamps": False,
            },
            mode="overwrite",
        )
        row_count = len(df)

        return self.create_table_from_s3(table, s3_uri, key_column, row_count, version)

    def create_table_from_s3(
        self,
        table: str,
        s3_uri: str,
        key_column: str,
        expected_row_count: int,
        version: Optional[str] = None,
    ) -> TableVersion:
        """
        Create (or overwrite) table from a DataFrame

        Arguments:
            table: Table name.
            s3_uri: S3 bucket URI.
            key_column: Name of column containing the prmary index for the table
            expected_row_count: Number of rows. Validated against what is ingested
            version: Use this existing empty table version. If unspecified, create a new table version.

        Returns:
            A `TableVersion` handle to the upload job.
        """

        if version is None:
            version, _ = self._create_empty_table_version(table, s3_uri)

        create_table_query = """
            mutation CreateTable($name: String!, $version: String!, $key: String!, $rowCount: Int!) {
                loadTableVersion(name: $name, version: $version, key: $key, rowCount: $rowCount) {
                    status
                }
            }
        """
        ret = self._execute_graphql(
            query=create_table_query,
            variables={
                "name": table,
                "version": version,
                "key": key_column,
                "rowCount": expected_row_count,
            },
        )

        return TableVersion(self, table, version)

    def delete_table_version(self, table: str, version: str) -> None:
        """
        Delete a specific version of a table permanently.

        If the table version is referenced in the LIVE topology, it cannot be deleted.

        Arguments:
            table: Table name.
            version: Version identifier.
        """
        query = """
            mutation DeleteTableVersion($name: String!, $version: String!) {
                deleteTableVersion(name: $name, version: $version) {
                    name
                    version
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={
                "name": table,
                "version": version,
            },
        )

    def delete_table(self, table: str) -> None:
        """
        Delete a table permanently.

        If the table is referenced in the LIVE topology, it cannot be deleted.

        Arguments:
            table: Table name.
        """
        query = """
            mutation DeleteTable($name: String!) {
                deleteTable(name: $name) {
                    name
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={
                "name": table,
            },
        )

    def delete_model_version(self, model: str, version: str) -> None:
        """
        Delete a specific version of a model permanently.

        If the model version is referenced in the LIVE topology, it cannot be deleted.

        Arguments:
            model: Model name.
            version: Version identifier.
        """
        query = """
            mutation DeleteModelVersion($name: String!, $version: String!) {
                deleteModelVersion(name: $name, version: $version) {
                    name
                    version
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={
                "name": model,
                "version": version,
            },
        )

    def delete_model(self, model: str) -> None:
        """
        Delete a model permanently.

        If the model is referenced in the LIVE topology, it cannot be deleted.

        Arguments:
            model: Model name.
        """
        query = """
            mutation DeleteModel($name: String!) {
                deleteModel(name: $name) {
                    name
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={
                "name": model,
            },
        )

    def list_users(self) -> pd.DataFrame:
        """
        List all of the users in this workspace

        Returns:
            A dataframe of the users and their metadata
        """

        query = """
            query getUsers($after: String) {
                currentTenant {
                    userRoles(first: 100, after: $after) {
                        nodes {
                            email
                            role
                            createdAt
                            updatedAt
                            creator
                            tenantSlug
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
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

            for d in ret["data"]["currentTenant"]["userRoles"]["nodes"]:
                rows.append({
                    "email": d["email"],
                    "role": d["role"],
                    "create_ts": d["createdAt"],
                    "update_ts": d["updatedAt"],
                    "creator": d["creator"],
                    "tenant": d["tenantSlug"],
                })
            has_next_page = ret["data"]["currentTenant"]["userRoles"]["pageInfo"]["hasNextPage"]
            variables["after"] = ret["data"]["currentTenant"]["userRoles"]["pageInfo"]["endCursor"]
        if not rows:
            return pd.DataFrame(
                columns=[
                    "email",
                    "role",
                    "create_ts",
                    "update_ts",
                    "creator",
                    "tenant",
                ]
            )
        df = pd.DataFrame(rows)
        df = parse_timestamp_columns(df, ["create_ts", "update_ts"])
        return df.set_index("email")

    def invite_user(self, email: str, role: str, resend_email: bool = True) -> Dict:
        """
        Invite a user to this workspace, with the given role.

        Arguments:
            email: The user's email address
            role: The desired role for the user. One of {'owner', 'publisher', 'writer', 'reader'}
            resend_email: If True, resend the invitation email if the user has already been invited to Sumatra

        Returns:
            A dict of the user's metadata
        """

        query = """
            mutation tenantCreateUser($email: String!, $role: String!, $resendEmail: Boolean) {
                tenantCreateUser(email: $email, role: $role, sendInvite: $resendEmail) {
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
            variables={"email": email, "role": role, "resendEmail": resend_email}
        )

        d = ret["data"]["tenantCreateUser"]
        return {
            "email": d["email"],
            "role": d["role"],
            "create_ts": pendulum.parse(d["createdAt"]),
            "update_ts": pendulum.parse(d["updatedAt"]),
            "creator": d["creator"],
            "tenant": d["tenantSlug"],
        }

    def remove_user(self, email: str) -> Dict:
        """
        Remove a user from this workspace

        Arguments:
            email: The user's email address

        Returns:
            A dict of the user's metadata
        """

        query = """
            mutation tenantDeleteUser($email: String!) {
                tenantDeleteUser(email: $email) {
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
            variables={"email": email}
        )

        d = ret["data"]["tenantDeleteUser"]
        return {
            "email": d["email"],
            "role": d["role"],
            "create_ts": pendulum.parse(d["createdAt"]),
            "update_ts": pendulum.parse(d["updatedAt"]),
            "creator": d["creator"],
            "tenant": d["tenantSlug"],
        }

    def set_user_role(self, email: str, role: str) -> Dict:
        """
        Set a user's role within this workspace.

        Note that the user must already be a member of the workspace. You can use `invite_user` to add a new user.

        Arguments:
            email: The user's email address
            role: The desired role for the user. One of {'owner', 'publisher', 'writer', 'reader'}

        Returns:
            A dict of the user's metadata
        """

        query = """
            mutation tenantSetUserRole($email: String!, $role: String!) {
                tenantSetUserRole(email: $email, role: $role) {
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
            variables={"email": email, "role": role}
        )

        d = ret["data"]["tenantSetUserRole"]
        return {
            "email": d["email"],
            "role": d["role"],
            "create_ts": pendulum.parse(d["createdAt"]),
            "update_ts": pendulum.parse(d["updatedAt"]),
            "creator": d["creator"],
            "tenant": d["tenantSlug"],
        }

class ModelVersion:
    """
    A handle to a versioned model resource
    """

    def __init__(self, client: Client, name: str, version: str):
        self._client = client
        self._name = name
        self._version = version
        self._mv = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    def __repr__(self) -> str:
        return f"ModelVersion(name='{self.name}', version='{self.version}', status='{self.status}')"

    def _get_model_version(self):
        return self._client._get_model_version(self.name, self.version)

    @property
    def status(self) -> str:
        """
        Current status of the job. One of {'Processing', 'Ready', 'Error'}
        """
        self._mv = self._get_model_version()
        return _humanize_status(self._mv["status"])

    @property
    def schema(self) -> str:
        """
        Scowl schema of the model
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["schema"]

    @property
    def error(self) -> Optional[str]:
        """
        Error reason string for a failed upload.
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["error"]

    @property
    def s3_uri(self) -> str:
        """
        S3 bucket path to PMML file
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["s3Uri"]

    @property
    def creator(self) -> str:
        """
        User that initiated the model upload
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["creator"]

    @property
    def created_at(self) -> datetime:
        """
        Timestamp when model version was created
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return pendulum.parser.parse(self._mv["createdAt"])

    @property
    def updated_at(self) -> datetime:
        """
        Timestamp when model version was last updated
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return pendulum.parser.parse(self._mv["updatedAt"])

    @property
    def schema(self) -> str:
        """
        Scowl model statement with schema
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["inputSchema"]

    @property
    def comment(self) -> str:
        """
        Comment from when the model version was uploaded
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["comment"]

    @property
    def scowl_snippet(self) -> str:
        """
        Example usage of the model version
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["scowlSnippet"]

    @property
    def metadata(self) -> str:
        """
        PMML metadata of the model version
        """
        if not self._mv:
            self._mv = self._get_model_version()
        return self._mv["metadata"]


class TableVersion:
    """
    A handle to a server-side table upload job, which uploads a new table version.

    Objects are not constructed directly. Table versions are returned by methods
    of the `Client` class.
    """

    def __init__(self, client: Client, name: str, version: str):
        self._client = client
        self._name = name
        self._version = version
        self._tv = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    def __repr__(self) -> str:
        return f"TableVersion(name='{self.name}', version='{self.version}', status='{self.status}')"

    def _get_table_version(self):
        return self._client._get_table_version(self.name, self.version)

    @property
    def status(self) -> str:
        """
        Current status of the job. One of {'New', 'Offline', 'Online', 'Error'}
        """
        self._tv = self._get_table_version()
        return _humanize_status(self._tv["status"])

    @property
    def error(self) -> Optional[str]:
        """
        Error reason string for a failed upload.
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["error"]

    def wait(self) -> str:
        """
        Wait until table version upload completes.

        Returns:
            Table version upload status
        """

        expected_status = "Ready"
        while self.status not in [expected_status, "Error"]:
            time.sleep(0.5)

        final_status = self.status
        if final_status != expected_status:
            raise RuntimeError(
                f"Table creation failed, status {final_status}, error {self.error}"
            )
        return final_status

    @property
    def s3_uri(self) -> str:
        """
        S3 bucket path to parquet file
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["s3Uri"]

    @property
    def creator(self) -> str:
        """
        User that initiated the table version job
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["creator"]

    @property
    def created_at(self) -> datetime:
        """
        Timestamp when table version was created
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return pendulum.parser.parse(self._tv["createdAt"])

    @property
    def updated_at(self) -> datetime:
        """
        Timestamp when table version was last updated
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return pendulum.parser.parse(self._tv["updatedAt"])

    @property
    def schema(self) -> str:
        """
        Scowl table statement with schema
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["schema"]

    @property
    def row_count(self) -> int:
        """
        Number of rows in table
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["rowCount"]

    @property
    def job_id(self) -> str:
        """
        Job indentifier for validation and ingest
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["jobId"]

    @property
    def key(self) -> str:
        """
        Name of primary index column
        """
        if not self._tv:
            self._tv = self._get_table_version()
        return self._tv["key"]


class Materialization:
    """
    A handle to a server-side materialization (replay) job, which enriches a Timeline
    (or set of Timelines) by running it (them) through a given Topology.

    Objects are not constructed directly. Materializations are returned by methods
    of the `Client` class.
    """

    def __init__(self, client, id):
        self._client = client
        self.id = id
        self._mtr = None

    def __repr__(self):
        return f"Materialization(id='{self.id}')"

    def _get_materialization(self):
        query = """
            query Materialization($id: String!) {
                materialization(id: $id) { id, state, path, timelines, events, branch, hash, jobsSubmitted, jobsCompleted }
            }
        """

        ret = self._client._execute_graphql(query=query, variables={"id": self.id})

        return ret["data"]["materialization"]

    def status(self) -> str:
        """
        Current status of the job. One of {'processing', 'materialized', 'error'}
        """
        self._mtr = self._get_materialization()
        return self._mtr["state"]

    def wait(self) -> str:
        """
        Wait until materialization completes. In a Notebook, a progress bar is displayed.

        Returns:
            Materialization status
        """

        self._mtr = self._get_materialization()
        if self._mtr["state"] not in ["new", "processing", "materialized"]:
            raise RuntimeError(f"Error in {self}: {self._mtr['state']}")

        # Do not show progress bars if already materialized
        if self._mtr["state"] == "materialized":
            return self._mtr["state"]

        while self._mtr["jobsSubmitted"] == 0 and self._mtr["state"] in [
            "new",
            "processing",
        ]:
            sleep(0.5)
            self._mtr = self._get_materialization()

        submitted = self._mtr["jobsSubmitted"]
        completed = self._mtr["jobsCompleted"]

        with tqdm(total=submitted) as pbar:
            pbar.update(completed)
            while self._mtr["state"] == "processing":
                sleep(0.5)
                self._mtr = self._get_materialization()
                new_completed = self._mtr["jobsCompleted"]
                new_submitted = self._mtr["jobsSubmitted"]
                if new_submitted != submitted:
                    pbar.total = new_submitted
                    submitted = new_submitted

                pbar.update(new_completed - completed)
                completed = new_completed
            if self._mtr["state"] == "materialized":
                pbar.update(submitted - completed)

        return self._mtr["state"]

    def progress(self) -> str:
        """
        Current progress of subjobs: X of Y jobs completed.
        """
        self._mtr = self._get_materialization()

        if self._mtr["state"] != "processing":
            return self._mtr["state"]
        else:
            completed = self._mtr["jobsCompleted"]
            submitted = self._mtr["jobsSubmitted"]
            return f"{completed} / {submitted} jobs completed."

    @property
    def timelines(self) -> List[str]:
        """
        Timelines materialized by the job.
        """
        if self._mtr is None:
            self._mtr = self._get_materialization()
        return list(sorted(self._mtr["timelines"]))

    @property
    def event_types(self) -> List[str]:
        """
        Materialized event types
        """
        if self._mtr is None:
            self._mtr = self._get_materialization()
        return list(sorted(self._mtr["events"]))

    @property
    def branch(self) -> str:
        """
        Topology branch used for materialization.
        """
        if self._mtr is None:
            self._mtr = self._get_materialization()
        return self._mtr["branch"]

    @property
    def hash(self) -> str:
        """
        Unique hash identifying the job.
        """
        if self._mtr is None:
            self._mtr = self._get_materialization()
        return self._mtr["hash"]

    @property
    def path(self) -> str:
        """
        S3 bucket path where results are stored.
        """
        self.wait()
        return self._mtr["path"]

    def get_events(self, event_type: str, features: List[str] = []) -> pd.DataFrame:
        """
        Return enriched events of specified type. Waits if
        job is still processing.
        (DEPRECATED) use get_features() instead.

        Arguments:
            event_type: Name of event type to fetch.
            features: Feature names to fetch. By default, fetch all.

        Returns:
            Enriched events
        """
        logger.warn(
            "get_events() is deprecated and will be removed in the next release. Use get_features() instead."
        )
        return self.get_features(event_type, features)

    def get_features(self, event_type: str, features: List[str] = []) -> pd.DataFrame:
        """
        Return feature values for given event type. Waits if
        job is still processing.

        Arguments:
            event_type: Name of event type to fetch.
            features: Feature names to fetch. By default, fetch all.

        Returns:
            Feature dataframe
        """
        # if event_type not in self.event_types:
        #    raise RuntimeError(f"Event type '{event_type}' not found.")

        self.wait()
        session = self._client._get_session()

        path = f"{self.path}/events/event_type={event_type}/"
        cols = ["_id", "_type", "_time"]

        if not features:
            df = wr.s3.read_parquet(
                boto3_session=session,
                path=path,
                use_threads=8,
            )
        else:
            cols.extend(features)
            df = wr.s3.read_parquet(
                boto3_session=session,
                path=path,
                columns=cols,
                use_threads=8,
            )

        df = tz_convert_timestamp_columns(df)
        return df.set_index("_id")

    def get_errors(self, event_type: str, features: List[str] = []) -> pd.DataFrame:
        """
        Return event-level materialization errors for specified event type. Waits if
        job is still processing.

        Arguments:
            event_type: Name of event type to fetch.
            features: Feature names to fetch. By default, fetch all.

        Returns:
            Event-level errors
        """
        # if event_type not in self.event_types:
        #    raise RuntimeError(f"Event type '{event_type}' not found.")

        self.wait()
        session = self._client._get_session()

        path = f"{self.path}/errors/event_type={event_type}/"
        cols = ["_id", "_type", "_time"]
        cols.extend(features)

        try:
            if not features:
                df = wr.s3.read_parquet(
                    boto3_session=session,
                    path=path,
                    ignore_empty=True,
                )
            else:
                df = wr.s3.read_parquet(
                    boto3_session=session,
                    path=path,
                    columns=cols,
                    ignore_empty=True,
                )
        except Exception as e:
            logger.debug(e)
            return pd.DataFrame(columns=cols)

        df = tz_convert_timestamp_columns(df)
        return df.set_index("_id")
