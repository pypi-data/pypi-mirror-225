import datetime
import os
from typing import Dict

from git import Repo
from giturlparse import parse

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class URLPatternsMixin:
    """
    A mixin that builds a set of f-strings to use when rendering links to commits,
    projects and diffs to upstream git hosting providers.
    """

    def build_url_patterns(self, repo: Repo) -> Dict[str, str]:
        """
        Build a set of f-strings to use when rendering links for commits,
        projects and diffs, and save them as :py:attr:`url_patterns`.  Different
        git hosting providers of course have different URLs for

        Detect the upstream provder by looking at the host for our upstream
        remote url a

        .. note::
            If our remote is a CodeStar connection, we assume it's a Bitbucket
            repo, but this is not always the case.  Unfortunately, there's no
            way to tell from the remote URL whether it's a Github or Bitbucket
            repo, so we have to rely on the environment variable
            ``CI_BUILDBOT_HOST`` and ``CI_BUILDBOT_GIT_OWNER`` to force it.
        """
        url_patterns: Dict[str, str] = {}
        p = parse(repo.remote().url)
        host = p.host
        owner = p.owner
        if host.startswith('codestar-connections'):
            # if our host is a CodeStar connection, we can't tell implicitly
            # what the actual upstream is, so we have to rely on environment
            # variables to tell us, defaulting to Bitbucket
            host = os.environ.get('CI_BUILDBOT_HOST', "bitbucket.org")
            owner = os.environ.get('CI_BUILDBOT_GIT_OWNER', "caltech-imss-ads")
        origin_url = f"https://{host}/{owner}/{p.repo}"
        if origin_url.endswith('.git'):
            origin_url = origin_url[:-4]
        if p.github:
            url_patterns['commit'] = f"<{origin_url}/commit/" + "{sha}|{sha}>"
            url_patterns['project'] = f"<{origin_url}/tree/" + "{version}|{name}>"
            url_patterns['diff'] = f"{origin_url}/compare/" + "{from_sha}..{to_sha}"
        else:
            # Assume bitbucket
            url_patterns['commit'] = f"<{origin_url}/commits/" + "{sha}|{sha}>"
            url_patterns['project'] = f"<{origin_url}/src/" + "{version}/|{name}>"
            url_patterns['diff'] = f"{origin_url}/branches/compare/" + "{from_sha}..{to_sha}#diff"
        url_patterns['repo'] = origin_url
        return url_patterns


