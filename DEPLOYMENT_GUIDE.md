# Deployment Guide for Sentiment Analysis App

## Prerequisites
- GitHub account
- Git installed locally

## Step 1: Prepare Your Code

### A. Create .gitignore
```bash
# Create .gitignore in project root
echo "node_modules/
__pycache__/
*.pyc
.env
venv/
dist/
.DS_Store" > .gitignore
```

### B. Push to GitHub
```bash
cd C:\Users\vaish\internship\day1
git init
git add .
git commit -m "Initial commit - Sentiment Analysis App"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sentiment-analysis.git
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### A. Sign Up
1. Go to https://render.com
2. Sign up with GitHub

### B. Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: sentiment-analysis-backend
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

### C. Environment Variables
Add these in Render dashboard:
```
PYTHON_VERSION=3.11
```

4. Click "Create Web Service"
5. Wait 5-10 minutes for deployment
6. Copy your backend URL (e.g., https://sentiment-analysis-backend.onrender.com)

---

## Step 3: Deploy Frontend to Vercel

### A. Update Frontend API URL
Edit `frontend/src/App.jsx`:

```javascript
// Change this line:
const response = await fetch('http://localhost:5000/api/analyze', {

// To:
const response = await fetch('https://YOUR-BACKEND-URL.onrender.com/api/analyze', {
```

Also update in `DataViewer.jsx`:
```javascript
const response = await fetch('https://YOUR-BACKEND-URL.onrender.com/api/data');
```

### B. Build Frontend
```bash
cd frontend
npm run build
```

### C. Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

**Or use Vercel Dashboard:**
1. Go to https://vercel.com
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Click "Deploy"

---

## Step 4: Deploy Both Together (Alternative - Railway)

### A. Railway Deployment
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects and deploys both backend and frontend!

---

## Option: Deploy with Docker (Advanced)

### Backend Dockerfile
Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Frontend Dockerfile
Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

Deploy to:
- **DigitalOcean App Platform**
- **AWS ECS**
- **Google Cloud Run**

---

## Recommended Deployment Strategy

### For Demo/Portfolio:
✅ **Frontend**: Vercel (Free, fast, automatic deployments)
✅ **Backend**: Render (Free, auto-sleep after 15 min)

### For Production:
✅ **Frontend**: Vercel or Netlify
✅ **Backend**: Railway ($5/month) or Heroku ($7/month)
✅ **Database**: Add PostgreSQL if storing data

---

## Cost Comparison

| Platform | Backend | Frontend | Total | Features |
|----------|---------|----------|-------|----------|
| **Vercel + Render** | Free | Free | $0 | Auto-sleep, SSL |
| **Railway** | Free $5 credit | Included | $5/mo after | No sleep |
| **Heroku** | $7/mo | Included | $7/mo | Professional |
| **DigitalOcean** | $4/mo | $4/mo | $8/mo | Full control |

---

## Quick Commands Summary

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Deploy Frontend to Vercel
cd frontend
npm run build
vercel --prod

# 3. Backend deploys automatically on Render
# Just connect GitHub repo!
```

---

## Important Notes

1. **Update CORS**: In `backend/app.py`, update CORS for production:
```python
CORS(app, origins=["https://your-frontend-url.vercel.app"])
```

2. **Environment Variables**: Store API keys in platform environment variables, not in code

3. **Free Tier Limitations**:
   - Render: Backend sleeps after 15 min inactivity (30s wake-up time)
   - Vercel: 100GB bandwidth/month (plenty for most projects)

4. **Custom Domain** (Optional):
   - Buy domain on Namecheap ($1-10/year)
   - Connect to Vercel (free SSL included)

---

## Testing Deployed App

After deployment:
1. Visit your Vercel URL
2. Test sentiment analysis
3. Check if backend wakes up (30s delay on first request)
4. Test all features

**Your app will be live at:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.onrender.com`

Good luck with deployment! 🚀
