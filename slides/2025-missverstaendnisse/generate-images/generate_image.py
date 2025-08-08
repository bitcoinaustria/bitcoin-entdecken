#!/usr/bin/env python3
"""
generate_image.py - AI image generation script for Bitcoin misconceptions presentation
Uses Replicate.com API with Python for better image handling and editing capabilities
"""

import argparse
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import replicate


# Available models
MODELS = {
    "flux-krea-dev": "black-forest-labs/flux-krea-dev",
    "flux-kontext-pro": "black-forest-labs/flux-kontext-pro", 
    "flux-pro": "black-forest-labs/flux-pro",
    "flux-dev": "black-forest-labs/flux-dev",
    "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
}

DEFAULT_MODEL = "flux-krea-dev"

# Map slide numbers to their image filenames
SLIDE_IMAGES = {
    "M1": "pix/mining.jpg",
    "M2": "pix/nichts-intrinsisches.jpg", 
    "M3": "pix/volatil.jpg",
    "M4": "pix/verbrecher-2.jpg",
    "M5": "pix/bitcoin-skalieren-2.jpg",
    "M6": "pix/blase.jpg",
    "M7": "pix/bitcoin-schneeball.jpg",
    "M8": "pix/kriminalitaet.jpg",
    "M9": "pix/no-bitcoin-in-shop.png",
    "M10": "pix/zentralbank.jpg",
    "M11": "pix/hacking-2.jpg"
}

SLIDE_DESCRIPTIONS = {
    "M1": "Umweltauswirkungen",
    "M2": "Kein intrinsischer Wert", 
    "M3": "Volatilität",
    "M4": "Regulierung",
    "M5": "Skalierbarkeit",
    "M6": "Spekulationsblase",
    "M7": "Schneeballsystem",
    "M8": "Kriminalität",
    "M9": "Praktische Adoption",
    "M10": "Bedenken von Zentralbanken",
    "M11": "Technische Sicherheit"
}


def check_api_key() -> str:
    """Check if REPLICATE_API environment variable is set."""
    api_key = os.getenv("REPLICATE_API")
    if not api_key:
        print("Error: REPLICATE_API environment variable not set")
        sys.exit(1)
    return api_key


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate AI images using Replicate.com API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available models:
{chr(10).join(f"  {name}" for name in MODELS.keys())}

Slide mapping:
{chr(10).join(f"  {slide} - {desc} ({SLIDE_IMAGES[slide]})" for slide, desc in SLIDE_DESCRIPTIONS.items())}

Examples:
  # Generate basic image (automatically adds "aspect ratio: 1:1")
  python generate_image.py "a hacker in a dark room with multiple monitors"
  
  # Generate with specific model and replace M8 (Kriminalität) slide  
  python generate_image.py -m flux-krea-dev -n kriminalitaet-alt -r M8 "cybercriminal silhouette with bitcoin symbols"
  
  # Generate with custom aspect ratio
  python generate_image.py --aspect-ratio "16:9" "landscape scene with bitcoin themes"
  
  # Edit existing image using flux-kontext-pro with automatic replacement
  python generate_image.py -m flux-kontext-pro -i ../pix/kriminalitaet.jpg -r M8 -y "make this image more abstract and artistic"
