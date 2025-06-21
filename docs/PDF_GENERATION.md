# PDF Documentation Generation

This guide explains how to generate PDF versions of the documentation using MkDocs with the `mkdocs-with-pdf` plugin.

## Overview

The PDF generation feature allows you to create a comprehensive PDF document that includes all documentation pages with:

- **Professional Layout**: Cover page with logo and title
- **Table of Contents**: Automatically generated with configurable depth
- **Page Numbering**: Sequential page numbers throughout the document
- **Cross-References**: Working internal links between sections
- **Mermaid Diagrams**: Rendered diagrams included in the PDF
- **Responsive Formatting**: Proper page breaks and spacing

## Prerequisites

### Required Dependencies

1. **Chrome or Chromium Browser**: Required for PDF rendering
   ```bash
   # macOS
   brew install --cask google-chrome
   
   # Ubuntu/Debian
   sudo apt install chromium-browser
   
   # CentOS/RHEL
   sudo yum install chromium
   ```

2. **Python Dependencies**: Install MkDocs PDF plugin
   ```bash
   pip install -r docs-requirements.txt
   ```

### Check Dependencies

Verify all dependencies are installed:
```bash
task docs:pdf-check
# or directly:
python scripts/generate_pdf_docs.py check
```

## Quick Start

### Generate PDF

```bash
# Using Taskfile (recommended)
task docs:pdf-generate

# Using script directly
python scripts/generate_pdf_docs.py generate

# Using MkDocs directly with environment variable
ENABLE_PDF_EXPORT=1 mkdocs build
```

### Preview PDF

```bash
# Open generated PDF
task docs:pdf-preview

# or directly
python scripts/generate_pdf_docs.py preview
```

### Clean PDF Files

```bash
# Remove generated PDF and build artifacts
task docs:pdf-clean

# or directly
python scripts/generate_pdf_docs.py clean
```

## Configuration

### PDF Settings (mkdocs.yml)

The PDF generation is configured in `mkdocs.yml` under the `with-pdf` plugin:

```yaml
plugins:
  - with-pdf:
      author: ixxeL2097
      copyright: Copyright © 2025 ixxeL-DevOps
      cover: true
      cover_title: ixxeL-DevOps HomeLab Documentation
      cover_subtitle: Complete Infrastructure Guide
      cover_logo: assets/k8s-home.png
      back_cover: true
      toc_title: Table of Contents
      toc_level: 3
      ordered_chapter_level: 2
      output_path: pdf/ixxel-homelab-documentation.pdf
      enabled_if_env: ENABLE_PDF_EXPORT
```

### Key Configuration Options

| Option | Description | Value |
|--------|-------------|-------|
| `cover` | Enable cover page | `true` |
| `cover_title` | Main title on cover | `ixxeL-DevOps HomeLab Documentation` |
| `cover_subtitle` | Subtitle on cover | `Complete Infrastructure Guide` |
| `cover_logo` | Logo image path | `assets/k8s-home.png` |
| `toc_level` | TOC depth (1-6) | `3` |
| `ordered_chapter_level` | Chapter numbering depth | `2` |
| `output_path` | PDF output location | `pdf/ixxel-homelab-documentation.pdf` |
| `enabled_if_env` | Environment variable to enable | `ENABLE_PDF_EXPORT` |

### Excluded Content

Some pages are excluded from the PDF to keep it focused:

```yaml
excludes_children:
  - 'Repository/Git Summary'
exclude_pages:
  - 'git-summary.md'
```

## Table of Contents Management

### TOC Structure

The PDF includes a hierarchical table of contents with:

- **Level 1**: Main sections (Documentation, Repository, etc.)
- **Level 2**: Subsections (Cluster, GitOps, TLS/HTTPS, etc.)
- **Level 3**: Individual pages and sub-topics

### Chapter Numbering

Chapters are automatically numbered up to level 2:
- 1. Documentation
  - 1.1 Cluster
  - 1.2 GitOps
  - 1.3 TLS/HTTPS
- 2. Repository

### Custom TOC Formatting

The TOC can be customized by modifying the `toc_level` and `ordered_chapter_level` settings:

```yaml
toc_level: 3              # Include headings up to ### level
ordered_chapter_level: 2  # Number chapters up to ## level
```

## Advanced Features

### Two-Column Layout

Some sections can be rendered in two-column layout for better space utilization:

```yaml
two_columns_level: 3  # Apply two-column layout to level 3 headings
```

### JavaScript Rendering

The PDF generator can render JavaScript content (like Mermaid diagrams):

```yaml
render_js: true  # Enable JavaScript rendering
```

### Custom CSS for PDF

Add PDF-specific styles in your CSS:

```css
@media print {
  /* PDF-specific styles */
  .md-header, .md-footer {
    display: none;
  }
  
  .pdf-page-break {
    page-break-before: always;
  }
}
```

## Troubleshooting

### Common Issues

**PDF Generation Fails**
- Ensure Chrome/Chromium is installed and in PATH
- Check that all required Python packages are installed
- Verify `ENABLE_PDF_EXPORT=1` environment variable is set

**Missing Images in PDF**
- Ensure image paths are relative to the docs directory
- Check that image files exist and are accessible
- Verify image formats are supported (PNG, JPG, SVG)

**Mermaid Diagrams Not Rendering**
- Ensure `render_js: true` is enabled
- Check that Mermaid JavaScript is properly loaded
- Verify diagram syntax is correct

**Large File Size**
- Optimize images before including in documentation
- Consider reducing TOC depth if not needed
- Check for unnecessary includes or duplicated content

### Debug Mode

Enable debug mode for troubleshooting:

```yaml
debug_html: true   # Save intermediate HTML for debugging
verbose: true      # Enable verbose logging
```

### Environment Variables

Useful environment variables for debugging:

```bash
export ENABLE_PDF_EXPORT=1        # Enable PDF generation
export MKDOCS_DEBUG=1             # Enable MkDocs debug mode
export PYTHONPATH=$PWD            # Ensure Python can find modules
```

## Automation

### CI/CD Integration

Add PDF generation to your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Generate PDF Documentation
  run: |
    pip install -r docs-requirements.txt
    task docs:pdf-generate
    
- name: Upload PDF Artifact
  uses: actions/upload-artifact@v3
  with:
    name: documentation-pdf
    path: pdf/ixxel-homelab-documentation.pdf
```

### Scheduled Generation

Use cron or scheduled tasks to regenerate PDF regularly:

```bash
# Daily PDF generation
0 2 * * * cd /path/to/repo && task docs:pdf-generate
```

## Output

### Generated PDF Features

The generated PDF includes:

- **Cover Page**: Professional cover with logo and title
- **Table of Contents**: Clickable TOC with page numbers
- **Documentation Sections**: All included pages with proper formatting
- **Page Headers/Footers**: Page numbers and section titles
- **Cross-References**: Working internal links
- **Index**: Automatically generated if enabled

### File Location

Generated PDF is saved to:
```
pdf/ixxel-homelab-documentation.pdf
```

### File Size

Typical file size ranges:
- **Text-heavy documentation**: 2-5 MB
- **With images and diagrams**: 5-15 MB
- **Comprehensive with many images**: 15-30 MB

## Best Practices

### Content Organization

1. **Logical Structure**: Organize content in a logical hierarchy
2. **Clear Headings**: Use descriptive headings for better TOC
3. **Page Breaks**: Use page break classes for better formatting
4. **Image Optimization**: Optimize images for print quality

### Performance

1. **Selective Generation**: Exclude non-essential pages
2. **Image Compression**: Compress images while maintaining quality
3. **Efficient TOC**: Use appropriate TOC depth
4. **Minimal JS**: Limit JavaScript usage for faster rendering

### Maintenance

1. **Regular Updates**: Regenerate PDF when content changes
2. **Version Control**: Tag PDF versions with documentation releases
3. **Quality Checks**: Review generated PDF for formatting issues
4. **Backup**: Keep copies of generated PDFs for historical reference

---

*For additional help with PDF generation, check the [mkdocs-with-pdf documentation](https://github.com/orzih/mkdocs-with-pdf) or create an issue in the repository.*
