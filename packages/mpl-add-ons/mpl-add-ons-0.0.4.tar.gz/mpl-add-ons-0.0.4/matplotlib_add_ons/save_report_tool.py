from matplotlib.backend_tools import ToolBase
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib_add_ons.choose_report_windows import ChooseReportWindows
import matplotlib
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
matplotlib.rcParams["toolbar"] = "toolmanager"


class SaveReport(ToolBase):
    """
    A custom Matplotlib tool for saving multiple figures to a PDF report.

    Attributes:
        image (str): Icon for the tool (set to "None").
        description (str): Description shown in the toolbar.
        figures (list): List of Matplotlib figures to be saved.

    Methods:
        trigger(sender, event, data=None): Opens the ChooseReportWindows dialog.
        save_figures(file_path, selected_figures): Saves the selected figures to a PDF.
    """
    image = "None"
    description = "Click to save each window to a separate page in a PDF.\nOpens a Dialog to Choose Save Location."

    def __init__(self, toolmanager, name, figures: list):
        super().__init__(toolmanager, name)
        self.figures = figures

    def trigger(self, sender, event, data=None):
        """
        Trigger function to open the ChooseReportWindows dialog.
        """
        ChooseReportWindows(self.figures)

    def save_figures(self, file_path, selected_figures):
        """
        Saves the selected figures to the given file path as a PDF.

        Args:
            file_path (str): Destination path for the PDF.
            selected_figures (list): List of selected figures (by index) to be saved.
        """
        # Create a PDF file and save the figures in it
        if file_path and len(selected_figures) != 0:
            with PdfPages(file_path) as pdf:
                for i, figure in enumerate(self.figures):
                    if i + 1 in selected_figures:
                        pdf.savefig(figure)
            print(f"Report Saved to location: {file_path}")
        else:
            print("Canceled Save of Report.")


def save_report_tool(figures: list, tool_name="SaveReport"):
    """
    Registers and adds the SaveReport tool to the given figure's toolbar.

    Args:
        figures (list): List of figures to be managed by the tool.
        tool_name (str): Optional name for the tool (default is "SaveReport").
    """
    for figure in figures:
        tm = figure.canvas.manager.toolmanager
        tm.add_tool(tool_name, SaveReport, figures)
        figure.canvas.manager.toolbar.add_tool(tm.get_tool(tool_name), "toolgroup")


if __name__ == '__main__':
    pass
