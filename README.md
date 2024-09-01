# Hamster Kombat Key Generator

Hamster Kombat Key Generator is a powerful tool designed to instantly generate and distribute game keys through a Telegram bot. It is comprised of two main components: the key generator and a Telegram bot built with aiogram v3. Both components can operate independently or together, offering a seamless and time-saving experience for users.

## Key Features

- **Multilingual Support:** The bot is translated into 18 languages, making it accessible to a global audience.
- **Game Support:** All current Hamster Kombat games are supported, all new games will be added as they are released as soon as possible
- **Simple and Functional Interface:** Easy to use and configure.
- **Proxy Support:** The key generator supports proxy configuration.
- **Lightweight:** Low system requirements, ensuring smooth operation even on modest hardware.
- **Community grow methods:** The bot offers various tools to increase the number of subscribers for you and your partners.

## Installation and Setup

### Requirements

- Python 3.11+
- MongoDB instance
- Required Python packages (see `requirements.txt`)

### Quick Start

1. Clone the repository:
    ```bash
    git clone https://github.com/Kovirum/hamster_kombat_instant_keygen_tg.git
    cd repo
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure environment variables:
    Create a `.env` file in the root directory with the following content:
    ```plaintext
    BOT_TOKEN=your-telegram-bot-token
    DB_URL=your-mongodb-url
    ```

4. Set the startup method in `config.py`:
    ```py
   STARTUP_METHOD = StartupMethods.KeygenAndBot # Run both the key generator and the Telegram bot
   ```
   ```py
   STARTUP_METHOD = StartupMethods.OnlyKeygen   # Run only the key generator
   ```
   ```py
   STARTUP_METHOD = StartupMethods.OnlyBot      # Run only the Telegram bot
   ```

5. Run the application:
    ```bash
    python main.py
    ```

## Documentation

Complete documentation is available in the [`/docs`](./docs/README.md) directory.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.

## Contributions

Contributions are welcome! Please see the [contributing guide](./docs/contributing.md) for more information.
