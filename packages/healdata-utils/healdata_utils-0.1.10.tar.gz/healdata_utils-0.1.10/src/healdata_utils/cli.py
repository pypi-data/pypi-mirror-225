''' 

command line interface for generating HEAL data dictionary/vlmd json files

''' 

import click 
from healdata_utils.transforms.csvtemplate.conversion import convert_templatecsv
from healdata_utils.transforms.jsontemplate.conversion import convert_templatejson
from healdata_utils.transforms.readstat.conversion import convert_readstat
from healdata_utils.transforms.redcapcsv.conversion import convert_redcapcsv
from healdata_utils.transforms.csvdata.conversion import convert_datacsv
from healdata_utils.transforms.frictionless.conversion import convert_frictionless_tableschema

from healdata_utils.validators.validate import validate_vlmd_json,validate_vlmd_csv
import json
from pathlib import Path
import petl as etl
import csv
from collections import deque

from healdata_utils.utils import find_docstring_desc

choice_fxn = {
    'data.csv':convert_datacsv,
    'template.csv':convert_templatecsv,
    'csv': convert_templatecsv, #maintained for backwards compatibility
    'sav': convert_readstat,
    'dta':convert_readstat,
    #'por':convert_readstat,
    'sas7bdat':convert_readstat,
    'template.json':convert_templatejson,
    'json':convert_templatejson, #maintain for bwds compat
    "redcap.csv":convert_redcapcsv,
    "frictionless.schema.json":convert_frictionless_tableschema

}

input_types = " - "+"\n - ".join(list(choice_fxn.keys()))

input_descriptions = {
    name:find_docstring_desc(fxn)
    for name,fxn in choice_fxn.items()
}

