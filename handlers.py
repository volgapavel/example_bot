import logging
from aiogram import types
from sqlalchemy.orm import Session
from models import Place, UserDialog
from keyboards import get_main_keyboard, create_places_keyboard
from gpt_service import GPTService

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self, db: Session, gpt_service: GPTService):
        self.db = db
        self.gpt_service = gpt_service

    async def start_command(self, message: types.Message):
        await message.answer(
            "Welcome! I can help you discover interesting places. "
            "Use the buttons below to get started:",
            reply_markup=get_main_keyboard()
        )

    async def handle_places_button(self, message: types.Message):
        try:
            places = self.db.query(Place).all()
            if not places:
                await message.reply(
                    "Sorry, there are no places available at the moment. "
                    "Please try again later."
                )
                return
            await message.reply(
                "Here are the available places:",
                reply_markup=create_places_keyboard(places)
            )
        except Exception as e:
            logger.error(f"Error handling places button: {str(e)}")
            await message.reply(
                "Sorry, I couldn't retrieve the places list. "
                "Please try again later."
            )

    async def handle_place_selection(self, callback_query: types.CallbackQuery):
        try:
            place_id = int(callback_query.data.split('_')[1])
            place = self.db.query(Place).filter(Place.id == place_id).first()
            
            if place:
                response = (
                    f"📍 {place.name}\n\n"
                    f"{place.description}\n\n"
                    "Feel free to ask me any questions about this place!"
                )
                await callback_query.message.answer(response)
                
                # Save dialog
                user_dialog = UserDialog(
                    user_id=callback_query.from_user.id,
                    message_text=callback_query.data,
                    response_text=response,
                    place_id=place_id
                )
                self.db.add(user_dialog)
                self.db.commit()
            else:
                await callback_query.message.answer(
                    "Sorry, I couldn't find information about this place. "
                    "Please try selecting another place."
                )
        except ValueError as e:
            logger.error(f"Invalid place_id format: {str(e)}")
            await callback_query.message.answer(
                "Sorry, there was an error processing your selection. "
                "Please try again."
            )
        except Exception as e:
            logger.error(f"Error in handle_place_selection: {str(e)}")
            await callback_query.message.answer(
                "An error occurred while processing your request. "
                "Please try again later."
            )

    async def handle_user_question(self, message: types.Message):
        logger.info(f"Handling user question from {message.from_user.id}: {message.text[:50]}...")
        # Find the last place the user was asking about
        try:
            logger.debug("Querying last dialog for user_id: %s", message.from_user.id)
            last_dialog = (
                self.db.query(UserDialog)
                .filter(UserDialog.user_id == message.from_user.id)
                .order_by(UserDialog.timestamp.desc())
                .first()
            )
            logger.info(f"Found last dialog: {last_dialog is not None}")
            if last_dialog:
                logger.debug(f"Last dialog place_id: {last_dialog.place_id}")
        except Exception as e:
            logger.error(f"Error querying last dialog: {str(e)}", exc_info=True)
            await message.reply("Sorry, I encountered an error while processing your request. Please try again.")
        
        if last_dialog and last_dialog.place_id:
            place = self.db.query(Place).filter(Place.id == last_dialog.place_id).first()
            if place:
                response = await self.gpt_service.get_place_information(
                    place.chatgpt_prompt,
                    message.text
                )
                
                # Save dialog
                user_dialog = UserDialog(
                    user_id=message.from_user.id,
                    message_text=message.text,
                    response_text=response,
                    place_id=place.id
                )
                self.db.add(user_dialog)
                self.db.commit()
                
                await message.reply(response)
            else:
                await message.reply(
                    "Sorry, I couldn't find the place you were asking about. "
                    "Please select a place first."
                )
        else:
            await message.reply(
                "Please select a place first using the 'Choose Places' button."
            )
            
    async def handle_location_button(self, message: types.Message):
        await message.reply(
            "This feature will be available soon! For now, you can explore our "
            "places using the 'Choose Places' button."
        )
