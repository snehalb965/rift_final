# 🚀 RIFT 2026 Deployment Guide

Quick deployment guide to get your hackathon submission live in minutes!

## 📋 Pre-Deployment Checklist

- [ ] Backend code is working locally
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Environment variables are configured
- [ ] GitHub repository is public
- [ ] All tests pass (`python test_hackathon_compliance.py`)

## 🌐 Frontend Deployment (Vercel)

### Option 1: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project root
cd frontend
vercel --prod

# Follow prompts:
# - Link to existing project? No
# - Project name: rift-agent-frontend
# - Directory: ./
# - Override settings? No
```

### Option 2: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set build settings:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add environment variables:
   - `VITE_API_URL`: Your backend URL (see backend deployment)
5. Deploy!

## 🔧 Backend Deployment (Railway)

### Option 1: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
cd backend
railway deploy

# Set environment variables in Railway dashboard
```

### Option 2: Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Select your repository
4. Set root directory: `backend`
5. Add environment variables:
   - `GITHUB_TOKEN`: Your GitHub personal access token
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)
   - `PORT`: 8000
6. Deploy!

### Alternative: Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

## 🔗 Update Frontend with Backend URL

After backend deployment, update your frontend:

1. Get your backend URL (e.g., `https://your-app.railway.app`)
2. Update `frontend/.env.local`:
   ```env
   VITE_API_URL=https://your-backend-url.railway.app
   ```
3. Redeploy frontend

## 🧪 Test Your Deployment

1. Visit your frontend URL
2. Enter a test repository: `https://github.com/octocat/Hello-World`
3. Team: "RIFT ORGANISERS", Leader: "Test User"
4. Click "Run Agent"
5. Verify real-time updates work
6. Check that results display correctly

## 📱 Get Your URLs

After deployment, you'll have:
- **Frontend URL**: `https://your-app.vercel.app`
- **Backend URL**: `https://your-app.railway.app`
- **API Docs**: `https://your-app.railway.app/docs`

## 🎬 Record LinkedIn Video

Now record your 2-3 minute demo video:

1. **Introduction** (30s): "Hi, I'm [name] presenting our RIFT 2026 hackathon submission..."
2. **Architecture** (60s): Show the architecture diagram, explain multi-agent system
3. **Live Demo** (60s): 
   - Show the live dashboard
   - Enter a repository URL
   - Show real-time progress
   - Show results with fixes table
4. **Conclusion** (30s): Summarize key features and thank judges

### Video Checklist:
- [ ] 2-3 minutes maximum
- [ ] Shows live deployed application
- [ ] Explains architecture clearly
- [ ] Demonstrates all 5 dashboard sections
- [ ] Tags @RIFT2026 on LinkedIn
- [ ] Post is public

## 📝 Final Submission

Update your README.md with:
```markdown
## 🚀 Live Demo

- **Live Application**: https://your-app.vercel.app
- **Demo Video**: https://linkedin.com/posts/your-video-url
- **GitHub Repository**: https://github.com/your-username/rift-agent
```

## 🏆 Submission Form

Fill out the RIFT 2026 submission form with:
1. **Problem Statement**: Autonomous CI/CD Healing Agent
2. **GitHub Repository URL**: Your repo URL
3. **Hosted Application URL**: Your Vercel frontend URL
4. **Demo Video Link**: Your LinkedIn post URL

## 🚨 Common Issues

### Frontend won't connect to backend
- Check CORS settings in `backend/main.py`
- Verify `VITE_API_URL` in frontend environment
- Ensure backend is accessible (test `/health` endpoint)

### Backend deployment fails
- Check `requirements.txt` is complete
- Verify Dockerfile syntax
- Check environment variables are set
- Review deployment logs

### WebSocket connection fails
- Ensure WebSocket URL uses `wss://` for HTTPS backends
- Check firewall/proxy settings
- Verify WebSocket endpoint is accessible

## 💡 Pro Tips

1. **Test locally first**: Always test the full flow locally before deploying
2. **Use environment variables**: Never hardcode URLs or API keys
3. **Check logs**: Use deployment platform logs to debug issues
4. **Test on mobile**: Ensure responsive design works on phones
5. **Backup plan**: Have a second deployment platform ready (Netlify, Heroku, etc.)

---

**Good luck with your RIFT 2026 submission! 🚀**