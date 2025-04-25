from typing import Dict, List, Optional
import openai

class PromptTemplate:
    def __init__(self, system: str, user: str):
        """Initialize a prompt template with system and user messages."""
        self.system = system
        self.user = user

    def build_messages(self, variables: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """Build the messages list, optionally replacing variables in the template."""
        system_content = self.system
        user_content = self.user

        if variables:
            system_content = system_content.format(**variables)
            user_content = user_content.format(**variables)

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

class OpenAIAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """Initialize the OpenAI analyzer with API key and model."""
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Parse the response text into a dictionary of key-value pairs."""
        result = {}
        lines = response_text.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
        
        return result

    def ask(self, messages: List[Dict[str, str]]) -> Dict[str, str]:
        """Send messages to OpenAI and parse the response."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            
            response_text = response["choices"][0]["message"]["content"].strip()
            return self._parse_response(response_text)
            
        except Exception as e:
            print(f"⚠️ OpenAI API Error: {e}")
            return {"ERROR": str(e)}

    def ask_with_template(self, template: PromptTemplate, variables: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Send messages using a template and optional variables."""
        messages = template.build_messages(variables)
        return self.ask(messages) 