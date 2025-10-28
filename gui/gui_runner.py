from datetime import datetime
from customtkinter import *
from threading import Thread
from third_party import CTkDatePicker
from parser import DATE_FORMAT, run_pipeline


class PinGui:
    """
    Graphical interface for manual control of the PIN parsing pipeline.

    This class provides a CustomTkinter-based GUI that allows users to:
    - Select a start and end date using CTkDatePicker widgets
    - Trigger the invoice download and parsing pipeline for the selected range

    Features:
    - Threaded execution to prevent GUI freezing during long-running tasks
    - Automatic window hiding and restoration during pipeline execution

    Usage:
        gui = PinGui()
        gui.run()

    Notes:
        - Requires `customtkinter` and a third-party `CTkDatePicker` widget
        - Designed to be launched via `run.py --gui`
    """
    def __init__(self):
        self.app = CTk()
        self.app.title("PIN Parser")
        set_appearance_mode("System")
        set_default_color_theme("blue")

        self._build_ui()

    def _build_ui(self):
        """
        Constructs and places all GUI widgets in the main application window.

        This includes:
        - Two CTkDatePicker widgets for selecting start and end dates
        - Labels for each date picker
        - A confirmation button to trigger the pipeline

        Grid layout is used with padding and column alignment.
        """
        # Start Date
        CTkLabel(self.app, text="Start Date").grid(row=0, column=0, padx=20, pady=10)
        self.start_date = CTkDatePicker(self.app)
        self.start_date.grid(row=1, column=0, padx=20, pady=10)

        # End Date
        CTkLabel(self.app, text="End Date").grid(row=0, column=1, padx=20, pady=10)
        self.end_date = CTkDatePicker(self.app)
        self.end_date.grid(row=1, column=1, padx=20, pady=10)

        # Confirm Button
        button = CTkButton(self.app, text="Confirm", command=self.on_confirm)
        button.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    def on_confirm(self) -> None:
        """
        Callback for the Confirm button. Converts dates and runs pipeline in a separate thread.
        """
        start = datetime.strptime(self.start_date.get_date(), "%m/%d/%Y").strftime(DATE_FORMAT)
        end = datetime.strptime(self.end_date.get_date(), "%m/%d/%Y").strftime(DATE_FORMAT)
        # start_date_convert = datetime.strptime(start_date.get_date(), "%m/%d/%Y").strftime("%Y-%m-%d")
        # end_date_convert = datetime.strptime(end_date.get_date(), "%m/%d/%Y").strftime("%Y-%m-%d")


        self.app.withdraw()
        Thread(target=lambda: [run_pipeline(start, end), self.app.deiconify()]).start()


    def run(self):
        """Run gui on Custom Tkinter"""
        self.app.mainloop()


