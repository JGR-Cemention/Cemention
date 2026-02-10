# 🚨 EMERGENCY TROUBLESHOOTING GUIDE - Save Your Credits!

## ⚡ Quick Fix for Babel Error (Use This Immediately)

### Step 1: Clear Build Cache and Restart
```bash
# Run these commands in order:
cd /app/frontend
rm -rf node_modules/.cache
sudo supervisorctl restart frontend

# Wait 15 seconds, then check:
curl -s http://localhost:3000 | head -20
```

### Step 2: If Still Failing, Nuclear Option
```bash
cd /app/frontend
rm -rf node_modules/.cache build
sudo supervisorctl restart frontend
```

### Step 3: Verify It's Working
```bash
# Wait 20 seconds, then:
curl -I http://localhost:3000
# Should return: HTTP/1.1 200 OK
```

---

## 💡 PREVENT CREDIT WASTAGE - Critical Tips

### 1. **Always Create Checkpoints Before Major Changes**
```bash
# Create checkpoint BEFORE:
# - Adding new features
# - Installing dependencies
# - Major code refactoring

# Use Emergent UI: Settings > Checkpoints > Create New
```

### 2. **Test Incrementally (Small Changes)**
❌ **DON'T:** Make 10 file changes at once
✅ **DO:** Make 2-3 file changes, test, then continue

### 3. **Use Simple Testing First**
Before calling expensive testing agents:
```bash
# Test backend API:
curl http://localhost:8001/api/

# Test frontend loads:
curl -I http://localhost:3000

# Check logs for errors:
tail -n 50 /var/log/supervisor/frontend.err.log
tail -n 50 /var/log/supervisor/backend.err.log
```

### 4. **Restart Services After These Changes**
ALWAYS restart after:
- Installing packages (yarn add, pip install)
- Changing .env files
- Adding new dependencies

```bash
# Backend restart needed:
pip install [package] && sudo supervisorctl restart backend

# Frontend restart needed:
yarn add [package] && sudo supervisorctl restart frontend
```

---

## 🛠️ Common Errors & Quick Fixes

### Error Type 1: Babel/Webpack Build Errors
**Symptoms:** "Cannot read properties of null", "Module build failed"

**Quick Fix:**
```bash
cd /app/frontend
rm -rf node_modules/.cache
sudo supervisorctl restart frontend
```

**Prevention:** 
- Don't edit files while build is running
- Wait for "Compiled successfully!" message

---

### Error Type 2: Import/Module Not Found
**Symptoms:** "Cannot find module", "Module not found"

**Quick Fix:**
```bash
# Check if package is installed:
cd /app/frontend
cat package.json | grep [package-name]

# If missing:
yarn add [package-name]
sudo supervisorctl restart frontend
```

**Prevention:**
- Always install packages before importing
- Check package.json has the dependency

---

### Error Type 3: Backend API Not Responding
**Symptoms:** 404, 500 errors, "Connection refused"

**Quick Fix:**
```bash
# Check backend is running:
sudo supervisorctl status backend

# If stopped, check logs:
tail -n 100 /var/log/supervisor/backend.err.log

# Common issues:
# - Missing imports: pip install [package]
# - Syntax error: Fix the Python file
# - Port already in use: sudo supervisorctl restart backend
```

---

### Error Type 4: Database Connection Issues
**Symptoms:** "Connection refused", "No connection to MongoDB"

**Quick Fix:**
```bash
# Check MongoDB is running:
sudo systemctl status mongodb

# If not running:
sudo systemctl start mongodb

# Test connection:
mongo --eval "db.version()"
```

---

## 🎯 Deployment Best Practices

### Before Deploying ANY App:

#### 1. **Clean Slate Check**
```bash
# Remove all build artifacts:
cd /app/frontend
rm -rf node_modules/.cache build .next

cd /app/backend
find . -type d -name "__pycache__" -exec rm -rf {} +
```

#### 2. **Verify Dependencies**
```bash
# Frontend:
cd /app/frontend
yarn install --check-files

# Backend:
cd /app/backend
pip install -r requirements.txt --no-cache-dir
```

#### 3. **Test Locally First**
```bash
# Start services:
sudo supervisorctl restart backend frontend

# Wait 20 seconds, then test:
curl http://localhost:8001/api/
curl http://localhost:3000

# Check for errors:
tail -f /var/log/supervisor/frontend.err.log &
tail -f /var/log/supervisor/backend.err.log &
```

#### 4. **Only Deploy If All Tests Pass**
✅ Backend API responds
✅ Frontend loads without errors
✅ Database connection works
✅ All routes accessible

---

## 💰 Save Credits Checklist

### Before Starting Work:
- [ ] Create a checkpoint
- [ ] Note current working state
- [ ] Plan changes (write them down)

### During Development:
- [ ] Make small, incremental changes
- [ ] Test after every 2-3 file edits
- [ ] Use curl/simple tests before testing agent
- [ ] Check logs immediately after changes

### When Errors Occur:
- [ ] DON'T panic and make random changes
- [ ] Check logs first: `tail -n 50 /var/log/supervisor/*.log`
- [ ] Try simple restart: `sudo supervisorctl restart frontend`
- [ ] Use checkpoints to rollback if stuck

