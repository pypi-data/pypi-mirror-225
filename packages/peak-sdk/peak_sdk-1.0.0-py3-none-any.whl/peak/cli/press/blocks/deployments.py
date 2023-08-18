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
"""Peak blocks deployments commands."""
from typing import Dict, List, Optional

import typer
from peak.cli import args, helpers
from peak.press.blocks import Block
from rich.console import Console

app = typer.Typer()
console = Console()

_DEPLOYMENT_ID = typer.Argument(..., help="ID of the Block deployment to be used in this operation")


@app.command(short_help="Create a Block deployment.")
def create(
    ctx: typer.Context,
    file: str = args.TEMPLATE_PATH,
    params_file: Optional[str] = args.TEMPLATE_PARAMS_FILE,
    params: Optional[List[str]] = args.TEMPLATE_PARAMS,
) -> None:
    """***Create*** a Block deployment This creates the resource described in the Block Spec.

    \b
    🧩 ***Input file schema (yaml):***<br/>
    ```yaml
      body (map):
        metadata (map):
            name (string | required: false): Name of the deployment. Must be unique within the tenant.
            title (string | required: false): Title of the deployment.
            summary (string | required: false): Summary of the deployment.
            description (string | required: false): Description of the deployment.
            descriptionContentType (string | required: false): Content type of the description. Should be one of "text/plain" or "text/markdown".
            imageUrl (string | required: false): URL of the image to be associated with the block deployment.
            tags (list(map) | required: false):
                - name (string): Name of the tag.
        revision (map | required: false):
            notes (string | required: false): Notes for the deployment revision.
        spec (map):
            id (string): ID of the block spec to be deployed.
            release (map | required: false):
                version (string): A valid semantic release version of the block spec.
    ```

    \b
    📝 ***Example usage:***
    ```bash
    peak blocks deployments create /path/to/body.yaml -v /path/to/params.yaml
    ```

    \b
    🆗 ***Response:***
    ```json
    {
        "id": "632a4e7c-ab86-4ecb-8f34-99b5da531ceb"
    }
    ```

    🔗 [**API Documentation**](https://press.peak.ai/api-docs/index.htm#/Block%20Deployments/post_v1_blocks_deployments)
    """
    body = helpers.template_handler(file, params_file, params)
    blocks_client: Block = ctx.obj["client"]
    body = helpers.remove_unknown_args(body, blocks_client.create_deployment)
    response: Dict[str, str] = blocks_client.create_deployment(**body)

    console.print(response)


@app.command("list", short_help="List Block deployments.")
def list_block_deployments(
    ctx: typer.Context,
    page_size: Optional[int] = args.PAGE_SIZE,
    page_number: Optional[int] = args.PAGE_NUMBER,
    status: Optional[List[str]] = args.STATUS_FILTER,
    name: Optional[str] = args.NAME_FILTER,
    title: Optional[str] = args.TITLE_FILTER,
    sort: Optional[List[str]] = args.SORT_KEYS,
) -> None:
    """***List*** Block deployments that have been created for the given tenant.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak blocks deployments list --status=deployed,failed --page-size 10 --page-number 1
    ```

    \b
    🆗 ***Response:***
    ```
    {
        "deploymentsCount": 1,
        "deployments": [...],
        "pageCount": 1,
        "pageNumber": 1,
        "pageSize": 25
    }
    ```

    🔗 [**API Documentation**](https://press.peak.ai/api-docs/index.htm#/Block%20Deployments/get_v1_blocks_deployments)
    """
    blocks_client: Block = ctx.obj["client"]
    response = blocks_client.list_deployments(
        status=status,
        name=name,
        sort=sort,
        title=title,
        page_size=page_size,
        page_number=page_number,
        return_iterator=False,
    )
    console.print(response)


@app.command(short_help="Describe the Block deployment.")
def describe(
    ctx: typer.Context,
    deployment_id: str = _DEPLOYMENT_ID,
) -> None:
    """***Describe*** the Block deployment with details of its latest revision.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak blocks deployments describe "632a4e7c-ab86-4ecb-8f34-99b5da531ceb"
    ```

    \b
    🆗 ***Response:***
    ```
    {
        "id": "632a4e7c-ab86-4ecb-8f34-99b5da531ceb",
        "kind": "app",
        "latestRevision": {...},
        "metadata": {...},
        "spec": {...}
    }
    ```

    🔗 [**API Documentation**](https://press.peak.ai/api-docs/index.htm#/Block%20Deployments/get_v1_blocks_deployments__deploymentId_)
    """
    blocks_client: Block = ctx.obj["client"]
    response = blocks_client.describe_deployment(deployment_id)
    console.print(response)


@app.command(short_help="Update the Block deployment metadata.")
def update_metadata(
    ctx: typer.Context,
    deployment_id: str = _DEPLOYMENT_ID,
    file: str = args.TEMPLATE_PATH,
    params_file: Optional[str] = args.TEMPLATE_PARAMS_FILE,
    params: Optional[List[str]] = args.TEMPLATE_PARAMS,
) -> None:
    """***Update*** the Block deployment metadata.

    \b
    🧩 ***Input file schema (yaml):***<br/>
    ```yaml
      body (map):
        name (string | required: false): Name of the deployment. Must be unique within the tenant.
        title (string | required: false): Title of the deployment.
        summary (string | required: false): Summary of the deployment.
        description (string | required: false): Description of the deployment.
        descriptionContentType (string | required: false): Content type of the description. Should be one of "text/plain" or "text/markdown".
        imageUrl (string | required: false): URL of the image to be associated with the block deployment.
        tags (list(map) | required: false):
            - name (string): Name of the tag.
    ```

    \b
    📝 ***Example usage:***
    ```bash
    peak blocks deployments update-metadata "632a4e7c-ab86-4ecb-8f34-99b5da531ceb" /path/to/body.yaml -v /path/to/params.yaml
    ```

    \b
    🆗 ***Response:***
    ```
    {
        "id": "632a4e7c-ab86-4ecb-8f34-99b5da531ceb"
        "kind": "workflow",
        "latestRevision": {...},
        "metadata": {...},
        "spec": {...}
    }
    ```

    🔗 [**API Documentation**](https://press.peak.ai/api-docs/index.htm#/Block%20Deployments/patch_v1_blocks_deployments__deploymentId_)
    """
    body = helpers.template_handler(file, params_file, params)
    blocks_client: Block = ctx.obj["client"]
    body = helpers.remove_unknown_args(body, blocks_client.update_deployment_metadata)
    response = blocks_client.update_deployment_metadata(deployment_id, **body)
    console.print(response)


@app.command(short_help="Delete a Block deployment.")
def delete(
    ctx: typer.Context,
    deployment_id: str = _DEPLOYMENT_ID,
) -> None:
    """***Delete*** a Block deployment. This will delete the resource that was created as part of the deployment.

    \b
    📝 ***Example usage:***<br/>
    ```bash
    peak blocks deployments delete "632a4e7c-ab86-4ecb-8f34-99b5da531ceb"
    ```

    \b
    🆗 ***Response:***
    ```json
    {}
    ```

    🔗 [**API Documentation**](https://press.peak.ai/api-docs/index.htm#/Block%20Deployments/delete_v1_blocks_deployments__deploymentId_)
    """
    blocks_client: Block = ctx.obj["client"]
    response = blocks_client.delete_deployment(deployment_id)
    console.print(response)
