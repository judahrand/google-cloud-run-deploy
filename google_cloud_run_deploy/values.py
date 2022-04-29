from collections import UserDict

from google_cloud_run_deploy.schema import OPERATOR_SCHEMA

DEPLOYMENT_PARAMS_WARNING = """# This file is maintained automatically by 
# "bentoctl generate" and "bentoctl build" commands. 
# Manual edits may be lost the next time these commands are run.

"""


class DeploymentValues(UserDict):
    def __init__(self, name, spec, template_type):
        if "image_tag" in spec:
            _, image_repository, image_version = self.parse_image_tag(spec["image_tag"])
            spec["image_repository"] = image_repository
            spec["image_version"] = image_version

        super().__init__({"deployment_name": name, **spec})
        self.template_type = template_type

    @staticmethod
    def parse_image_tag(image_tag: str):
        registry_url, project_id, tag = image_tag.split("/")
        repository, version = tag.split(":")

        return registry_url, repository, version

    def to_params_file(self, file_path):
        if self.template_type == "terraform":
            self.generate_terraform_tfvars_file(file_path)

    @classmethod
    def from_params_file(cls, file_path):
        pass

    def generate_terraform_tfvars_file(self, file_path):
        params = []
        for param_name, param_value in self.items():
            params.append(f'{param_name} = "{param_value}"')

        with open(file_path, "w") as params_file:
            params_file.write(DEPLOYMENT_PARAMS_WARNING)
            params_file.write("\n".join(params))
            params_file.write("\n")
