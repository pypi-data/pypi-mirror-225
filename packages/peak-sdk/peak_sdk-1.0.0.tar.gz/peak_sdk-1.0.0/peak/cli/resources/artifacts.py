#
# # Copyright © 2023 Peak AI Limited. or its affiliates. All Rights Reserved.
# #
# # Licensed under the Apache License, Version 2.0 (the "License"). You
# # may not use this file except in compliance with the License. A copy of
# # the License is located at:
# #
# # https://github.com/PeakBI/peak-sdk/blob/main/LICENSE
# #
# # or in the "license" file accompanying this file. This file is
# # distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# # ANY KIND, either express or implied. See the License for the specific
# # language governing permissions and limitations under the License.
# #
# # This file is part of the peak-sdk.
# # see (https://github.com/PeakBI/peak-sdk)
# #
# # You should have received a copy of the APACHE LICENSE, VERSION 2.0
# # along with this program. If not, see <https://apache.org/licenses/LICENSE-2.0>
#
"""Peak Artifacts service commands."""
from typing import Any, Dict, List, Optional

import typer
from peak.cli import args, helpers
from peak.resources.artifacts import Artifact
from rich.console import Console

app = typer.Typer(
    help="Manage artifacts used to create resources like images.",
    short_help="Create and manage Artifacts.",
)
console = Console()

_ARTIFACT_ID = typer.Argument(..., help="ID of the artifact to be used in this operation.")

_DOWNLOAD_PATH = typer.Argument(..., help="Path (including filename) where the downloaded file will be stored.")

_DOWNLOAD_VERSION = typer.Option(
    None,
    help="Artifact version to download. If no version is given then latest version is downloaded.",
)

_DELETE_VERSION = typer.Argument(..., help="Artifact version number to delete.")


@app.command("list", short_help="List artifacts.")
def list_artifacts(
    ctx: typer.Context,
    page_size: Optional[int] = args.PAGE_SIZE,
    page_number: Optional[int] = args.PAGE_NUMBER,
) -> None:
    """***List*** all artifacts for the given tenant.

    \b
    📝 ***Example Usage:***<br/>
    ```bash
    peak artifacts list --page-size 10 --page-number 1
    ```

    \b
    🆗 ***Response:***
    ```
    {
        "artifactCount": 1,
        "artifacts": [...],
        "pageCount": 1,
        "pageNumber": 1,
        "pageSize": 25
    }
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/get_api_v1_artifacts)
    """
    artifact_client: Artifact = ctx.obj["client"]
    response = artifact_client.list_artifacts(page_size=page_size, page_number=page_number, return_iterator=False)
    console.print(response)


@app.command(short_help="Describe an artifact.")
def describe(
    ctx: typer.Context,
    artifact_id: str = _ARTIFACT_ID,
    page_number: Optional[int] = args.PAGE_NUMBER,
    page_size: Optional[int] = args.PAGE_SIZE,
) -> None:
    """***Describe*** an artifact with list of its versions.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak artifacts describe "c7575459-e265-4944-a539-1fbb3336799e" --page-size 10 --page-number 1
    ```

    \b
    🆗 ***Response:***
    ```
    {
        "description": "description of this artifact",
        "id": "c7575459-e265-4944-a539-1fbb3336799e",
        "name": "my-artifact",
        "pageCount": 1,
        "pageNumber": 1,
        "pageSize": 1,
        "versionCount": 1,
        "versions": [...]
    }
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/get_api_v1_artifacts__artifactId_)
    """
    artifact_client: Artifact = ctx.obj["client"]
    response = artifact_client.describe_artifact(artifact_id=artifact_id, page_number=page_number, page_size=page_size)
    console.print(response)


@app.command(short_help="Delete an artifact.")
def delete(ctx: typer.Context, artifact_id: str = _ARTIFACT_ID) -> None:
    """***Delete*** an artifact along with all of its versions.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak artifacts delete "c7575459-e265-4944-a539-1fbb3336799e"
    ```

    \b
    🆗 ***Response:***
    ```json
    {}
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/delete_api_v1_artifacts__artifactId_)
    """
    artifact_client: Artifact = ctx.obj["client"]
    response = artifact_client.delete_artifact(artifact_id=artifact_id)
    console.print(response)


