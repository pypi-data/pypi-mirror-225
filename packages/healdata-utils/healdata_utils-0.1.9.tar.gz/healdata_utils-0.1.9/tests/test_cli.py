import shutil
from pathlib import Path
from healdata_utils.cli import convert_to_vlmd
import json

def test_convert_to_vlmd_with_registered_formats(
    valid_input_params,valid_output_json,valid_output_csv,fields_propname):
    inputtypes = list(valid_input_params.keys())
    outputdir="tmp"

    for inputtype in inputtypes:
   
        # make an empty temporary output directory
        try:
            Path(outputdir).mkdir()
        except FileExistsError:
            shutil.rmtree(outputdir)
            Path(outputdir).mkdir()

        _valid_input_params = valid_input_params[inputtype]
        _valid_output_json = valid_output_json[inputtype]
        _valid_output_csv = valid_output_csv[inputtype]

        data_dictionaries = convert_to_vlmd(
            **_valid_input_params,
        outputdir=outputdir
        )

        ddjson = json.loads(list(Path("tmp").glob("*.json"))[0].read_text())
        #NOTE: csv are just fields so no ddcsv

        # check for incorrect fields       
        csv_fields = list(Path("tmp").glob("*.csv"))[0].read_text().split("\n")
        json_fields = ddjson.pop(fields_propname) #NOTE: testing individual fields

        valid_output_json_fields = _valid_output_json.pop(fields_propname)
        valid_output_csv_fields = _valid_output_csv

        invalid_json_fields = []
        invalid_csv_fields = []
        indices = range(len(json_fields))
        for i in indices:
            if json_fields[i]!=valid_output_json_fields[i]:
                invalid_json_fields.append(i)
            if csv_fields[i]!=valid_output_csv_fields[i]:
                invalid_csv_fields.append(i)
        
        json_field_names = [f["name"] for f in json_fields]
        csv_field_names = [f["name"] for f in json_fields]

        assert sorted(json_field_names)==sorted(csv_field_names),f"{inputtype} conversion: json fields must have the same field names as csv fields"
        assert len(invalid_json_fields)==0,f"{inputtype} conversion: The following **json** dd fields are not valid: {str(invalid_json_fields)}"
        assert len(invalid_csv_fields)==0,f"{inputtype} conversion: The following **csv** dd fields are not valid: {str(invalid_csv_fields)}"
        
        
         # check if root level properties other than the fields are valid
        for propname in ddjson:
            assert ddjson[propname] == _valid_output_json[propname],f"{inputtype} conversion to json dd property '{propname}' assertion failed"

    
        # clean up
        shutil.rmtree(outputdir)
