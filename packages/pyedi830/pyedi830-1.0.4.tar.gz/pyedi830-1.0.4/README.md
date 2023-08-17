# pyedi830
EDI830 parser in Python. Parse EDI830 files and convert to JSON &amp; CSV file according to specific formats

## TODOs

* Finish 830 definition
* Implement colorful exceptions

## EDI Format Definitions
EDI830 parser messages consist of a set of Segments (usually lines) comprised of Elements. Some segments can be part of a Loop. These formats are defined in JSON. See the provided format(s) for examples.

A loop has certain expected properties:

* `id` (Loop ID)
* `repeat` (Max times the loop can repeat)

Each segment has certain expected properties:

* `id` (Segment ID)
* `name` (Human-readable segment name)
* `req` (Whether segment is required: [M]andatory, [O]ptional)
* `max_uses` (Some segments can be included more than once)
* `notes` (Optional details for hinting documentation)
* `syntax` (An optional list of syntax rules, defined below)
* `elements` (List of included elements)

Each element has certain expected features: 

* `id` (Element ID)
* `name` (Human-readable element name)
* `req` (Whether segment is required: [M]andatory, [O]ptional)
* `data_type` (Type of segment data, defined below)
* `data_type_ids` (If `data_type` is `ID`, this is a dict of valid IDs with descriptions)
* `length` (Dict specifying field length)
    * `min` (Min length of field)
    * `max` (Max length of field)

Valid data types include:

* `AN` (Any data type)
* `DT` (Date, must be provided as Python DATE or DATETIME object)
* `ID` (Alphanumeric ID. List of valid IDs provided as dict with descriptions)
* `R`  (Percentage)
* `Nx` (Number with `x` decimal points)
* `TM` (Time, must be provided as Python TIME or DATETIME object)

Syntax rules are specified as a dict with a `rule` and a list of `criteria`. Valid syntax rules include:

* `ATLEASTONE` (where at least one of the element IDs in the `criteria` list is included and is not empty)
* `ALLORNONE` (where either all of the element IDs in the `criteria` list are included, or none are)
* `IFATLEASTONE` (if the first element in `criteria` is included, then at least one of the other elements must be included)

# Code Examples

```python
    from pyedi830 import EDIParser
    from pyedi830 import EDIParserDF

    
    
    edi_file_path = "test/test_edi_830_forecast.edi"

    # Convert to json file
    json_file_path = "test_edi_830_forecast.json"
    edi830_parser = EDIParser(
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
    edi830_parser.to_json(edi_file_path, json_file_path)

    # Parse to json data
    json_data = edi830_parser.parse_from_file(edi_file_path)


    # Convert to csv file.
    csv_file_path = "test_edi_830_forecast.csv"
    edi830_parser_df = EDIParserDF(use_debug=True)
    edi830_parser_df.to_csv(edi_file_path, csv_file_path)
    
    # Parse to dataframe
    df = edi830_parser_df.create_df_from_file(edi_file_path)
```

# Install

Install system-wide

    pip install pyedi830

Or install in a virtual environment

    virtualenv my_env
    pip -E my_env install pyedi830

# Licensing

pyedi830 has a BSD license. The full license text is included with the source code for the package. 