"""
    )
    
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, choices=MODELS.keys(),
                        help=f"AI model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("-n", "--name", default="generated", 
                        help="Base name for output file (default: generated)")
    parser.add_argument("-i", "--input-image", type=Path,
                        help="Input image for editing (required for flux-kontext-pro)")
    parser.add_argument("-r", "--replace", choices=SLIDE_IMAGES.keys(),
                        help="Replace image in slide (e.g., M8 for Kriminalität)")
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("../pix"),
                        help="Output directory (default: ../pix)")
    parser.add_argument("--list-models", action="store_true",
                        help="List available models and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without executing")
    parser.add_argument("--output-format", choices=["jpg", "png"], default="jpg",
                        help="Output format (default: jpg)")
    parser.add_argument("--guidance", type=float, default=3.0,
                        help="Guidance scale (default: 3.0)")
    parser.add_argument("--quality", type=int, default=95,
                        help="Output quality (default: 95)")
    parser.add_argument("--aspect-ratio", default="1:1",
                        help="Aspect ratio for the image (default: 1:1)")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="Automatically replace image without prompting")
    
    return parser


def list_models():
    """List all available models."""
    print("Available models:")
    for name, model_id in MODELS.items():
        print(f"  {name:<20} -> {model_id}")


def generate_image(model_name: str, prompt: str, input_image: Optional[Path] = None,
                  output_format: str = "jpg", guidance: float = 3.0, 
                  quality: int = 95, aspect_ratio: str = "1:1", dry_run: bool = False) -> Optional[str]:
    """Generate image using Replicate API."""
    model_id = MODELS[model_name]
    
    # Ensure aspect ratio is always appended to prompt
    if f"aspect ratio: {aspect_ratio}" not in prompt.lower():
        prompt = f"{prompt}. aspect ratio: {aspect_ratio}"
    
    print(f"Generating image with model: {model_id}")
    print(f"Prompt: {prompt}")
    
    if input_image:
        print(f"Input image: {input_image}")
        if not input_image.exists():
            print(f"Error: Input image {input_image} does not exist")
            return None
    
    # Prepare input
    input_data = {
        "prompt": prompt,
        "guidance": guidance,
        "output_quality": quality,
        "output_format": output_format
    }
    
    # Add input image if provided (required for flux-kontext-pro)
    if input_image:
        input_data["input_image"] = open(input_image, "rb")
    
    if dry_run:
        print("DRY RUN - Would call:")
        print(f"replicate.run('{model_id}', input={input_data})")
        return None
    
    # Check if model requires input image
    if model_name == "flux-kontext-pro" and not input_image:
        print("Error: flux-kontext-pro requires an input image (-i/--input-image)")
        return None
    
    print("Calling Replicate API...")
    try:
        # Set API key
        os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API")
        
        output = replicate.run(model_id, input=input_data)
        
        # Handle different output types
        if isinstance(output, list) and len(output) > 0:
            # Get the first output
            result = output[0]
            if hasattr(result, 'url'):
                return result.url
            else:
                return str(result)
        elif hasattr(output, 'url'):
            return output.url
        else:
            return str(output)
            
    except Exception as e:
        print(f"Error calling Replicate API: {e}")
        return None


def download_image(image_url: str, output_path: Path) -> bool:
    """Download image from URL to local file."""
    try:
        import httpx
        
        print(f"Downloading image from: {image_url}")
        with httpx.stream("GET", image_url) as response:
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        
        print(f"Image saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def replace_in_latex(current_image: str, new_image: str, 
                    latex_file: Path = Path("../2025-missverstaendnisse.tex")) -> bool:
    """Replace image reference in LaTeX file."""
    if not latex_file.exists():
        print(f"Error: {latex_file} not found")
        return False
    
    # Create backup
    backup_file = latex_file.with_suffix(f".tex.backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    latex_file.rename(backup_file)
    print(f"Created backup: {backup_file}")
    
    try:
        # Read and replace
        with open(backup_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated_content = content.replace(current_image, new_image)
        
        with open(latex_file, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print(f"✓ Replaced {current_image} with {new_image} in {latex_file}")
        return True
        
    except Exception as e:
        print(f"Error replacing in LaTeX file: {e}")
        # Restore backup
        backup_file.rename(latex_file)
        return False


def main():
    """Main function."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.list_models:
        list_models()
        return
    
    # Check API key
    api_key = check_api_key()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output_dir / f"{args.name}-{timestamp}.{args.output_format}"
    
    # Generate image
    image_url = generate_image(
        model_name=args.model,
        prompt=args.prompt,
        input_image=args.input_image,
        output_format=args.output_format,
        guidance=args.guidance,
        quality=args.quality,
        aspect_ratio=args.aspect_ratio,
        dry_run=args.dry_run
    )
    
    if not image_url or args.dry_run:
        return
    
    # Download image
    if not download_image(image_url, output_file):
        return
    
    # Handle slide replacement
    if args.replace:
        current_image = SLIDE_IMAGES[args.replace]
        
        # Create final filename matching slide pattern  
        current_path = Path(current_image)
        final_name = current_path.parent / f"{current_path.stem}-alt-{timestamp}.{args.output_format}"
        
        # Move to final location
        final_path = Path("..") / final_name
        output_file.rename(final_path)
        
        print(f"Moved generated image to: {final_path}")
        print()
        print("To replace the image in the presentation:")
        print(f"  Current image: {current_image}")
        print(f"  New image:     {final_name}")
        print()
        
        # Ask for automatic replacement (or use --yes flag)
        if args.yes:
            print("Auto-replacing image (--yes flag provided)")
            if replace_in_latex(current_image, str(final_name)):
                print()
                print("✓ Image replaced successfully!")
                print("Don't forget to run: make format && make build")
            else:
                print("✗ Auto-replacement failed. Manual replacement required.")
        else:
            try:
                response = input("Replace automatically? (y/N): ").strip().lower()
                if response in ('y', 'yes'):
                    if replace_in_latex(current_image, str(final_name)):
                        print()
                        print("✓ Image replaced successfully!")
                        print("Don't forget to run: make format && make build")
                    else:
                        print("✗ Replacement failed. Manual replacement required.")
                else:
                    print("Manual replacement required.")
            except (KeyboardInterrupt, EOFError):
                print("\nManual replacement required.")
    
    print("Done!")


if __name__ == "__main__":
    main()