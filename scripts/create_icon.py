# Script to create icon from existing image
from PIL import Image
import os

def create_icon():
    """Create .ico file from PNG image"""
    
    # Try to use Senang.png as icon
    input_image = 'assets/photo/Senang.png'
    output_icon = 'assets/images/icon.ico'
    
    # Create images directory if not exists
    os.makedirs('assets/images', exist_ok=True)
    
    try:
        # Open and resize image
        img = Image.open(input_image)
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create icon with multiple sizes
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(output_icon, format='ICO', sizes=icon_sizes)
        
        print(f"✅ Icon created successfully: {output_icon}")
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: {input_image} not found!")
        print("Please ensure assets/photo/Senang.png exists")
        return False
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        return False

if __name__ == "__main__":
    create_icon()
