def get_welcome_message():
    # Ask for the user's name
    name = input("What's your name? ")
    
    # Create a personalized welcome message
    welcome_message = f"""
    ╔══════════════════════════════════════╗
    ║                                      ║
    ║    Welcome to the Hello World App!   ║
    ║                                      ║
    ║    Hello, {name}!                    ║
    ║    We're glad to have you here!      ║
    ║                                      ║
    ╚══════════════════════════════════════╝
    """
    return welcome_message

if __name__ == "__main__":
    print(get_welcome_message()) +