"""
Manage code on your website.

- Implements [PEP 503 -- Simple Repository API][0] managing Python packages.

[0]: https://www.python.org/dev/peps/pep-0503/

"""

# TODO PEP 592 -- Adding "Yank" Support to the Simple API
# TODO PEP 658 -- Serve Distribution Metadata in the Simple Repository API

import os
import pathlib
import re
import shutil
import subprocess
import time

import gmpg
import pkg_resources
import semver
import web
import webagt

app = web.application(
    __name__,
    prefix="code",
    args={
        "project": r"[A-Za-z0-9\.-][A-Za-z0-9\._-]+",
        "commit_id": r"[a-f0-9]{3,40}",
        "release": r"((\d+\.)?\d+\.)?\d+",
        "filename": r"[\w./\-]+",
        "package": r"[\w.-]+",
        "namespace": r"[\w._/]+",
    },
    model={
        "projects": {
            "name": "TEXT UNIQUE",
            "pypi": "TEXT UNIQUE",
            "visibility": "TEXT",
        },
        "packages": {
            "project_id": "INTEGER",
            "filename": "TEXT",
            "author": "TEXT",
            "author_email": "TEXT",
            "classifiers": "JSON",
            "home_page": "TEXT",
            "keywords": "JSON",
            "license": "TEXT",
            "project_urls": "JSON",
            "requires_dist": "JSON",
            "requires_python": "TEXT",
            "sha256_digest": "TEXT",
            "summary": "TEXT",
            "version": "TEXT",
        },
    },
)

code_dir = pathlib.Path("code")
meta_dir = code_dir / "meta"
# XXX working_dir = code_dir / "working"


# XXX def update_system():
# XXX     print(
# XXX         subprocess.run(
# XXX             ["poetry", "update"],
# XXX             cwd=working_dir / "ragt.ag",
# XXX             capture_output=True,
# XXX         )
# XXX     )


def run_ci(project):
    """
    Run continuous integration pipeline.

    Execute tests.

    """
    project_dir = meta_dir / project
    testing_dir = project_dir / "testing"
    shutil.rmtree(testing_dir, ignore_errors=True)
    gmpg.clone_repo(project_dir / "source.git", testing_dir)
    admin_home = "/home/admin"
    env = os.environ.copy()
    env["HOME"] = admin_home
    print(
        subprocess.run(
            [f"{admin_home}/bin/act", "--artifact-server-path", "artifacts"],
            cwd=testing_dir,
            env=env,
        )
    )
    for artifact in (testing_dir / "artifacts/1/analysis").iterdir():
        shortened = artifact.name[:-2]
        artifact.rename(testing_dir / shortened)
        subprocess.run(["gunzip", shortened], cwd=testing_dir)


@app.query
def search(db, query):
    """Search for `query` in commited code."""
    files = {}
    context = "2"
    for file in (
        subprocess.run(
            [
                "ag",
                "--ackmate",
                "-B",
                context,
                "-A",
                context,
                "-G",
                ".*/working",
                query,
            ],
            cwd=meta_dir,
            capture_output=True,
        )
        .stdout.decode()
        .split("\n\n")
    ):
        filename, _, blocks_text = file.partition("\n")
        blocks = {}
        for block_text in blocks_text.split("\n--\n"):
            starting_line = block_text.partition(":")[0].partition(";")[0]
            block = "\n".join(
                [line.partition(":")[2] for line in block_text.splitlines()]
            )
            blocks[starting_line] = block
        files[filename.lstrip(":").partition("/working/")[::2]] = blocks
    return files


# XXX @app.wrap
# XXX def set_working_dir(handler, main_app):
# XXX     web.tx.host.working_dir = working_dir
# XXX     yield


