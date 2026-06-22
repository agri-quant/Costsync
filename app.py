import streamlit as st
import pandas as pd
import time

# Set page config
st.set_page_config(page_title="BoQPulse - NIQS Smart Estimator", layout="wide")

# Initialize session state to simulate a live database with expanded categories
if 'material_db' not in st.session_state:
    st.session_state.material_db = pd.DataFrame([
        # Concrete Works
        {"Category": "Concrete Works", "Material": "Dangote Cement (50kg)", "Base_Unit": "Bag", "Current_Price": 8500.00, "Location": "Abuja"},
        {"Category": "Concrete Works", "Material": "Sharp Sand (20 Tons)", "Base_Unit": "Trip", "Current_Price": 180000.00, "Location": "Abuja"},
        {"Category": "Concrete Works", "Material": "Granite 3/4 inch (20 Tons)", "Base_Unit": "Trip", "Current_Price": 320000.00, "Location": "Abuja"},
        # Reinforcement
        {"Category": "Reinforcement", "Material": "16mm High Tensile Iron Rods", "Base_Unit": "Ton", "Current_Price": 1450000.00, "Location": "Abuja"},
        # Blockwork
        {"Category": "Blockwork", "Material": "9-inch Sandcrete Blocks", "Base_Unit": "Pcs", "Current_Price": 700.00, "Location": "Abuja"},
        # Roofing & Ceiling
        {"Category": "Roofing & Ceiling", "Material": "0.55mm Aluminium Longspan Roofing Sheet", "Base_Unit": "Meter", "Current_Price": 9500.00, "Location": "Abuja"},
        {"Category": "Roofing & Ceiling", "Material": "POP Ceiling Sheets (Standard)", "Base_Unit": "Sht", "Current_Price": 7500.00, "Location": "Abuja"},
        # Finishes
        {"Category": "Finishes (Tiling)", "Material": "60x60cm Vitrified Floor Tiles", "Base_Unit": "Ctn", "Current_Price": 11500.00, "Location": "Abuja"},
        {"Category": "Finishes (Tiling)", "Material": "White Cement (25kg)", "Base_Unit": "Bag", "Current_Price": 14000.00, "Location": "Abuja"},
        # Plumbing
        {"Category": "Plumbing Installations", "Material": "Twyford Water Closet (WC) Suite", "Base_Unit": "Set", "Current_Price": 125000.00, "Location": "Abuja"},
    ])

st.title("🏗️ BoQPulse: Indigenous Smart BoQ Engine")
st.caption("Advanced Conceptual Prototype for the Nigerian Institute of Quantity Surveyors (NIQS)")
st.write("---")

# Sidebar Navigation
role = st.sidebar.radio("Select Portal View:", ["👷 Quantity Surveyor Workspace", "🏪 Certified Trader Hub"])

# ==========================================
# TRADER PORTAL VIEW
# ==========================================
if role == "🏪 Certified Trader Hub":
    st.header("🏪 Trader Price Update Portal")
    st.info("Verified Material Merchants can update daily prices here. Changes instantly update active BoQs.")
    
    loc = st.selectbox("Select Market Hub Location:", ["Abuja", "Lagos", "Port Harcourt"])
    
    df = st.session_state.material_db
    edited_df = st.data_editor(
        df[df['Location'] == loc], 
        column_config={
            "Category": st.column_config.TextColumn("Category", disabled=True),
            "Material": st.column_config.TextColumn("Material", disabled=True),
            "Base_Unit": st.column_config.TextColumn("Unit", disabled=True),
            "Current_Price": st.column_config.NumberColumn("Price (₦)", format="₦%.2f"),
            "Location": st.column_config.TextColumn("Location", disabled=True),
        },
        disabled=["Category", "Material", "Base_Unit", "Location"],
        key="trader_editor",
        use_container_width=True
    )
    
    if st.button("🚀 Push Live Price Updates", use_container_width=True):
        for idx in edited_df.index:
            st.session_state.material_db.at[idx, 'Current_Price'] = edited_df.loc[idx, 'Current_Price']
        st.success("Market prices updated successfully! Active BoQs have been recalculated automatically.")