class GitProcessor(URLPatternsMixin, AbstractContextProcessor):
    """
    A context processor that adds information about the current git repository.

    This adds the following keys to the context:

    * ``repo``: the URL of the upstream repository
    * ``branch``: the name of the current branch
    * ``sha``: the sha of the HEAD commit
    * ``committer``: the author of the latest commit
    * ``last_version_sha``: the sha of the commit for the previous version
    * ``last_version_url``: the URL to the previous version in the upstream git
      hosting provider
    * ``previous_version``: the version number for the tag before this one
    * ``diff_url``: the URL to the diff between the previous version and this one
    * ``git_info``: a string containing the branch, commit, and committer of the
      last commit
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.repo: Repo = Repo('.')
        self.url_patterns: Dict[str, str] = self.build_url_patterns(self.repo)

    def __get_last_version(self, context: MessageContext) -> None:
        """
        Update the `values` dict with:

        * ``previous_version``: the version number for the tag immediately preceeding ours
        * ``last_version_sha``: the sha that that tag points to
        """
        # Get all tags, sorted by the authored_date on their associated commit.
        # We should have at least one tag -- the one for this commit.
        ordered_tags = sorted(self.repo.tags, key=lambda x: x.commit.authored_date)
        if len(ordered_tags) >= 2:
            # If there are 2 or more tags, there was a previous version.
            # Extract info from the tag preceeding this one.
            context['last_version_sha'] = ordered_tags[-2].commit.hexsha
            context['last_version_url'] = self.url_patterns['project'].format(
                version=context['version'],
                name=f"{context['name']}-{context['version']}"
            )
            context['previous_version'] = ordered_tags[-2].name
        else:
            # There was just our current version tag, and no previous tag.  Go
            # back to the initial commit.
            commits = list(self.repo.iter_commits())
            commits.reverse()
            context['last_version_sha'] = commits[0].hexsha
            context['last_version_url'] = self.url_patterns['project'].format(
                version=context['version'],
                name=f"{context['name']}-{context['version']}"
            )
            context['previous_version'] = "initial"

    def __get_concise_info(self) -> str:
        """
        Build a string that describes who did the build, what branch that is and
        what sha.  Determine this by looking at the owner of the latest commit.

        The string will look like this::

            {branch} {sha_url} {author name} <{author email}>

        Returns:
            A string representing
        """
        branch = self.get_branch()
        current = self.repo.head.commit
        sha = current.hexsha[0:7]
        sha_url = self.url_patterns['commit'].format(sha=sha)
        committer = f"{current.author.name} <{current.author.email}>"
        return f"{branch} {sha_url} {committer}"

    def get_branch(self) -> str:
        """
        Return the name of the current git branch.  This will be empty string
        if we are in ``DETACHED_HEAD`` state.

        Returns:
            The name of the current git branch, if any.
        """
        try:
            return self.repo.head.reference.name
        except TypeError:
            # We're in DETACHED_HEAD state, so we have no branch name
            return ''

    def annotate(self, context: MessageContext) -> None:
        """
        Extract info about the git repo.  Assume we're in the checked out clone.

        Add these values:

        * ``committer``: who committed the HEAD commit
        * ``sha``: the SHA of the HEAD commit
        * ``branch``: the name current branch, if any
        * ``diff_url``: the URL string (``[Click here]<url>``) for the diff on
          the origin provider, if any
        * ``git_info``: the ``{branch} {sha_url} {committer}`` string for the release

        Args:
            context: the current message context
        """
        super().annotate(context)
        headcommit = self.repo.head.commit
        context['committer'] = str(headcommit.author)
        context['sha'] = headcommit.hexsha
        context['branch'] = self.get_branch()
        self.__get_last_version(context)
        # Add the diff URL
        if 'diff' in self.url_patterns:
            context['diff_url'] = self.url_patterns['diff'].format(
                from_sha=context['sha'][0:7],
                to_sha=context['last_version_sha'][0:7],
            )
        context['git_info'] = self.__get_concise_info()


class GitChangelogProcessor(URLPatternsMixin, AbstractContextProcessor):
    """
    A context processor that adds information about the changelog for the
    git repository.

    This adds the following keys to the context:

    * ``authors``: a list of all authors in those commits
    * ``changelog``: a list of strings representing the commits

    .. important::
        This needs to be used after GitMixin in the inheritance chain.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.repo: Repo = Repo('.')
        self.url_patterns = self.build_url_patterns(self.repo)

    def annotate(self, context: MessageContext) -> None:
        """
        Look through the commits between the current version and the last version
        Update ``context`` with two new keys:

        * ``authors``: a list of all authors in those commits
        * ``changelog``: a list of strings representing the commits

        Args:
            context: the current message context
        """
        # get the changes between here and the previous tag
        changelog_commits = []
        current = self.repo.head.commit
        # Gather all commits from HEAD to `last_version_sha`
        while True:
            changelog_commits.append(current)
            if current.hexsha == context['last_version_sha']:
                break
            try:
                current = current.parents[0]
            except IndexError:
                # We really should never get here
                break
        changelog = []
        authors = set()
        for commit in changelog_commits:
            authors.add(commit.author.name)
            d = datetime.datetime.fromtimestamp(commit.committed_date).strftime("%Y/%m/%d")
            commit_link = self.url_patterns['commit'].format(sha=commit.hexsha[0:7])
            # escape any double quotes in the summary
            summary = commit.summary.replace('"', r'\"')
            changelog.append(f"{commit_link} [{d}] {summary} - {str(commit.author)}")
        context['authors'] = sorted(authors)
        context['changelog'] = changelog