@app.query
def create_project(db, name):
    """Create a project."""
    db.insert("projects", name=name, pypi=name, visibility="public")
    project_dir = meta_dir / name
    bare_repo = project_dir / "source.git"
    working_repo = project_dir / "working"
    repo = gmpg.get_repo(bare_repo, init=True, bare=True)
    repo.update_server_info()
    repo.config("http.receivepack", "true")
    post_receive_hook = bare_repo / "hooks/post-receive"
    with post_receive_hook.open("w") as fp:
        fp.write(
            "\n".join(
                (
                    "#!/bin/sh",
                    "git -C $PWD/../working --git-dir=.git pull origin main --rebase",
                    f"wget --method=post -qO- {web.tx.origin}/code/projects/{name}",
                )
            )
        )
    gmpg.clone_repo(bare_repo, working_repo)
    subprocess.run(["chmod", "775", post_receive_hook])
    subprocess.run(["chgrp", "www-data", bare_repo, working_repo, "-R"])
    subprocess.run(["chmod", "g+w", bare_repo, working_repo, "-R"])
    if not (meta_dir / "gitpasswd").exists():
        token = web.application("webint_auth").model.generate_local_token(
            "/code", "webint_code", "git_owner"
        )
        subprocess.run(["htpasswd", "-cb", meta_dir / "gitpasswd", "owner", token])
    # XXX subprocess.run(["sudo", "service", "nginx", "restart"])

    # XXX gmpg.clone_repo(
    # XXX     f"{web.tx.origin}/code/projects/{name}.git", f"{working_dir}/{name}"
    # XXX )

    web.application("webint_posts").model.create(
        "entry",
        url=f"/code/projects/{name}",
        content=(
            f"Created repository <a href=/code/projects/{name}><code>{name}</code></a>"
        ),
    )


@app.query
def get_projects(db):
    """Return a list of project names."""
    visibility_wheres = ["public"]
    if web.tx.user.is_owner:
        visibility_wheres.extend(["protected", "private"])
    return [
        r["name"]
        for r in db.select(
            "projects",
            what="name",
            order="name",
            where=" OR ".join(len(visibility_wheres) * ["visibility = ?"]),
            vals=visibility_wheres,
        )
    ]


@app.query
def get_pypi_projects(db):
    """Return a list of PyPI project names."""
    return [r["pypi"] for r in db.select("projects", what="pypi", order="name")]


@app.query
def get_project_from_name(db, name):
    """Return the project associated with project name."""
    try:
        return db.select("projects", where="name = ?", vals=[name])[0]
    except IndexError:
        return None


@app.query
def get_project_from_pypi_name(db, pypi_name):
    """Return the project name associated with pypi package name."""
    try:
        return db.select("projects", where="pypi = ?", vals=[pypi_name])[0]
    except IndexError:
        return None


@app.query
def create_package(db, form):
    """Create a project."""
    project_id = db.select(
        "projects", what="rowid, name", where="pypi = ?", vals=[form.name]
    )[0]["rowid"]
    return db.insert(
        "packages",
        project_id=project_id,
        filename=form.content.fileobj.filename,
        author=form.author,
        author_email=form.author_email,
        # classifiers=form.classifiers,
        home_page=form.home_page,
        # keywords=form.keywords.split(","),
        license=form.license,
        # project_urls=form.project_urls if "project_urls" in form else [],
        # requires_dist=form.requires_dist,
        requires_python=form.requires_python,
        sha256_digest=form.sha256_digest,
        summary=form.summary,
        version=form.version,
    )


@app.query
def get_packages(db, project):
    """Return a list of packages for given project."""
    return db.select(
        "packages",
        join="""projects ON packages.project_id = projects.rowid""",
        where="projects.pypi = ?",
        vals=[project],
    )


@app.query
def get_package_versions(db, project):
    """Return a list of packages for given project."""
    return [
        r["version"]
        for r in db.select(
            "packages",
            what="DISTINCT version",
            join="""projects ON packages.project_id = projects.rowid""",
            where="projects.name = ?",
            vals=[project],
            order="version",
        )
    ]


@app.control("")
class Code:
    """Code index."""

    def get(self):
        """Return a list of projects."""
        return app.view.index(
            None,  # get_versions("webint"),
            web.get_apps(),
            app.model.get_projects(),
        )


@app.control("projects")
class Projects:
    """List of projects."""

    owner_only = ["post"]

    def get(self):
        """Return a list of projects."""
        return app.view.projects(app.model.get_projects())

    def post(self):
        """Create a project."""
        project = web.form("project").project
        app.model.create_project(project)
        return web.Created(app.view.project.created(project), f"/{project}")


