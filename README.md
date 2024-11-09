# EchoBot

Bot Framework v4 echo bot sample.

This bot has been created using [Bot Framework](https://dev.botframework.com), it shows how to create a simple bot that accepts input from the user and echoes it back.

## To try this sample

- Clone the repository
```bash
git clone https://github.com/Microsoft/botbuilder-samples.git
```
- In a terminal, navigate to `botbuilder-samples\samples\python\02.echo-bot` folder
- Activate your desired virtual environment
- In the terminal, type `pip install -r requirements.txt`
- Run your bot with `python app.py`

## Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the latest Bot Framework Emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- File -> Open Bot
- Enter a Bot URL of `http://localhost:3978/api/messages`

## Interacting with the bot

Enter text in the emulator.  The text will be echoed back by the bot.

## Deploy the bot to Azure

To learn more about deploying a bot to Azure, see [Deploy your bot to Azure](https://aka.ms/azuredeployment) for a complete list of deployment instructions.

## Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
- [Azure Portal](https://portal.azure.com)
- [Channels and Bot Connector Service](https://docs.microsoft.com/en-us/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)

# Echo Bot with Sentiment Analysis

This project is an enhanced version of the basic Echo Bot created in Python. The bot now includes functionality to process user input through Azure's Sentiment Analysis API and respond based on the sentiment score.

## Project Overview

The bot was initially based on the Echo Bot example from **Topic 5**. This enhanced version processes user messages, performs sentiment analysis on the input text, and provides feedback based on the sentiment score. 

### Key Modifications

1. **Sentiment Analysis Integration**: 
   - A new `TextAnalyticsClient` instance was created in the bot code to connect to Azure's Text Analytics API. 
   - The bot sends user messages to the sentiment analysis API and receives a sentiment score (positive, neutral, or negative).
   - The bot's response changes based on the sentiment:
     - **Positive Sentiment**: The bot provides an enthusiastic response.
     - **Neutral Sentiment**: The bot provides a neutral response.
     - **Negative Sentiment**: The bot provides a supportive, empathetic response.

2. **Environment Variables**:
   - The `ENDPOINT_URI` and `API_KEY` for Azure's Text Analytics API are stored as environment variables to secure sensitive data and avoid hardcoding keys directly in the source code.
   - This setup is configured in the `config.py` file, where the bot retrieves these values using `os.environ.get`.

3. **README.md Documentation**:
   - Initial notes were added here to clarify the source of files and describe the reasons for each modification.

## Files Modified

- **`main.py`**: Added sentiment analysis processing and adapted responses based on sentiment scores.
- **`config.py`**: Updated configuration to include placeholders for `API_KEY` and `ENDPOINT_URI` retrieved through environment variables.
- **`README.md`**: Updated to document the changes made and the setup instructions.

## Setup Instructions

1. **Environment Setup**:
   - Define the environment variables for Azure's Text Analytics API:
     ```bash
     export MicrosoftAPIKey="YOUR_AZURE_API_KEY"
     export MicrosoftAIServiceEndpoint="YOUR_AZURE_ENDPOINT_URI"
     ```

2. **Dependencies**:
   - Install the required packages using pip:
     ```bash
     pip install azure-ai-textanalytics aiohttp botbuilder
     ```

3. **Running the Bot**:
   - Start the bot:
     ```bash
     python main.py
     ```

4. **Testing the Bot**:
   - Use Bot Framework Emulator to connect to `http://localhost:3978/api/messages` and test the sentiment-based responses.

## Additional Notes

- The bot gracefully handles malformed or irrelevant queries by returning a default neutral response.
- Further enhancements may include additional features, such as natural language understanding or expanded sentiment categories.
