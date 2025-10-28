"""
Google Sheets integration.

Provides GoogleSheetWriter class to:
- Append rows with totals
- Update specific cells
- Handle authentication via service account

Used as final output step in the pipeline.
"""

import gspread
from parser.config import logger, GOOGLE_TOKEN
from oauth2client.service_account import ServiceAccountCredentials


class SheetService:
    def __init__(self, sheet_name: str) -> None:
        self.client = self.__authorize()
        self.sheet = self.client.open(sheet_name)

    def __authorize(self) -> gspread.Client:
        """
        Authorizes and returns a gspread client using service account credentials.

        Returns:
            gspread.Client: Authorized client for interacting with Google Sheets.
        """
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_TOKEN, scope)
        client = gspread.authorize(creds)
        logger.debug("Authorize to Google Service complete")

        return client

    def get_worksheet(self, worksheet_name: str) -> gspread.Worksheet:
        """
        Returns a specific worksheet by name.

        Args:
            name (str): The name of the worksheet tab.

        Returns:
            gspread.Worksheet: The worksheet object.
        """
        return self.sheet.worksheet(worksheet_name)

    def append_rows(self, worksheet_name: str, rows: list[float, float, float]) -> None:
        """
        Updates specific cells in the worksheet with provided values.

        Args:
            worksheet_name (str): Name of the worksheet to update.
            rows (list[float]): List of three floats: [EUROPE, NON-EUROPE, GERMAN]
        """
        if len(rows) != 3:
            raise ValueError("Expected exatly 3 value")
        ws = self.get_worksheet(worksheet_name)
        ws.update("G21", [[rows[0]]])
        ws.update("F21", [[rows[1]]])
        ws.update("D21", [[rows[2]]])
