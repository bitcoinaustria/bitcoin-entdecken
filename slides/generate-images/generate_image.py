#!/usr/bin/env python3
"""
generate_image.py - AI image generation script for Bitcoin misconceptions presentation
Supports multiple AI providers: Replicate.com and fal.ai (Google Imagen4)
"""

import argparse
import asyncio
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import replicate
import fal_client


# Available models by provider
REPLICATE_MODELS = {
    "flux-krea-dev": "black-forest-labs/flux-krea-dev",
    "flux-kontext-pro": "black-forest-labs/flux-kontext-pro", 
    "flux-pro": "black-forest-labs/flux-pro",
    "flux-dev": "black-forest-labs/flux-dev",
    "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
}

FAL_MODELS = {
    "imagen4": "fal-ai/imagen4/preview",
    "imagen4-turbo": "fal-ai/imagen4-turbo"
}

# Combined models dictionary for easy access
MODELS = {**REPLICATE_MODELS, **FAL_MODELS}

DEFAULT_MODEL = "flux-krea-dev"
DEFAULT_PROVIDER = "replicate"

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


def get_provider_for_model(model_name: str) -> str:
    """Determine which provider hosts the given model."""
    if model_name in REPLICATE_MODELS:
        return "replicate"
    elif model_name in FAL_MODELS:
        return "fal"
    else:
        raise ValueError(f"Unknown model: {model_name}")


def check_api_keys(provider: Optional[str] = None) -> Dict[str, Optional[str]]:
    """Check API keys for specified provider or all providers."""
    keys = {
        "replicate": os.getenv("REPLICATE_API"),
        "fal": os.getenv("FAL_AI")
    }
    
    if provider:
        key = keys.get(provider)
        if not key:
            key_name = "REPLICATE_API" if provider == "replicate" else "FAL_AI"
            print(f"Error: {key_name} environment variable not set")
            sys.exit(1)
        return {provider: key}
    
    return keys


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate AI images using Replicate.com and fal.ai APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Replicate models:
{chr(10).join(f"  {name}" for name in REPLICATE_MODELS.keys())}

fal.ai models:
{chr(10).join(f"  {name}" for name in FAL_MODELS.keys())}

Slide mapping:
{chr(10).join(f"  {slide} - {desc} ({SLIDE_IMAGES[slide]})" for slide, desc in SLIDE_DESCRIPTIONS.items())}

Examples:
  # Generate with Replicate (flux-krea-dev)
  python generate_image.py "a hacker in a dark room with multiple monitors"
  
  # Generate with fal.ai Imagen4
  python generate_image.py -m imagen4 "cybercriminal silhouette with bitcoin symbols"
  
  # Generate with specific provider and replace M8 slide  
  python generate_image.py -p fal -m imagen4 -n kriminalitaet-alt -r M8 "cybercriminal with bitcoin logo"
  
  # Edit existing image using flux-kontext-pro
  python generate_image.py -m flux-kontext-pro -i ../pix/kriminalitaet.jpg -r M8 -y "make this image more abstract"
