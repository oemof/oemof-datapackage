import json
import tempfile
from pathlib import Path

import oemof.solph

import oemof.datapackage
import oemof.datapackage.datapackage as datapackage

TEST_FILES = Path(__file__).parent / "_files"


def test_version_specification():
    """`
    oemof.datapackage`'s version specification is importable and a string.
    """
    assert isinstance(oemof.datapackage.__version__, str)
    assert isinstance(oemof.solph.__version__, str)


def test_project_name():
    """`oemof.datapackage`'s project name is importable and correct."""
    assert oemof.datapackage.__project__ == "oemof.datapackage"


def test_conversion_dp_to_json_and_back_to_dp():
    """`
    Test that a datapackage can be converted to json format and back to a
    datapackage without alteration
    """

    dp_path = TEST_FILES / "example_datapackage"

    json_export = datapackage.export_dp_to_json(dp_path)
    dict_export = json.loads(json_export)

    with tempfile.TemporaryDirectory() as temp_dp:
        dp_from_json_path = datapackage.rebuild_dp_from_json(
            dict_export, Path(temp_dp), overwrite=True
        )

        json_export2 = datapackage.export_dp_to_json(dp_from_json_path)

    dict_export2 = json.loads(json_export2)

    # check the right keys are within the dictionaries
    for k in ["data", "metadata"]:
        assert k in dict_export.keys()
        assert k in dict_export2.keys()

    # check the resources are the same in both dictionaries
    assert set(dict_export["data"].keys()) == set(dict_export2["data"].keys())

    # compare the json' data
    data_formatted1 = json.dumps(
        json.loads(json_export)["data"], sort_keys=True
    )
    data_formatted2 = json.dumps(
        json.loads(json_export2)["data"], sort_keys=True
    )
    assert (
        data_formatted1 == data_formatted2
    ), "The data of source file and the round converted file do not match"

    # compare the json' metadata
    metadata_formatted1 = json.dumps(
        json.loads(json_export)["metadata"], sort_keys=True
    )
    metadata_formatted2 = json.dumps(
        json.loads(json_export2)["metadata"], sort_keys=True
    )
    assert (
        metadata_formatted1 == metadata_formatted2
    ), "The metadata of source file and the round converted file do not match"
