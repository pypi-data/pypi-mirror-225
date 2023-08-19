import logging
from penvy.env.EnvConfig import EnvConfig
from penvy.PenvyConfig import PenvyConfig
from benvy.databricks.repos.project_root_resolver import resolve_project_root


class BootstrapConfig(EnvConfig):
    def get_parameters(self) -> dict:
        poetry_version = PenvyConfig().get_parameters()["poetry"]["install_version"]

        return {
            "project": {
                "dir": resolve_project_root(),
            },
            "poetry": {
                "version": poetry_version,
                "home": "/root/.poetry",
                "executable": "/root/.poetry/bin/poetry",
                "archive_url": f"https://github.com/python-poetry/poetry/releases/download/{poetry_version}/{self.__get_archive_filename(poetry_version)}",
                "install_script_url": f"https://raw.githubusercontent.com/python-poetry/poetry/{poetry_version}/get-poetry.py",
                "archive_path": f"/dbfs/FileStore/jars/daipe/poetry/{self.__get_archive_filename(poetry_version)}",
                "install_script_path": "/dbfs/FileStore/jars/daipe/poetry/get-poetry.py",
            },
            "logger": {
                "name": "daipe-bootstrap",
                "level": logging.INFO,
            },
        }

    def __get_archive_filename(self, version: str) -> str:
        return f"poetry-{version}-linux.tar.gz" if version < "1.2.0" else f"poetry-{version}.tar.gz"
