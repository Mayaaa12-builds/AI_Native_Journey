import os
import time
import random
from datetime import datetime
from PIL import Image, ImageFilter, ImageEnhance

def create_directories():
    """Create necessary directories"""
    dirs = ["input_images", "output_gallery", "styles"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ Created {dir_name}/ directory")

def create_sample_images():
    """Create sample images for testing"""
    # Create sample content image
    content_img = Image.new('RGB', (300, 200), color='lightblue')
    content_img.save("input_images/sample_photo.jpg")
    print("✓ Created sample photo")
    
    # Create style images
    styles = {
        "van_gogh": "navy",
        "monet": "lightcyan", 
        "picasso": "orange",
        "dali": "purple",
        "warhol": "hotpink"
    }
    
    for style, color in styles.items():
        style_img = Image.new('RGB', (150, 150), color=color)
        style_img.save(f"styles/{style}.jpg")
    
    print("✓ Created style reference images")

def simulate_ai_processing(style_name):
    """Simulate AI processing with realistic steps"""
    steps = [
        "Analyzing image composition...",
        "Extracting style features...",
        "Training neural networks...",
        "Applying style transfer...",
        "Optimizing colors...",
        "Finalizing artwork..."
    ]
    
    print(f"\n🎨 Applying {style_name} style...")
    print("🤖 AI Processing:")
    
    for i, step in enumerate(steps, 1):
        print(f"   [{i}/{len(steps)}] {step}")
        time.sleep(random.uniform(0.3, 0.8))
        print("   ✓ Complete")
    
    print("🎯 Style transfer successful!")

def apply_style_effect(image, style_name):
    """Apply different artistic effects"""
    if style_name == "Van Gogh":
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        image = image.filter(ImageFilter.CONTOUR)
    elif style_name == "Monet":
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
    elif style_name == "Picasso":
        image = image.filter(ImageFilter.FIND_EDGES)
    elif style_name == "Dali":
        image = image.filter(ImageFilter.EMBOSS)
    elif style_name == "Warhol":
        image = image.quantize(colors=6).convert('RGB')
    
    # Enhance colors
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.5)
    
    return image

def generate_artwork(content_path, style_name):
    """Generate AI artwork"""
    try:
        # Load image
        content_img = Image.open(content_path).convert("RGB")
        print(f"📸 Loaded: {os.path.basename(content_path)}")
        
        # Simulate processing
        simulate_ai_processing(style_name)
        
        # Apply effects
        stylized_img = apply_style_effect(content_img, style_name)
        
        # Save artwork
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"ai_art_{style_name.lower().replace(' ', '_')}_{timestamp}.png"
        output_path = os.path.join("output_gallery", output_filename)
        
        stylized_img.save(output_path)
        return output_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def show_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("🎨 AI ART GENERATOR")
    print("="*50)
    print("1. 🖼️  Create New Artwork")
    print("2. 🖼️  View Gallery")
    print("3. 🎨 Show Styles")
    print("4. ❌ Exit")
    print("="*50)

def main():
    """Main function"""
    print("🎨" + "="*50)
    print("    AI ART GENERATOR")
    print("="*50)
    print("🤖 Neural Style Transfer Simulation")
    print("✨ Create art inspired by famous artists")
    print("="*50)
    
    # Setup
    print("\n📁 Setting up studio...")
    create_directories()
    create_sample_images()
    
    styles = ["Van Gogh", "Monet", "Picasso", "Dali", "Warhol"]
    
    while True:
        show_menu()
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            print("\n🎨 CREATE NEW ARTWORK")
            print("-" * 30)
            
            # Get image path
            content_path = input("Image path (or Enter for sample): ").strip()
            if not content_path:
                content_path = "input_images/sample_photo.jpg"
            
            if not os.path.exists(content_path):
                print(f"❌ Image not found: {content_path}")
                continue
            
            # Show styles
            print("\n🎨 Available Styles:")
            for i, style in enumerate(styles, 1):
                print(f"   {i}. {style}")
            
            # Get style choice
            style_choice = input("\nSelect style (1-5): ").strip()
            
            try:
                style_index = int(style_choice) - 1
                if 0 <= style_index < len(styles):
                    style_name = styles[style_index]
                    print(f"\n🎨 Generating {style_name} artwork...")
                    
                    output_path = generate_artwork(content_path, style_name)
                    
                    if output_path:
                        print(f"\n🎉 SUCCESS!")
                        print(f"📁 Saved: {output_path}")
                        print("🌟 Your AI masterpiece is ready!")
                    else:
                        print("❌ Generation failed")
                else:
                    print("❌ Invalid style number")
            except ValueError:
                print("❌ Please enter a number 1-5")
                
        elif choice == "2":
            # View gallery
            output_dir = "output_gallery"
            if os.path.exists(output_dir):
                files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg'))]
                if files:
                    print(f"\n🖼️  Gallery ({len(files)} pieces):")
                    for i, file in enumerate(files, 1):
                        print(f"   {i}. {file}")
                else:
                    print("\n🖼️  Gallery is empty")
            else:
                print("\n🖼️  Gallery not found")
                
        elif choice == "3":
            print("\n🎨 ARTISTIC STYLES:")
            print("-" * 30)
            for i, style in enumerate(styles, 1):
                print(f"{i}. {style}")
                if style == "Van Gogh":
                    print("   Swirling brushstrokes, vibrant colors")
                elif style == "Monet":
                    print("   Soft watercolor, impressionist")
                elif style == "Picasso":
                    print("   Geometric, cubist forms")
                elif style == "Dali":
                    print("   Surreal, dreamlike distortion")
                elif style == "Warhol":
                    print("   Pop art, bold colors")
                print()
                
        elif choice == "4":
            print("\n👋 Thanks for creating art!")
            print("🎨 Keep being creative!")
            break
            
        else:
            print("❌ Please select 1-4")

if __name__ == "__main__":
    main() 