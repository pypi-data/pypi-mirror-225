from __future__ import annotations

import asyncio
import os

import label_studio_sdk

from slingshot.schemas import Example

DATASET_MOUNT_PATH = '/mnt/data'


async def import_label_studio_tasks(ls_client: label_studio_sdk.Client, examples: list[Example]) -> list[int]:
    unannotated_examples = [example for example in examples if not example.annotations]
    print(f"Importing {len(unannotated_examples)} unannotated examples")

    tasks = []
    for example in unannotated_examples:
        tasks.append({"data": example.data.model_dump()})

    print(f"Tasks: {tasks}")
    project = ls_client.get_project(id=1)
    task_ids = project.import_tasks(tasks=tasks)
    return task_ids


async def main():
    # Read the dataset from the mounted path and convert it according to your data schema
    # To change your schema, edit the 'label_studio_data_type.py' file
    examples = []
    with open(os.path.join(DATASET_MOUNT_PATH, 'dataset.jsonl'), 'r') as f:
        for line in f:
            if not (line := line.strip()):
                continue
            example = Example.model_validate_json(line)
            examples.append(example)

    ls_client = label_studio_sdk.Client()
    await import_label_studio_tasks(ls_client, examples)


if __name__ == "__main__":
    assert "LABEL_STUDIO_API_KEY" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_API_KEY'"
    assert "LABEL_STUDIO_URL" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_URL'"
    asyncio.run(main())
