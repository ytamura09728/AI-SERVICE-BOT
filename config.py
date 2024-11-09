#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "")
    API_KEY = os.environ.get("MicrosoftAPIKey", "7ZATrShKqMKXa4qbka6W5K5JIftrDJkANu5PNRwHDjUb715gbYZ1JQQJ99AKACYeBjFXJ3w3AAAaACOGz4fN")  # Your Azure API Key
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint", "https://ai-lang-service01.cognitiveservices.azure.com/")  # Your Azure Text Analytics endpoint
    #Retrieve API Key and Endpoint URI from environment variables for secure access
    #API_KEY = os.environ.get("MicrosoftAPIKey")
    #ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint")
