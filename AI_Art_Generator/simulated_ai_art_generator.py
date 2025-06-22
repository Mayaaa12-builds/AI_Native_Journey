import os
import sys
import time
import random
from typing import Optional, Tuple, List
from datetime import datetime
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

class SimulatedAIArtGenerator:
    """
    Advanced Simulated AI Art Generator with realistic processing simulation
    """
    
    def __init__(self):
        self.styles = {
            "Van Gogh Starry Night": {"color": "blue", "filter": "swirl", "enhance": 1.5},
            "Monet Watercolor": {"color": "pastel", "filter": "blur", "enhance": 1.2},
            "Picasso Cubist": {"color": "geometric", "filter": "edge", "enhance": 1.8},
            "Salvador Dali Surreal": {"color": "dreamy", "filter": "distort", "enhance": 1.6},
            "Andy Warhol Pop": {"color": "vibrant", "filter": "posterize", "enhance": 2.0},
            "Leonardo da Vinci": {"color": "classic", "filter": "sepia", "enhance": 1.3}
        }
        
        self.processing_steps = [
            "Analyzing image composition...",
            "Extracting style features...",
            "Training neural networks...",
            "Applying style transfer algorithms...",
            "Optimizing color palette...",
            "Enhancing artistic elements...",
            "Finalizing masterpiece..."
        ]
    
    def create_directories(self):
        """Create necessary directories for the project"""
        directories = ["input_images", "style_references", "output_gallery", "temp_processing"]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created {directory}/ directory")
    
    def generate_dummy_images(self):
        """Generate sample images for testing"""
        # Create sample content image
        content_img = Image.new('RGB', (400, 300), color='lightblue')
        content_img.save("input_images/sample_photo.jpg")
        
        # Create style reference images
        for style_name in self.styles.keys():
            style_img = Image.new('RGB', (200, 200), color=self._get_style_color(style_name))
            style_img.save(f"style_references/{style_name.lower().replace(' ', '_')}.jpg")
        
        print("✓ Generated sample images for testing")
    
    def _get_style_color(self, style_name: str) -> str:
        """Get representative color for each style"""
        color_map = {
            "Van Gogh Starry Night": "navy",
            "Monet Watercolor": "lightcyan", 
            "Picasso Cubist": "orange",
            "Salvador Dali Surreal": "purple",
            "Andy Warhol Pop": "hotpink",
            "Leonardo da Vinci": "brown"
        }
        return color_map.get(style_name, "gray")
    
    def simulate_ai_processing(self, style_name: str):
        """Simulate realistic AI processing with progress updates"""
        print(f"\n🎨 Applying {style_name} style...")
        print("🤖 AI Neural Network Processing:")
        
        for i, step in enumerate(self.processing_steps, 1):
            print(f"   [{i}/{len(self.processing_steps)}] {step}")
            time.sleep(random.uniform(0.5, 1.5))  # Random processing time
            print("   ✓ Complete")
        
        print("🎯 Style transfer successful!")
    
    def apply_style_effects(self, image: Image.Image, style_name: str) -> Image.Image:
        """Apply various artistic effects based on the selected style"""
        style_config = self.styles[style_name]
        
        # Apply different effects based on style
        if style_config["filter"] == "swirl":
            # Simulate Van Gogh swirl effect
            image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            image = image.filter(ImageFilter.CONTOUR)
        elif style_config["filter"] == "blur":
            # Simulate Monet's soft watercolor effect
            image = image.filter(ImageFilter.GaussianBlur(radius=2))
        elif style_config["filter"] == "edge":
            # Simulate Picasso's geometric style
            image = image.filter(ImageFilter.FIND_EDGES)
        elif style_config["filter"] == "distort":
            # Simulate Dali's surreal distortion
            image = image.filter(ImageFilter.EMBOSS)
        elif style_config["filter"] == "posterize":
            # Simulate Warhol's pop art effect
            image = image.quantize(colors=8).convert('RGB')
        elif style_config["filter"] == "sepia":
            # Simulate da Vinci's classical style
            image = ImageOps.colorize(image.convert('L'), '#8B4513', '#F4A460')
        
        # Apply color enhancement
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(style_config["enhance"])
        
        return image
    
    def generate_artwork(self, content_path: str, style_name: str) -> str:
        """Main function to generate AI artwork"""
        try:
            # Load and validate content image
            content_img = Image.open(content_path).convert("RGB")
            print(f"📸 Loaded content image: {os.path.basename(content_path)}")
            
            # Simulate AI processing
            self.simulate_ai_processing(style_name)
            
            # Apply style effects
            stylized_img = self.apply_style_effects(content_img, style_name)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"ai_artwork_{style_name.lower().replace(' ', '_')}_{timestamp}.png"
            output_path = os.path.join("output_gallery", output_filename)
            
            # Save the artwork
            stylized_img.save(output_path, quality=95)
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error during art generation: {e}")
            return None
    
    def display_gallery(self):
        """Display generated artworks"""
        output_dir = "output_gallery"
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if files:
                print(f"\n🖼️  Your AI Art Gallery ({len(files)} pieces):")
                for i, file in enumerate(files, 1):
                    print(f"   {i}. {file}")
            else:
                print("\n🖼️  Gallery is empty. Generate some artwork first!")

