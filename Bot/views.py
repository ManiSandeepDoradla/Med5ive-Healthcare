# from django.shortcuts import render
 
# # Create your views here.
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
 
# # import your engine exactly
# from .ChatBot.Engine import get_bot_response
 
 
# @csrf_exempt
# def chatbot_api(request):
#     """
#     Django view that behaves the same as
#     running your chatbot script directly.
#     """
 
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse(
#                 {"reply": "Invalid request format"},
#                 status=400
#             )
 
#         user_message = data.get("message", "").strip()
 
#         if not user_message:
#             return JsonResponse(
#                 {"reply": "Please enter a message"}
#             )
 
#         # 🔹 SAME CALL FLOW AS YOUR ORIGINAL CODE
#         bot_reply = get_bot_response(user_message)
 
#         return JsonResponse(
#             {"reply": bot_reply}
#         )
 
#     # for non-POST requests
#     return JsonResponse(
#         {"reply": "Only POST requests are allowed"},
#         status=405
#     )

from django.shortcuts import render
import json
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .ChatBot.Engine import get_bot_response


@csrf_exempt
def chatbot_api(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Invalid request format"}, status=400)

        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"reply": "Please enter a message"})

        try:
            bot_reply = get_bot_response(user_message)
            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            print("=" * 80)
            print("CHATBOT ERROR")
            traceback.print_exc()
            print("=" * 80)

            return JsonResponse(
                {"reply": f"Server Error: {str(e)}"},
                status=500,
            )

    return JsonResponse({"reply": "Only POST requests are allowed"}, status=405)