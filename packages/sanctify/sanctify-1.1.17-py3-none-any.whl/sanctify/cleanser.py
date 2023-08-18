import pandas as pd
from frozendict import frozendict

# Internal Imports
from sanctify.constants import Constants, DefaultColumns
from sanctify.utils import replace_dict_keys


class Cleanser:
    """
    The Cleanser class is responsible for validating and checking if a column is present and should be used.
    """

    def __init__(self, df: pd.DataFrame, column_mapping_schema: frozendict) -> None:
        """
        Initializes the Cleanser object.

        Args:
            df (pd.DataFrame): The input DataFrame to be cleansed.
            column_mapping_schema (frozendict): The mapping schema for column names.
        """
        self.df = df
        self.mandatory_column_headers = []
        self.column_mapping_schema = column_mapping_schema
        self.input_vs_standard_column_mapping = self.extract_input_vs_standard_column_mapping()

    def check_if_all_columns_mapping_exist_in_df(self) -> None | ValueError:
        """
        Checks if all columns specified in the column mapping schema exist in the DataFrame.

        Returns:
            None: If all columns are present.

        Raises:
            ValueError: If any mandatory column is missing.
        """
        self.mandatory_column_headers = self.input_vs_standard_column_mapping.keys()

        missing_columns = set(self.mandatory_column_headers) - set(self.df.columns.to_list())
        if len(missing_columns) == 0:
            return None
        else:
            raise ValueError(f"Missing mandatory columns: ({', '.join(missing_columns)})")

    def extract_input_vs_standard_column_mapping(self) -> frozendict:
        """
        Extracts the input vs standard column mapping from the column mapping schema.

        Returns:
            frozendict: The input vs standard column mapping.
        """
        input_vs_standard_column_mapping = {}
        for input_column_name, column_config in self.column_mapping_schema.items():
            input_vs_standard_column_mapping[input_column_name] = column_config.get(
                Constants.STANDARD_COLUMN.value, input_column_name
            )
        return frozendict(input_vs_standard_column_mapping)

    def remove_trailing_spaces_from_column_headers(self) -> pd.DataFrame:
        """
        Removes trailing spaces from column headers in the DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with trailing spaces removed from column headers.
        """
        self.df.columns = self.df.columns.str.strip()
        return self.df

    def drop_unmapped_columns(self) -> pd.DataFrame:
        """
        Drops columns from the DataFrame that are not present in the mandatory column headers.

        Returns:
            pd.DataFrame: The DataFrame with unmapped columns dropped.
        """
        self.mandatory_column_headers = self.input_vs_standard_column_mapping.keys()
        columns_to_keep = self.mandatory_column_headers
        self.df = self.df[columns_to_keep]
        return self.df

    def drop_fully_empty_rows(self, inplace: bool = True) -> pd.DataFrame:
        """
        Drops rows from the DataFrame that are fully empty.

        Args:
            inplace (bool): Whether to drop rows in-place or return a new DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with fully empty rows dropped.
        """
        if inplace is True:
            self.df.dropna(how="all", inplace=inplace)
        else:
            self.df = self.df.dropna(how="all", inplace=inplace)

        return self.df

    def drop_rows_with_errors(self, inplace: bool = True) -> pd.DataFrame:
        """
        Drops all rows where the 'Error' column is not an empty string.

        Args:
            inplace (bool): If True, modify the DataFrame in-place. If False, return a new DataFrame.

        Returns:
            pd.DataFrame: The cleaned DataFrame with rows dropped where the 'Error' column is not an empty string.
        """
        if DefaultColumns.ERROR.value not in self.df.columns:
            self.df[DefaultColumns.ERROR.value] = ""

        mask = self.df[DefaultColumns.ERROR.value].fillna("") != ""

        if inplace:
            self.df.drop(self.df[mask].index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
        else:
            df = self.df[~mask].copy()
            df.reset_index(drop=True, inplace=True)
            return df

        return self.df

    def remove_trailing_spaces_from_each_cell_value(self) -> pd.DataFrame:
        """
        Removes trailing spaces from each cell value in the DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with trailing spaces removed from each cell value.
        """
        self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return self.df

    def replace_column_headers(self, inplace: bool = True) -> tuple[pd.DataFrame, frozendict]:
        """
        Replaces column headers in the DataFrame based on the input vs standard column mapping.

        Args:
            inplace (bool): Whether to replace column headers in-place or return a new DataFrame.

        Returns:
            tuple[pd.DataFrame, frozendict]: The DataFrame with updated column headers
                and the updated column mapping schema.
        """
        if inplace is True:
            self.df.rename(columns=self.input_vs_standard_column_mapping, inplace=inplace)
        else:
            self.df = self.df.rename(columns=self.input_vs_standard_column_mapping, inplace=inplace)

        self.df.rename(columns=self.input_vs_standard_column_mapping, inplace=True)
        self.mandatory_column_headers = self.input_vs_standard_column_mapping.values()
        updated_column_mapping_schema = frozendict(
            replace_dict_keys(
                original_dict=self.column_mapping_schema,
                key_mapping=self.input_vs_standard_column_mapping,
            )
        )
        return self.df, updated_column_mapping_schema

    def mark_all_duplicates(self, columns: list[str], drop_duplicates: bool = False) -> pd.DataFrame:
        """
        Marks all duplicates based on the specified columns and populates the 'Error' column.

        Args:
            columns (list[str]): The list of column names to check for duplicates.
            drop_duplicates (bool): Whether to drop the duplicate rows or keep them.

        Returns:
            pd.DataFrame: The DataFrame with duplicates marked and the 'Error' column populated.
        """
        if DefaultColumns.ERROR.value not in self.df.columns:
            self.df[DefaultColumns.ERROR.value] = ""

        if drop_duplicates is True:
            result = self.df.drop_duplicates(subset=columns, keep="first", inplace=False, ignore_index=True)
        else:
            duplicate_rows = self.df.duplicated(subset=columns, keep="first")

            error_message = f"Duplicate entry for {', '.join(columns)} passed"
            self.df.loc[duplicate_rows, DefaultColumns.ERROR.value] += " | " + error_message
            result = self.df

        return result

    def drop_fully_duplicate_rows(self, inplace: bool = True) -> pd.DataFrame:
        """
        Drops rows from the DataFrame that are fully duplicates.

        Args:
            inplace (bool): Whether to drop rows in-place or return a new DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with fully duplicate rows dropped.
        """
        if inplace is True:
            self.df.drop_duplicates(inplace=inplace, ignore_index=True)
        else:
            self.df = self.df.drop_duplicates(inplace=inplace, ignore_index=True)

        return self.df