@app.command(short_help="Create a new artifact.")
def create(
    ctx: typer.Context,
    file: str = args.TEMPLATE_PATH,
    params_file: str = args.TEMPLATE_PARAMS_FILE,
    params: List[str] = args.TEMPLATE_PARAMS,
) -> None:
    """***Create*** a new artifact. This also creates the first version inside the artifact.

    \b
    🧩 ***Input File Schema(yaml):***<br/>
    ```yaml
      name (str): Name of the artifact.
      description (str): Description of the artifact.
      artifact (map):
        path (str): Path to the artifact.
        ignore_files (list(str) | required: false): Ignore files to use when creating artifact.
    ```

    \b
    📝 ***Example Usage:***
    ```bash
    peak artifacts create '/path/to/body.yaml' --params-file '/path/to/params.yaml'
    ```

    \b
    🆗 ***Response:***
    ```json
    {
        "id": "c7575459-e265-4944-a539-1fbb3336799e",
        "version": 1
    }
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/post_api_v1_artifacts)
    """
    artifact_client: Artifact = ctx.obj["client"]
    body = helpers.template_handler(file=file, params_file=params_file, params=params)
    body = helpers.remove_unknown_args(body, artifact_client.create_artifact)
    response: Dict[str, Any] = artifact_client.create_artifact(**body)
    console.print(response)


@app.command(short_help="Update an artifact's metadata.")
def update_metadata(
    ctx: typer.Context,
    artifact_id: str = _ARTIFACT_ID,
    file: str = args.TEMPLATE_PATH,
    params_file: str = args.TEMPLATE_PARAMS_FILE,
    params: List[str] = args.TEMPLATE_PARAMS,
) -> None:
    """***Update*** an artifact's metadata.

    \b
    🧩 ***Input file schema(yaml):***<br/>
    ```yaml
      body (map): Artifact metadata.
    ```

    \b
    📝 ***Example usage:***
    ```bash
    peak artifacts update-metadata '/path/to/body.yaml' --params-file '/path/to/params.yaml'
    ```

    \b
    🆗 ***Response:***
    ```json
    {}
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/patch_api_v1_artifacts__artifactId_)
    """
    artifact_client: Artifact = ctx.obj["client"]

    body: Dict[str, Any] = helpers.template_handler(file=file, params_file=params_file, params=params)
    body = helpers.remove_unknown_args(body, artifact_client.update_artifact)
    response: Dict[None, None] = artifact_client.update_artifact(artifact_id, **body)
    console.print(response)


@app.command(short_help="Download an artifact.")
def download(
    ctx: typer.Context,
    artifact_id: str = _ARTIFACT_ID,
    download_path: str = _DOWNLOAD_PATH,
    version: Optional[int] = _DOWNLOAD_VERSION,
) -> None:
    """***Download*** a specific version for an artifact and save it with the given filename on the local system.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak artifacts download "c7575459-e265-4944-a539-1fbb3336799e" '/path/to/download' --version 1
    ```

    \b
    🆗 ***Response:***
    ```python
    None
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/get_api_v1_artifacts__artifactId__download)
    """
    artifact_client: Artifact = ctx.obj["client"]
    artifact_client.download_artifact(artifact_id=artifact_id, download_path=download_path, version=version)


@app.command(short_help="Create a new version of the artifact.")
def create_version(
    ctx: typer.Context,
    artifact_id: str = _ARTIFACT_ID,
    file: str = args.TEMPLATE_PATH,
    params_file: str = args.TEMPLATE_PARAMS_FILE,
    params: List[str] = args.TEMPLATE_PARAMS,
) -> None:
    """***Create*** a new version of the artifact.

    \b
    🧩 ***Input file schema(yaml):***<br/>
    ```yaml
      artifact (map):
        path (str): Path to the artifact.
        ignore_files (list(str) | required: false): Ignore files to use when creating artifact.
    ```

    \b
    📝 ***Example usage:***
    ```bash
    peak artifacts create-version "c7575459-e265-4944-a539-1fbb3336799e" '/path/to/body.yaml' --params-file '/path/to/params.yaml'
    ```

    \b
    🆗 ***Response:***
    ```json
    {
        "version": 2
    }
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/put_api_v1_artifacts__artifactId_)
    """
    artifact_client: Artifact = ctx.obj["client"]

    body: Dict[str, Any] = helpers.template_handler(file=file, params_file=params_file, params=params)
    body = helpers.remove_unknown_args(body, artifact_client.create_artifact_version)
    response: Dict[str, int] = artifact_client.create_artifact_version(artifact_id=artifact_id, **body)
    console.print(response)


@app.command(short_help="Delete a version of an artifact.")
def delete_version(ctx: typer.Context, artifact_id: str = _ARTIFACT_ID, version: int = _DELETE_VERSION) -> None:
    """***Delete*** a version of an artifact.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak artifacts delete-version "c7575459-e265-4944-a539-1fbb3336799e" 1
    ```

    \b
    🆗 ***Response:***
    ```json
    {}
    ```

    🔗 [**API Documentation**](https://service.peak.ai/artifacts/api-docs/index.htm#/artifacts/delete_api_v1_artifacts__artifactId___version_)
    """
    artifact_client: Artifact = ctx.obj["client"]
    response = artifact_client.delete_artifact_version(artifact_id=artifact_id, version=version)
    console.print(response)
