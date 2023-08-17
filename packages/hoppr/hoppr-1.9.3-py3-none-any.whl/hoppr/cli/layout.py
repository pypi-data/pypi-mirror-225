"""
Hoppr stage output Rich layout
"""
from __future__ import annotations

from typing import MutableMapping

from rich.console import Console, RenderableType
from rich.containers import Lines
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskID, TextColumn
from rich.text import Text

from hoppr import __version__

# Renderable constants
BORDER_LINES = 2
HEADER_SIZE = 3

# Padding constants
PAD_BOTTOM = 0
PAD_LEFT = 1
PAD_RIGHT = 1
PAD_TOP = 0

# Panel size ratio constants
JOBS_PANEL_RATIO_SIZE = 1
OUTPUT_PANEL_RATIO_SIZE = 2
TOTAL_PANEL_RATIO_SIZE = JOBS_PANEL_RATIO_SIZE + OUTPUT_PANEL_RATIO_SIZE
OUTPUT_PANEL_RATIO = OUTPUT_PANEL_RATIO_SIZE / TOTAL_PANEL_RATIO_SIZE

console = Console()


class HopprBasePanel(Panel):  # pylint: disable=too-few-public-methods
    """
    Customized base Rich Panel
    """

    def __init__(self, renderable: RenderableType, title: str | None = None, **kwargs) -> None:
        super().__init__(
            renderable=renderable,
            padding=(PAD_TOP, PAD_RIGHT, PAD_BOTTOM, PAD_LEFT),
            title=f"[bold blue]{title}" if title else None,
            title_align="left",
            border_style="bold purple",
            style="white on grey0",
            **kwargs,
        )


class HopprJobsPanel(HopprBasePanel):
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress(
        "{task.description}",
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )

    def __init__(self) -> None:
        super().__init__(renderable=self.progress_bar, title="Jobs")

    def add_task(self, description: str, total: int = 1, **fields) -> TaskID:
        """
        Add a task to be tracked in the `jobs` side panel

        Args:
            description (str): A description of the task

        Returns:
            int: ID of the added task
        """
        return self.progress_bar.add_task(description, total=total, start=False, **fields)


class HopprOutputPanel(HopprBasePanel):
    """
    Customized Rich Text box to simulate a console
    """

    lines = Lines()

    def __init__(self) -> None:
        super().__init__(renderable=self.lines)

    def get_height(self) -> int:
        """
        Return the height of the writeable area of the output panel

        Returns:
            int: Height of the output panel
        """
        self.height = self.height or console.height - HEADER_SIZE
        return self.height - BORDER_LINES

    def get_width(self) -> int:
        """
        Return the width of the writeable area of the output panel

        Returns:
            int: Width of the output panel
        """
        self.width = self.width or int(console.width * OUTPUT_PANEL_RATIO)
        return self.width - BORDER_LINES - PAD_LEFT - PAD_RIGHT

    def print(self, msg: str, source: str | None = None, style: str = "") -> None:
        """
        Write a message to the console output panel

        Args:
            line (str): Message to write
            style (str): Style to apply to message string
        """
        msg = msg if source is None else f"[bold cyan]{source}[/] {msg}"
        new_lines = Text.from_markup(text=msg, style=style)
        self.lines.extend(new_lines.wrap(console, self.get_width()))

        # Remove messages from top of output panel until most recent messages are visible
        output_height = self.get_height()

        while len(self.lines) > output_height:
            self.lines.pop(index=0)


class HopprProgressPanel(HopprBasePanel):  # pylint: disable=too-few-public-methods
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress()

    def __init__(self) -> None:
        super().__init__(renderable=self.progress_bar, title="Progress")
        self.progress_bar.add_task(description="All Jobs")
        self.progress_task = self.progress_bar.tasks[0]


class HopprLayout(Layout):
    """
    Layout of the Hoppr console application
    """

    name: str = "root"
    job_id_map: MutableMapping[str, TaskID] = {}
    jobs_panel = HopprJobsPanel()
    output_panel = HopprOutputPanel()
    overall_progress = HopprProgressPanel()

    def __init__(self, title: str = f"Hoppr v{__version__}") -> None:
        super().__init__()

        self.split(Layout(name="header", size=HEADER_SIZE), Layout(name="main"))
        self["main"].split_row(Layout(name="side"), Layout(name="console", ratio=OUTPUT_PANEL_RATIO_SIZE))
        self["side"].split(Layout(name="jobs"), Layout(name="progress", size=3))

        # Initialize header
        header = Text(text=title, style="bold blue", justify="center")
        self["header"].update(renderable=HopprBasePanel(renderable=header))

        # Initialize jobs side bar panel
        self["jobs"].update(renderable=self.jobs_panel)

        # Initialize overall progress side bar
        self["progress"].update(renderable=self.overall_progress)
        self.progress_task = self.overall_progress.progress_bar.tasks[0]
        self.progress_task.total = 0

        # Initialize main body panel
        self["console"].update(renderable=self.output_panel)

        # Set size attributes for output console renderable
        render_map = self.render(console, console.options)
        self.output_panel.height = render_map[self["console"]].region.height
        self.output_panel.width = render_map[self["console"]].region.width

    def add_job(self, description: str, total: int = 1, **fields) -> TaskID:
        """
        Add a job to the `jobs` side panel

        Args:
            description (str): Description of the job to add
        """
        self.progress_task.total = self.progress_task.total or 0

        self.progress_task.total += total
        self.job_id_map[description] = self.jobs_panel.add_task(description, total=total, **fields)

        return self.job_id_map[description]

    def advance_job(self, name: str):
        """
        Advance progress of a job in the jobs panel and overall progress

        Args:
            name (str): Name of the job to advance
        """
        task_id = self.job_id_map[name]
        self.jobs_panel.progress_bar.advance(task_id)
        self.overall_progress.progress_bar.advance(self.overall_progress.progress_task.id)

    def is_job_finished(self, name: str) -> bool:
        """
        Check if a job is finished

        Args:
            name (str): Name of the job
        """
        task_id = self.job_id_map[name]

        return self.jobs_panel.progress_bar.tasks[task_id].finished

    def print(self, msg: str, source: str | None = None, style: str = "") -> None:
        """
        Write a message to the console output panel

        Args:
            line (str): Message to write
        """
        self.output_panel.print(msg, source, style=style)

    def start_job(self, name: str):
        """
        Start a job in the jobs panel

        Args:
            name (str): Name of the job to start
        """
        task_id = self.job_id_map[name]
        self.jobs_panel.progress_bar.start_task(task_id)

    def stop_job(self, name: str):
        """
        Stop a job in the jobs panel

        Args:
            name (str): Name of the job to stop
        """
        task_id = self.job_id_map[name]
        self.jobs_panel.progress_bar.stop_task(task_id)

    def update_job(self, name: str, **fields):
        """
        Update a job in the jobs panel

        Args:
            name (str): Name of the job to update
        """
        task_id = self.job_id_map[name]
        self.jobs_panel.progress_bar.update(task_id, **fields)
