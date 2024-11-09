# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from http import HTTPStatus
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import TurnContext
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
#from botbuilder.core import BotFrameworkAuthentication

from bots import EchoBot
from config import DefaultConfig

CONFIG = DefaultConfig()
# Initialize configuration
CONFIG = DefaultConfig()

# Print environment variables for debugging (comment out in production)
print(f"DEBUG - Retrieved API_KEY: {CONFIG.API_KEY}")
print(f"DEBUG - Retrieved ENDPOINT_URI: {CONFIG.ENDPOINT_URI}")

# Create the Text Analytics client
#def authenticate_client():
   # return TextAnalyticsClient(
   #     endpoint=CONFIG.ENDPOINT_URI,
    #    credential=AzureKeyCredential(CONFIG.API_KEY)
 #   )

#client = authenticate_client()

# Initialize Azure Text Analytics Client
text_analytics_client = TextAnalyticsClient(
    endpoint=CONFIG.ENDPOINT_URI,
    credential=AzureKeyCredential(CONFIG.API_KEY)
)

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))
#ADAPTER = CloudAdapter(BotFrameworkAuthentication(CONFIG))
#ADAPTER = CloudAdapter()



# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

# Create the Bot
BOT = EchoBot()

# Sentiment analysis function
async def analyze_sentiment(text: str):
    try:
        response = text_analytics_client.analyze_sentiment([text])[0]
        return response.sentiment  # 'positive', 'neutral', or 'negative'
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return "neutral"  # Default to neutral if an error occurs

async def on_turn_override(turn_context):
    turn_context.activity.caller_id = "local-testing"  # Bypass caller_id for local tests
    await BOT.on_turn(turn_context)

ADAPTER.process_activity = on_turn_override

# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    if "application/json" in req.headers.get("Content-Type", ""):
        body = await req.json()
        
        # Reverse the text in the "text" field if it exists
        if "text" in body:
            body["text"] = body["text"][::-1]
            print(body)
         # Analyze sentiment if the "text" field exists
        if "text" in body:
            text = body["text"]
            sentiment = await analyze_sentiment(text)

            # Prepare response based on sentiment
            if sentiment == "positive":
                response_text = "I'm glad to hear that! 😊"
            elif sentiment == "negative":
                response_text = "I'm here for you. Let me know if there's anything I can do. 😔"
            else:
                response_text = "Thanks for sharing that with me."

            body["text"] = response_text
            print(f"Sentiment: {sentiment} - Response: {response_text}")
        
        # Deserialize the request body into an Activity object

        # Deserialize the body into an Activity
        activity = Activity().deserialize(body)
        auth_header = req.headers.get("Authorization", "")

        # Process the activity and get the response
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=HTTPStatus.OK)
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
