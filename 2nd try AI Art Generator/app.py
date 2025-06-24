# Import necessary Flask modules and other libraries
import os
import uuid
import datetime
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import random # For iterative refinement variations
import traceback # Import traceback for detailed error logging

# Initialize the Flask application
app = Flask(__name__)

# Define directories for storing uploaded and generated images
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Limit uploads to 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Global list to hold metadata of generated artworks (in-memory)
generated_artworks_metadata = []

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _apply_single_style_effect(image_obj, style_name, is_refinement=False):
    """
    Applies a single style effect to a PIL Image object.
    Internal helper function for apply_style_transfer_logic.
    Includes minor variations for refinement.
    """
    stylized_img = image_obj.copy()

    # Base parameters that can be varied for refinement
    sharpness_factor = 2.0
    contrast_factor = 1.5
    color_factor = 1.8
    brightness_factor = 1.1
    blur_radius = 2
    pixelate_factor = 10

    if is_refinement:
        # Introduce slight random variations for iterative refinement
        sharpness_factor += random.uniform(-0.3, 0.3)
        contrast_factor += random.uniform(-0.2, 0.2)
        color_factor += random.uniform(-0.2, 0.2)
        brightness_factor += random.uniform(-0.1, 0.1)
        blur_radius += random.uniform(-0.5, 0.5)
        pixelate_factor = max(5, pixelate_factor + random.randint(-2, 2)) # Ensure factor is at least 5

    try: # Added try-except around the effect application
        if style_name == 'abstract_lines':
            img = stylized_img.resize((stylized_img.width // pixelate_factor, stylized_img.height // pixelate_factor), Image.NEAREST)
            img = img.resize(stylized_img.size, Image.NEAREST)
            stylized_img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(contrast_factor)
        elif style_name == 'watercolor':
            img = stylized_img.filter(ImageFilter.BoxBlur(radius=max(1, int(blur_radius))))
            stylized_img = ImageEnhance.Color(img).enhance(color_factor)
            stylized_img = ImageEnhance.Brightness(stylized_img).enhance(brightness_factor)
        elif style_name == 'oil_painting':
            img = stylized_img.filter(ImageFilter.BoxBlur(radius=max(1, int(blur_radius + 1))))
            edges = img.filter(ImageFilter.FIND_EDGES)
            stylized_img = Image.blend(stylized_img, edges.convert("RGB"), alpha=0.5)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(contrast_factor + 0.3)
        elif style_name == 'sketch':
            img_gray = stylized_img.convert("L")
            img_inverted = ImageEnhance.Brightness(img_gray).enhance(0.5).point(lambda x: 255 - x)
            stylized_img = img_inverted.filter(ImageFilter.FIND_EDGES)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(sharpness_factor + 0.5)
        elif style_name == 'picasso_cubist':
            img = stylized_img.resize((stylized_img.width // pixelate_factor, stylized_img.height // pixelate_factor), Image.NEAREST)
            img = img.resize(stylized_img.size, Image.NEAREST)
            edges = img.filter(ImageFilter.FIND_EDGES)
            stylized_img = Image.blend(img, edges.convert("RGB"), alpha=0.3)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(contrast_factor)
            stylized_img = ImageEnhance.Color(stylized_img).enhance(color_factor - 0.5)
        elif style_name == 'dali_surreal':
            img = stylized_img.filter(ImageFilter.GaussianBlur(radius=max(1, int(blur_radius * 2))))
            img_np = np.array(img)
            img_np[:, :, 0] = np.clip(img_np[:, :, 0] * (1.1 + random.uniform(-0.05, 0.05)), 0, 255)
            img_np[:, :, 1] = np.clip(img_np[:, :, 1] * (0.9 + random.uniform(-0.05, 0.05)), 0, 255)
            stylized_img = Image.fromarray(img_np.astype(np.uint8))
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(contrast_factor - 0.3)
        elif style_name == 'gaudi_gothic':
            img = stylized_img.filter(ImageFilter.DETAIL)
            img = img.filter(ImageFilter.SHARPEN)
            img_mosaic = img.resize((stylized_img.width // max(5, int(pixelate_factor + 5)),
                                    stylized_img.height // max(5, int(pixelate_factor + 5))), Image.NEAREST)
            img_mosaic = img_mosaic.resize(stylized_img.size, Image.NEAREST)
            stylized_img = Image.blend(img, img_mosaic, alpha=0.2)
            stylized_img = ImageEnhance.Contrast(stylized_img).enhance(contrast_factor + 0.5)
            stylized_img = ImageEnhance.Color(stylized_img).enhance(color_factor - 0.2)
        # Note: 'custom' style is handled directly in process_image as it needs a separate image input
        return stylized_img
    except Exception as e:
        print(f"Error applying single style effect for '{style_name}': {e}")
        traceback.print_exc() # Print full traceback
        return None # Return None if style application fails

def apply_style_transfer_logic(content_image_path, style_choice_1, style_choice_2, blend_ratio, custom_style_image_path=None, refine_flag=False):
    """
    Orchestrates the style transfer simulation, including blending and refinement.
    """
    try:
        # Check if content_image_path is valid before opening
        if not content_image_path or not os.path.exists(content_image_path):
            print(f"Error: Content image path is invalid or file does not exist: {content_image_path}")
            return None, None

        content_img = Image.open(content_image_path).convert("RGB")
        content_img = ImageOps.exif_transpose(content_img) # Correct orientation

        final_stylized_img = None

        if style_choice_1 == 'custom' and custom_style_image_path:
            # Handle custom style directly as it involves blending with an external image
            if not custom_style_image_path or not os.path.exists(custom_style_image_path):
                print(f"Error: Custom style image path is invalid or file does not exist: {custom_style_image_path}")
                return None, None
            custom_style_img = Image.open(custom_style_image_path).convert("RGB")
            custom_style_img = custom_style_img.resize(content_img.size)
            final_stylized_img = Image.blend(content_img, custom_style_img, alpha=0.3)
        elif refine_flag:
            # For refinement, re-apply the primary style with slight variation
            final_stylized_img = _apply_single_style_effect(content_img, style_choice_1, is_refinement=True)
        elif style_choice_2 and style_choice_2 != 'none': # Blending two pre-defined styles
            img_style1 = _apply_single_style_effect(content_img, style_choice_1)
            img_style2 = _apply_single_style_effect(content_img, style_choice_2)

            if img_style1 is None or img_style2 is None: # Check if individual style applications failed
                print("One or both styles failed to apply during blending.")
                return None, None

            # Ensure blend_ratio is between 0 and 1
            blend_alpha = float(blend_ratio) / 100.0 if blend_ratio else 0.5
            blend_alpha = max(0.0, min(1.0, 0.9999)) # Cap at just under 1.0 to avoid alpha=1.0 blend issues if source image has no transparency
            
            # Ensure images have same mode and size before blending
            if img_style1.mode != img_style2.mode or img_style1.size != img_style2.size:
                print("Error: Images to blend do not have matching mode or size.")
                # Attempt to convert/resize for blending if possible, or fail
                try:
                    img_style2 = img_style2.resize(img_style1.size).convert(img_style1.mode)
                except Exception as resize_e:
                    print(f"Error resizing/converting image for blend: {resize_e}")
                    return None, None


            # Blend the two stylized images
            final_stylized_img = Image.blend(img_style1, img_style2, alpha=blend_alpha)
        else: # Single style application
            final_stylized_img = _apply_single_style_effect(content_img, style_choice_1)
        
        if final_stylized_img is None: # Catch if single style application failed
            print("Final stylized image is None after style application logic.")
            return None, None

        output_filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
        final_stylized_img.save(output_path)

        return output_path, output_filename

    except Exception as e:
        print(f"Error during overall style transfer logic: {e}")
        traceback.print_exc() # Print full traceback
        return None, None

@app.route('/')
def index():
    """Renders the main page for image upload and style selection."""
    return render_template('index.html', generated_image=None)

@app.route('/process', methods=['POST'])
def process_image():
    """Handles the image upload and triggers the style transfer logic."""
    content_file = request.files.get('content_image')
    style_choice_1 = request.form.get('style_choice_1')
    style_choice_2 = request.form.get('style_choice_2')
    blend_ratio = request.form.get('blend_ratio')
    custom_style_file = request.files.get('custom_style_image')
    refine_flag = request.form.get('refine_flag') == 'true'
    last_generated_filename = request.form.get('last_generated_filename')

    current_content_filepath = None
    original_uploaded_filename_for_metadata = None # To store the original filename for metadata

    # --- Determine content image source (new upload vs. refinement) ---
    if refine_flag and last_generated_filename:
        # Use previously generated image for refinement
        current_content_filepath = os.path.join(app.config['GENERATED_FOLDER'], last_generated_filename)
        original_uploaded_filename_for_metadata = last_generated_filename # For metadata, the 'original' for this step is the previous output
        
        if not os.path.exists(current_content_filepath):
            print(f"Error: Previous generated image '{last_generated_filename}' not found for refinement.")
            return render_template('index.html', error="Previous generated image not found for refinement. Please upload a new image or generate first.")
    else:
        # New upload scenario
        if not content_file or content_file.filename == '':
            print("Error: No content image file provided for a new generation.")
            return render_template('index.html', error="Please upload a content image to start.")
        
        if not allowed_file(content_file.filename): # Validate file extension before saving
            print(f"Error: Disallowed file extension for '{content_file.filename}'.")
            return render_template('index.html', error="Please upload a valid image (PNG, JPG, JPEG, GIF).")

        original_uploaded_filename_for_metadata = content_file.filename # Store the user's original filename
        content_filename_saved = f"{uuid.uuid4()}_{content_file.filename}"
        current_content_filepath = os.path.join(app.config['UPLOAD_FOLDER'], content_filename_saved)
        
        try:
            content_file.save(current_content_filepath)
            print(f"Content file saved: {current_content_filepath}")
        except Exception as e:
            print(f"Error saving content file: {e}")
            traceback.print_exc()
            return render_template('index.html', error="Failed to save content image.")
    # --- End content image source determination ---


    custom_style_filepath = None
    if custom_style_file and custom_style_file.filename != '':
        if not allowed_file(custom_style_file.filename): # Validate custom style file extension
            print(f"Error: Disallowed file extension for custom style '{custom_style_file.filename}'.")
            return render_template('index.html', error="Please upload a valid custom style image (PNG, JPG, JPEG, GIF).")

        custom_style_filename_saved = f"{uuid.uuid4()}_{custom_style_file.filename}"
        custom_style_filepath = os.path.join(app.config['UPLOAD_FOLDER'], custom_style_filename_saved)
        try:
            custom_style_file.save(custom_style_filepath)
            print(f"Custom style file saved: {custom_style_filepath}")
        except Exception as e:
            print(f"Error saving custom style file: {e}")
            traceback.print_exc()
            return render_template('index.html', error="Failed to save custom style image.")
        
        style_choice_1 = 'custom' # Force style to 'custom' if a custom image is provided
        style_choice_2 = 'none' # No blending when custom is primary
    elif style_choice_1 == 'custom': # If custom was chosen but no file provided for it
        print("Error: Custom style chosen but no custom style image provided.")
        return render_template('index.html', error="Please upload a custom style image if 'Custom' is chosen.")

    # --- Validate style choices if not custom ---
    if style_choice_1 not in ['abstract_lines', 'watercolor', 'oil_painting', 'sketch', 'picasso_cubist', 'dali_surreal', 'gaudi_gothic', 'custom']:
        print(f"Error: Invalid style_choice_1 received: {style_choice_1}")
        return render_template('index.html', error="Invalid primary style selected.")
    if style_choice_2 not in ['none', 'abstract_lines', 'watercolor', 'oil_painting', 'sketch', 'picasso_cubist', 'dali_surreal', 'gaudi_gothic']:
        print(f"Error: Invalid style_choice_2 received: {style_choice_2}")
        return render_template('index.html', error="Invalid secondary style selected.")
    # --- End validation ---

    # Orchestrate style transfer
    generated_image_path, generated_image_filename = apply_style_transfer_logic(
        current_content_filepath,
        style_choice_1,
        style_choice_2,
        blend_ratio,
        custom_style_filepath,
        refine_flag
    )

    if generated_image_path:
        artwork_id = str(uuid.uuid4())
        user_id = "anonymous_user_" + str(uuid.uuid4())[:8]

        # Construct the title carefully
        primary_style_title = style_choice_1.replace('_', ' ').title() if style_choice_1 else "Unknown Primary Style"
        title_parts = [primary_style_title]

        if style_choice_2 and style_choice_2 != 'none':
            secondary_style_title = style_choice_2.replace('_', ' ').title() if style_choice_2 else "Unknown Secondary Style"
            title_parts.append(secondary_style_title)
        
        artwork_title = f"Art - {' + '.join(title_parts)}"


        artwork_metadata = {
            "artwork_id": artwork_id,
            "generated_image_path": generated_image_path,
            "generated_image_filename": generated_image_filename,
            "input_content_filepath_for_this_step": current_content_filepath, # The actual image used as input for this step
            "original_uploaded_filename_by_user": original_uploaded_filename_for_metadata, # The user's original filename
            "style_applied_1": style_choice_1,
            "style_applied_2": style_choice_2 if style_choice_2 and style_choice_2 != 'none' else None,
            "blend_ratio": float(blend_ratio) if blend_ratio else None,
            "refinement_step": refine_flag,
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "title": artwork_title,
            "is_public": False
        }
        generated_artworks_metadata.append(artwork_metadata)
        print(f"Stored artwork metadata: {artwork_metadata}")
        print(f"Total artworks in memory: {len(generated_artworks_metadata)}")

        return render_template('index.html', generated_image=generated_image_filename, last_processed_image=generated_image_filename)
    else:
        print("Image processing failed, returning error to user.")
        return render_template('index.html', error="Failed to process image. Please try again.")

@app.route('/download/<filename>')
def download_file(filename):
    """Allows users to download the generated image."""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serves uploaded content/style images."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/generated/<filename>')
def generated_file(filename):
    """Serves the generated image for display."""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)

@app.route('/view_metadata')
def view_metadata():
    """Displays the current in-memory artwork metadata."""
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
    app.run(debug=True)


