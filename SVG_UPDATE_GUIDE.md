# SVG Icon Update Guide

## 🎨 **How to Manually Update SVG Icons**

Your application now uses **external SVG files** that are referenced by local file paths, making it easy to manually update icons without touching the HTML code.

### **📁 Icon File Locations**

All SVG icons are stored in: `static/images/icons/`

```
static/images/icons/
├── chart-line.svg          # Main header icon
├── cloud-upload.svg        # Upload area icon
├── folder-open.svg         # Browse files button
├── settings.svg            # Configuration section
├── refresh.svg             # Reset button
├── chart-bar.svg           # Graph type selection
├── info-circle.svg         # Instructions and help
├── columns.svg             # Column selection
├── palette.svg             # Styling configuration
├── ruler.svg               # Axis range configuration
├── magic.svg               # Generate graph button
├── chart-area.svg          # Generated graph section
├── download.svg            # Download button
├── expand.svg              # Fullscreen button
└── ... (other icons)
```

### **🔧 How to Update an Icon**

#### **Method 1: Edit the SVG File Directly**

1. **Navigate to the icons folder**:
   ```bash
   cd static/images/icons/
   ```

2. **Open any SVG file** (e.g., `chart-line.svg`):
   ```bash
   # Using nano
   nano chart-line.svg
   
   # Using VS Code
   code chart-line.svg
   
   # Using any text editor
   open chart-line.svg
   ```

3. **Modify the SVG content** and save

4. **Refresh your browser** to see changes immediately!

#### **Method 2: Replace with a New SVG**

1. **Create or download a new SVG file**
2. **Save it to** `static/images/icons/` with the same name
3. **Refresh your browser**

### **📝 SVG Structure Explained**

#### **Basic SVG Template**:
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <!-- Your paths here -->
    <path d="M3 3v18h18"/>
    <path d="M18 17V9"/>
</svg>
```

#### **Key Attributes**:
- `width="24" height="24"` - Base size (will be scaled by CSS)
- `viewBox="0 0 24 24"` - Coordinate system
- `fill="none"` - No fill color
- `stroke="currentColor"` - Inherits text color
- `stroke-width="2"` - Line thickness
- `stroke-linecap="round"` - Rounded line ends
- `stroke-linejoin="round"` - Rounded line joins

### **🎯 Common Path Commands**

- `M` = Move to (absolute)
- `L` = Line to (absolute)
- `H` = Horizontal line
- `V` = Vertical line
- `C` = Cubic curve
- `Z` = Close path

### **💡 Practical Examples**

#### **Example 1: Simple Line Icon**
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 3v18h18"/>
    <path d="M8 17l4-4 4 4"/>
</svg>
```

#### **Example 2: Circle Icon**
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <path d="M12 16v-4"/>
    <path d="M12 8h.01"/>
</svg>
```

#### **Example 3: Bar Chart Icon**
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 3v18h18"/>
    <rect x="6" y="15" width="2" height="6"/>
    <rect x="11" y="10" width="2" height="11"/>
    <rect x="16" y="5" width="2" height="16"/>
</svg>
```

### **🎨 Color Customization**

The icons automatically inherit colors from CSS:

- **White icons**: Default (inherit text color)
- **Blue icons**: Use `icon-primary` class
- **Custom colors**: Modify the CSS filter in `static/css/icons.css`

### **📱 Responsive Sizing**

Icons are sized using CSS classes:
- `icon-sm` = 0.875em
- `icon-lg` = 1.5em  
- `icon-xl` = 2em
- `icon-2xl` = 3em
- `icon-3xl` = 4em

### **⚡ Quick Update Workflow**

1. **Edit SVG file** in `static/images/icons/`
2. **Save the file**
3. **Refresh browser** (Ctrl+F5 or Cmd+Shift+R)
4. **See changes immediately!**

### **🔍 Testing Your Changes**

1. **Start the application**:
   ```bash
   python3 app.py
   ```

2. **Open browser** to `http://localhost:5001`

3. **Navigate to the section** with your updated icon

4. **Verify the changes** appear correctly

### **💾 Backup Your Icons**

Before making major changes, consider backing up your icons:
```bash
cp -r static/images/icons/ static/images/icons_backup/
```

### **🎯 Tips for Best Results**

- **Keep viewBox consistent**: Always use `viewBox="0 0 24 24"`
- **Use stroke-based icons**: Avoid fills for consistency
- **Test different sizes**: Make sure icons look good at all sizes
- **Maintain stroke-width**: Keep it at `2` for consistency
- **Use round caps**: `stroke-linecap="round"` for modern look

### **🚀 Advanced Customization**

For more advanced customization, you can:
- Modify the CSS filters in `static/css/icons.css`
- Add new icon classes for different colors
- Create animated icons with CSS transitions
- Add hover effects and interactions

---

**Happy icon editing!** 🎨✨
