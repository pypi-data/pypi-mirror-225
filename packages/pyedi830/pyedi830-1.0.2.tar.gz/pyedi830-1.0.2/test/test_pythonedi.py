"""
Test cases for pyedi830 module
"""

import string
import random
import unittest
from datetime import datetime

import pyedi830

class TestConvertEdiToCsv(unittest.TestCase):

    def setUp(self):
        self.parser_df = pyedi830.EDIParserDF()

    def test_csv(self):
        edi_file_path = "test/test_edi_830_forecast.edi"
        csv_file_path = "test/test_edi_830_forecast.csv"
        self.parser_df.to_csv(edi_file_path, csv_file_path)
