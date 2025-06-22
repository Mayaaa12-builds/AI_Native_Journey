import os
import sys
from typing import Optional, Tuple
from datetime import datetime
from PIL import Image # Pillow library for image manipulation

# --- 1. get_user_images_and_style Function ---
def get_user_images_and_style(
    content_image_path: str,
    style_choice: str,
    user_style_image_path: Optional[str] = None
) -> Tuple[str, str]:
    """
    Simulates the 'Image Upload and Style Selection' step for an AI Art Generator.

    Args:
        content_image_path (str): The file path for the 'content image'.
        style_choice (str): The choice for the style, either a curated style name
                            or "user_upload".
        user_style_image_path (Optional[str]): The optional file path for a
                                                 user-provided style image.

    Returns:
        Tuple[str, str]: A tuple containing the absolute paths to the
                         content image and the chosen style image.

    Raises:
        FileNotFoundError: If any required image file does not exist.
        ValueError: If an invalid style choice is made or a user upload path
                    is missing when "user_upload" is chosen.
    """
    # Define predefined curated style images and their hypothetical paths
    # In a real application, these paths would point to actual image files.
    CURATED_STYLES = {
        "Starry Night": os.path.join("styles", "starry_night.jpg"),
        "The Scream": os.path.join("styles", "the_scream.jpg"),
        "Watercolor Abstract": os.path.join("styles", "watercolor_abstract.jpg"),
        "Cubist Portrait": os.path.join("styles", "cubist_portrait.jpg"),
        # Add more curated styles as desired
    }

    # Ensure styles directory exists for this example (optional for function logic)
    if not os.path.exists("styles"):
        print("Note: 'styles/' directory not found. Please create it and add dummy image files for curated styles.", file=sys.stderr)
        # For a truly robust example, you might want to create dummy files here or raise an error.
        # For now, we'll let os.path.exists() handle the check later.

    # 1. Validate content_image_path
    abs_content_path = os.path.abspath(content_image_path)
    if not os.path.exists(abs_content_path):
        raise FileNotFoundError(f"Content image not found at: {abs_content_path}")

    selected_style_path: str

    # 2. Determine style_image_path based on style_choice
    if style_choice == "user_upload":
        if user_style_image_path is None:
            raise ValueError("For 'user_upload' style_choice, 'user_style_image_path' must be provided.")
        
        abs_user_style_path = os.path.abspath(user_style_image_path)
        if not os.path.exists(abs_user_style_path):
            raise FileNotFoundError(f"User-provided style image not found at: {abs_user_style_path}")
        selected_style_path = abs_user_style_path
    else:
        if style_choice not in CURATED_STYLES:
            available_styles = ", ".join(CURATED_STYLES.keys())
            raise ValueError(f"Invalid style choice: '{style_choice}'. Available choices: {available_styles} or 'user_upload'.")
        
        relative_curated_path = CURATED_STYLES[style_choice]
        abs_curated_path = os.path.abspath(relative_curated_path)
        if not os.path.exists(abs_curated_path):
            # This check is crucial even for curated styles, as the developer might misconfigure
            raise FileNotFoundError(f"Curated style image not found at: {abs_curated_path}. Please ensure it exists.")
        selected_style_path = abs_curated_path

    return abs_content_path, selected_style_path

