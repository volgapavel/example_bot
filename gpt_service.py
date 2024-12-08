import json
import asyncio
import logging
from typing import Optional
from openai import OpenAI, APIError, RateLimitError
from config import OPENAI_API_KEY, GPT_MODEL

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key is not set")
            raise ValueError("OpenAI API key is not set!")
            
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            # Test the client with a simple completion
            self._test_client_connection()
            logger.info("OpenAI client initialized and tested successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}", exc_info=True)
            raise

    def _test_client_connection(self) -> None:
        """Test the OpenAI client connection with a simple completion."""
        try:
            self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
        except Exception as e:
            logger.error("Failed to test OpenAI client connection", exc_info=True)
            raise

    async def get_place_information(self, place_prompt: str, user_question: str) -> str:
        """
        Generate a response about a place using OpenAI's GPT model.
        
        Args:
            place_prompt: Detailed information about the place
            user_question: The user's specific question about the place
            
        Returns:
            str: The generated response or an error message
        """
        if not place_prompt or not user_question:
            logger.error("Missing required parameters")
            return "I'm sorry, but I'm missing some information. Please try again."

        try:
            logger.info(f"Generating response for question: {user_question[:50]}...")
            logger.debug(f"Place prompt (truncated): {place_prompt[:100]}...")
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a knowledgeable tour guide specialized in providing detailed information "
                            "about specific locations. Your goal is to give informative, accurate, and engaging "
                            "responses. Use Telegram markdown for formatting where appropriate.\n\n"
                            f"Location Details: {place_prompt}\n\n"
                            "Focus on answering the specific question while incorporating relevant details "
                            "from the location information provided. Keep responses concise but informative. "
                            "Limit responses to 2-3 paragraphs maximum."
                        )
                    },
                    {"role": "user", "content": user_question}
                ],
                max_tokens=500,
                temperature=0.7,  # Add some creativity while keeping responses focused
                presence_penalty=0.6  # Encourage diverse information
            )
            
            logger.debug("Response received from OpenAI")
            response_text = response.choices[0].message.content.strip()
            
            if not response_text:
                logger.warning("Empty response received from OpenAI")
                return "I apologize, but I couldn't generate a proper response. Please try asking your question differently."
            
            logger.info("Successfully generated response")
            return response_text
            
        except RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            return "I'm receiving too many requests right now. Please try again in a few moments."
            
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            return "I'm having trouble connecting to my knowledge base. Please try again later."
            
        except Exception as e:
            logger.error(f"Unexpected error in get_place_information: {str(e)}", exc_info=True)
            return "I apologize, but I encountered an unexpected error. Please try again later."
