# Frequently Asked Questions (FAQ)

## How do I configure the bot?

Configuration is handled via the `config.py` file and `.env` file in the root directory. Refer to the [configuration guide](./configuration.md) for more details.

## How do I add more games?

To add additional games, you need to update config.py by adding a new object to `GAME_PROMO_CONFIGS` and `GamePromoTypes`

## How do I add a new language?

All you need is to add a new JSON with the translated text to `/bot/i18n/locales`. The script will do the rest on its own.

# This list will be updated as new questions become available