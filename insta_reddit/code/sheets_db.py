# https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
# NOTE: Google Sheets cells are 1-base indexed
import warnings
import gspread


class SheetsDb:
    def __init__(self, sheet_id, credentials_path=None):
        """
        Initialize gspread handler with credentials
        :param sheet_id: The long-ass alphanumeric code in the URL of the Google Sheet
        :param credentials_path: If None, will look at ~/.config/gspread/service_account.json
        """
        self.gc = gspread.service_account(filename=credentials_path)
        self.sheet_id = sheet_id
        self.sheet = self.gc.open_by_key(sheet_id).sheet1

    def get_row_for_id(self, post_id: str) -> int:
        """
        Finds the row given the ID, returns -1 if not found
        :param str post_id: Reddit post ID
        :return int: The index of the row the ID is on
        """
        id_col = self.get_index_for_column("id")
        id_list = self.sheet.col_values(id_col)
        try:
            return id_list.index(post_id) + 1
        except ValueError as _:
            return -1

    def get_index_for_column(self, colname: str) -> int:
        """
        Returns the column index for the column name
        :param str colname: Name of the column, e.g. image_uploaded
        :return int: The index of the column the colname is on
        """
        colnames = self.sheet.row_values(1)
        return colnames.index(colname) + 1

    def update_image_uploaded(self, post_id: str):
        """
        Update the Google sheet to reflect that an image has been already uploaded
        :param str post_id: The "id" of the Reddit post to be uploaded
        :return: None
        """
        col_idx = self.get_index_for_column("image_uploaded")
        row_idx = self.get_row_for_id(post_id)
        if self.sheet.cell(row_idx, col_idx).value == "TRUE":
            warnings.warn("Cell at {}, {} already updated to True.".format(row_idx, col_idx))
        else:
            self.sheet.update_cell(row_idx, col_idx, "TRUE")

    def append_row(self, row: list, col_idx: int = 1):
        """
        Append a list after the last cell of the given column
        :param list row:    Row to append
        :param int col_idx: Which column to use to decide the last cell beyond which to append
        :return: None
        """
        last_row_idx = len(self.sheet.col_values(col_idx))
        for idx, elem in enumerate(row):
            self.sheet.update_cell(last_row_idx + 1, idx + 1, elem)
        print("Row {} appended.".format(last_row_idx + 1))

    def get_unuploaded_rows(self):
        """
        Get all the records that are yet to be uploaded
        :rtype: list(dict)
        """
        all_rows = self.sheet.get_all_records()
        return [row for row in all_rows if row['image_uploaded'] != "TRUE"]
