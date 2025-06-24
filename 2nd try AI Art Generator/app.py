# Import necessary Flask modules and other libraries
import os
import uuid
import datetime # Import datetime for timestamps
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from PIL import Image, ImageEnhance, ImageFilter, ImageOps # Import ImageOps
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Define directories for storing uploaded and generated images
# Create these directories if they don't exist
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Configure the upload folder for Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# --- Global list to hold metadata of generated artworks ---
# IMPORTANT: Data stored here is IN-MEMORY and will be lost when the server restarts.
# For persistent storage, a database (e.g., Firestore) is required.
generated_artworks_metadata = []

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def apply_style_transfer_simulation(content_image_path, style_choice, custom_style_image_path=None):
    """
    Simulates style transfer using PIL (Pillow) library.
    In a real AI art generator, this function would integrate with
    a deep learning model (e.g., based on Neural Style Transfer).

    For demonstration, it applies different image manipulations based on
    the chosen style or attempts a simple blend with a custom style image.

    Args:
        content_image_path (str): Path to the user's uploaded content image.
        style_choice (str): The name of the pre-defined style chosen by the user.
        custom_style_image_path (str, optional): Path to a user-uploaded style image.
                                                 Defaults to None.

    Returns:
        tuple: (str, str) - Path to the generated stylized image and its filename,
              or (None, None) if an error occurs.
    """
    try:
        content_img = Image.open(content_image_path).convert("RGB")
        # Apply EXIF orientation
        content_img = ImageOps.exif_transpose(content_img)

        output_filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)

        if style_choice == 'abstract_lines':
            # Apply a mosaic/pixelation and then sharpen to simulate abstract lines
            img = content_img.resize((content_img.width // 10, content_img.height // 10), Image.NEAREST)
            img = img.resize(content_img.size, Image.NEAREST)
            enhancer = ImageEnhance.Sharpness(img)
            stylized_img = enhancer.enhance(2.0)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(1.5)
        elif style_choice == 'watercolor':
            # Apply a light blur and then enhance colors to mimic watercolor
            img = content_img.filter(ImageFilter.BoxBlur(radius=2))
            enhancer = ImageEnhance.Color(img)
            stylized_img = enhancer.enhance(1.8)
            stylized_img = ImageEnhance.Brightness(stylized_img).enhance(1.1)
        elif style_choice == 'oil_painting':
            # Apply a strong blur and enhance contrast to simulate oil painting texture
            img = content_img.filter(ImageFilter.BoxBlur(radius=3))
            stylized_img = img.filter(ImageFilter.FIND_EDGES) # Find edges to give a painterly feel
            stylized_img = Image.blend(content_img, stylized_img.convert("RGB"), alpha=0.5)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(1.8)
        elif style_choice == 'sketch':
            # Convert to grayscale, invert, and apply an edge detection filter
            img_gray = content_img.convert("L") # L for grayscale
            img_inverted = ImageEnhance.Brightness(img_gray).enhance(0.5).point(lambda x: 255 - x) # Invert and darken
            stylized_img = img_inverted.filter(ImageFilter.FIND_EDGES)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(2.0)
        elif style_choice == 'picasso_cubist':
            # Simulate cubist style: pixelate, then create strong edges and geometric distortion
            img = content_img.resize((content_img.width // 8, content_img.height // 8), Image.NEAREST)
            img = img.resize(content_img.size, Image.NEAREST)
            edges = img.filter(ImageFilter.FIND_EDGES)
            stylized_img = Image.blend(img, edges.convert("RGB"), alpha=0.3)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(1.5)
            stylized_img = ImageEnhance.Color(stylized_img).enhance(1.2)
        elif style_choice == 'dali_surreal':
            # Simulate surrealism: apply distortions, color shifts, and blur
            img = content_img.filter(ImageFilter.GaussianBlur(radius=5)) # Dreamy blur
            img_np = np.array(img)
            # Simple color shift (e.g., slightly tinting)
            img_np[:, :, 0] = np.clip(img_np[:, :, 0] * 1.1, 0, 255) # Red channel
            img_np[:, :, 1] = np.clip(img_np[:, :, 1] * 0.9, 0, 255) # Green channel
            stylized_img = Image.fromarray(img_np.astype(np.uint8))
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(1.2)
        elif style_choice == 'gaudi_gothic':
            # Simulate Gaudi's style: strong contrast, architectural lines, and mosaic-like texture
            img = content_img.filter(ImageFilter.DETAIL) # Enhance details and edges
            img = img.filter(ImageFilter.SHARPEN)
            # Create a mosaic effect
            img_mosaic = img.resize((content_img.width // 15, content_img.height // 15), Image.NEAREST)
            img_mosaic = img_mosaic.resize(content_img.size, Image.NEAREST)
            stylized_img = Image.blend(img, img_mosaic, alpha=0.2)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(2.0)
            stylized_img = ImageEnhance.Color(stylized_img).enhance(1.3)
        elif style_choice == 'custom' and custom_style_image_path:
            # Simple blending with custom style image (very basic simulation)
            custom_style_img = Image.open(custom_style_image_path).convert("RGB")
            # Resize style image to match content image dimensions
            custom_style_img = custom_style_img.resize(content_img.size)

            # A very simple blend: weighted average of pixel values
            # This is NOT real style transfer, but demonstrates the concept of using a style image
            stylized_img = Image.blend(content_img, custom_style_img, alpha=0.3)
        else:
            # Default to original if no valid style or custom image specified
            stylized_img = content_img

        stylized_img.save(output_path)
        return output_path, output_filename # Return both path and filename for metadata

    except Exception as e:
        print(f"Error during style transfer simulation: {e}")
        return None, None

@app.route('/')
def index():
    """
    Renders the main page for image upload and style selection.
    """
    return render_template('index.html', generated_image=None)

@app.route('/process', methods=['POST'])
def process_image():
    """
    Handles the image upload and triggers the style transfer simulation.
    """
    content_file = request.files.get('content_image')
    style_choice = request.form.get('style_choice')
    custom_style_file = request.files.get('custom_style_image')

    if not content_file or not allowed_file(content_file.filename):
        return render_template('index.html', error="Please upload a valid content image (PNG, JPG, JPEG, GIF).")

    content_filename = f"{uuid.uuid4()}_{content_file.filename}"
    content_filepath = os.path.join(app.config['UPLOAD_FOLDER'], content_filename)
    content_file.save(content_filepath)

    custom_style_filepath = None
    if custom_style_file and allowed_file(custom_style_file.filename):
        custom_style_filename = f"{uuid.uuid4()}_{custom_style_file.filename}"
        custom_style_filepath = os.path.join(app.config['UPLOAD_FOLDER'], custom_style_filename)
        custom_style_file.save(custom_style_filepath)
        style_choice = 'custom' # Force style to 'custom' if a custom image is provided

    # Simulate style transfer
    generated_image_path, generated_image_filename = apply_style_transfer_simulation(
        content_filepath,
        style_choice,
        custom_style_filepath
    )

    if generated_image_path:
        # --- Store artwork metadata in the global list ---
        artwork_id = str(uuid.uuid4()) # Unique ID for this specific artwork generation
        # For user_id, since there's no authentication, we'll use a placeholder or assign one randomly
        # In a real app, this would come from the authenticated user session.
        user_id = "anonymous_user_" + str(uuid.uuid4())[:8] # Simple placeholder user ID

        artwork_metadata = {
            "artwork_id": artwork_id,
            "generated_image_path": generated_image_path,
            "generated_image_filename": generated_image_filename,
            "original_image_path": content_filepath,
            "original_image_filename": content_filename,
            "style_applied": style_choice,
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "title": f"Art - {style_choice.replace('_', ' ').title()}", # Simple title based on style
            "is_public": False # Default to private, can be changed with UI
        }
        generated_artworks_metadata.append(artwork_metadata)
        print(f"Stored artwork metadata: {artwork_metadata}")
        print(f"Total artworks in memory: {len(generated_artworks_metadata)}")
        # --- End of storing metadata ---

        return render_template('index.html', generated_image=generated_image_filename)
    else:
        return render_template('index.html', error="Failed to process image. Please try again.")

@app.route('/download/<filename>')
def download_file(filename):
    """
    Allows users to download the generated image.
    """
    return send_from_directory(app.config['GENERATED_FOLDER'], filename, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serves uploaded content/style images (for display if needed, though not directly used in this demo's UI).
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/generated/<filename>')
def generated_file(filename):
    """
    Serves the generated image for display on the webpage.
    """
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)

# Optional: A route to view the in-memory metadata (for testing/debugging)
@app.route('/view_metadata')
def view_metadata():
    """
    Displays the current in-memory artwork metadata.
    NOTE: This is for demonstration only and not for production.
    """
    metadata_display = ""
    if generated_artworks_metadata:
        for i, artwork in enumerate(generated_artworks_metadata):
            metadata_display += f"--- Artwork {i+1} ---\n"
            for key, value in artwork.items():
                metadata_display += f"{key}: {value}\n"
            metadata_display += "\n"
    else:
        metadata_display = "No artworks generated yet."

    return render_template('metadata_viewer.html', metadata=metadata_display)

if __name__ == '__main__':
    # Run the Flask app in debug mode.
    # In a production environment, use a production-ready WSGI server like Gunicorn or uWSGI.
    app.run(debug=True)
