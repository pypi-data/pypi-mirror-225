import ast
import json
import logging
import os
import pathlib
import re

import requests

# Setup logger
logger = logging.getLogger(__name__)


class PromptFunction:
    """
    Represents a function that interfaces with OpenAI's chat completion.
    """

    OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

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
        self.fields = self._detect_template_fields()

        self.function_args["required"] = required or list(
            self.function_args["properties"].keys()
        )
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", None)

        if not self.openai_api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )

    @classmethod
    def from_dir(cls, dir_path: str, openai_api_key: str = None, version: str = None):
        target_dir = cls._determine_target_directory(dir_path, version)

        template = cls._load_file_content(target_dir / "template.txt")
        system_message = cls._load_file_content(
            target_dir / "system_message.txt", required=False
        )
        model_args = json.loads(cls._load_file_content(target_dir / "model_args.json"))
        function_args = json.loads(
            cls._load_file_content(target_dir / "function_args.json")
        )

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
        payload = self._create_payload(prompt)
        response_json = self._fetch_openai_completion(payload, headers)
        prediction = self._extract_prediction_from_response(response_json)

        return (prediction, response_json) if return_openai_response else prediction

    def _format_prompt(self, **kwargs) -> str:
        missing_fields = [field for field in self.fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Missing fields: {', '.join(missing_fields)}")
        return self.template.format(**kwargs)

    def _create_payload(self, prompt: str) -> dict:
        function_schema = self._generate_function_schema()
        messages = self._build_messages(prompt)

        return {
            "model": self.model_args["model"],
            "messages": messages,
            "functions": [function_schema],
            "function_call": {"name": self.function_args["function_name"]},
            "temperature": self.model_args["temperature"],
        }

    def _fetch_openai_completion(self, payload: dict, headers: dict) -> dict:
        try:
            response = requests.post(
                self.OPENAI_ENDPOINT, headers=headers, json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error from OpenAI request: {e}")
            return {}

    def _extract_prediction_from_response(self, response_json: dict) -> dict:
        try:
            choices = response_json.get("choices", [])
            values = choices[0]["message"]["function_call"].pop("arguments", {})
            return ast.literal_eval(values)
        except (ValueError, IndexError, TypeError, KeyError):
            try:
                return json.loads(values)
            except Exception as e:
                logger.error(f"Error evaluating OpenAI JSON output: {e}")
                return None

    def _detect_template_fields(self) -> list:
        return re.findall(r"\{(.*?)\}", self.template)

    @staticmethod
    def _determine_target_directory(dir_path: str, version: str) -> pathlib.Path:
        base_path = pathlib.Path(dir_path)
        if version:
            return base_path / version
        elif (base_path / "default").is_dir():
            return base_path / "default"
        else:
            return base_path

    @staticmethod
    def _load_file_content(file_path: pathlib.Path, required: bool = True) -> str:
        if file_path.exists():
            with open(file_path, "r") as file:
                return file.read()
        elif required:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        else:
            return None

    def _generate_function_schema(self) -> dict:
        return {
            "name": self.function_args["function_name"],
            "description": self.function_args["description"],
            "parameters": {
                "type": "object",
                "properties": self.function_args["properties"],
                "required": self.function_args["required"],
            },
        }

    def _build_messages(self, prompt: str) -> list:
        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        messages.append({"role": "user", "content": prompt})
        return messages
