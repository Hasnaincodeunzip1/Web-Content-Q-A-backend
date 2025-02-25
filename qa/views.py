import os
import requests
# from bs4 import BeautifulSoup  # No longer needed directly if using trafilatura
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from .serializers import QuestionSerializer
from dotenv import load_dotenv
import trafilatura  # Import trafilatura

load_dotenv()  # Load environment variables from .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('models/gemini-1.5-flash-8b-latest')

class AnswerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            urls = serializer.validated_data['urls']
            question = serializer.validated_data['question']

            combined_text = ""
            for url in urls:
                try:
                    # No need for requests.get() and BeautifulSoup directly
                    downloaded = trafilatura.fetch_url(url)  # Fetch using trafilatura
                    if downloaded:
                        extracted_text = trafilatura.extract(downloaded, favor_recall=True)
                        if extracted_text:  # Check if extraction was successful
                            combined_text += extracted_text + "\n"
                        else:
                            # Handle cases where trafilatura extracted *nothing*
                            return Response({"error": f"Could not extract content from URL {url}"}, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        # Handle cases where trafilatura couldn't even fetch the URL
                        return Response({"error": f"Could not fetch URL {url}"}, status=status.HTTP_400_BAD_REQUEST)



                except requests.RequestException as e:  # You might still catch requests errors
                    return Response({"error": f"Error fetching URL {url}: {e}"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e: #Catching for errors realted to trafilatura
                    return Response({"error": f"Error extracting content from URL {url}: {e}"}, status=status.HTTP_400_BAD_REQUEST)

            if not combined_text:
                return Response({"error": "No content extracted from URLs."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                prompt = f"Context:\n{combined_text}\n\nQuestion:\n{question}\n\nAnswer concisely, using ONLY the provided context:"
                response = model.generate_content(prompt)
                answer = response.text
                return Response({"answer": answer})
            except Exception as e:
                return Response({"error": f"Gemini API error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)