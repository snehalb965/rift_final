# 🎨 How to Add Your Logo

## 📁 **Step 1: Download and Prepare Your Logo**

1. **Download your logo image** (PNG, SVG, or JPG format)
2. **Resize it** to around 32x32 pixels or 64x64 pixels for best results
3. **Name it** `logo.png` (or `logo.svg` if it's an SVG)

## 📂 **Step 2: Place the Logo File**

Put your logo file in the `frontend/public/` directory:

```
frontend/
├── public/
│   └── logo.png          ← Put your logo HERE
├── src/
│   └── App.jsx
```

## 🔧 **Step 3: The Code is Already Updated**

I've already updated the code in `frontend/src/App.jsx` to use your logo image. The current code looks for `/logo.png` in the public folder.

## 🎯 **What You Need to Do**

### **Option 1: Use PNG Logo**
1. Save your logo as `frontend/public/logo.png`
2. That's it! The code will automatically use it.

### **Option 2: Use SVG Logo**
1. Save your logo as `frontend/public/logo.svg`
2. Update `frontend/src/App.jsx` line 73:
   ```jsx
   // Change this:
   <img src="/logo.png" alt="RIFT 2026 Logo" className="logo-icon" style={{width: '28px', height: '28px', marginRight: '8px'}} />
   
   // To this:
   <img src="/logo.svg" alt="RIFT 2026 Logo" className="logo-icon" style={{width: '28px', height: '28px', marginRight: '8px'}} />
   ```

### **Option 3: Use Different Name**
If your logo has a different name (like `my-logo.png`):
1. Save it as `frontend/public/my-logo.png`
2. Update `frontend/src/App.jsx` line 73:
   ```jsx
   <img src="/my-logo.png" alt="RIFT 2026 Logo" className="logo-icon" style={{width: '28px', height: '28px', marginRight: '8px'}} />
   ```

## 🎨 **Customize Logo Size**

To change the logo size, edit the `style` in `frontend/src/App.jsx`:

```jsx
// Small logo (24x24)
style={{width: '24px', height: '24px', marginRight: '8px'}}

// Medium logo (32x32) 
style={{width: '32px', height: '32px', marginRight: '8px'}}

// Large logo (48x48)
style={{width: '48px', height: '48px', marginRight: '8px'}}
```

## 🚀 **Test Your Logo**

1. **Add your logo** to `frontend/public/logo.png`
2. **Start your frontend**: `cd frontend && npm run dev`
3. **Open browser**: `http://localhost:5173`
4. **Check the header** - your logo should appear next to "RIFT 2026"

## 🔄 **If Logo Doesn't Show**

1. **Check file path**: Make sure it's `frontend/public/logo.png`
2. **Check file name**: Must match exactly what's in the code
3. **Refresh browser**: Hard refresh with Ctrl+F5
4. **Check browser console**: Press F12 and look for errors

## 📱 **Logo Recommendations**

- **Size**: 32x32 pixels or 64x64 pixels
- **Format**: PNG with transparent background (best)
- **Colors**: Should work well on dark background
- **Style**: Simple, clean design that's readable at small size

## 🎯 **Quick Example**

If you have a logo called `rift-logo.png`:

1. **Save it as**: `frontend/public/rift-logo.png`
2. **Update code**: Change `/logo.png` to `/rift-logo.png` in App.jsx
3. **Done!**

Your logo will appear in the top-left corner of your RIFT 2026 dashboard!