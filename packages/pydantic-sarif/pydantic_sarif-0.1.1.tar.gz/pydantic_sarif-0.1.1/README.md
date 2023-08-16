# PySarif 

This is a simple pydantic model for the SARIF format, generated with datamodel-codegen.

## Installation

```bash
pip install pysarif
```

### Usage
`StaticAnalysisResultsFormatSarifVersion210JsonSchema` is likely the class that you'll be referencing the most.

## Example

```python
from pydantic_sarif.model import StaticAnalysisResultsFormatSarifVersion210JsonSchema as Report

example_json = """
"""
report: Report = Report.parse_raw(example_json)

assert report.version == "2.1.0"
```