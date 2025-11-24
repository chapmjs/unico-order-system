# UniCo Plant - Due Date Performance & Promise System

A simple order management system based on Theory of Constraints principles from "The Goal" by Eliyahu Goldratt.

## What This App Does

1. **Order Dashboard** - Visualize all orders with real-time status and risk levels
2. **Promise Calculator** - Calculate realistic delivery dates based on bottleneck capacity
3. **Order Management** - Track order progress and update statuses
4. **Analytics** - Monitor bottleneck utilization and forecast capacity needs

## Key Principles from "The Goal"

- Manages by the constraint (bottleneck) not by local efficiencies
- Prevents unrealistic promises that lead to late deliveries
- Shows true capacity-based lead times
- Protects bottleneck time as the most valuable resource

## Quick Start - Run Locally

```bash
pip install -r requirements.txt
streamlit run due_date_app.py
```

The app will open in your browser at http://localhost:8501

## Deploy for FREE in Under 30 Minutes

### Option 1: Streamlit Community Cloud (Recommended - Easiest!)

**Time: 10-15 minutes**

1. **Create a GitHub account** (if you don't have one): https://github.com

2. **Create a new repository:**
   - Go to https://github.com/new
   - Name it: `unico-order-system`
   - Make it Public
   - Click "Create repository"

3. **Upload files to GitHub:**
   - Click "uploading an existing file"
   - Drag and drop these files:
     - `due_date_app.py`
     - `requirements.txt`
     - `README.md`
   - Click "Commit changes"

4. **Deploy to Streamlit Cloud:**
   - Go to: https://share.streamlit.io
   - Click "Sign in with GitHub"
   - Click "New app"
   - Select your repository: `unico-order-system`
   - Main file path: `due_date_app.py`
   - Click "Deploy!"

5. **Done!** Your app will be live at: `https://[your-username]-unico-order-system.streamlit.app`

### Option 2: Hugging Face Spaces

**Time: 15-20 minutes**

1. **Create account**: https://huggingface.co/join
2. **Create new Space**: https://huggingface.co/new-space
3. Select "Streamlit" as SDK
4. Upload files
5. Your app will deploy automatically!

### Option 3: Railway.app

**Time: 15-20 minutes**

1. Go to: https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Railway will auto-detect Streamlit and deploy

## Features

### Dashboard Tab
- Real-time order status visualization
- Progress tracking with color-coded risk levels
- Order health metrics
- Bottleneck queue visibility

### Promise Calculator Tab
- Input new order details
- Automatic bottleneck time calculation
- Capacity-based promise date calculation
- Feasibility check against customer requests
- Built-in 20% buffer (safety margin)

### Order Details Tab
- Complete order listing with risk assessment
- Update order status and progress
- Export capabilities

### Analytics Tab
- Weekly bottleneck utilization forecast
- Customer order distribution
- Capacity planning visualization

## Understanding the Data

**Key Metrics:**
- **Bottleneck Hours**: Time required at the constraint (NCX-10 machine)
- **Capacity**: 16 hours/day (2 shifts minus setup time)
- **Buffer**: 20% safety margin for realistic promises

**Order Status Colors:**
- 🟢 Green: On track (>7 days until due)
- 🟠 Orange: At risk (<7 days until due)
- 🔴 Red: Late (past due date)

## Customization

You can easily customize:
- `BOTTLENECK_HOURS_PER_DAY`: Adjust for your shift schedule
- Product processing times in the hours_per_unit dictionary
- Buffer percentage (currently 1.2 = 20%)
- Number of bottleneck resources

## Theory of Constraints Background

This app implements concepts from Eliyahu Goldratt's "The Goal":

1. **Identify the constraint** - The bottleneck machine that limits throughput
2. **Exploit the constraint** - Never let it sit idle
3. **Subordinate everything else** - Make promises based on constraint capacity
4. **Elevate the constraint** - Add capacity only where it matters

The app helps avoid Alex Rogo's mistakes:
- ❌ Making promises without checking bottleneck capacity
- ❌ Running machines for "efficiency" instead of need
- ❌ Expediting everything (which means nothing is truly expedited)

## License

Free to use and modify for educational and commercial purposes.
