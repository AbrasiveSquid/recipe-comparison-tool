import os
import resend

def send_feedback(message: str) -> None:
    resend.api_key = os.environ["RESEND_API_KEY"]


    resend.Emails.send({
        "from": "RecipeTools Feedback <feedback@recipetools.app>",
        "to": [os.environ["FEEDBACK_EMAIL"]],
        "subject": "New RecipeTools feedback",
        "text": message,
    })