@app.control("projects/{project}")
class Project:
    """Project index."""

    def get(self, project):
        """Return details about the project."""
        mentions = web.application(
            "webint_mentions"
        ).model.get_received_mentions_by_target(
            f"{web.tx.origin}/{web.tx.request.uri.path}"
        )
        project_dir = meta_dir / project
        try:
            with (project_dir / "working" / "README.md").open() as fp:
                readme = fp.read()
        except FileNotFoundError:
            readme = None
        try:
            pyproject = gmpg.get_current_project(project_dir / "testing")
        except FileNotFoundError:
            pyproject = None
        testing_dir = project_dir / "testing"
        try:
            api_python = web.load(path=testing_dir / "api_python.json")
        except FileNotFoundError:
            api_python = {}
        try:
            test_results = gmpg.analysis._parse_junit(testing_dir / "test_results.xml")
        except FileNotFoundError:
            test_results = {}
        try:
            test_coverage = gmpg.analysis._parse_coverage(
                testing_dir / "test_coverage.xml"
            )
        except FileNotFoundError:
            test_coverage = {}
        return app.view.project.index(
            project,
            gmpg.get_repo(project_dir / "working"),
            readme,
            app.model.get_package_versions(project),
            pyproject,
            api_python,
            test_results,
            test_coverage,
            mentions,
        )

    def post(self, project):
        web.enqueue(run_ci, project)
        return "CI enqueued"

    def delete(self, project):
        """Delete the project."""
        return "deleted"


@app.control("projects/{project}.git")
class ProjectGitRedirect:
    """Project .git redirect."""

    def get(self, project):
        """Redirect to main project index."""
        raise web.SeeOther(project)


@app.control("projects/{project}/api/{namespace}.svg")
class ProjectAPIDeps:
    """Project's API in JSON."""

    def get(self, project, namespace):
        """Return the API's JSON."""
        return meta_dir / project / "testing" / f"deps.svg"


@app.control("projects/{project}/api/{namespace}")
class ProjectAPINamespace:
    """Project's API namespace."""

    def get(self, project, namespace):
        """Return the API's namespace."""
        details = web.load(path=meta_dir / project / "testing" / "api_python.json")
        return app.view.project.namespace(project, namespace, details)


@app.control("projects/{project}/api.json")
class ProjectAPIJSON:
    """Project's API in JSON."""

    def get(self, project):
        """Return the API's JSON."""
        return meta_dir / project / "testing" / "api_python.json"


@app.control("projects/{project}/settings")
class ProjectSettings:
    """Project settings."""

    def get(self, project):
        """Return settings for the project."""
        return app.view.project.settings(project)

    def post(self, project):
        form = web.form("visibility")
        return form.visibility


@app.control("projects/{project}/files(/{filename})?")
class ProjectRepoFile:
    """A file in a project's repository."""

    def get(self, project, filename=""):
        """Return a view of the repository's file."""
        project_dir = meta_dir / project
        filepath = project_dir / "working" / filename
        try:
            with filepath.open() as fp:
                content = fp.read()
        except IsADirectoryError:
            content = filepath.iterdir()
        except UnicodeDecodeError:
            content = None
        testing_dir = project_dir / "testing"
        try:
            test_coverage = gmpg.analysis._parse_coverage(
                testing_dir / "test_coverage.xml"
            )[filename][1]
        except (FileNotFoundError, KeyError):
            test_coverage = None
        return app.view.project.repository_file(
            project, filename, content, test_coverage
        )


@app.control("projects/{project}/raw(/{filename})?")
class ProjectRepoRawFile:
    """A file in a project's repository."""

    def get(self, project, filename=""):
        """Return a view of the repository's file."""
        return meta_dir / project / "working" / filename


@app.control("projects/{project}/commits")
class ProjectCommitLog:
    """A commit log of a project's repository."""

    def get(self, project):
        """Return a view of the repository's commit."""
        repo = gmpg.get_repo(meta_dir / project / "working")
        return app.view.project.commit_log(project, repo)


@app.control("projects/{project}/commits/{commit_id}")
class ProjectCommit:
    """A commit to a project's repository."""

    def get(self, project, commit_id=None):
        """Return a view of the repository's commit."""
        repo = gmpg.get_repo(meta_dir / project / "working")
        full_commit_id = repo.git("rev-parse", commit_id)[0]
        if commit_id != full_commit_id:
            raise web.SeeOther(f"/code/projects/{project}/commits/{full_commit_id}")
        return app.view.project.commit(project, repo, commit_id)


@app.control("projects/{project}/releases")
class ProjectReleases:
    """A project's release."""

    def get(self, project):
        """Return a view of the package file."""
        return f"releases for {project}"
        # files = sorted((meta_dir / project / "releases" / release).iterdir())
        # return app.view.project.release(project, release, files)


