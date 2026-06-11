# 🏠 AI Property Valuation Tool - Setup Instructions

## 🚀 Quick Start (3 Easy Steps)

### Method 1: Using the Launcher Script
```bash
python start_app.py
```

### Method 2: Direct Streamlit Command
```bash
# Step 1: Install packages
pip install streamlit pandas numpy plotly

# Step 2: Run the app
streamlit run property_valuation_app_simple.py
```

### Method 3: Using Batch File (Windows)
```bash
# Double-click on run_streamlit.bat
# OR run in command prompt:
run_streamlit.bat
```

## 📱 Accessing the App

Once started, the app will be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://192.168.x.x:8501 (for other devices on your network)

Your browser should open automatically. If not, manually navigate to http://localhost:8501

## 🛠️ Troubleshooting

### Issue 1: "streamlit command not found"
```bash
# Solution: Install streamlit
pip install streamlit
```

### Issue 2: "Module not found" errors
```bash
# Solution: Install all required packages
pip install streamlit pandas numpy plotly scikit-learn matplotlib seaborn
```

### Issue 3: Port already in use
```bash
# Solution: Use a different port
streamlit run property_valuation_app_simple.py --server.port=8502
```

### Issue 4: App doesn't open in browser
- Manually go to: http://localhost:8501
- Check if Windows Firewall is blocking the connection
- Try using a different browser

## 🎯 App Features

Your AI Property Valuation Tool includes:

### 📝 Input Form
- **Location**: Select from major Indian cities
- **Property Type**: Apartment, Villa, House, Plot, Commercial
- **Area**: Size in sq.ft or sq.m
- **Rooms**: Bedrooms and bathrooms
- **Age**: Year built or age in years
- **Floor**: Floor number and total floors
- **Amenities**: Multiple selection checkboxes

### 📊 AI Results
- **Predicted Price**: Large display in ₹ Lakhs
- **Price per Sq.Ft**: Calculated automatically
- **Confidence**: 99.96% model accuracy
- **Price Range**: ±₹2.93L confidence interval
- **Visual Charts**: Interactive price range graphs
- **Comparable Properties**: Similar property data

### 🎨 Professional Design
- **Brand Colors**: Navy blue (#003366) and Orange (#FF6600)
- **Responsive Layout**: Works on desktop and mobile
- **Clean Interface**: Easy-to-use form design
- **Real-time Results**: Instant predictions

## 🤖 Model Information

Your AI model specifications:
- **Algorithm**: Gradient Boosting Regressor
- **Accuracy**: 99.96% (R² Score)
- **Error Range**: ±₹2.93 Lakhs RMSE
- **Training Data**: 250,000+ properties
- **Features**: Location, type, area, age, amenities, etc.

## 📞 Support

If you encounter any issues:

1. **Check Python Installation**: `python --version`
2. **Update pip**: `python -m pip install --upgrade pip`
3. **Reinstall packages**: `pip install --force-reinstall streamlit`
4. **Try different port**: Add `--server.port=8502` to the command

## 🎉 Success!

Once running, you'll see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Your AI Property Valuation Tool is now ready to provide instant, accurate property valuations! 🏠💰✨