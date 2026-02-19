# 🧪 RIFT 2026 Testing Guide

Complete guide to test your autonomous CI/CD healing agent before submission.

## 🚀 Quick Start Testing

### 1. Test the Agent Core (Backend Only)
```bash
# Quick test with a simple repository
python quick_test.py

# Expected output:
# ✅ SUCCESS! Agent completed successfully
# Status: COMPLETED
# Branch: RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix
# Total fixes: X
# Final score: XXX/100
```

### 2. Test API Endpoints
```bash
# Start backend first
cd backend
uvicorn main:app --reload

# In another terminal, test APIs
python test_dashboard_api.py

# Expected output:
# 🎉 All API tests passed! Your backend is ready!
```

### 3. Test Full Dashboard
```bash
# Start frontend (backend should still be running)
cd frontend
npm run dev

# Visit http://localhost:5173
# Use test data from the sections below
```

## 📊 Test Data for Dashboard

### ✅ Recommended Test Repositories

#### 1. **Simple Test** (Always works)
- **Repository**: `https://github.com/octocat/Hello-World`
- **Team Name**: `RIFT ORGANISERS`
- **Leader Name**: `Saiyam Kumar`
- **Expected Branch**: `RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix`
- **Expected Result**: Quick completion, minimal issues

#### 2. **Python Project Test** (Good for finding issues)
- **Repository**: `https://github.com/psf/requests`
- **Team Name**: `Python Masters`
- **Leader Name**: `Kenneth Reitz`
- **Expected Branch**: `PYTHON_MASTERS_KENNETH_REITZ_AI_Fix`
- **Expected Result**: Multiple issues found, longer execution

#### 3. **Learning Project Test** (Likely has issues)
- **Repository**: `https://github.com/realpython/python-basics-exercises`
- **Team Name**: `Code Learners`
- **Leader Name**: `Real Python`
- **Expected Branch**: `CODE_LEARNERS_REAL_PYTHON_AI_Fix`
- **Expected Result**: Educational code with fixable issues

### 🔧 Branch Naming Tests

Test these combinations to verify branch naming works correctly:

| Team Name | Leader Name | Expected Branch |
|-----------|-------------|-----------------|
| `RIFT ORGANISERS` | `Saiyam Kumar` | `RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix` |
| `Code Warriors` | `John Doe` | `CODE_WARRIORS_JOHN_DOE_AI_Fix` |
| `Team@123!` | `User#456$` | `TEAM_USER_AI_Fix` |
| `My Awesome Team` | `Jane Smith-Jones` | `MY_AWESOME_TEAM_JANE_SMITHJONES_AI_Fix` |

### 🐛 Expected Bug Types

Your agent should detect and report these bug types:

1. **LINTING**: `LINTING error in src/utils.py line 15 → Fix: remove the import statement`
2. **SYNTAX**: `SYNTAX error in src/validator.py line 8 → Fix: add the colon at the correct position`
3. **LOGIC**: `LOGIC error in src/main.py line 23 → Fix: use == for comparison`
4. **TYPE_ERROR**: `TYPE_ERROR in src/calc.py line 45 → Fix: convert types before concatenation`
5. **IMPORT**: `IMPORT error in src/module.py line 3 → Fix: use absolute imports`
6. **INDENTATION**: `INDENTATION error in src/func.py line 12 → Fix: use consistent indentation`

## 🎯 Dashboard Testing Checklist

### Input Section ✅
- [ ] Repository URL field accepts GitHub URLs
- [ ] Team name field works with special characters
- [ ] Leader name field works with special characters
- [ ] Branch preview updates in real-time
- [ ] "Run Agent" button shows loading state
- [ ] Form validation works for empty fields

### Live Updates ✅
- [ ] WebSocket connection establishes
- [ ] Live log shows agent progress
- [ ] Status updates appear in real-time
- [ ] Loading indicators work properly
- [ ] Error messages display clearly

### Run Summary Card ✅
- [ ] Repository URL displays correctly
- [ ] Team and leader names show properly
- [ ] Branch name matches expected format
- [ ] Total fixes counter updates
- [ ] CI/CD status badge shows PASSED/FAILED
- [ ] Execution time displays

