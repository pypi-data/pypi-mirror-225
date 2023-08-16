#  Copyright (c) 2023 Roboto Technologies, Inc.
import textwrap

from ...domain.actions import Action


def finalize_docker_image_registration_instructions(action: Action) -> str:
    # fmt: off
    return textwrap.dedent(f"""\
        If needed, finish registering Docker image with this action by pushing the image to Roboto's private registry:

            1. Tag your locally-built Docker image:
            $ docker tag <existing_image>:<existing_image_tag> {action.uri}

            2. Temporarily login to Roboto's private registry (requires Docker CLI; valid for 12hr):
            $ roboto actions docker-login --org {action.org_id} --name '{action.name}'

            3. Push the Docker image
            $ docker push {action.uri}
    """)
    # fmt: on
