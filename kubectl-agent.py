# Copyright 2025 Vinayak Goyal
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#
# distributed under the License is distributed on an "AS IS" BASIS,
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
#
# limitations under the License.


import logging
import sys
import os
import subprocess
from google import genai
from google.genai import types
from datetime import datetime
from art import tprint


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("kubectl-agent")


def kubectl(command: str) -> dict[str, str]:
    """
    This function executes the given kubectl command and return the result of
    the command including the status_code, stderr and stdout.
    """

    # Some times the model doesn't put kubectl before the command.
    if not command.startswith("kubectl"):
        command = "kubectl " + command

    process_result = subprocess.run(command, shell=True, capture_output=True)

    result = {
        "status_code": process_result.returncode,
        "stderr": process_result.stderr.decode(),
        "stdout": process_result.stdout.decode(),
    }

    return result


def handle_function_call(function_call):
    if function_call.name != "kubectl":
        raise ValueError(f"no function named {function_call.name}")

    return kubectl(**function_call.args)


key = os.getenv("GOOGLE_GENAI_API_KEY")

if key == None or key == "":
    logger.fatal(f"API key is empty!")

client = genai.Client(api_key=key)

system_promot = (
    "You are a kubernetes security expert who is helping the "
    + "user answer questions about the cluster that they are connected to."
    + "When possible run kubectl commands such that they output json data."
)

model_config = types.GenerateContentConfig(
    tools=[
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="kubectl",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={
                            "command": types.Schema(
                                type="STRING",
                                description="The kubectl command to run.",
                            )
                        },
                    ),
                    description="runs a kubectl command and return the result as including the status_code, stderr and stdout.",
                )
            ]
        )
    ],
    automatic_function_calling={"disable": True},
    system_instruction=system_promot,
)

model_name = "gemini-2.0-flash"


def process_user_input(contents, user_input: str):
    user_content = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"Toady is {datetime.now()}. {user_input}"
            )
        ],
    )

    contents.append(user_content)

    response = client.models.generate_content(
        model=model_name, contents=contents, config=model_config
    )

    while response.function_calls:
        contents.append(response.candidates[0].content)
        function_response_parts = []

        for function_call in response.function_calls:
            logger.debug(
                f"model called {function_call.name} with arrgs {function_call.args}"
            )

            api_response = handle_function_call(function_call)
            function_response_parts.append(
                types.Part.from_function_response(
                    name=function_call.name, response={"result": api_response}
                )
            )
        contents.append(
            types.Content(role="tool", parts=function_response_parts)
        )
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=model_config,
        )

    # Display the response from the model to the user.
    print(response.text)
    contents.append(response.candidates[0].content)


def main():
    print(
        """
========================================================================
Copyright 2025 Vinayak Goyal

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
========================================================================
       """
    )

    tprint(text="kubectl agent")

    print(
        'Ask your cluster some questions? E.g. "How many pods are running in the kube-system namespace?"'
    )

    print("Hint: Type // to reset context.")

    contents = []

    while True:
        prompt = input(">>")
        # This lets you clear all previous context.
        if prompt == "//":
            contents.clear()
            print("Removing all previous context.")
        else:
            process_user_input(contents=contents, user_input=prompt)


if __name__ == "__main__":
    main()
