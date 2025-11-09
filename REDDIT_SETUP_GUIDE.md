# Reddit API Setup Guide

## ❌ Current Issue: 401 Unauthorized Error

Your credentials are properly formatted, but Reddit is rejecting them with a 401 error. This usually means one of these issues:

## 🔧 How to Fix

### Step 1: Verify Your Reddit App Settings

1. Go to: https://www.reddit.com/prefs/apps
2. Find your app in the list
3. **CRITICAL**: Make sure the app type is **"script"** (not "web app" or "installed app")

If it's not a script app:
- You'll need to create a NEW app
- Select "script" as the type
- Fill in the required fields (name, description, redirect uri can be http://localhost:8080)

### Step 2: Get the Correct Credentials

When you look at your app on https://www.reddit.com/prefs/apps, you'll see:

```
[App Name]
personal use script
[THIS IS YOUR CLIENT_ID - 14 characters under the app name]

secret: [THIS IS YOUR CLIENT_SECRET - click 'edit' to see it]
```

**CLIENT_ID**: The string of characters directly under your app name (usually 14-22 characters)
**CLIENT_SECRET**: The long string next to "secret:" (usually 27-30 characters)

### Step 3: Update Your .env File

Your .env file should look EXACTLY like this (no spaces, no quotes):

```
REDDIT_CLIENT_ID=YourActualClientID
REDDIT_CLIENT_SECRET=YourActualClientSecret
REDDIT_USER_AGENT=SentimentAnalysis/1.0
```

### Step 4: Test Again

Run this command to test:
```bash
source venv/bin/activate
python3 check_credentials.py
```

## 📋 Common Mistakes

1. ❌ **Wrong app type**: Must be "script", not "web app"
2. ❌ **Copied wrong ID**: The client ID is UNDER the app name, not the app name itself
3. ❌ **Extra spaces**: No spaces before or after the = sign
4. ❌ **Quotes included**: Don't put quotes around the values
5. ❌ **Old credentials**: If you recreated the app, you need new credentials

## ✅ What Your Credentials Should Look Like

Based on the check, your current credentials are:
- Client ID: 19 characters (starts with "Comfo")
- Client Secret: 30 characters (starts with "FVZlK")

These lengths look reasonable, but the values might be incorrect.

## 🔍 Double-Check Checklist

- [ ] App type is "script" on Reddit
- [ ] Client ID is the text UNDER the app name
- [ ] Client Secret is from the "secret:" field
- [ ] No extra spaces in .env file
- [ ] No quotes around values in .env file
- [ ] Saved the .env file after editing

## 🆘 Still Not Working?

If you've verified everything above and it still doesn't work:

1. **Create a completely new Reddit app**:
   - Go to https://www.reddit.com/prefs/apps
   - Click "create another app"
   - Name: "SentimentAnalysis"
   - Type: **"script"** (IMPORTANT!)
   - Description: "Sentiment analysis tool"
   - Redirect URI: http://localhost:8080
   - Click "create app"

2. **Get the NEW credentials**:
   - Client ID: The text under the app name
   - Client Secret: Click "edit" to see it

3. **Update .env with the NEW credentials**

4. **Test again**:
   ```bash
   python3 check_credentials.py
   ```

## 📞 Need More Help?

Check the Reddit API documentation:
https://github.com/reddit-archive/reddit/wiki/OAuth2

Or the PRAW documentation:
https://praw.readthedocs.io/en/stable/getting_started/authentication.html
