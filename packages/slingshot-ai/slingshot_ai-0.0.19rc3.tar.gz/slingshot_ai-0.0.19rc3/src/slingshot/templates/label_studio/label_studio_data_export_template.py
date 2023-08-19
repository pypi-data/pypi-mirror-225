from __future__ import annotations

import asyncio
import os

import label_studio_sdk
from label_studio_data_type import LabelStudioExportFields, LabelStudioImportFields

from slingshot.schemas import Annotation, Example, Result, Upsert
from slingshot.sdk import SlingshotSDK

# This is the tag of your existing Slingshot dataset that you want to upsert annotations into
DATASET_TAG = 'dataset'
UPSERT_FILENAME = 'dataset.jsonl'


# This is an example annotation object from Label Studio where the task type is classification and
# the classification result is stored in the `classification` field. You should modify this class
# to match the annotation object that you are exporting from your own use case.
class LabelStudioResult(LabelStudioImportFields, LabelStudioExportFields):
    annotator: int
    annotation_id: int
    created_at: str
    updated_at: str
    lead_time: float


def convert_label_studio_annotations_to_examples(ls_annotations: list[LabelStudioResult]) -> list[Example]:
    examples: list[Example] = []
    for ls_annotation in ls_annotations:
        data = LabelStudioImportFields.model_validate(ls_annotation.model_dump())
        export_fields = LabelStudioExportFields.model_validate(ls_annotation.model_dump())
        annotation = Annotation(
            created_at=ls_annotation.created_at,
            updated_at=ls_annotation.updated_at,
            annotator=str(ls_annotation.annotator),
            result=[Result(task_type="classification", value=export_fields.model_dump())],
        )
        example = Example(data=data.model_dump(), annotations=[annotation])
        examples.append(example)
    return examples


def get_label_studio_annotations(ls_client: label_studio_sdk.Client) -> list[Example]:
    # Get the Label Studio project
    project = ls_client.get_project(id=1)
    # Retrieve all annotations from the project
    res = project.export_tasks(export_type='JSON_MIN')
    ls_annotations = [LabelStudioResult.model_validate(annotation_obj) for annotation_obj in res]
    # Convert LS annotations to Slingshot examples
    examples = convert_label_studio_annotations_to_examples(ls_annotations)
    return examples


def create_upsert(ls_annotations: list[Example]) -> Upsert:
    # TODO: should we add update logic here?
    return Upsert(new_examples=ls_annotations)


async def main() -> None:
    """
    This script will export all annotations from Label Studio and upsert them into a Slingshot dataset artifact with the
    tag specified under `DATASET_TAG`.
    """
    ls_client = label_studio_sdk.Client()
    ls_annotations = get_label_studio_annotations(ls_client)
    print(f"Found {len(ls_annotations)} examples with annotations in Label Studio")
    upsert = create_upsert(ls_annotations)
    sdk = SlingshotSDK()
    await sdk.setup()
    await sdk.upsert_dataset_artifact(upsert, dataset_tag=DATASET_TAG)


if __name__ == "__main__":
    assert "LABEL_STUDIO_API_KEY" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_API_KEY'"
    assert "LABEL_STUDIO_URL" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_URL'"
    asyncio.run(main())
