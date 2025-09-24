import requests
import json
from datetime import datetime
import io
import os
import yaml

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
project_id = os.getenv("PROJECT_ID")
env_name = "env_dev"

def get_token():
    token_url = "https://id.core.matillion.com/oauth/dpc/token"

    payload = (
        "grant_type=client_credentials"
        f"&client_id={client_id}"
        f"&client_secret={client_secret}"
        "&audience=https%3A%2F%2Fapi.matillion.com"
    )

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    print("Access Token:", access_token, "\n")

    if not access_token:
        raise Exception("Failed to retrieve access token.")
    return access_token

import glob

def publish_artifact(token):
    url = f"https://us1.api.matillion.com/dpc/v1/projects/{project_id}/artifacts"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version_name = f'v_{current_time}'

    print(f"\nScanning project for .tran.yaml and .orch.yaml files...")
    files = {}

    try:
        pipeline_files = glob.glob("**/*.tran.yaml", recursive=True) + glob.glob("**/*.orch.yaml", recursive=True)
        if not pipeline_files:
            raise Exception("No pipeline files found")

        for file_path in pipeline_files:
            with open(file_path, "rb") as f:
                filename = os.path.basename(file_path)
                files[f"{filename}"] = (filename, f.read(), 'text/plain')
                print(f"Found pipeline: {file_path}")

    except Exception as e:
        print(f" Failed to load pipeline files: {e}")

    headers = {
        'Authorization': f'Bearer {token}',
        'environmentName': env_name,
        'versionName': version_name
    }
    response = requests.post(url, headers=headers, files=files)
    print("\n Artifact Response:", response.status_code)
    print(response.text)

def execute_pipeline(token, pipeline_name):
    url = f"https://us1.api.matillion.com/dpc/v1/projects/{project_id}/pipeline-executions"

    payload = json.dumps({
        "pipelineName": pipeline_name,
        "environmentName": env_name,
    })

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    print(f"\nExecuted pipeline: {pipeline_name}")
    print("Status Code:", response.status_code)
    print(response.text)

def get_changed_pipelines():
    pipelines = []
    try:
        with open("changed_pipelines.txt", "r") as f:
            for line in f:
                filename = os.path.basename(line.strip())
                pipeline_name = filename.replace(".orch.yaml", "").replace(".tran.yaml", "")
                if pipeline_name:
                    pipelines.append(pipeline_name)
    except Exception as e:
        print("Error reading changed_pipelines.txt:", e)
    return pipelines

def hardcoding_quality_checks():
    print("\n🔍 Running Hardcoding Quality Checks...")

    issues_found = False

    try:
        with open("changed_pipelines.txt", "r") as f:
            for line in f:
                pipeline_path = line.strip()
                if not pipeline_path or not os.path.exists(pipeline_path):
                    continue

                with open(pipeline_path, "r") as pf:
                    try:
                        pipeline_yaml = yaml.safe_load(pf)
                    except Exception as e:
                        print(f"⚠️ Could not parse YAML for {pipeline_path}: {e}")
                        continue

                print(f" Checking Pipeline: {pipeline_path}")

                # Navigate to pipeline components
                components = pipeline_yaml.get("pipeline", {}).get("components", {})
                for comp_name, comp_def in components.items():
                    params = comp_def.get("parameters", {})

                    
                    # --- Check warehouse ---
                    if "warehouse" in params and params["warehouse"] != "[Environment Default]":
                        print(f"❌ Hard coded warehouse in Component name {comp_name}: {params['warehouse']}")
                        issues_found = True

                    # --- Check database ---
                    if "database" in params and not str(params["database"]).startswith("${"):
                        print(f"❌ Hard coded database in Component name {comp_name}: {params['database']}")
                        issues_found = True

                    # --- Check schema ---
                    if "schema" in params and not str(params["schema"]).startswith("${"):
                        print(f"❌ Hard coded schema in Component name {comp_name}: {params['schema']}")
                        issues_found = True
                    else:
                        print(f" No hard coded issues found in pipeline: {pipeline_path}")

        if not issues_found:
            print("✅ No hardcoding issues found in pipelines.")
        else:
            raise Exception("Hardcoding violations detected. Please fix before proceeding.")

    except Exception as e:
        raise Exception(f"Hardcoding quality check failed: {e}")


def main():
    try:
        changed_pipelines = get_changed_pipelines()
        if not changed_pipelines:
            print("No pipeline changes detected. Skipping artifact creation and execution.")
            return

        print("\nChanged Pipelines Detected:", changed_pipelines)

        token = get_token()

        hardcoding_quality_checks() # Run quality checks before publishing

        publish_artifact(token)

        for pipeline_name in changed_pipelines:
            execute_pipeline(token, pipeline_name)

    except Exception as e:
        print(f"\nExecution failed: {e}")


if __name__ == "__main__":
    main()
