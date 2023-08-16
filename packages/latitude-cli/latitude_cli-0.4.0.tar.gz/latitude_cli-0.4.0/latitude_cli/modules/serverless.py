import os
from shutil import rmtree

import typer
from git import Repo

app = typer.Typer()


@app.command(short_help="Creates a new Serverless App from a template")
def init(app_name: str):
    print(f"creating {app_name}")
    new_app_directory = os.path.abspath(
        os.path.join(os.getcwd(), app_name))

    Repo.clone_from(
        "https://github.com/hloughrey/latitude55-serverless-template",
        new_app_directory,
        branch="master",
        depth=1,
    )

    git_directory = os.path.abspath(os.path.join(new_app_directory, ".git"))
    rmtree(git_directory)
    new_app_repo = Repo.init(new_app_directory)
    new_app_repo.git.add("--all")
    new_app_repo.index.commit("inital commit")


if __name__ == "__main__":
    app()
