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
   - In `SUBSCRIBE_REQUIRED_CHANNEL_ID` , you need to specify the ID of the channel that people will need to subscribe to in order to use the bot. You can set this value to `None` to cancel this requirement.
   > **Warning:**
   > If you specify a value other than `None` as the `SUBSCRIBE_REQUIRED_CHANNEL_ID`, you must invite the bot to the specified channel as an administrator. Otherwise, the subscription verification will always fail.
   - In `SUBSCRIBE_REQUIRED_CHANNEL_INVITE_LINK` you need to specify a link to the channel you want to subscribe to. This value will be assigned to the url of the subscribe channel button.  

6. **Running the Application:**
    ```bash
    python main.py
    ```