### Score Panel ✅
- [ ] Base score shows 100 points
- [ ] Speed bonus applies correctly (< 5 minutes = +10)
- [ ] Efficiency penalty calculates (commits > 20 = -2 each)
- [ ] Final score displays prominently
- [ ] Progress bars/charts work

### Fixes Table ✅
- [ ] All fixes display in table format
- [ ] Columns: File | Bug Type | Line Number | Commit Message | Status
- [ ] Bug types match expected format
- [ ] Status shows ✓ Fixed or ✗ Failed
- [ ] Color coding works (green/red)

### CI/CD Timeline ✅
- [ ] Timeline shows multiple iterations
- [ ] Pass/fail badges display correctly
- [ ] Iteration counter shows (e.g., "3/5")
- [ ] Timestamps appear for each run
- [ ] Final status indicator works

## 🔍 Comprehensive Testing

### Run Full Test Suite
```bash
# Test agent with multiple repositories
python test_agent_functionality.py

# This will test:
# - Simple repository (Hello-World)
# - Medium repository (Flask)
# - Large repository (Requests)
# - Complex repository (CPython)
```

### Test Hackathon Compliance
```bash
# Verify all hackathon requirements
python test_hackathon_compliance.py

# This checks:
# - Branch naming convention
# - Bug detection format
# - Score calculation
# - API endpoints
# - Results JSON generation
```

## 🚨 Common Issues & Solutions

### Backend Issues

**Agent fails to clone repository**
```bash
# Check Git installation
git --version

# Test manual clone
git clone https://github.com/octocat/Hello-World /tmp/test-repo
```

**Import errors**
```bash
# Install missing dependencies
cd backend
pip install -r requirements.txt
```

**Port conflicts**
```bash
# Change port in backend/.env
BACKEND_PORT=8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Can't connect to backend**
```bash
# Check frontend/.env.local
VITE_API_URL=http://localhost:8000

# Verify backend is running
curl http://localhost:8000/health
```

**WebSocket connection fails**
```bash
# Check WebSocket URL in frontend code
# Should be ws://localhost:8000 for development
```

### Agent Issues

**No issues found**
- This is normal for simple repositories
- Try with `https://github.com/psf/requests` for more issues

**Timeout errors**
- Agent has 5-minute timeout protection
- Large repositories may hit this limit
- This is expected behavior

**Git errors**
- Ensure Git is installed and in PATH
- Check repository URL is accessible
- Verify internet connection

## 📈 Performance Expectations

### Execution Times
- **Simple repos** (Hello-World): 10-30 seconds
- **Medium repos** (Flask): 1-3 minutes  
- **Large repos** (Requests): 2-5 minutes
- **Very large repos**: May timeout (expected)

### Issue Detection
- **Simple repos**: 0-5 issues
- **Medium repos**: 5-20 issues
- **Large repos**: 10-50 issues (capped at 50)

### Score Ranges
- **Base score**: Always 100
- **Speed bonus**: +10 if < 5 minutes
- **Efficiency penalty**: -2 per commit over 20
- **Typical range**: 80-110 points

## ✅ Pre-Submission Checklist

- [ ] `python quick_test.py` passes
- [ ] `python test_dashboard_api.py` passes  
- [ ] `python test_hackathon_compliance.py` passes
- [ ] Dashboard loads at http://localhost:5173
- [ ] Can successfully run agent with test repository
- [ ] All 5 dashboard sections display correctly
- [ ] Real-time updates work
- [ ] Branch naming follows exact format
- [ ] Bug descriptions match required format
- [ ] Commit messages have [AI-AGENT] prefix

## 🎬 Demo Video Testing

Before recording your LinkedIn video, test this flow:

1. **Start with clean dashboard**
2. **Enter test repository**: `https://github.com/psf/requests`
3. **Team**: `RIFT ORGANISERS`, **Leader**: `Saiyam Kumar`
4. **Click "Run Agent"** and show real-time progress
5. **Wait for completion** (should take 1-3 minutes)
6. **Show all 5 dashboard sections** with results
7. **Highlight key metrics**: fixes found, score, CI/CD status

This gives you a complete, impressive demo for the judges!

---

**🏆 Good luck with your RIFT 2026 submission!**