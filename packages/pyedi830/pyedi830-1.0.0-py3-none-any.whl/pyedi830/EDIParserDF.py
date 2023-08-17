"""
Parses a provided EDI message and tries to build a dictionary from the data
Provides hints if data is missing, incomplete, or incorrect.
"""

import datetime
import json
import pandas as pd

from .supported_formats import supported_formats
from .debug import Debug
from .EDIParser import EDIParser

class EDIParserDF(object):
    def __init__(
        self, edi_format="830_Forecast", element_delimiter="*", segment_delimiter="~\n", data_delimiter="`",
        use_debug=False,
    ):
        self.parser = EDIParser(
            edi_format="830_Forecast",
            element_delimiter="*",
            segment_delimiter="~\n",
            use_parent_key_detail=True,
            use_parent_detail=True,
            parent_headers=['symbol', 'name', 'type', 'notes'],
            use_child_key_detail=True,
            use_child_detail=False,
            use_debug=False
        )
        self.use_debug = use_debug

    def to_csv(self, edi_file_path, csv_file_path):
        df = self.create_df_from_file(edi_file_path)
        df.to_csv(csv_file_path)

    def create_df_from_file(self, edi_file_path):
        data = self.parser.parse_from_file(edi_file_path)
        parent_df = self.create_parent_df(data)
        loop_df = self.create_loop_df(data)
        merged_df = pd.concat([parent_df, loop_df], axis=1)
        
        if self.use_debug:
            Debug.log_debug(f"parent df: \n{parent_df}")
            Debug.log_debug(f"loop df: \n{loop_df}")
            Debug.log_debug(f"merged df: \n{merged_df}")

        return merged_df

    def create_parent_df(self, data):
        df = pd.DataFrame()
        for parent_key, parent in data.items():
            parent_type = parent['type']
            parent_symbol = parent['symbol']

            if parent_type == 'loop':
                continue

            if self.use_debug:
                Debug.log_debug(f"\nParsing: {parent_symbol}")

            values = parent[EDIParser.VALUE_NAME]
            for name, value in values.items():
                col_name = f"{parent_symbol}_{name}"
                if self.use_debug:
                    Debug.log_debug(f"{col_name}: {value}")
                df[col_name] = [value]

            # Create Names dataframe
            n1_df = self.create_n1_df(data["Names"])
            df = pd.concat([df, n1_df], axis=1)
        return df

    def create_n1_df(self, n1_segment):
        df = pd.DataFrame()
        segments = n1_segment[EDIParser.VALUE_NAME]
        for segment in segments:
            for segment_key, segment_data in segment.items():
                n1_values = segment_data[EDIParser.VALUE_NAME]
                prefix_key = f"{segment_data['symbol']}_{n1_values['Entity_ID_Code']}"
                for n1_value_name, n1_vavlue in n1_values.items():
                    col_name = f'{prefix_key}_{n1_value_name}'
                    df[col_name] = [n1_vavlue]
        return df

    def create_loop_df(self, data):
        df = pd.DataFrame()
        # segment_value = data[EDIParser.VALUE_NAME]
        for s_key, segment in data.items():
            s_type = segment['type']
            s_symbol = segment['symbol']

            if s_type != 'loop':
                continue
            # e_value = segment[EDIParser.VALUE_NAME]
            if s_symbol == "L_N1":
                continue

            if self.use_debug:
                Debug.log_debug(f"\nParsing: {s_symbol}")
            
            loop_df = self.parse_loop_df(segment)
            df = pd.concat([df, loop_df], axis=1)
        return df

    def parse_loop_df(self, loop_segment):
        df = pd.DataFrame()
        loop_key = loop_segment["symbol"]
        loop_value = loop_segment["value"]
        # Array data
        for list_item in loop_value:
            # Dict data
            v_df = pd.DataFrame(index=[0])
            for s_key, segment in list_item.items():
                s_symbol = segment["symbol"]
                s_type = segment["type"]
                
                if s_type == "segment":
                    prefix_col_name = f"{s_symbol}_{s_key}"
                    s_values = segment["value"]
                    for v_key, v_value in s_values.items():
                        col_name = f"{prefix_col_name}_{v_key}"
                        v_df[col_name] = [v_value]
                if s_type == "loop":
                    nested_df = self.parse_loop_df(segment)
                    # v_df = pd.concat([v_df, nested_df], axis=1)
                    num_rows = len(nested_df)
                    v_df = v_df.loc[v_df.index.repeat(num_rows)].reset_index(drop=True)
                    v_df = pd.concat([v_df, nested_df.reset_index(drop=True)], axis=1)

            if df.empty:
                df = v_df
            else:
                df = pd.concat([df, v_df], axis=0, ignore_index=True)
        return df

    