import ast
import json
import logging
import os
import pathlib
import re

import requests

logger = logging.getLogger(__name__)


class LLMFunction:
    openai_endpoint = "https://api.openai.com/v1/chat/completions"

    def __init__(
        self,
        model_args: dict,
        function_args: dict,
        template: str,
        system_message: str = None,
        openai_api_key: str = None,
        required: list[str] = None,
    ):
        self.model_args = model_args
        self.function_args = function_args
        self.template = template
        self.system_message = system_message
        self.fields = self._detect_template_fields(self.template)

        if not required:
            self.required = list(self.function_args["properties"].keys())
        else:
            self.required = required
            # check valid here

        if openai_api_key:
            self.openai_api_key = openai_api_key
        else:
            self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not self.openai_api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )

    @classmethod
    def from_dir(
        cls,
        dir_path: str,
        openai_api_key: str = None,
        version: str = None,
    ):
        # Convert string dir_path to pathlib.Path object
        base_path = pathlib.Path(dir_path)
        # Determine the correct sub-directory to use
        if version:
            target_dir = base_path / version
        else:
            default_dir = base_path / "default"
            if default_dir.exists() and default_dir.is_dir():
                target_dir = default_dir
            else:
                target_dir = base_path

        # Verify if target directory exists
        if not target_dir.exists() or not target_dir.is_dir():
            raise FileNotFoundError(
                f"Directory '{target_dir}' does not exist or is not a directory."
            )

        # Load template.txt
        template_path = target_dir / "template.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"File '{template_path}' not found.")

        with open(template_path, "r") as f:
            template = f.read()

        # Load system_message.txt
        system_message_path = target_dir / "system_message.txt"
        if system_message_path.exists():
            with open(system_message_path, "r") as f:
                system_message = f.read()
        else:
            system_message = None

        # Load model_args.json
        model_args_path = target_dir / "function_args.json"
        if not model_args_path.exists():
            raise FileNotFoundError(f"File '{model_args_path}' not found.")

        with open(model_args_path, "r") as f:
            model_args = json.loads(f.read())

        # Load function_args.json
        function_args_path = target_dir / "function_args.json"
        if not function_args_path.exists():
            raise FileNotFoundError(f"File '{function_args_path}' not found.")

        with open(function_args_path, "r") as f:
            function_args = json.loads(f.read())

        return cls(
            openai_api_key=openai_api_key,
            model_args=model_args,
            function_args=function_args,
            template=template,
            system_message=system_message,
        )

    def __call__(self, return_openai_response: bool = False, **kwargs):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
        }
        prompt = self._format_prompt(**kwargs)
        payload = self._get_payload(prompt=prompt)
        response_json = self._fetch_openai_completion(payload=payload, headers=headers)
        prediction = self._parse_completion(response_json=response_json)
        if return_openai_response:
            return prediction, response_json

        return prediction

    def _format_prompt(self, **kwargs) -> str:
        # Check for missing fields
        missing_fields = [field for field in self.fields if field not in kwargs]

        # Raise an error if any fields are missing
        if missing_fields:
            raise ValueError(f"Missing fields: {', '.join(missing_fields)}")

        prompt = self.template.format(**kwargs)
        return prompt

    def _get_payload(self, prompt: str) -> dict:
        function_schema = {
            "name": self.function_args["function_name"],
            "description": self.function_args["description"],
            "parameters": {
                "type": "object",
                "properties": self.function_args["properties"],
                "required": self.function_args["required"],
            },
        }
        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        messages.append({"role": "user", "content": prompt})
        return {
            "model": self.model_args["model"],
            "messages": messages,
            "functions": [function_schema],
            "function_call": {
                "name": self.function_name,
            },
            "temperature": self.model_args["temperature"],
        }

    def _fetch_openai_completion(self, payload: dict, headers: dict) -> dict:
        try:
            response = requests.post(
                self.openai_endpoint, headers=headers, json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error from OpenAI request: {e}")
            return {}

    def _parse_completion(self, response_json: dict) -> dict:
        try:
            choices = response_json.get("choices")
            values = choices[0]["message"]["function_call"].pop("arguments")
            prediction = ast.literal_eval(values)
        except:
            try:
                prediction = json.loads(values)
            except Exception as e:
                logger.error(f"Error evaluating OpenAI JSON output: {e}")
                return None

        return prediction

    @staticmethod
    def _detect_template_fields(template: str) -> list:
        """
        Extracts format fields from a string.
        """
        fields = re.findall(r"\{(.*?)\}", template)
        return fields
