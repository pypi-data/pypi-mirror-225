
CREATE_DESCRIPTION = (
    "Create a new plugin."
    + " This command will generate the skeleton folder structure and "
    "code for a new plugin, based on the provided plugin.spec.yaml file"
)
SERVER_DESCRIPTION = (
    "Run the plugin in HTTP mode."
    + " This allows an external API testing program to be "
    "used to test a plugin "
)
SAMPLES_DESCRIPTION = (
    "Create test samples for actions and triggers."
    + " This command will create new files under the 'tests' folder "
    "which can be used to test each new action/trigger. "
    "Note if a file already exists for a particular action/trigger, it will not be overwritten"
)
REFRESH_DESCRIPTION = (
    "Refresh the plugin."
    + " This command will update the current plugin code, when updates are made in the "
    "plugin.spec.yaml file"
)
RUN_DESCRIPTION = (
    "Run an action/trigger from a json test file"
    + " (created during sample generation)"
)
SHELL_DESCRIPTION = (
    "Run the plugin via the docker shell"
    + " to enable advanced debugging"
)
EXPORT_DESCRIPTION = (
    "Export a plugin Docker image to a tarball."
    + " This tarball can be uploaded as a custom plugin via the import "
    "functionality in the InsightConnect UI"
)
VALIDATE_DESCRIPTION = (
    "Validate / Run checks against the plugin."
    + " This command performs quality control checks on the current "
    "state of the plugin. This should be run before finalizing any new updates"
)
VERSION_DESCRIPTION = (
    "Update the plugin versioning."
    + " This command should be run after finalizing any updates, defect fixes or "
    "new functionality, to update the versioning"
)
VIEW_DESCRIPTION = (
    "View plugin docker container info"
    + "Provides an overview of the plugin"
)
