import os
import shutil

from bentoctl.exceptions import TemplateExists, TemplateTypeNotDefined

from google_cloud_run_deploy.values import DeploymentValues


def copy_template(template_name: str, destination_dir: str):
    TERRAFORM_TEMPLATE_FILE_NAME = "main.tf"
    template_name = template_name + ".tf"

    template_file = os.path.join(destination_dir, TERRAFORM_TEMPLATE_FILE_NAME)
    if os.path.exists(template_file):
        raise TemplateExists(template_file)

    shutil.copyfile(
        os.path.join(os.path.dirname(__file__), f"templates/{template_name}"),
        template_file,
    )

    return template_file


def generate_terraform_template(_, destination_dir: str):
    return copy_template("terraform_default", destination_dir)


def generate_terraform_values(name: str, spec: dict, destination_dir: str):
    TERRAFORM_VALUES_FILE_NAME = "bentoctl.tfvars"

    params = DeploymentValues(name, spec, "terraform")
    values_file = os.path.join(destination_dir, TERRAFORM_VALUES_FILE_NAME)
    params.to_params_file(values_file)

    return values_file


def generate(
    name: str,
    spec: dict,
    template_type: str,
    destination_dir: str,
    values_only: bool = True,
):
    """
    generates the template corresponding to the template_type.

    Parameters
    ----------
    name : str
        deployment name to be used by the template. This name will be used
        to create the resource names.
    spec : dict
        The properties of the deployment (specifications) passed from the
        deployment_config's `spec` section.
    template_type: str
        The type of template that is to be generated by the operator. The
        available ones are [terraform, cloudformation]
    destination_dir: str
        The directory into which the files are generated.
    values_only: bool
        Generate only the values files.

    Returns
    -------
    generated_path : str
        The path for the generated template.
    """
    generated_files = []

    if template_type == "terraform":
        if not values_only:
            template_file_path = generate_terraform_template(spec, destination_dir)
            generated_files.append(template_file_path)
        values_file_path = generate_terraform_values(name, spec, destination_dir)
        generated_files.append(values_file_path)
    else:
        raise TemplateTypeNotDefined(template_type)

    return generated_files