"""
    )
    
    parser.add_argument("prompt", nargs='?', help="Text prompt for image generation")
    parser.add_argument("-p", "--provider", choices=["replicate", "fal", "auto"], default="auto",
                        help="AI provider to use (default: auto - determined by model)")
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
    parser.add_argument("--negative-prompt", 
                        help="Negative prompt (fal.ai only) - describes what to avoid")
    parser.add_argument("--num-images", type=int, default=1,
                        help="Number of images to generate (fal.ai: 1-4, default: 1)")
    parser.add_argument("--seed", type=int,
                        help="Seed for reproducible generation")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="Automatically replace image without prompting")
    
    return parser


def list_models():
    """List all available models."""
    print("Replicate models:")
    for name, model_id in REPLICATE_MODELS.items():
        print(f"  {name:<20} -> {model_id}")
    print("\nfal.ai models:")
    for name, model_id in FAL_MODELS.items():
        print(f"  {name:<20} -> {model_id}")


async def generate_image_fal(model_name: str, prompt: str, input_image: Optional[Path] = None,
                            aspect_ratio: str = "1:1", negative_prompt: Optional[str] = None,
                            num_images: int = 1, seed: Optional[int] = None,
                            dry_run: bool = False) -> Optional[Union[str, list]]:
    """Generate image using fal.ai API with async support."""
    model_id = FAL_MODELS[model_name]
    
    print(f"Generating image with fal.ai model: {model_id}")
    print(f"Prompt: {prompt}")
    
    if input_image:
        print(f"Input image: {input_image}")
        if not input_image.exists():
            print(f"Error: Input image {input_image} does not exist")
            return None
    
    # Prepare input arguments
    arguments = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "num_images": num_images
    }
    
    if negative_prompt:
        arguments["negative_prompt"] = negative_prompt
    
    if seed is not None:
        arguments["seed"] = seed
    
    # Handle input image upload if provided
    if input_image:
        try:
            # Upload file to fal.ai
            print("Uploading input image to fal.ai...")
            image_url = fal_client.upload_file(str(input_image))
            arguments["image_url"] = image_url
            print(f"Image uploaded: {image_url}")
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None
    
    if dry_run:
        print("DRY RUN - Would call:")
        print(f"fal_client.subscribe('{model_id}', arguments={arguments})")
        return None
    
    print("Calling fal.ai API...")
    try:
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    print(f"[LOG] {log['message']}")
        
        result = await fal_client.subscribe_async(
            model_id,
            arguments=arguments,
            with_logs=True,
            on_queue_update=on_queue_update
        )
        
        # Extract image URLs from result
        if "images" in result:
            images = result["images"]
            if images:
                if len(images) == 1:
                    return images[0]["url"]
                else:
                    return [img["url"] for img in images]
        
        print(f"Unexpected result format: {result}")
        return None
        
    except Exception as e:
        print(f"Error calling fal.ai API: {e}")
        return None


def generate_image_replicate(model_name: str, prompt: str, input_image: Optional[Path] = None,
                            output_format: str = "jpg", guidance: float = 3.0, 
                            quality: int = 95, aspect_ratio: str = "1:1", dry_run: bool = False) -> Optional[str]:
    """Generate image using Replicate API."""
    model_id = REPLICATE_MODELS[model_name]
    
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


async def generate_image(provider: str, model_name: str, prompt: str, input_image: Optional[Path] = None,
                        output_format: str = "jpg", guidance: float = 3.0, quality: int = 95, 
                        aspect_ratio: str = "1:1", negative_prompt: Optional[str] = None,
                        num_images: int = 1, seed: Optional[int] = None, 
                        dry_run: bool = False) -> Optional[Union[str, list]]:
    """Generate image using the specified provider."""
    if provider == "replicate":
        return generate_image_replicate(
            model_name=model_name,
            prompt=prompt,
            input_image=input_image,
            output_format=output_format,
            guidance=guidance,
            quality=quality,
            aspect_ratio=aspect_ratio,
            dry_run=dry_run
        )
    elif provider == "fal":
        return await generate_image_fal(
            model_name=model_name,
            prompt=prompt,
            input_image=input_image,
            aspect_ratio=aspect_ratio,
            negative_prompt=negative_prompt,
            num_images=num_images,
            seed=seed,
            dry_run=dry_run
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")


def save_metadata(metadata: Dict, output_path: Path) -> bool:
    """Save generation metadata to JSON file."""
    try:
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"Metadata saved to: {metadata_path}")
        return True
        
    except Exception as e:
        print(f"Error saving metadata: {e}")
        return False


def download_image(image_url: str, output_path: Path, metadata: Optional[Dict] = None) -> bool:
    """Download image from URL to local file and optionally save metadata."""
    try:
        import httpx
        
        print(f"Downloading image from: {image_url}")
        with httpx.stream("GET", image_url) as response:
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        
        print(f"Image saved to: {output_path}")
        
        # Save metadata if provided
        if metadata:
            save_metadata(metadata, output_path)
        
        return True
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def replace_in_latex(current_image: str, new_image: str, 
                    latex_file: Path = Path("../missverstaendnisse.tex")) -> bool:
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


async def main():
    """Main function."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.list_models:
        list_models()
        return
    
    if not args.prompt:
        parser.error("prompt is required unless using --list-models")
    
    # Determine provider
    if args.provider == "auto":
        provider = get_provider_for_model(args.model)
    else:
        provider = args.provider
        # Validate model is available for chosen provider
        if provider == "replicate" and args.model not in REPLICATE_MODELS:
            print(f"Error: Model '{args.model}' not available for Replicate provider")
            sys.exit(1)
        elif provider == "fal" and args.model not in FAL_MODELS:
            print(f"Error: Model '{args.model}' not available for fal.ai provider")
            sys.exit(1)
    
    # Check API keys for the selected provider
    api_keys = check_api_keys(provider)
    
    # Set up fal.ai client if needed
    if provider == "fal":
        os.environ["FAL_KEY"] = api_keys["fal"]
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    generation_time = datetime.now().isoformat()
    output_file = args.output_dir / f"{args.name}-{timestamp}.{args.output_format}"
    
    # Create metadata
    metadata = {
        "prompt": args.prompt,
        "time": generation_time,
        "provider": provider,
        "model": args.model,
        "aspect_ratio": args.aspect_ratio,
        "output_format": args.output_format,
        "timestamp": timestamp
    }
    
    # Add provider-specific metadata
    if provider == "replicate":
        metadata.update({
            "guidance": args.guidance,
            "quality": args.quality
        })
        if args.input_image:
            metadata["input_image"] = str(args.input_image)
    elif provider == "fal":
        metadata.update({
            "num_images": args.num_images
        })
        if args.negative_prompt:
            metadata["negative_prompt"] = args.negative_prompt
        if args.seed is not None:
            metadata["seed"] = args.seed
        if args.input_image:
            metadata["input_image"] = str(args.input_image)
    
    # Add slide replacement info if applicable
    if args.replace:
        metadata["slide_replacement"] = {
            "slide": args.replace,
            "description": SLIDE_DESCRIPTIONS.get(args.replace, ""),
            "original_image": SLIDE_IMAGES.get(args.replace, "")
        }
    
    # Generate image
    image_result = await generate_image(
        provider=provider,
        model_name=args.model,
        prompt=args.prompt,
        input_image=args.input_image,
        output_format=args.output_format,
        guidance=args.guidance,
        quality=args.quality,
        aspect_ratio=args.aspect_ratio,
        negative_prompt=args.negative_prompt,
        num_images=args.num_images,
        seed=args.seed,
        dry_run=args.dry_run
    )
    
    if not image_result or args.dry_run:
        return
    
    # Handle multiple images from fal.ai
    if isinstance(image_result, list):
        # For multiple images, download each one with a different name
        downloaded_files = []
        for i, image_url in enumerate(image_result):
            if len(image_result) > 1:
                file_path = args.output_dir / f"{args.name}-{timestamp}-{i+1:02d}.{args.output_format}"
                # Create metadata for each image
                image_metadata = metadata.copy()
                image_metadata["image_index"] = i + 1
                image_metadata["total_images"] = len(image_result)
            else:
                file_path = output_file
                image_metadata = metadata
            
            if download_image(image_url, file_path, image_metadata):
                downloaded_files.append(file_path)
        
        if not downloaded_files:
            return
        
        # Use the first image for slide replacement
        output_file = downloaded_files[0]
        image_url = image_result[0]
        
        if len(downloaded_files) > 1:
            print(f"\nGenerated {len(downloaded_files)} images:")
            for file_path in downloaded_files:
                print(f"  - {file_path}")
                print(f"  - {file_path.with_suffix('.json')}")
    else:
        # Single image
        image_url = image_result
        if not download_image(image_url, output_file, metadata):
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
    asyncio.run(main())