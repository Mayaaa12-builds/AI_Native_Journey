# AI Art Generator

A Flask-based web application that simulates AI-powered style transfer for images. This project demonstrates various artistic style transformations using Python's Pillow library.

## Features

- **Multiple Artistic Styles**: Choose from various pre-defined styles including:
  - Abstract Lines
  - Watercolor
  - Oil Painting
  - Sketch
  - Picasso Cubist
  - Dali Surreal
  - Gaudi Gothic
- **Custom Style Images**: Upload your own style reference image
- **Image Upload**: Support for PNG, JPG, JPEG, and GIF formats
- **Download Generated Images**: Save your stylized images
- **Web Interface**: User-friendly HTML interface

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd "2nd try AI Art Generator"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

3. Upload an image and select a style

4. Click "Generate Art" to process your image

5. Download the generated image

## Project Structure

```
2nd try AI Art Generator/
├── app.py              # Main Flask application
├── index.html          # Web interface template
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
├── uploads/           # Directory for uploaded images
└── generated/         # Directory for generated images
```

## Technical Details

- **Framework**: Flask
- **Image Processing**: Pillow (PIL)
- **Style Transfer**: Simulated using various image filters and enhancements
- **File Storage**: Local file system with UUID-based naming

## Development

This is a demonstration project that simulates AI style transfer. In a production environment, you would integrate with actual deep learning models for more sophisticated style transfer capabilities.

## License

This project is open source and available under the MIT License. 