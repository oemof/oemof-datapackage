import tempfile
import json
from pathlib import Path

import oemof.datapackage.datapackage as datapackage

TEST_FILES = Path(__file__).parent / "_files"


def test_conversion_dp_to_json():
    """`
    Test that a datapackage can be converted to json format and back to a datapackage without alteration
    """

    dp_path = TEST_FILES / "multi_column_results_datapackage"

    json_export = datapackage.export_dp_to_json(dp_path)
    dict_export = json.loads(json_export)

    with tempfile.TemporaryDirectory() as temp_dp:
        df_from_json_path = datapackage.rebuild_dp_from_json(
            dict_export, Path(temp_dp)
        )

        json_export2 = datapackage.export_dp_to_json(df_from_json_path)

    dict_export2 = json.loads(json_export2)

    # check the right keys are within the dictionaries
    for k in ["data", "metadata"]:
        assert k in dict_export.keys()
        assert k in dict_export2.keys()

    # check the resources are the same in both dictionaries
    assert set(dict_export["data"].keys()) == set(dict_export2["data"].keys())

    # compare the json
    formatted1 = json.dumps(json.loads(json_export), sort_keys=True)
    formatted2 = json.dumps(json.loads(json_export2), sort_keys=True)
    assert formatted1 == formatted2


test_conversion_dp_to_json()