@app.control("projects/{project}/releases/{release}")
class ProjectRelease:
    """A project's release."""

    def get(self, project, release):
        """Return a view of the package file."""
        pypi_name = app.model.get_project_from_name(project)["pypi"]
        files = sorted(
            (meta_dir / project / "releases" / f"{pypi_name}-{release}").iterdir()
        )
        return app.view.project.release(project, release, files)


@app.control("projects/{project}/releases/{release}/files(/{filename})?")
class ProjectReleaseFile:
    """A file in a project's release."""

    def get(self, project, release, filename=""):
        """Return a view of the release's file."""
        pypi_name = app.model.get_project_from_name(project)["pypi"]
        filepath = meta_dir / project / "releases" / f"{pypi_name}-{release}" / filename
        try:
            with filepath.open() as fp:
                content = fp.read()
        except IsADirectoryError:
            content = filepath.iterdir()
        return app.view.project.release_file(project, release, filename, content)


@app.control("projects/{project}/issues")
class ProjectIssues:
    """A project's issues."""

    def get(self, project):
        """Return a view of the package's issues."""
        mentions = web.application(
            "webint_mentions"
        ).model.get_received_mentions_by_target(
            f"{web.tx.origin}/{web.tx.request.uri.path}"
        )
        return [dict(r) for r in mentions]
        # files = sorted((meta_dir / project / "releases" / release).iterdir())
        # return app.view.project.release(project, release, files)


def split_release(release):
    """Return a 4-tuple of the parts in given `release` (eg foo-1.2.3 -> foo,1,2,3)."""
    return re.match(r"([\w.-]+)\-(\d+\.\d+\.\d+.*)", release).groups()


@app.control("pypi")
class PyPIIndex:
    """PyPI repository in Simple Repository format."""

    # TODO owner_only = ["post"]

    def get(self):
        """Return a view of the simplified list of projects in repository."""
        return app.view.pypi.index(app.model.get_pypi_projects())

    def post(self):
        """Accept PyPI package upload."""
        form = web.form(":action")
        if form[":action"] != "file_upload":
            raise web.BadRequest(f"Provided `:action={form[':action']}` not supported.")
        try:
            release_file = form.content.save(file_dir="/tmp")
        except FileExistsError:
            return
        release_name, release_remaining = split_release(release_file.name)
        project = app.model.get_project_from_pypi_name(
            release_name.replace("_", "-").replace(".", "-")
        )
        releases_dir = meta_dir / project["name"] / "releases"
        releases_dir.mkdir(exist_ok=True)
        release_file = release_file.replace(
            releases_dir / f"{release_name}-{release_remaining}"
        )
        if release_file.suffix == ".gz":
            subprocess.run(
                [
                    "tar",
                    "xf",
                    release_file.name,
                ],
                cwd=releases_dir,
            )
        app.model.create_package(form)
        # web.application("webint_posts").model.create(
        #     "entry",
        #     url=f"/code/{form.name}/releases/{release_file.name}",
        #     content=(
        #         f"Released <a href=/code/{form.name}><code>{form.name}</code></a> "
        #         f"version <code>{release_remaining}</code>"
        #     ),
        # )
        raise web.Created(
            "Package has been uploaded.",
            "/{form.name}/packages/{form.content.fileobj.filename}",
        )


@app.control("pypi/{project}")
class PyPIProject:
    """PyPI project in Simple Repository format."""

    def get(self, project):
        """Return a view of the simplified list of packages in given `project`."""
        if packages := app.model.get_packages(project):
            return app.view.pypi.project(project, packages)
        raise web.SeeOther(f"https://pypi.org/simple/{project}")


@app.control("search")
class Search:
    """Search all code."""

    def get(self):
        """"""
        try:
            query = web.form("q").q
        except web.BadRequest:
            return app.view.search.index()
        return app.view.search.results(query, app.model.search(query))


# XXX @app.control("system")
# XXX class System:
# XXX     """System code."""
# XXX
# XXX     def get(self):
# XXX         """"""
# XXX         return app.view.system(web.tx.app)
# XXX
# XXX
# XXX @app.control("system/update")
# XXX class SystemUpdate:
# XXX     """Update the system."""
# XXX
# XXX     def post(self):
# XXX         """"""
# XXX         web.enqueue(update_system)
# XXX         return "update has been started"
