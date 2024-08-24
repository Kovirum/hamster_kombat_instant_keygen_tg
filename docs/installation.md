# Installation Guide

This guide provides step-by-step instructions on how to install and set up the Hamster Kombat Key Generator and Telegram bot.

## Requirements

- **Python 3.11+**
- **MongoDB instance**
- **Required Python packages** (listed in `requirements.txt`)

## Installation Steps


1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Kovirum/hamster_kombat_instant_keygen_tg.git
    cd repo
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables:**\
    Create a `.env` file in the root directory with the following content:
    ```plaintext
    BOT_TOKEN=your-telegram-bot-token
    DB_URL=your-mongodb-url
    ```

4. **Configure the Startup Method:**\
    Edit the `config.py` file to set the `STARTUP_METHOD` based on your needs:
    - `KeygenAndBot = 0`: Run both the key generator and Telegram bot.
    - `OnlyKeygen = 1`: Run only the key generator.
    - `OnlyBot = 2`: Run only the Telegram bot.

5. **Set up a subscription channel:**
   In the `SUBSCRIBE_REQUIRED_CHANNEL_LIST` you must specify a list of objects of the following type:
   ```json
   {
      "name": "channel name",
      "id": -100123456789,
      "invite_link": "channel invite link" 
   }
   ```
   You can also leave this list empty. In this case, subscription verification will be disabled and the bot will be available without restrictions.\
   You can read get details here: [Set up a subscription channel](configuration.md#set-up-a-subscription-channel)
6. **Running the Application:**
    ```bash
    python main.py
    ```