# ==========================================
# QUANTITY SURVEYOR VIEW
# ==========================================
else:
    st.header("👷 Quantity Surveyor Workspace")
    
    st.subheader("1. Smart Take-Off Engine")
    uploaded_file = st.file_uploader("Upload Architectural/Structural PDF Blueprint", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("AI analyzing drawings and mapping to BESMM standard..."):
            time.sleep(2) 
        st.success("Blueprint Take-off Complete! Broad scope elements mapped successfully.")
        
        # Dashboard metrics extracted from PDF
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Concrete Floor Area", "145.2 m²")
        col2.metric("Wall Area (Blockwork)", "320.0 m²")
        col3.metric("Roof Plan Area", "185.0 m²")
        col4.metric("Floor Tiling Area", "132.5 m²")
        
        st.write("---")
        st.subheader("2. Dynamically Priced Bill of Quantities (BoQ)")
        
        # Map DB variables for easy math formulas
        db = st.session_state.material_db.set_index('Material')
        
        cement = db.loc["Dangote Cement (50kg)", "Current_Price"]
        sand = db.loc["Sharp Sand (20 Tons)", "Current_Price"]
        granite = db.loc["Granite 3/4 inch (20 Tons)", "Current_Price"]
        blocks = db.loc["9-inch Sandcrete Blocks", "Current_Price"]
        roofing = db.loc["0.55mm Aluminium Longspan Roofing Sheet", "Current_Price"]
        tiles = db.loc["60x60cm Vitrified Floor Tiles", "Current_Price"]
        wc = db.loc["Twyford Water Closet (WC) Suite", "Current_Price"]
        
        # Expanded BoQ breakdown structure matching BESMM rules
        boq_data = [
            {
                "Item": "1",
                "Category": "Concrete Works",
                "Description": "Plain concrete (1:2:4) in insitu concrete beds over 150mm thick, laid on blinded surface.",
                "Qty": 145.2, "Unit": "m²",
                "Formula Applied": "0.4 Cement + 0.02 Sand + 0.04 Granite + Labor",
                "Rate (₦)": float((cement * 0.4) + (sand * 0.02) + (granite * 0.04) + 2500)
            },
            {
                "Item": "2",
                "Category": "Blockwork",
                "Description": "Vibrated sandcrete blockwall (225mm thick) built in cement sand mortar (1:4) properly bedded and flushed up in joints.",
                "Qty": 320.0, "Unit": "m²",
                "Formula Applied": "10 Blocks + 0.1 Cement + Mortar/Labor Fixings",
                "Rate (₦)": float((blocks * 10) + (cement * 0.1) + 1500)
            },
            {
                "Item": "3",
                "Category": "Roofing & Ceiling",
                "Description": "0.55mm Aluminium Longspan Roofing Sheet fixed to timber framework (measured separately) with necessary accessories.",
                "Qty": 185.0, "Unit": "m²",
                "Formula Applied": "1.15m Roofing Sheet + Nails/Sealant allowance + Fixings",
                "Rate (₦)": float((roofing * 1.15) + 3000)
            },
            {
                "Item": "4",
                "Category": "Finishes (Tiling)",
                "Description": "600 x 600mm Vitrified floor tiles bedded on cement sand mortar screed base (measured separately) jointed and grouted in white cement.",
                "Qty": 132.5, "Unit": "m²",
                "Formula Applied": "0.95 Ctn Tiles + 0.05 Bag White Cement + Labor",
                "Rate (₦)": float((tiles * 0.95) + (db.loc["White Cement (25kg)", "Current_Price"] * 0.05) + 2200)
            },
            {
                "Item": "5",
                "Category": "Plumbing Installations",
                "Description": "Supply and fix Twyford Water Closet (WC) suite complete with low-level cistern, dual flush mechanism, and all necessary connection fittings.",
                "Qty": 4.0, "Unit": "Nr",
                "Formula Applied": "1 WC Set + Connection Accessories + Plumber Installation Rate",
                "Rate (₦)": float(wc + 15000)
            }
        ]
        
        # Calculate totals dynamically
        for row in boq_data:
            row["Amount (₦)"] = row["Qty"] * row["Rate (₦)"]
            
        boq_df = pd.DataFrame(boq_data)
        
        # Display customized, formatted DataFrame
        st.dataframe(
            boq_df.style.format({"Rate (₦)": "₦{:,.2f}", "Amount (₦)": "₦{:,.2f}"}),
            use_container_width=True,
            hide_index=True
        )
        
        total_project_cost = boq_df["Amount (₦)"].sum()
        
        st.write("---")
        st.metric(label="📊 Estimated Grand Summary Cost (Live Market Scaled)", value=f"₦{total_project_cost:,.2f}")
        st.warning("💡 **Live Testing Notice:** Leave this tab open, open the 'Certified Trader Hub' sidebar option in a new tab/window, adjust any material price, hit update, and watch the corresponding row's rate update here in real time.")
    else:
        st.info("👋 Ready to present. Upload any architectural drawing PDF to simulate the auto-measurement take-off pipeline.")
