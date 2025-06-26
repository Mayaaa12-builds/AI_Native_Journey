AI Art Generator
A Flask-based web application that simulates AI-powered style transfer for images. This project demonstrates various artistic style transformations using Python's Pillow library, now with enhanced creative control.

Features
Image Upload: Users can upload their own content images (PNG, JPG, JPEG, GIF formats supported).

Multiple Artistic Styles: Choose from various pre-defined styles including:

Abstract Lines

Watercolor

Oil Painting

Sketch

Picasso Cubist

Salvador Dalí (Surrealism)

Antoni Gaudí (Gothic Style)

Custom Style Images: Upload your own image to serve as a style reference.

Style Blending: Combine two different pre-defined artistic styles on a single image with an adjustable blend ratio, creating unique hybrid effects.

Iterative Refinement: Evolve your generated artwork by re-applying the primary style, allowing for a more nuanced artistic vision.

Download Generated Images: Save your stylized images to your device.

Enhanced Web Interface: A user-friendly and visually updated HTML interface, featuring a distinct watercolor-abstract outer background and an oil-texture pastel palette background for the main application card, providing a more engaging aesthetic experience.

Installation
Clone the repository:

git clone <your-repository-url>
cd "2nd try AI Art Generator" # Or whatever your project folder is named

Install dependencies:

pip install -r requirements.txt

Usage
Run the application:

python app.py

Open your web browser and navigate to http://127.0.0.1:5000

Upload an image and select one or two styles. Adjust the blend ratio if using two styles.

Click "Generate Art" to process your image.

Optionally, click "Refine Last Artwork" to iterate on the most recent creation.

Download the generated image.

Project Structure
2nd try AI Art Generator/
├── app.py              # Main Flask application logic
├── templates/          # Contains HTML templates (e.g., index.html)
│   └── index.html
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── uploads/            # Directory for uploaded content and custom style images
└── generated/          # Directory for generated stylized images

Technical Details
Framework: Flask

Image Processing: Pillow (PIL) for image manipulation, filtering, and blending.

Style Transfer: Simulated using various image filters, enhancements, and blending techniques.

File Storage: Local file system for uploaded and generated images.

Data Structure: In-memory metadata storage for generated artworks, facilitating features like iterative refinement.

Development
This is a demonstration project that simulates AI style transfer. In a production environment, you would typically integrate with actual deep learning models (e.g., neural style transfer, generative adversarial networks) for more sophisticated and realistic style transfer capabilities.

License
This project is open source and available under the MIT License.
