import os

import uuid
import requests
from dotenv import load_dotenv

load_dotenv()


class AZTranslator:
    def __init__(self, api_key, api_endpoint, az_location) -> None:
        self._api_key      = api_key
        self._api_endpoint = api_endpoint
        self._az_location  = az_location

    def translate(self, text: str, to: str = "ar") -> str:
        """
        Translate a text to the specified language.

        :param text: The text to translate.
        :param to: The language to translate to (default: "ar").
        :return: The translated text.
        """
        url = f"{self._api_endpoint}/translate"

        # Input validation
        if not text:
            raise ValueError("Text to translate is empty.")

        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': [to]
        }

        headers = {
            'Ocp-Apim-Subscription-Key':    self._api_key,
            'Ocp-Apim-Subscription-Region': self._az_location,
            'Content-type':                 'application/json',
            'X-ClientTraceId':              str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        try:
            request = requests.post(
                url, params=params, headers=headers, json=body)
            request.raise_for_status()  # Raise an exception for HTTP errors

            response = request.json()
            translated_text = response[0]["translations"][0]["text"]

            return translated_text
        except requests.exceptions.RequestException as e:
            # Handle network or API errors
            # You can log the error and re-raise or return a custom error message
            raise Exception(f"Translation failed: {str(e)}")


if __name__ == "__main__":
    translated_text = AZTranslator(
        api_key      = os.getenv("AZ_TRANSLATOR_KEY"),
        api_endpoint = os.getenv("AZ_TRANSLATOR_TEXT_TRANSLATION_ENDPOINT"),
        az_location  = os.getenv("AZ_TRANSLATOR_LOCATION")
    ).translate("I would really like to drive your car around the block a few times!")
    print(translated_text)
