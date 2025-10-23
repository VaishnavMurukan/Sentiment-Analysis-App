# Quick Fix for "Failed to Fetch" Error

## Problem
Your Vercel frontend can't connect to your Render backend.

## Solution - Two Options:

### Option 1: Using Environment Variables (Recommended)

1. **Get your Render backend URL**
   - Go to your Render dashboard
   - Copy the URL (e.g., `https://sentiment-backend-abc123.onrender.com`)

2. **Add Environment Variable in Vercel**
   - Go to your Vercel dashboard
   - Select your project
   - Go to Settings → Environment Variables
   - Add new variable:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://your-backend-name.onrender.com` (your Render URL)
   - Click "Save"

3. **Redeploy**
   - Go to Deployments tab
   - Click "..." → "Redeploy"
   - Check "Use existing Build Cache"
   - Click "Redeploy"

### Option 2: Direct Edit (Quick but not ideal)

1. **Edit config.js locally**
   ```javascript
   // frontend/src/config.js
   const API_URL = 'https://your-backend-name.onrender.com';
   export default API_URL;
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update API URL for production"
   git push origin main
   ```

3. **Vercel auto-deploys** (wait 1-2 minutes)

---

## Testing

After redeployment:

1. Visit your Vercel site
2. Type a topic (e.g., "AI")
3. Click Analyze
4. **First request may take 30-60 seconds** (Render free tier wakes up)
5. Subsequent requests are fast

---

## Common Issues

### Issue: Still getting "Failed to fetch"
**Solution**: Check browser console (F12) for CORS errors
- Make sure backend CORS is enabled (we already updated this)
- Verify backend is running on Render

### Issue: Request takes forever
**Solution**: Render free tier sleeps after 15 minutes
- First request wakes it up (30-60 seconds)
- This is normal on free tier
- Consider upgrading to paid tier ($7/mo) for instant responses

### Issue: Backend shows error on Render
**Solution**: 
1. Check Render logs
2. Make sure all dependencies are in requirements.txt
3. Check if NLTK data downloads correctly

---

## Verify Backend is Working

Test your backend directly:

1. Visit: `https://your-backend-name.onrender.com/api/health`
2. Should see: `{"status": "healthy", "message": "..."}`

If this doesn't work, your backend isn't deployed correctly.

---

## Quick Commands

```bash
# Update frontend with new API URL
cd frontend
echo VITE_API_URL=https://your-backend.onrender.com > .env

# Test locally
npm run dev

# Push to production
git add .
git commit -m "Fix API URL"
git push origin main
```

---

## Your Backend URL

Check your Render dashboard for the URL. It looks like:
- `https://sentiment-analysis-backend.onrender.com`
- `https://sentiment-backend-xyz123.onrender.com`

**Don't forget the `https://`!**

---

## Need More Help?

Tell me:
1. Your Vercel frontend URL
2. Your Render backend URL
3. Error message from browser console (F12)

I'll help you fix it!
