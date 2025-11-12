# How to Add Images to The Loft Page

## Step 1: Add Your Image Files
Place all your image files in the same folder as `loft.html` (the project root directory).

## Step 2: Replace Placeholders with Images

For each placeholder in `loft.html`, replace this pattern:

**FIND:**
```html
<div class="image-placeholder">
    <!-- Image placeholder: [description] -->
</div>
```

**REPLACE WITH:**
```html
<img src="your-image-filename.jpg" alt="[description]">
```

## Image Locations in loft.html

Here are all the places where you need to add images:

### 1. First Photo (Single Image) - Line ~360
- **Current:** Already has `<img src="loft-cat-table.jpg">`
- **Action:** Make sure you have a file named `loft-cat-table.jpg` in your project folder

### 2. Diptych 1 - Line ~367
- **Caption:** "First paint weekend"
- **Replace:** The placeholder div with: `<img src="first-paint-weekend.jpg" alt="First paint weekend">`

### 3. Diptych 1 - Line ~373
- **Caption:** "Before — raw space"
- **Replace:** The placeholder div with: `<img src="before-raw-space.jpg" alt="Before — raw space">`

### 4. Diptych 2 - Line ~383
- **Caption:** "Kitchen installation"
- **Replace:** The placeholder div with: `<img src="kitchen-installation.jpg" alt="Kitchen installation">`

### 5. Diptych 2 - Line ~389
- **Caption:** "Morning light after the final touch"
- **Replace:** The placeholder div with: `<img src="morning-light.jpg" alt="Morning light after the final touch">`

### 6. Diptych 3 - Line ~399
- **Caption:** "Materials in harmony"
- **Replace:** The placeholder div with: `<img src="materials-harmony.jpg" alt="Materials in harmony">`

### 7. Diptych 3 - Line ~405
- **Caption:** "Everyday creativity"
- **Replace:** The placeholder div with: `<img src="everyday-creativity.jpg" alt="Everyday creativity">`

## Example: Complete Replacement

**BEFORE:**
```html
<div class="diptych-item">
    <div class="image-placeholder">
        <!-- Image placeholder: First paint weekend -->
    </div>
    <div class="diptych-caption">First paint weekend</div>
</div>
```

**AFTER:**
```html
<div class="diptych-item">
    <img src="first-paint-weekend.jpg" alt="First paint weekend">
    <div class="diptych-caption">First paint weekend</div>
</div>
```

## Tips

1. **File Names:** Use lowercase, hyphens instead of spaces (e.g., `first-paint-weekend.jpg` not `First Paint Weekend.jpg`)

2. **Image Formats:** Supported formats are `.jpg`, `.jpeg`, `.png`, `.webp`

3. **Image Size:** Images will be automatically resized to fit, but for best quality, use images that are at least 1200px wide

4. **Alt Text:** Always include descriptive alt text for accessibility

5. **File Path:** Make sure the image files are in the same folder as `loft.html` (not in a subfolder)

## Quick Checklist

- [ ] Add all image files to the project root folder
- [ ] Replace placeholder #1 (First paint weekend)
- [ ] Replace placeholder #2 (Before — raw space)
- [ ] Replace placeholder #3 (Kitchen installation)
- [ ] Replace placeholder #4 (Morning light)
- [ ] Replace placeholder #5 (Materials in harmony)
- [ ] Replace placeholder #6 (Everyday creativity)
- [ ] Test the page in a browser to see all images

