""" Parsing test cases for PythonEDI """

import unittest
import pprint
import pyedi830

class TestParse830(unittest.TestCase):
    """ Tests the Parser module """
    def setUp(self):
        self.parser = pyedi830.EDIParser(
        edi_format="830_Forecast",
        element_delimiter="*",
        segment_delimiter="~\n",
        use_parent_key_detail=True,
        use_parent_detail=True,
        parent_headers=['symbol', 'name', 'type', 'notes'],
        use_child_key_detail=True,
        use_child_detail=False,
        use_debug=True
    )

    def test_parse(self):
        edi_file_path = "test/test_edi_830_forecast.edi"
        json_file_path = "test/test_edi_830_forecast.json"
        
        # Parse the EDI file to JSON data
        edi_data = self.parser.parse_from_file(edi_file_path)
        print("\n\n{}".format(edi_data))
        print("\n\n")
        pprint.pprint(edi_data)
        
        # Write to JSON file
        self.parser.to_json(edi_file_path, json_file_path)