def main():
    """Main execution function"""
    print("🎨" + "="*50)
    print("    SIMULATED AI ART GENERATOR")
    print("="*50)
    print("🤖 Advanced Neural Style Transfer Simulation")
    print("✨ Create masterpieces inspired by famous artists")
    print("="*50)
    
    # Initialize the generator
    generator = SimulatedAIArtGenerator()
    
    # Setup directories and sample images
    print("\n📁 Setting up AI Art Studio...")
    generator.create_directories()
    generator.generate_dummy_images()
    
    while True:
        print("\n" + "="*50)
        print("🎨 AI ART GENERATOR MENU")
        print("="*50)
        print("1. 🖼️  Generate New Artwork")
        print("2. 🖼️  View Art Gallery")
        print("3. 🎨 Available Styles")
        print("4. ❌ Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            # Generate artwork
            print("\n🎨 GENERATE NEW ARTWORK")
            print("-" * 30)
            
            # Get content image
            content_path = input("Enter content image path (or press Enter for sample): ").strip()
            if not content_path:
                content_path = "input_images/sample_photo.jpg"
            
            if not os.path.exists(content_path):
                print(f"❌ Image not found: {content_path}")
                continue
            
            # Display available styles
            print("\n🎨 Available Artistic Styles:")
            for i, style in enumerate(generator.styles.keys(), 1):
                print(f"   {i}. {style}")
            
            # Get style choice
            style_choice = input("\nSelect style (1-6) or enter style name: ").strip()
            
            try:
                if style_choice.isdigit():
                    style_index = int(style_choice) - 1
                    style_name = list(generator.styles.keys())[style_index]
                else:
                    style_name = style_choice
                
                if style_name in generator.styles:
                    print(f"\n🎨 Generating artwork with {style_name} style...")
                    output_path = generator.generate_artwork(content_path, style_name)
                    
                    if output_path:
                        print(f"\n🎉 ARTWORK COMPLETE!")
                        print(f"📁 Saved to: {output_path}")
                        print("🌟 Your AI-generated masterpiece is ready!")
                    else:
                        print("❌ Failed to generate artwork")
                else:
                    print(f"❌ Invalid style: {style_name}")
                    
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                
        elif choice == "2":
            # View gallery
            generator.display_gallery()
            
        elif choice == "3":
            # Show available styles
            print("\n🎨 AVAILABLE ARTISTIC STYLES:")
            print("-" * 40)
            for i, (style, config) in enumerate(generator.styles.items(), 1):
                print(f"{i}. {style}")
                print(f"   Effect: {config['filter']} | Enhancement: {config['enhance']}x")
                print()
                
        elif choice == "4":
            print("\n👋 Thank you for using the AI Art Generator!")
            print("🎨 Keep creating amazing art!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main() 