# --- 2. apply_style_transfer_and_save Function ---
def apply_style_transfer_and_save(
    content_image_path: str,
    style_image_path: str
) -> str:
    """
    Performs the core AI style transfer processing (simulated) and saves the output.

    Args:
        content_image_path (str): Absolute path to the content image.
        style_image_path (str): Absolute path to the style image.

    Returns:
        str: Absolute file path to the saved stylized image.
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    try:
        content_img = Image.open(content_image_path).convert("RGB")
        style_img = Image.open(style_image_path).convert("RGB")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error opening image for style transfer: {e}")
    except Exception as e:
        raise IOError(f"Could not open or process image files: {e}")

    # --- AI Backend Integration: Placeholder for Real Style Transfer Model ---
    # This is the crucial part where your actual AI model would be integrated.
    # For this mini-project simulation, we'll perform a simple image manipulation
    # to represent the 'stylized' output.
    #
    # In a real scenario, you would:
    # 1. Load your pre-trained Neural Style Transfer model (e.g., using TensorFlow, PyTorch).
    # 2. Preprocess content_img and style_img for your model's input.
    # 3. Run the inference: stylized_image = model.transfer_style(content_img, style_img).
    # 4. Post-process the output to convert it back to a PIL Image or NumPy array.
    print("\n--- Performing (Simulated) AI Style Transfer ---")
    print(f"Applying style from '{os.path.basename(style_image_path)}' to '{os.path.basename(content_image_path)}'...")

    # SIMULATION: A basic blending of the two images
    # Resize style image to match content image dimensions for blending
    style_img_resized = style_img.resize(content_img.size)

    # Perform a simple alpha blend (e.g., 70% content, 30% style)
    # This provides a basic visual transformation without complex AI.
    stylized_img = Image.blend(content_img, style_img_resized, alpha=0.3) 
    
    print("Style transfer simulation complete!")
    # --- END AI Placeholder ---

    # Generate a unique output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_content_name = os.path.splitext(os.path.basename(content_image_path))[0]
    base_style_name = os.path.splitext(os.path.basename(style_image_path))[0]
    output_filename = f"{base_content_name}_styled_with_{base_style_name}_{timestamp}.png"
    output_path = os.path.join(output_dir, output_filename)
    abs_output_path = os.path.abspath(output_path)

    # Save the generated stylized image
    stylized_img.save(abs_output_path)
    print(f"Stylized image saved to: {abs_output_path}")

    return abs_output_path

# --- Main Execution Block for User Interaction ---
if __name__ == "__main__":
    print("Welcome to the AI Art Generator!")
    print("---------------------------------")

    # --- Setup for demonstration (create dummy files/dirs if not exist) ---
    if not os.path.exists("styles"):
        os.makedirs("styles")
        print("Created 'styles/' directory. Please place dummy style images there for testing.")
        # Create a tiny dummy image for basic testing if styles dir is empty
        try:
            dummy_style_img = Image.new('RGB', (100, 100), color = 'red')
            dummy_style_img.save(os.path.join("styles", "starry_night.jpg"))
            print("Created dummy 'starry_night.jpg' in 'styles/' for testing.")
        except Exception as e:
            print(f"Could not create dummy style image: {e}")
            pass # Continue without dummy if fails

    if not os.path.exists("user_photos"):
        os.makedirs("user_photos")
        print("Created 'user_photos/' directory. Place your content images here.")
        # Create a tiny dummy image for basic testing if photos dir is empty
        try:
            dummy_content_img = Image.new('RGB', (200, 200), color = 'blue')
            dummy_content_img.save(os.path.join("user_photos", "my_pic.jpg"))
            print("Created dummy 'my_pic.jpg' in 'user_photos/' for testing.")
        except Exception as e:
            print(f"Could not create dummy content image: {e}")
            pass # Continue without dummy if fails

    if not os.path.exists("output"):
        os.makedirs("output")
        print("Created 'output/' directory for generated art.")
    # --- End Setup ---

    # --- Simulate User Input for Content Image ---
    # Targeting Casual Creatives: Keep prompts simple and guide them.
    content_input_path = input("Enter the path to your content image (e.g., user_photos/my_pic.jpg): ")
    
    # --- Simulate User Input for Style Selection ---
    print("\n--- Choose Your Art Style ---")
    print("Available Curated Styles:")
    # Use the keys from your CURATED_STYLES dictionary directly for display
    # This avoids the complex type hint introspection that caused the AttributeError
    curated_style_names_display = list(CURATED_STYLES.keys())
    for i, style_name in enumerate(curated_style_names_display):
    print(f"   {i+1}. {style_name}")
    print("   Or type 'user_upload' to use your own style image.")

    style_choice_input = input("Enter your choice (e.g., 'Starry Night' or 'user_upload'): ").strip()

    user_style_path_input = None
    if style_choice_input.lower() == "user_upload":
        user_style_path_input = input("Enter the path to your custom style image (e.g., styles/my_custom_style.jpg): ").strip()

    # --- Integrate and Run the Functions ---
    try:
        # Step 1: Get validated image paths
        print("\n--- Validating Image Selection ---")
        content_img_abs_path, style_img_abs_path = get_user_images_and_style(
            content_image_path=content_input_path,
            style_choice=style_choice_input,
            user_style_image_path=user_style_path_input
        )
        print("Image selection validated successfully!")
        print(f"Content Image: {content_img_abs_path}")
        print(f"Style Image: {style_img_abs_path}")

        # Step 2: Apply style transfer and save
        stylized_image_output_path = apply_style_transfer_and_save(
            content_image_path=content_img_abs_path,
            style_image_path=style_img_abs_path
        )

        # --- Output and Download/Share Information ---
        # Targeting Casual Creatives: Provide clear outcome and next steps.
        print("\n---------------------------------")
        print("AI Art Generation Complete!")
        print(f"Your unique artwork is saved at: \n{stylized_image_output_path}")
        print("\nYou can now open this file to view your art!")
        print("To 'share' your art, simply upload this image file to your favorite social media platform.")
        print("---------------------------------")

    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("Please check your input paths and try again.", file=sys.stderr)
    except Exception as e:
    print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    print("Please contact support if the issue persists.", file=sys.stderr)
        