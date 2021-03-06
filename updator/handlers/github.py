# Copyright 2021 Naveen M K
# SPDX-License-Identifier: MIT
import os

from github import Github

from .handler import Handler
from ..utils import VersionSort

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)


class GithubHandler(Handler):
    def __init__(self, info) -> None:
        self.info = info
        if info["api_url"] == "":
            self.gh = Github(GITHUB_TOKEN)
        else:
            self.gh = Github(base_url=info["api_url"], login_or_token=GITHUB_TOKEN)

    @property
    def remote_version(self) -> None:
        if hasattr(self, "_remote_version"):
            return self._remote_version
        gh = self.gh
        info = self.info
        repo = gh.get_repo(info["slug"])
        releases = repo.get_releases()
        if releases.totalCount != 0:
            releases = repo.get_releases()[:10]
            version_list=[]
            for v in releases:
                if not v.prerelease:
                    version_list.append(v.tag_name if v.tag_name[0] != "v" else v.tag_name[1:])
        else:
            versions = repo.get_tags()[:10]
            version_list = [v.name if v.name[0] != "v" else v.name[1:] for v in versions]
        version_list.sort(key=VersionSort)
        version = version_list[-1]
        self._remote_version = version
        return version
