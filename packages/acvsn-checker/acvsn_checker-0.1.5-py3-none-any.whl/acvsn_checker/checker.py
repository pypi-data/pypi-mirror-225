import json
import click
import os

# Loads configuration files containing controlled vocabulary
data_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), 'data'))


def find_path(file: str):
    return os.path.join(data_folder, file)


config_file = find_path('config.json')

gas_vocab_file = find_path('gas_vocab.json')

aerosol_vocab_file = find_path('aerosol_vocab.json')

cloud_vocab_file = find_path('cloud_vocab.json')

meteorology_vocab_file = find_path('meteorology_vocab.json')

photolysis_rate_vocab_file = find_path('photolysis_rate_vocab.json')

platform_vocab_file = find_path('platform_vocab.json')

radiation_vocab_file = find_path('radiation_vocab.json')


def load_config(file: str):
    with open(file) as json_data:
        temp_config_data = json.load(json_data)
    return temp_config_data


config_data = load_config(config_file)

# Stores the possible error messages
error_messages = {
    'MEASURE_CAT_ERROR': lambda measure_cat:
    f"Measurement category {click.style(measure_cat, fg='red')} is not valid; valid measurement categories are "
    f"{click.style(', '.join([str(s) for s in list(config_data['MeasurementCategory'].keys())]), fg='green')}",

    'NUM_ATTRIBUTES_ERROR': lambda num_attributes, expected:
    f"Number of descriptive attributes ({click.style(num_attributes, fg='red')}) does not match with expected "
    f"number of attributes ({click.style(expected, fg='green')}).",

    'ACQUISITION_ERROR': lambda acquisition_met:
    f"Acquisition method {click.style(acquisition_met, fg='red')} is not valid; valid acquisition methods are "
    f"{click.style(', '.join([str(s) for s in config_data['AcquisitionMethod']]), fg='green')}",

    'CORE_NAME_ERROR': lambda core_name, measure_cat:
    f"Core Name {click.style(core_name, fg='red')} is not valid for the measurement category "
    f"{click.style(measure_cat, fg='blue')}.",

    'SPECIFICITY_ERROR': lambda specificity, expected:
    f"Specificity attribute {click.style(specificity, fg='red')} does not match with the core name; "
    f"expected to see {click.style(expected, fg='green')}",

    'REPORTING_ERROR': lambda reporting, valid_list:
    f"Reporting attribute {click.style(reporting, fg='red')} is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'WL_ERROR': lambda wave_length, valid_list:
    f"WaveLength attribute {click.style(wave_length, fg='red')} is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'MEASUREMENT_RH_ERROR': lambda relative_humidity, valid_list:
    f"MeasurementRH attribute {click.style(relative_humidity, fg='red')} is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'SIZING_TECHNIQUE_ERROR': lambda sizing_technique, valid_list:
    f"SizingTechnique attribute {click.style(sizing_technique, fg='red')} is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'SIZE_RANGE_ERROR': lambda size_range, sizing_technique, valid_list:
    f"SizeRange attribute {click.style(size_range, fg='red')} is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}" if sizing_technique != 'None' else
    f"SizingRange attribute must be {click.style('Bulk', fg='green')} if SizingTechnique is "
    f"{click.style('None', fg='blue')}",

    'MEASURE_DIR_ERROR': lambda measurement_direction, valid_list:
    f"MeasurementDirection attribute {click.style(measurement_direction, fg='red')} is not valid; valid attributes "
    f"are {click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'SPECTRAL_COV_ERROR': lambda spectral_coverage, valid_list:
    f"SpectralCoverage attribute {click.style(spectral_coverage, fg='red')} is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'PRODUCT_ERROR': lambda products, valid_list:
    f"{click.style(products, fg='red')} is not a known product; known products are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}" if valid_list else
    f"{click.style(products, fg='red')} is not valid; expected to see "
    f"{click.style('NoProductsSpecified', fg='green')}",

    'WL_MODE_ERROR': lambda wl_mode, valid_list:
    f"WLMode attribute ({click.style(wl_mode, fg='red')}) is not valid; valid attributes are "
    f"{click.style(', '.join([str(s) for s in valid_list]), fg='green')}",

    'ZERO_ATTRIBUTE_ERROR': lambda measure_cat:
    f"Descriptive attribute for {click.style(measure_cat, fg='blue')} must be {click.style('None', fg='green')}.",

    'INSITU_ERROR': lambda acquisition_met:
    f"Acquisition method ({click.style(acquisition_met, fg='red')}) is not valid; must be "
    f"{click.style('InSitu', fg='green')}",

    'NO_ERROR': click.style("Standard name is valid.", fg='green'),
}


