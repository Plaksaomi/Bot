from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Поиск товаров", callback_data='search')],
        [InlineKeyboardButton("Сравнение товаров", callback_data='compare')],
        [InlineKeyboardButton("Купоны", callback_data='coupons')],
        [InlineKeyboardButton("Избранное", callback_data='favorites')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Здравствуйте, чего желаете?', reply_markup=reply_markup)

def show_favorites(update, context):
    favorites = context.user_data.get('favorites', [])
    
    favorites_keyboard = [[InlineKeyboardButton("Добавить товар", callback_data='add_item')],
                          [InlineKeyboardButton("Удалить товар", callback_data='remove_item')],
                          [InlineKeyboardButton("Назад", callback_data='back')]]
    favorites_markup = InlineKeyboardMarkup(favorites_keyboard)
    
    if not favorites:
        if update.message:
            update.message.reply_text('Список избранного пуст.', reply_markup=favorites_markup)
    else:
        if update.message:
            update.message.reply_text('\n'.join(favorites), reply_markup=favorites_markup)

def add_item(update, context, favorites_markup):
    query = update.callback_query
    query.edit_message_text(text='Пришлите ссылку на товар')
    context.user_data['current_action'] = 'add_item'
    context.user_data['favorites_markup'] = favorites_markup
    
def button(update, context):
    query = update.callback_query
    
    if query.data == 'search':
        # Ваше действие при нажатии на кнопку "Поиск товаров"
        pass
    elif query.data == 'compare':
        # Ваше действие при нажатии на кнопку "Сравнение товаров"
        pass
    elif query.data == 'coupons':
        # Ваше действие при нажатии на кнопку "Купоны"
        pass
    elif query.data == 'favorites':
        favorites_keyboard = [[InlineKeyboardButton("Добавить товар", callback_data='add_item')],
                              [InlineKeyboardButton("Удалить товар", callback_data='remove_item')],
                              [InlineKeyboardButton("Назад", callback_data='back')]]
        favorites_markup = InlineKeyboardMarkup(favorites_keyboard)
        
        favorites = context.user_data.get('favorites', [])
        
        if update.message is not None:
            update.message.reply_text('Вы выбрали "Избранное".', reply_markup=favorites_markup)
    elif query.data == 'add_item':
        favorites_markup = context.user_data.get('favorites_markup')
        if favorites_markup is not None:
            add_item(update, context, favorites_markup)
    elif query.data == 'back':
        # Получаем информацию о предыдущем меню
        previous_menu = context.user_data.get('previous_menu', '')
        
        if previous_menu == 'favorites':
            keyboard = [
                [InlineKeyboardButton("Поиск товаров", callback_data='search')],
                [InlineKeyboardButton("Сравнение товаров", callback_data='compare')],
                [InlineKeyboardButton("Купоны", callback_data='coupons')],
                [InlineKeyboardButton("Избранное", callback_data='favorites')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            query.edit_message_text(text='Здравствуйте, чего желаете?', reply_markup=reply_markup)
        
        # Удаляем информацию о предыдущем меню из context.user_data
        if previous_menu:
            del context.user_data['previous_menu']
    
    # Остальной код функции
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Поиск товаров", callback_data='search')],
        [InlineKeyboardButton("Сравнение товаров", callback_data='compare')],
        [InlineKeyboardButton("Купоны", callback_data='coupons')],
        [InlineKeyboardButton("Избранное", callback_data='favorites')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Здравствуйте, чего желаете?', reply_markup=reply_markup)

def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text(['Избранное', 'избранное']), show_favorites))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_item, pattern='^add_item$'))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()