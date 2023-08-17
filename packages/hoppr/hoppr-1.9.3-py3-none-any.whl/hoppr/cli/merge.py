"""
`merge` subcommand for `hoptctl`
"""
from __future__ import annotations

import time

from pathlib import Path

import typer

from pydantic import ValidationError
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn
from rich.table import Table
from typer import BadParameter, Option, Typer

from hoppr.cli.layout import HopprJobsPanel, HopprLayout, console
from hoppr.models.manifest import Manifest
from hoppr.models.sbom import CycloneDXBaseModel, Sbom

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Merge all properties of two or more SBOM files",
    invoke_without_command=True,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="markdown",
    subcommand_metavar="",
)


class HopprMergeJobsPanel(HopprJobsPanel):
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress(
        "{task.description}",
        SpinnerColumn(),
        "{task.fields[status]}",
        expand=True,
    )


class HopprMergeLayout(HopprLayout):
    """
    Layout of the `hopctl merge` console application
    """

    name: str = "root"
    jobs_panel = HopprMergeJobsPanel()


def manifest_callback(manifest_file: Path | None) -> Path | None:
    """
    Extract and return SBOM refs from manifest files
    """
    if manifest_file is None:
        return None

    # Load manifest file to populate `Sbom.loaded_sboms`
    Manifest.load(manifest_file)

    return manifest_file


def output_file_callback(output_file: Path | None) -> Path:
    """
    Auto-generate an output file name if not provided
    """
    return output_file or Path.cwd() / f"hopctl-merge-{time.strftime('%Y%m%d-%H%M%S')}.json"


def sbom_callback(sbom_sources: list[str | Path]) -> list[str | Path]:
    """
    Load SBOM input files
    """
    # Combine SBOM files from all CLI input file arguments
    _load_sbom_files(sbom_sources)

    return sbom_sources


def sbom_dir_callback(sbom_dirs: list[Path]) -> list[Path]:
    """
    Load SBOM files from input directories
    """
    for sbom_dir in sbom_dirs:
        sbom_files = sbom_dir.glob("*.json")

        _load_sbom_files(list(sbom_files))

    return sbom_dirs


def _load_sbom_files(sbom_files: list[str | Path]) -> None:
    """
    Load SBOM input files
    """
    for sbom_file in sbom_files:
        try:
            Sbom.load(sbom_file)
        except ValidationError as ex:
            raise BadParameter(f"'{sbom_file}' is not a valid SBOM file") from ex


def _merge_sboms() -> Sbom:
    """
    Merge SBOMs into single object
    """
    merged_sbom = Sbom()  # pyright: ignore
    layout = HopprMergeLayout()
    merged_sbom.subscribe(observer=layout, callback=layout.print)

    summary_table = Table("File Name", "# Components", "Elapsed Time", box=None, pad_edge=False, show_edge=False)

    total_components = 0
    for sbom_ref, sbom in Sbom.loaded_sboms.items():
        total_components += len(sbom.components)
        layout.add_job(description=Path(str(sbom_ref)).name, status="[yellow]:pause_button:", sbom=sbom)

    with Live(layout, console=console, refresh_per_second=10):
        for task in layout.jobs_panel.progress_bar.tasks:
            layout.print(f"Merging {task.description}...")
            layout.start_job(task.description)

            merged_sbom.merge(task.fields["sbom"])

            layout.stop_job(task.description)
            layout.advance_job(task.description)
            layout.update_job(task.description, status="[green]:heavy_check_mark:")

            summary_table.add_row(task.description, str(len(task.fields["sbom"].components)), f"{task.elapsed:.3f}")

        layout.print("Writing merged SBOM...")

        layout.overall_progress.progress_bar.stop_task(layout.progress_task.id)

    before_after = Table.grid(padding=(0, 1))
    before_after.add_row()
    before_after.add_row("Total components before merge:", str(total_components))
    before_after.add_row("Total components after merge:", str(len(merged_sbom.components)))

    console.print(
        Panel(
            renderable=Group(summary_table, before_after),
            title="[bold blue]Summary",
            title_align="left",
            border_style="purple",
        )
    )

    merged_sbom.unsubscribe(observer=layout)
    return merged_sbom


@app.callback()
def merge(  # pylint: disable=too-many-arguments, unused-argument
    manifest_file: Path = Option(
        None,
        "-m",
        "--manifest",
        callback=manifest_callback,
        dir_okay=False,
        exists=True,
        help="Manifest file containing SBOMs to merge",
        resolve_path=True,
        show_default=False,
    ),
    sbom_files: list[Path] = Option(
        [],
        "-s",
        "--sbom",
        callback=sbom_callback,
        dir_okay=False,
        exists=True,
        help="SBOM file to merge (can be specified multiple times)",
        resolve_path=True,
        show_default=False,
    ),
    sbom_dirs: list[Path] = Option(
        [],
        "-d",
        "--sbom-dir",
        callback=sbom_dir_callback,
        exists=True,
        file_okay=False,
        help="Directory containing SBOM files to merge (can be specified multiple times)",
        resolve_path=True,
        show_default=False,
    ),
    sbom_urls: list[str] = Option(
        [],
        "-u",
        "--sbom-url",
        callback=sbom_callback,
        help="URL of SBOM to merge (can be specified multiple times)",
        metavar="URL",
        show_default=False,
    ),
    output_file: Path = Option(
        None,
        "-o",
        "--output-file",
        callback=output_file_callback,
        dir_okay=False,
        exists=False,
        help=f"Path to output file {typer.style(text='[default: hopctl-merge-YYMMDD-HHMMSS.json]', dim=True)}",
        resolve_path=True,
        show_default=False,
    ),
    deep_merge: bool = Option(
        False,
        "--deep-merge",
        help="Resolve and expand `externalReferences` in-place",
        show_default=False,
    ),
    flatten: bool = Option(
        False,
        "--flatten",
        help="Flatten nested `components` into single unified list",
        show_default=False,
    ),
):
    """
    Merge SBOM files
    """
    if not any([manifest_file, *sbom_dirs, *sbom_files, *sbom_urls]) or len(Sbom.loaded_sboms) < 2:
        raise BadParameter(
            "A minimum of two SBOM files must be provided via the "
            "--sbom, --sbom-dir, --sbom-url, and --manifest arguments."
        )

    CycloneDXBaseModel.deep_merge = deep_merge
    CycloneDXBaseModel.flatten = flatten

    merged_sbom = _merge_sboms()

    output_file.write_text(
        data=merged_sbom.json(exclude_none=True, exclude_unset=True, by_alias=True, indent=2),
        encoding="utf-8",
    )
