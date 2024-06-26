import logging
import os

import dotenv
import requests
from django.http import JsonResponse
from django.shortcuts import render

from .rag_gpt_integration import create_question_answering_chain

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()


def chatbot(request):
    """
    Handle POST requests to interact with the chatbot.

    Args:
    - request (HttpRequest): Request object.

    Returns:
    - JsonResponse: JSON response containing chatbot response.
    """
    if request.method == "POST":
        try:
            # Get user input from front end
            message = request.POST.get("message")
            current_directory = os.getcwd()
            data_source_dir = os.path.join(current_directory, "data_source")

            # Get question and answering chain
            chain = create_question_answering_chain(data_source_dir)
            response_dict = chain(message)

            # Get only response text
            response = response_dict.get("result")
            logging.info({"message": message, "response": response})
            return JsonResponse({"message": message, "response": response})
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error occurred: {e}")
            return JsonResponse(
                {"error": "Network error occurred. Please try again later."}, status=500
            )
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return JsonResponse(
                {"error": "An Error occured. Please try again later."}, status=500
            )
    return render(request, "chatbot.html")