def convert_to_vlmd(
    filepath,
    data_dictionary_props={},
    inputtype=None,
    outputdir=None,
    sas7bcat_filepath=None,
    csvtemplate_output_quoting=None,

    ):
    """
    Writes a data dictionary (i.e. variable level metadata) to a HEAL metadata JSON file using a registered function.

    Parameters
    ----------
    filepath : str
        Path to input file. See documentation on individual input types for more details.
    outputdir : str
        output file path or directory to where output will go. 
        1. Outputdir is a directory, will give standard names,
        2. If path to the to-be-written file is specified, will use this as new outputted filename
    data_dictionary_props : dict, optional
        The other data-dictionary level properties. By default, will give the data_dictionary `title` property as the file name stem.
    inputtype : str, optional
        The input type. If none specified, will default to using the file extension.
        See the currently registered input types in the input_types list.
    sas7bcat_filepath: str,optional
        [FOR SAS7BDAT ONLY]: Path to a sas catalog file (sas7bcat). Needed for value formats if a sas (sas7bdat) input file
    csvtemplate_output_quoting: bool, optional
        If true, all nonnumeric values will be quoted. This helps reduce ambiguity for programs
        like excel that uses special characters for specific purposes (eg = for formulas)
    
    Returns
    -------
    dict
        Dictionary with:
         1. csvtemplated array of fields.
         2. jsontemplated data dictionary object as specified by an originally drafted design doc.
            That is, a dictionary with title:<title>,description:<description>,data_dictionary:<fields>
            where data dictionary is an array of fields as specified by the JSON schema.
         3. error objects for corresponding validators (ie frictionless for csv and jsonschema for json)
    NOTE
    ----
    In future versions, this will be more of a package bundled with corresponding schemas (whether csv or JSON),better organization 
    (e.g., see frictionless Package). 
    However, right now, it simply returns the csvtemplate and jsontemplate as specified
    in the heal specification repository.
    This is an intermediate solution to socialize a proof-of-concept.

    TODO
    --------
    make sub command for each file format rather than just one function? Added sas7bcat and can predict additional complexity
    
    """

    filepath = Path(filepath)
    
    #infer input type
    if not inputtype:
        inputtype = ''.join(filepath.suffixes)[1:].lower()

    ## add dd title
    if not data_dictionary_props.get('title'):
        data_dictionary_props['title'] = filepath.stem

    
    # get data dictionary package based on the input type
    if sas7bcat_filepath:
        data_dictionary_package = choice_fxn[inputtype](filepath,data_dictionary_props,sas7bcat_file_path=sas7bcat_filepath,) 
    else:
        data_dictionary_package = choice_fxn[inputtype](filepath,data_dictionary_props)


    #TODO: currently only validates fields (ie table) but no reason it cant validate entire data package
    package_csv = validate_vlmd_csv(data_dictionary_package['templatecsv']['data_dictionary'],to_sync_fields=True)
    package_json = validate_vlmd_json(data_dictionary_package['templatejson'])

    # TODO: in future just return the packages (eg reports nested within package and not out of)
    # for now, keep same (report_xxx and templatexxx)

    report_csv = package_csv["report"]
    report_json = package_json["report"]
    templatecsv = package_csv["data"]
    templatejson = package_json["data"]

    # write to file
    if outputdir!=None:
        outputdir = Path(outputdir)
        if outputdir.is_dir():
            jsontemplate_path = outputdir/"heal-jsontemplate-data-dictionary.json"
            csvtemplate_path = outputdir/"heal-csvtemplate-data-dictionary.csv"
        elif outputdir.parent.is_dir():
            jsontemplate_path = outputdir.with_suffix(".json")
            csvtemplate_path = outputdir.with_suffix(".csv")
            outputdir = outputdir.parent
        else:
            raise Exception("outputdir must be an existing directory where files can be saved")
        
        # print data dictionaries
        jsontemplate_path.write_text(json.dumps(templatejson,indent=4))

        # NOTE: quoting non-numeric to allow special characters for nested delimiters within string columns (ie "=")
        (
            etl.fromdicts(templatecsv)
            .tocsv(
                csvtemplate_path,
                quoting=csv.QUOTE_NONNUMERIC if csvtemplate_output_quoting else csv.QUOTE_MINIMAL)

        )

        # print errors

        if not report_json['valid']:
            print("JSON data dictionary not valid, see heal-json-errors.json for errors.")
            print(f"(view the outputted data dictionary at {jsontemplate_path})")
 
        if not report_csv['valid']:
            print("CSV data dictionary not valid, see heal-csv-errors.json")
            print(f"(view the outputted data dictionary at {csvtemplate_path})")
        
        # write error reports to file
        errordir = Path(outputdir).joinpath('errors')
        errordir.mkdir(exist_ok=True)
        errordir.joinpath('heal-json-errors.json').write_text(
            json.dumps(report_json,indent=4)
        )
        errordir.joinpath('heal-csv-errors.json').write_text(
            json.dumps(report_csv,indent=4)
        )
    
    return {
        "csvtemplate":templatecsv,
        "jsontemplate":templatejson,
        "errors":{
            "csvtemplate":report_csv,
            "jsontemplate":report_json}
        }

@click.command()
@click.option('--filepath',required=True,help='Path to the file you want to convert to a HEAL data dictionary')
@click.option('--title',default=None,help='The title of your data dictionary. If not specified, then the file name will be used')
@click.option('--description',default=None,help='Description of data dictionary')
@click.option('--inputtype',default=None,type=click.Choice(list(choice_fxn.keys())),help='The type of your input file.')
@click.option('--outputdir',default="",help='The folder where you want to output your HEAL data dictionary')
@click.option('--sas7bcat-filepath',default=None,help="[FOR SAS7BDAT ONLY]: Path to a sas catalog file (sas7bcat). Needed for value formats if a sas (sas7bdat) input file")
@click.option('--csvtemplate-output-quoting',default=None,help="If true, all nonnumeric values will be quoted."
    " This helps reduce ambiguity for programs like excel that uses special characters for specific purposes (eg = for formulas)")
def main(filepath,title,description,inputtype,outputdir,sas7bcat_filepath,csvtemplate_output_quoting):
    data_dictionary_props = {'title':title,'description':description}

    #save dds and error reports to files
    data_dictionaries = convert_to_vlmd(
        filepath=filepath,
        data_dictionary_props=data_dictionary_props,
        outputdir=outputdir,
        inputtype=inputtype,
        sas7bcat_filepath=sas7bcat_filepath,
        csvtemplate_output_quoting=csvtemplate_output_quoting
    )
     
if __name__=='__main__':
    main()