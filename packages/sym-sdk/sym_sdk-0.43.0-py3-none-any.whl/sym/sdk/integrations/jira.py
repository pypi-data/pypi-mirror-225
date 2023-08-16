"""Helpers for interacting with the Jira API within the Sym SDK."""


from typing import List, Optional

from sym.sdk.exceptions import JiraError  # noqa


def search_issues(
    jql: str,
    fields: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
) -> List[dict]:
    """Returns a list of issues matching the given JQL query.

    See Jira's API docs
    `here <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-postt>`_ for details.

    Args:
        jql: A non-empty JQL expression.
        fields: A list of fields to return for each issue. Use it to retrieve a subset of fields.
        expand: An optional list of strings indicating what additional information about issues to include in the response.

    Returns:
        A list of dictionaries representing Jira issues.

    Raises:
        :class:`~sym.sdk.exceptions.jira.JiraError`: If the JQL expression is empty.
    """
