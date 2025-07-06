#!/usr/bin/env python3
"""
Generate PDF Documentation

This script helps generate PDF documentation from MkDocs with proper
configuration and error handling.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    # Check if chromium is installed
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser', 
        '/usr/bin/google-chrome',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium'
    ]
    
    chromium_found = False
    for path in chromium_paths:
        if os.path.exists(path):
            print(f"✓ Found Chrome/Chromium at: {path}")
            chromium_found = True
            break
    
    if not chromium_found:
        print("❌ Chrome/Chromium not found. Please install Chrome or Chromium for PDF generation.")
        print("On macOS: brew install --cask google-chrome")
        print("On Ubuntu: sudo apt install chromium-browser")
        return False
    
    # Check if mkdocs-with-pdf is installed
    try:
        import mkdocs_with_pdf
        print("✓ mkdocs-with-pdf plugin found")
    except ImportError:
        print("❌ mkdocs-with-pdf plugin not found. Please install requirements:")
        print("pip install -r docs-requirements.txt")
        return False
    
    return True


def create_pdf_directory():
    """Create PDF output directory if it doesn't exist"""
    pdf_dir = Path("pdf")
    pdf_dir.mkdir(exist_ok=True)
    print(f"✓ PDF directory created: {pdf_dir.absolute()}")


def generate_pdf():
    """Generate PDF documentation"""
    print("Generating PDF documentation...")
    
    # Set environment variable to enable PDF export
    env = os.environ.copy()
    env['ENABLE_PDF_EXPORT'] = '1'
    
    try:
        # Build the documentation with PDF export
        result = subprocess.run(
            ['mkdocs', 'build', '--clean'],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✓ PDF documentation generated successfully!")
        
        # Check if PDF was created
        pdf_path = Path("pdf/ixxel-homelab-documentation.pdf")
        if pdf_path.exists():
            file_size = pdf_path.stat().st_size / (1024 * 1024)  # Size in MB
            print(f"✓ PDF file created: {pdf_path.absolute()}")
            print(f"  File size: {file_size:.2f} MB")
        else:
            print("⚠️  PDF file not found in expected location")
            # Check site directory for PDF
            site_pdf = Path("site/pdf/ixxel-homelab-documentation.pdf")
            if site_pdf.exists():
                shutil.copy2(site_pdf, pdf_path)
                print(f"✓ PDF copied to: {pdf_path.absolute()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating PDF: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def preview_pdf():
    """Open the generated PDF for preview"""
    pdf_path = Path("pdf/ixxel-homelab-documentation.pdf")
    
    if not pdf_path.exists():
        print("❌ PDF file not found for preview")
        return False
    
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(['open', str(pdf_path)])
        elif sys.platform == "linux":  # Linux
            subprocess.run(['xdg-open', str(pdf_path)])
        elif sys.platform == "win32":  # Windows
            os.startfile(str(pdf_path))
        
        print(f"✓ PDF opened for preview: {pdf_path.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return False


def clean_pdf():
    """Clean up PDF files"""
    pdf_dir = Path("pdf")
    site_dir = Path("site")
    
    if pdf_dir.exists():
        shutil.rmtree(pdf_dir)
        print("✓ PDF directory cleaned")
    
    if site_dir.exists():
        shutil.rmtree(site_dir)
        print("✓ Site directory cleaned")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PDF documentation from MkDocs")
    parser.add_argument("action", choices=["generate", "preview", "clean", "check"], 
                       help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "check":
        if check_dependencies():
            print("✅ All dependencies are available for PDF generation")
            return 0
        else:
            print("❌ Some dependencies are missing")
            return 1
    
    elif args.action == "generate":
        if not check_dependencies():
            return 1
        
        create_pdf_directory()
        
        if generate_pdf():
            print("\n🎉 PDF documentation generated successfully!")
            print("📄 You can now preview the PDF or find it in the pdf/ directory")
            return 0
        else:
            return 1
    
    elif args.action == "preview":
        if preview_pdf():
            return 0
        else:
            return 1
    
    elif args.action == "clean":
        clean_pdf()
        print("✓ PDF files cleaned")
        return 0


if __name__ == "__main__":
    exit(main())
