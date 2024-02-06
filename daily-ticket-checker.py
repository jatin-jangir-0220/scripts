import subprocess
import json
import os

def prettify_json(data, indent=4, sort_keys=False):
    """
    Prettifies JSON data and returns a formatted string.

    Args:
        data (str or dict): The JSON data to prettify.
        indent (int, optional): The indentation level (default: 4 spaces).
        sort_keys (bool, optional): Whether to sort keys alphabetically (default: False).

    Returns:
        str: The prettified JSON string.

    Raises:
        TypeError: If `data` is not a string or dictionary.
    """

    if not isinstance(data, (str, dict)):
        raise TypeError("Input data must be a string or dictionary.")

    try:
        # Load JSON if necessary
        if isinstance(data, str):
            data = json.loads(data)

        # Use json.dumps with parameters for flexible formatting
        return json.dumps(
            data, ensure_ascii=False, indent=indent, sort_keys=sort_keys
        )

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {e}")

def run_gh_command(command):
    """
    Runs a given `gh` command and returns the captured JSON output as a Python object.

    Args:
        command (str): The `gh` command to run (e.g., "gh issue list -s open --json").

    Returns:
        object: The parsed JSON output as a Python object.
    """

    try:
        # Use capture_output for cleaner code and error handling
        result = subprocess.run(
            command.split(), capture_output=True, text=True, check=True
        )

        # Check for successful execution
        if result.returncode != 0:
            raise Exception(f"Failed to run gh command: {result.stderr}")

        # Parse JSON output
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON output: {result.stdout}")

        return output

    except Exception as e:
        raise Exception(f"Error running gh command: {e}")


def add_label_to_issue( issue_number, label_name):
    """
    Adds a label to a GitHub issue using the `gh` command.

    Args:
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        issue_number (int): The number of the issue to add the label to.
        label_name (str): The name of the label to add.

    Raises:
        ValueError: If any of the arguments are invalid.
        subprocess.CalledProcessError: If the `gh` command fails to execute.
        Exception: If an unexpected error occurs.
    """

    if not all(isinstance(arg, str) for arg in [label_name]) or not isinstance(issue_number, int):
        raise ValueError(
            "Invalid arguments: label_name must be strings, and issue_number must be an integer.")

    command = f"gh issue edit  {issue_number} --add-label '{label_name}'"

    try:
        result = os.system(command)
        if result != 0:
            print(f"Failed to add label: {issue_number}")
        else:
            print(
                f"Label '{label_name}' added to issue #{issue_number} successfully.")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Error adding label: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def remove_label_from_issue(issue_number, label_name):
    """
    Removes a label from a GitHub issue using the `gh` command.

    Args:
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        issue_number (int): The number of the issue to remove the label from.
        label_name (str): The name of the label to remove.

    Raises:
        ValueError: If any of the arguments are invalid.
        subprocess.CalledProcessError: If the `gh` command fails to execute.
        Exception: If an unexpected error occurs.
    """

    if not all(isinstance(arg, str) for arg in [ label_name]) or not isinstance(issue_number, int):
        raise ValueError(
            "Invalid arguments:  label_name must be strings, and issue_number must be an integer.")

    command = f"gh issue edit {issue_number} --remove-label {label_name}"
    try:
        result = os.system(command)

        if result != 0:
           print(f"Failed to remove label: {result}")
        else:
            print(
                f"Label '{label_name}' removed from issue #{issue_number} successfully.")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Error removing label: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}") 
    

default_value = "6"
project_id = os.getenv("PROJECT_ID", default_value)
command = "gh project  item-list "+project_id+" --format json --owner jatin-jangir-0220"
issues = run_gh_command(command)
# pretty_json = prettify_json(issues, indent=2, sort_keys=True)
# print(pretty_json)
for item in issues['items']:
    if "estimate" not in item:
        add_label_to_issue(item["content"]["number"], "DSV-FAILED")
    else :
        remove_label_from_issue(item["content"]["number"], "DSV-FAILED")

# Customize further processing based on your specific needs