### Before Calling Testing Agent:
- [ ] Backend is running: `curl localhost:8001/api/`
- [ ] Frontend is running: `curl localhost:3000`
- [ ] No compilation errors in logs
- [ ] Basic functionality works

---

## 🔧 Emergency Commands Reference

### Quick Status Check
```bash
# All services status:
sudo supervisorctl status

# Frontend compilation status:
tail -20 /var/log/supervisor/frontend.out.log | grep -E "(Compiled|Failed)"

# Backend status:
curl http://localhost:8001/api/ || echo "Backend not responding"
```

### Quick Restart All
```bash
sudo supervisorctl restart all
sleep 20
curl -I http://localhost:3000
curl http://localhost:8001/api/
```

### Clear Everything and Start Fresh
```bash
# Frontend:
cd /app/frontend
rm -rf node_modules/.cache build
yarn install
sudo supervisorctl restart frontend

# Backend:
cd /app/backend
find . -type d -name "__pycache__" -exec rm -rf {} +
sudo supervisorctl restart backend
```

### Check What's Using Credits
- File operations: FREE
- Code generation: LOW cost
- Testing agent calls: MEDIUM cost
- Multiple large file changes: MEDIUM cost
- Integration agent calls: LOW cost
- Design agent calls: LOW cost

**Highest Credit Usage:**
- Testing agent with full E2E tests
- Multiple testing agent calls in succession
- Large file rewrites (500+ lines)

**Save Credits By:**
- Using curl for simple API tests
- Taking screenshots for visual checks
- Making smaller, targeted changes
- Reading logs instead of debugging with agent

---

## 📋 Deployment Troubleshooting Steps

### Step 1: Identify the Error
```bash
# Check frontend logs:
tail -100 /var/log/supervisor/frontend.err.log

# Check backend logs:
tail -100 /var/log/supervisor/backend.err.log

# Check compilation status:
curl -I http://localhost:3000
```

### Step 2: Common Solutions
**If Babel Error:**
```bash
cd /app/frontend
rm -rf node_modules/.cache
sudo supervisorctl restart frontend
```

**If Import Error:**
```bash
cd /app/frontend
yarn install
sudo supervisorctl restart frontend
```

**If Backend Error:**
```bash
cd /app/backend
pip install -r requirements.txt
sudo supervisorctl restart backend
```

### Step 3: Verify Fix
```bash
# Wait for services to start (20 seconds)
sleep 20

# Test:
curl http://localhost:8001/api/
curl -I http://localhost:3000

# Should both return 200 OK
```

### Step 4: If Still Broken
1. Check the specific error in logs
2. Fix the syntax error or missing import
3. Restart the service
4. Test again

---

## 🎓 Pro Tips to Avoid Issues

1. **Work in Phases**
   - Phase 1: Backend models and APIs
   - Phase 2: Frontend pages (one at a time)
   - Phase 3: Integration and testing
   - Test after each phase!

2. **Use Version Control Thinking**
   - Before big changes: Create checkpoint
   - After working feature: Create checkpoint
   - Stuck? Rollback to last checkpoint

3. **Debug Smartly**
   - Read error messages carefully
   - Check logs before making changes
   - Google the specific error
   - Use curl for API testing

4. **Communicate Clearly**
   - Be specific: "Fix login button on AuthPage"
   - Not vague: "Fix my app"
   - Provide error messages
   - Share what you've already tried

5. **When to Use Testing Agent**
   - After major feature completion
   - Before deployment
   - When you've fixed bugs and want to verify
   - NOT for every small change

---

## 📞 When You're Stuck

### Don't:
- ❌ Make random changes hoping it works
- ❌ Call testing agent repeatedly
- ❌ Delete entire directories
- ❌ Reinstall everything

### Do:
- ✅ Check logs for the actual error
- ✅ Try the simplest solution first
- ✅ Restart the specific service
- ✅ Create checkpoint before trying fixes
- ✅ Ask for help with specific error messages

---

## 🚀 Deployment Checklist Template

Copy this for every deployment:

```
[ ] Backend Dependencies Installed
    cd /app/backend && pip install -r requirements.txt

[ ] Frontend Dependencies Installed
    cd /app/frontend && yarn install

[ ] Environment Variables Set
    Check /app/backend/.env
    Check /app/frontend/.env

[ ] Database Seeded (if needed)
    python /app/backend/seed_db.py

[ ] Services Started
    sudo supervisorctl status all

[ ] Backend API Responding
    curl http://localhost:8001/api/

[ ] Frontend Loading
    curl -I http://localhost:3000

[ ] No Errors in Logs
    tail -50 /var/log/supervisor/frontend.err.log
    tail -50 /var/log/supervisor/backend.err.log

[ ] Basic Functionality Working
    Test one key feature manually

[ ] Ready for Full Testing
    Now call testing agent if needed
```

---

## 💡 Remember

**The goal is working software, not perfect software.**

- Start simple
- Test often
- Save frequently (checkpoints)
- Debug systematically
- Don't waste credits on guesswork

**Your credits are valuable - use them wisely!**
