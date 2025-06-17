def get_welcome_message():
    """
    Prompts the user for their name and generates a personalized welcome message.

    Returns:
        str: A multi-line string containing the welcome message with the user's name.
    """
    # Ask for the user's name using the input() function.
    # The input() function displays the prompt and waits for the user
    # to type something and press Enter. The entered text is then
    # stored in the 'name' variable.
    name = input("What's your name? ")

    # Create a personalized welcome message using an f-string (formatted string literal).
    # An f-string allows you to embed expressions (like variables) directly
    # inside string literals by placing them inside curly braces {}.
    # The triple quotes """ allow for a multi-line string.
    welcome_message = f"""
╔══════════════════════════════════════╗
║                                      ║
║     Welcome to the Hello World App!  ║
║                                      ║
║     Hello, {name}!                   ║
║     We're glad to have you here!     ║
║                                      ║
╚══════════════════════════════════════╝
    """
    # Return the complete personalized welcome message.
    return welcome_message

# This is a common Python idiom.
# It checks if the script is being run directly by the Python interpreter
# (as opposed to being imported as a module into another script).
# Code inside this block will only execute when the script is run directly.
if __name__ == "__main__":
    # Call the get_welcome_message() function to get the message.
    # The print() function then displays this message in the console.
    print(get_welcome_message())