# Constructs StandardName object, then parses name with underscore delimiter
class StandardName:
    def __init__(self, standard_name):
        self.standard_name = standard_name
        self.parsed_name = []
        self.num_of_attributes = 0
        self.measurement_cat = ""
        self.error_codes = []

    def parse_name(self):
        self.parsed_name = self.standard_name.split('_')
        self.num_of_attributes = max(0, len(self.parsed_name) - 3)
        self.measurement_cat = self.parsed_name[0]

    # Functions for checking the measurement category and acquisition method
    def check_measure_cat(self) -> bool:
        valid_measure_cat = self.measurement_cat in config_data["MeasurementCategory"].keys()
        if not valid_measure_cat:
            self.error_codes.append(error_messages['MEASURE_CAT_ERROR'](self.measurement_cat))
        return valid_measure_cat

    def check_acquisition_met(self) -> bool:
        acquisition_met = self.parsed_name[2]
        valid_acquisition_met = self.parsed_name[2] in config_data["AcquisitionMethod"]
        if not valid_acquisition_met:
            self.error_codes.append(error_messages["ACQUISITION_ERROR"](acquisition_met))
        return valid_acquisition_met

    # Checks if the number of descriptive attributes matches with measurement category
    def check_num_attributes(self) -> bool:
        expected_attributes = config_data["MeasurementCategory"].get(self.measurement_cat)
        valid_num_attributes = (expected_attributes == self.num_of_attributes) if expected_attributes != 0 \
            else (self.num_of_attributes == 1)
        if not valid_num_attributes:
            self.error_codes.append(error_messages["NUM_ATTRIBUTES_ERROR"](self.num_of_attributes, expected_attributes))
        return valid_num_attributes

    # Helper functions to check if the descriptive attributes are valid for the corresponding measurement category
    def check_gas(self) -> bool:
        gas_vocab = load_config(gas_vocab_file)

        core_name = self.parsed_name[1]
        specificity = self.parsed_name[3]
        reporting = self.parsed_name[4]

        expected_specificity = gas_vocab["Gas CoreName:MeasurementSpecificity"].get(core_name)

        valid_core_name = core_name in gas_vocab["Gas CoreName:MeasurementSpecificity"].keys()
        valid_specificity = (specificity == expected_specificity)
        valid_reporting = reporting in gas_vocab["Reporting"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_specificity and valid_core_name:
            self.error_codes.append(error_messages["SPECIFICITY_ERROR"](specificity, expected_specificity))
        if not valid_reporting:
            self.error_codes.append(error_messages["REPORTING_ERROR"](reporting, gas_vocab["Reporting"]))

        return valid_core_name and valid_reporting and valid_specificity

    def check_aermp(self) -> bool:
        aerosol_vocab = load_config(aerosol_vocab_file)

        core_name = self.parsed_name[1]
        relative_humidity = self.parsed_name[3]
        sizing_technique = self.parsed_name[4]
        size_range = self.parsed_name[5]
        reporting = self.parsed_name[6]

        valid_core_name = core_name in aerosol_vocab["AerMP CoreName"]
        valid_rh = relative_humidity in aerosol_vocab["MeasurementRH"]
        valid_size_technique = sizing_technique in aerosol_vocab["SizingTechnique"]
        valid_size_range = (size_range == "Bulk") if sizing_technique == "None" else \
            size_range in aerosol_vocab["SizeRange"]
        valid_reporting = reporting in aerosol_vocab["AerMP/AerOpt Reporting"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_rh:
            self.error_codes.append(error_messages["MEASUREMENT_RH_ERROR"](relative_humidity,
                                                                           aerosol_vocab["MeasurementRH"]))
        if not valid_size_technique:
            self.error_codes.append(error_messages["SIZING_TECHNIQUE_ERROR"](sizing_technique,
                                                                             aerosol_vocab["SizingTechnique"]))
        if not valid_size_range:
            self.error_codes.append(error_messages["SIZE_RANGE_ERROR"](size_range, sizing_technique,
                                                                       aerosol_vocab["SizeRange"]))
        if not valid_reporting:
            self.error_codes.append(error_messages["REPORTING_ERROR"](reporting,
                                                                      aerosol_vocab["AerMP/AerOpt Reporting"]))

        return valid_core_name and valid_rh and valid_size_technique and valid_size_range and valid_reporting

    def check_aercomp(self) -> bool:
        aerosol_vocab = load_config(aerosol_vocab_file)

        core_name = self.parsed_name[1]
        sizing_technique = self.parsed_name[3]
        size_range = self.parsed_name[4]
        reporting = self.parsed_name[5]

        valid_core_name = core_name in aerosol_vocab["AerComp CoreName"]
        valid_size_technique = sizing_technique in aerosol_vocab["SizingTechnique"]
        valid_size_range = (size_range == "Bulk") if sizing_technique == "None" else \
            size_range in aerosol_vocab["SizeRange"]
        valid_reporting = reporting in aerosol_vocab["AerComp Reporting"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_size_technique:
            self.error_codes.append(error_messages["SIZING_TECHNIQUE_ERROR"](sizing_technique,
                                                                             aerosol_vocab["SizingTechnique"]))
        if not valid_size_range:
            self.error_codes.append(error_messages["SIZE_RANGE_ERROR"](size_range, sizing_technique,
                                                                       aerosol_vocab["SizeRange"]))
        if not valid_reporting:
            self.error_codes.append(error_messages["REPORTING_ERROR"](reporting, aerosol_vocab["AerComp Reporting"]))

        return valid_core_name and valid_size_technique and valid_size_range and valid_reporting

    def check_aeropt(self) -> bool:
        aerosol_vocab = load_config(aerosol_vocab_file)

        core_name = self.parsed_name[1]
        wave_length = self.parsed_name[3]
        relative_humidity = self.parsed_name[4]
        size_range = self.parsed_name[5]
        reporting = self.parsed_name[6]

        valid_core_name = core_name in aerosol_vocab["AerOpt CoreName"]
        valid_wl = wave_length in aerosol_vocab["WL"]
        valid_rh = relative_humidity in aerosol_vocab["MeasurementRH"]
        valid_size_range = size_range in aerosol_vocab["SizeRange"]
        valid_reporting = reporting in aerosol_vocab["AerMP/AerOpt Reporting"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_wl:
            self.error_codes.append(error_messages["WL_ERROR"](wave_length, aerosol_vocab["WL"]))
        if not valid_rh:
            self.error_codes.append(error_messages["MEASUREMENT_RH_ERROR"](relative_humidity,
                                                                           aerosol_vocab["MeasurementRH"]))
        if not valid_size_range:
            self.error_codes.append(error_messages["SIZE_RANGE_ERROR"](size_range, "Default",
                                                                       aerosol_vocab["SizeRange"]))
        if not valid_reporting:
            self.error_codes.append(error_messages["REPORTING_ERROR"](reporting,
                                                                      aerosol_vocab["AerMP/AerOpt Reporting"]))

        return valid_core_name and valid_wl and valid_rh and valid_size_range and valid_reporting

    def check_cldcomp(self) -> bool:
        cloud_vocab = load_config(cloud_vocab_file)

        core_name = self.parsed_name[1]
        sizing_technique = self.parsed_name[3]
        size_range = self.parsed_name[4]
        reporting = self.parsed_name[5]

        valid_core_name = core_name in cloud_vocab["CldComp CoreName"]
        valid_size_technique = sizing_technique in cloud_vocab["SizingTechnique"]
        valid_size_range = (size_range == "Bulk") if sizing_technique == "None" else \
            size_range in cloud_vocab["SizeRange"]
        valid_reporting = reporting in cloud_vocab["CldComp Reporting"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_size_technique:
            self.error_codes.append(error_messages["SIZING_TECHNIQUE_ERROR"](sizing_technique,
                                                                             cloud_vocab["SizingTechnique"]))
        if not valid_size_range:
            self.error_codes.append(error_messages["SIZE_RANGE_ERROR"](size_range, sizing_technique,
                                                                       cloud_vocab["SizeRange"]))
        if not valid_reporting:
            self.error_codes.append(error_messages["REPORTING_ERROR"](reporting, cloud_vocab["CldComp Reporting"]))

        return valid_core_name and valid_size_technique and valid_size_range and valid_reporting

    def check_cldmicro(self) -> bool:
        cloud_vocab = load_config(cloud_vocab_file)

        core_name = self.parsed_name[1]
        sizing_technique = self.parsed_name[3]
        size_range = self.parsed_name[4]
        reporting = self.parsed_name[5]

        valid_core_name = core_name in cloud_vocab["CldMicro CoreName"]
        valid_size_technique = sizing_technique in cloud_vocab["SizingTechnique"]
        valid_size_range = (size_range == "Bulk") if sizing_technique == "None" else \
            size_range in cloud_vocab["SizeRange"]
        valid_reporting = reporting in cloud_vocab["CldMicro Reporting"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_size_technique:
            self.error_codes.append(error_messages["SIZING_TECHNIQUE_ERROR"](sizing_technique,
                                                                             cloud_vocab["SizingTechnique"]))
        if not valid_size_range:
            self.error_codes.append(error_messages["SIZE_RANGE_ERROR"](size_range, sizing_technique,
                                                                       cloud_vocab["SizeRange"]))
        if not valid_reporting:
            self.error_codes.append(error_messages["REPORTING_ERROR"](valid_reporting,
                                                                      cloud_vocab["CldMicro Reporting"]))

        return valid_core_name and valid_size_technique and valid_size_range and valid_reporting

    def check_cldmacro(self) -> bool:
        cloud_vocab = load_config(cloud_vocab_file)

        core_name = self.parsed_name[1]
        attributes = self.parsed_name[3]

        valid_core_name = core_name in cloud_vocab["CldMacro CoreName"]
        valid_zero_attribute = (attributes == "None")

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_zero_attribute:
            self.error_codes.append(error_messages["ZERO_ATTRIBUTE_ERROR"](self.measurement_cat))

        return valid_core_name and valid_zero_attribute

    def check_cldopt(self) -> bool:
        cloud_vocab = load_config(cloud_vocab_file)

        core_name = self.parsed_name[1]
        wave_length = self.parsed_name[3]

        valid_core_name = core_name in cloud_vocab["CldOpt CoreName"]
        valid_wl = wave_length in cloud_vocab["WL"]

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_wl:
            self.error_codes.append(error_messages["WL_ERROR"](wave_length, cloud_vocab["WL"]))

        return valid_core_name and valid_wl

    def check_met(self) -> bool:
        meteorology_vocab = load_config(meteorology_vocab_file)

        core_name = self.parsed_name[1]
        attributes = self.parsed_name[3]

        valid_core_name = core_name in meteorology_vocab["Met CoreName"]
        valid_zero_attribute = (attributes == "None")

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_zero_attribute:
            self.error_codes.append(error_messages["ZERO_ATTRIBUTE_ERROR"](self.measurement_cat))

        return valid_core_name and valid_zero_attribute

    def check_gasjvalue(self) -> bool:
        photolysis_rate_vocab = load_config(photolysis_rate_vocab_file)

        core_name = self.parsed_name[1]
        acquisition_met = self.parsed_name[2]
        measurement_direction = self.parsed_name[3]
        spectral_coverage = self.parsed_name[4]
        products = self.parsed_name[5]

        expected_products = photolysis_rate_vocab["GasJvalue CoreName:Products"].get(core_name)

        valid_core_name = core_name in photolysis_rate_vocab["GasJvalue CoreName:Products"].keys()
        valid_measure_dir = measurement_direction in photolysis_rate_vocab["MeasurementDirection"]
        valid_spectral_cov = spectral_coverage in photolysis_rate_vocab["SpectralCoverage"]
        valid_products = (products in expected_products) if expected_products else (products == "NoProductsSpecified")
        valid_acquisition = (acquisition_met == "InSitu")

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_measure_dir:
            self.error_codes.append(error_messages["MEASURE_DIR_ERROR"](measurement_direction,
                                                                        photolysis_rate_vocab['MeasurementDirection']))
        if not valid_spectral_cov:
            self.error_codes.append(error_messages["SPECTRAL_COV_ERROR"](spectral_coverage,
                                                                         photolysis_rate_vocab['SpectralCoverage']))
        if not valid_products and valid_core_name:
            self.error_codes.append(error_messages["PRODUCT_ERROR"](products, expected_products))
        if not valid_acquisition:
            self.error_codes.append(error_messages["INSITU_ERROR"](acquisition_met))

        return valid_core_name and valid_measure_dir and valid_spectral_cov and valid_products and valid_acquisition

    def check_aqujvalue(self) -> bool:
        photolysis_rate_vocab = load_config(photolysis_rate_vocab_file)

        core_name = self.parsed_name[1]
        acquisition_met = self.parsed_name[2]
        measurement_direction = self.parsed_name[3]
        spectral_coverage = self.parsed_name[4]
        products = self.parsed_name[5]

        expected_products = photolysis_rate_vocab["AquJvalue CoreName:Products"].get(core_name)

        valid_core_name = core_name in photolysis_rate_vocab["AquJvalue CoreName:Products"].keys()
        valid_measure_dir = measurement_direction in photolysis_rate_vocab["MeasurementDirection"]
        valid_spectral_cov = spectral_coverage in photolysis_rate_vocab["SpectralCoverage"]
        valid_products = (products in expected_products) if expected_products else (products == "NoProductsSpecified")
        valid_acquisition = (acquisition_met == "InSitu")

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_measure_dir:
            self.error_codes.append(error_messages["MEASURE_DIR_ERROR"](measurement_direction,
                                                                        photolysis_rate_vocab['MeasurementDirection']))
        if not valid_spectral_cov:
            self.error_codes.append(error_messages["SPECTRAL_COV_ERROR"](spectral_coverage,
                                                                         photolysis_rate_vocab['SpectralCoverage']))
        if not valid_products and valid_core_name:
            self.error_codes.append(error_messages["PRODUCT_ERROR"](products, expected_products))
        if not valid_acquisition:
            self.error_codes.append(error_messages["INSITU_ERROR"](acquisition_met))

        return valid_core_name and valid_measure_dir and valid_spectral_cov and valid_products and valid_acquisition

    def check_platform(self) -> bool:
        platform_vocab = load_config(platform_vocab_file)

        core_name = self.parsed_name[1]
        acquisition_met = self.parsed_name[2]
        attributes = self.parsed_name[3]

        valid_core_name = core_name in platform_vocab["Platform CoreName"]
        valid_acquisition = (acquisition_met == "InSitu")
        valid_zero_attribute = (attributes == "None")

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_acquisition:
            self.error_codes.append(error_messages["INSITU_ERROR"](acquisition_met))
        if not valid_zero_attribute:
            self.error_codes.append(error_messages["ZERO_ATTRIBUTE_ERROR"](self.measurement_cat))

        return valid_core_name and valid_acquisition and valid_zero_attribute

    def check_rad(self) -> bool:
        radiation_vocab = load_config(radiation_vocab_file)

        core_name = self.parsed_name[1]
        acquisition_met = self.parsed_name[2]
        wl_mode = self.parsed_name[3]

        valid_core_name = core_name in radiation_vocab["Rad CoreName"]
        valid_wl_mode = wl_mode in radiation_vocab["WLMode"]
        valid_acquisition = (acquisition_met == "InSitu")

        if not valid_core_name:
            self.error_codes.append(error_messages["CORE_NAME_ERROR"](core_name, self.measurement_cat))
        if not valid_wl_mode:
            self.error_codes.append(error_messages["WL_MODE_ERROR"](wl_mode, radiation_vocab["WLMode"]))
        if not valid_acquisition:
            self.error_codes.append(error_messages["INSITU_ERROR"](acquisition_met))

        return valid_core_name and valid_wl_mode and valid_acquisition

    # Main function that checks all the attributes of standard name
    def check_standard_name(self) -> bool:
        self.parse_name()

        valid_measure_cat = self.check_measure_cat()
        valid_num_att = False
        valid_acquisition = False
        valid_attributes = False

        check_descriptive_att = {
            "Gas": self.check_gas,
            "AerMP": self.check_aermp,
            "AerComp": self.check_aercomp,
            "AerOpt": self.check_aeropt,
            "CldComp": self.check_cldcomp,
            "CldMicro": self.check_cldmicro,
            "CldMacro": self.check_cldmacro,
            "CldOpt": self.check_cldopt,
            "Met": self.check_met,
            "GasJvalue": self.check_gasjvalue,
            "AquJvalue": self.check_aqujvalue,
            "Platform": self.check_platform,
            "Rad": self.check_rad
        }

        if valid_measure_cat:
            valid_num_att = self.check_num_attributes()
        if valid_num_att:
            valid_acquisition = self.check_acquisition_met()
        if valid_acquisition:
            valid_attributes = check_descriptive_att[self.measurement_cat]()

        return valid_measure_cat and valid_num_att and valid_acquisition and valid_attributes


# Command line interface that prints whether standard name is valid; if not, prints list of errors
@click.group()
def main():
    """Checks if a STANDARD NAME is valid. For documentation on ACVSNC, visit
    https://www.earthdata.nasa.gov/esdis/esco/standards-and-practices/acvsnc"""
    pass


@click.command()
@click.argument('name')
def check_name(name):
    standard_name = StandardName(name)
    is_valid = standard_name.check_standard_name()
    errors = standard_name.error_codes

    click.echo(f"Checking {click.style(standard_name.standard_name, fg='yellow')} ... \n")

    if is_valid:
        click.echo(f"{error_messages['NO_ERROR']}")
    elif len(errors) == 1:
        click.echo(f"{errors[0]}")
    else:
        for index, error in enumerate(errors):
            click.echo(f"{index + 1}. {error}")


@click.command()
@click.argument('filename')
def check_file(filename):
    click.echo("Checking file ... \n")

    try:
        with open(filename, 'r') as file_input:
            file_header = file_input.readlines()
    except IOError:
        click.secho("File was not found.", fg='red')
        exit()

    num_variables = int(file_header[9])
    valid_header = True

    for line_index in range(12, 12 + num_variables):
        line = file_header[line_index]
        if not ('TIME' in line.upper()):

            standard_name = StandardName(line.split(',')[2].strip())
            is_valid = standard_name.check_standard_name()
            errors = standard_name.error_codes

            if not is_valid and standard_name.standard_name != 'None':
                click.echo(f"Error found on line {click.style(line_index, fg='yellow')} with standard name "
                           f"{click.style(standard_name.standard_name, fg='red')}")
                valid_header = False
                if len(errors) == 1:
                    click.echo(f"{errors[0]}")
                else:
                    for index, error in enumerate(errors):
                        click.echo(f"{index + 1}. {error}")
                click.echo("-------------------------------------------------------------------------------")

    if valid_header:
        click.echo("All standard names in file header are valid.")


main.add_command(check_name)
main.add_command(check_file)

if __name__ == '__main__':
    main()
