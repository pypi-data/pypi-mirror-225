"""
A module containing the documentation API.

This module contains the bulk of the documentation website generation logic.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from subprocess import run
from json import dumps
from distutils.dir_util import copy_tree
from typing import Callable
from .configuration import Configuration
from .markers import Markers
from .replacement import Replacement
from ..structures import Package, Structure, Subroutine, SourceStructure
from ..tags import Example


@dataclass(frozen=True, slots=True)
class Documentation:
    """
    A dataclass containing all logic regarding the final documentation website.

    This dataclass encompasses all the data used in the final website output, and includes
    functionality to write to the final output folder with a working and adaptable website.
    """
    project: Package
    base_directory: Path
    configuration: Configuration
    filter: Callable[[Structure], bool] = lambda structure: (
        not (isinstance(structure, SourceStructure) and (
                (
                        structure.is_private or structure.is_dunder) or
                (isinstance(structure, Subroutine) and structure.is_lambda)
        ))
    )

    def output(self) -> None:
        """
        Outputs the prepared documentation website files.

        Outputs all the prepared documentation files into the base directory,
        and automatically installs any dependencies so that the website is ready to run.
        """
        self.create_skeleton_template()
        self.install_dependencies()
        self.copy_templates()
        self.dump_project()
        self.configure_project()

    def create_skeleton_template(self) -> None:
        """
        Creates a bare-bones project.

        An internal function to run an NPM command that
        installs a bare-bones SvelteKit template with SkeletonUI.
        """
        run(
            ["pnpm", "create", "skeleton-app@latest", "-q", "-n", self.project.name, "-p", str(self.base_directory)],
            shell=True
        )

    def install_dependencies(self) -> None:
        """
        Installs the required project dependencies.

        An internal function which runs several NPM commands, installing all the necessary requirements
        for the documentation website to function as intended out-of-the-box.
        """
        dependencies = [
            ["highlight.js"],
            ["-D", "@tailwindcss/forms"]
        ]
        for dependency in dependencies:
            run(
                ["pnpm", "install", *dependency],
                shell=True,
                cwd=str(self.base_directory)
            )

    def copy_templates(self) -> None:
        """
        Copies all the locally stored project templates into the bare-bones layout.
        """
        copy_tree(str(Path(f"{__file__}/../../templates/lib")), str(self.base_directory / "src/lib"))
        copy_tree(str(Path(f"{__file__}/../../templates/routes")), str(self.base_directory / "src/routes"))
        copy_tree(str(Path(f"{__file__}/../../templates/static")), str(self.base_directory / "static"))

    def replace_content_in_file(self, path: Path, *replacements: Replacement, json: bool = True) -> None:
        """
        A utility method to replace the content at a specific marker with given content.

        An internal method to place specified content in place of an internal marker,
        used to copy dynamic information such as certain configuration settings into the website files.

        :param path: The path at which the target file exists
        :param replacements: The replacements that should be made to the target file
        :param json: Whether the given content should be converted into a JSON format or not
        """
        with path.open("r+") as f:
            content = f.read()
            for replacement in replacements:
                content = content.replace(
                    replacement.marker,
                    dumps(replacement.content, indent=self.configuration.json_indent) if json else replacement.content
                )
            f.seek(0)
            f.truncate(0)
            f.write(content)

    def dump_project(self) -> None:
        """
        Places the project JSON tree into the website files.
        """
        self.replace_content_in_file(
            self.base_directory / "src/lib/content/project.ts",
            Replacement(
                Markers.PROJECT.value,
                self.project.serialize(child_filter=self.filter).to_json()
            )
        )

    def configure_project(self) -> None:
        """
        Places content into the website files regarding user configuration.
        """
        self.replace_content_in_file(
            self.base_directory / "src/lib/content/configuration.ts",
            Replacement(
                Markers.PROJECT_NAME.value,
                self.configuration.project_name
            )
        )
        self.replace_content_in_file(
            self.base_directory / "src/routes/+layout.svelte",
            Replacement(
                Markers.THEME.value,
                self.configuration.theme.value
            ),
            json=False
        )
        self.replace_content_in_file(
            self.base_directory / "src/app.html",
            Replacement(
                "%sveltekit.head%",
                f"<title>{self.configuration.project_name} Documentation</title>\n\t\t"
                f"<meta name=\"title\" content={self.configuration.project_name}>\n\t\t"
                f"<meta name=\"description\" content=\"Documentation for {self.configuration.project_name}\">\n\t\t"
                "<meta name=\"robots\" content=\"index, follow\">\n\t\t"
                "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n\t\t"
                "<meta name=\"language\" content=\"English\">\n\t\t"
                "%sveltekit.head%"
            ),
            json=False
        )
