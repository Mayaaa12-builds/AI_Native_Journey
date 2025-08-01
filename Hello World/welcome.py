import datetime

def get_welcome_message():
    """
    Prompts the user for their name and generates a personalized welcome message.
    Provides a time-based greeting with a smiley emoji.
    Special greeting for Sumaya.
    """
    name = input("What's your name? ").strip()

    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 5 <= hour < 12:
        time_greeting = "Good morning"
        emoji = "😊"
    elif 12 <= hour < 18:
        time_greeting = "Good afternoon"
        emoji = "☀️"
    else:
        time_greeting = "Good evening"
        emoji = "🌙"

    if name.lower() == "sumaya":
        welcome_message = (
            f"{time_greeting}, {name}! {emoji}\n"
            "Hey, it's the awesome AI Director, Sumaya!\n"
            "We're honored to have you here!"
        )
    else:
        welcome_message = f"{time_greeting}, {name}! {emoji}\nWe're glad to have you here!"

    return welcome_message

# This is a common Python idiom.
# It checks if the script is being run directly by the Python interpreter
# (as opposed to being imported as a module into another script).
# Code inside this block will only execute when the script is run directly.
if __name__ == "__main__":
    # Call the get_welcome_message() function to get the message.
    # The print() function then displays this message in the console.
    print(get_welcome_message())
