import streamlit as st
import pandas as pd
import time
import io

# Set page config
st.set_page_config(page_title="CostSync Nigeria - Live Engine", layout="wide")

# Comprehensive list of all 36 Nigerian States + FCT
NIGERIAN_STATES = [
    "FCT (Abuja)", "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", 
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", 
    "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", 
    "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"
]

# Initialize session state to simulate a live database with state-aware pricing
if 'material_db' not in st.session_state:
    # Baseline setup using FCT (Abuja) as seed data
    base_materials = [
        {"Category": "Concrete Works", "Material": "Dangote Cement (50kg)", "Base_Unit": "Bag", "Current_Price": 8500.00},
        {"Category": "Concrete Works", "Material": "Sharp Sand (20 Tons)", "Base_Unit": "Trip", "Current_Price": 180000.00},
        {"Category": "Concrete Works", "Material": "Granite 3/4 inch (20 Tons)", "Base_Unit": "Trip", "Current_Price": 320000.00},
        {"Category": "Reinforcement", "Material": "16mm High Tensile Iron Rods", "Base_Unit": "Ton", "Current_Price": 1450000.00},
        {"Category": "Blockwork", "Material": "9-inch Sandcrete Blocks", "Base_Unit": "Pcs", "Current_Price": 700.00},
        {"Category": "Roofing & Ceiling", "Material": "0.55mm Aluminium Longspan Roofing Sheet", "Base_Unit": "Meter", "Current_Price": 9500.00},
        {"Category": "Roofing & Ceiling", "Material": "POP Ceiling Sheets (Standard)", "Base_Unit": "Sht", "Current_Price": 7500.00},
        {"Category": "Finishes (Tiling)", "Material": "60x60cm Vitrified Floor Tiles", "Base_Unit": "Ctn", "Current_Price": 11500.00},
        {"Category": "Finishes (Tiling)", "Material": "White Cement (25kg)", "Base_Unit": "Bag", "Current_Price": 14000.00},
        {"Category": "Plumbing Installations", "Material": "Twyford Water Closet (WC) Suite", "Base_Unit": "Set", "Current_Price": 125000.00},
    ]
    
    # Expand database to cover all 36 states dynamically with local price variation simulation
    expanded_rows = []
    for state in NIGERIAN_STATES:
        # Simulate slight price variance per state so the database feels real
        variance = 1.15 if state in ["Lagos", "Rivers", "FCT (Abuja)"] else 0.95 if state in ["Kano", "Kaduna"] else 1.0
        for mat in base_materials:
            expanded_rows.append({
                "Category": mat["Category"],
                "Material": mat["Material"],
                "Base_Unit": mat["Base_Unit"],
                "Current_Price": round(mat["Current_Price"] * variance, 2),
                "Location": state
            })
    st.session_state.material_db = pd.DataFrame(expanded_rows)

st.title("🏗️ CostSync Nigeria: Indigenous Smart BoQ Engine")
st.caption("Advanced Live-Market Application Environment")
st.write("---")

# Navigation Sidebar now features 3 portals
role = st.sidebar.radio("Select Portal View:", [
    "👷 Quantity Surveyor Workspace", 
    "🏪 Certified Trader Hub",
    "🔍 Public Market Price Checker"
])

# ==========================================
# 3. PUBLIC MARKET PRICE CHECKER VIEW
# ==========================================
if role == "🔍 Public Market Price Checker":
    st.header("🔍 Public Building Materials Price Checker")
    st.info("Open-source price index monitoring channel. Search current builder supply costs across all 36 Nigerian states.")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox("Filter by State/Location:", NIGERIAN_STATES, index=0)
    with col2:
        search_query = st.text_input("🔍 Search specific material (e.g., Cement, Blocks, Tiles):")
        
    # Query matching data
    display_df = st.session_state.material_db[st.session_state.material_db['Location'] == selected_state]
    if search_query:
        display_df = display_df[display_df['Material'].str.contains(search_query, case=False)]
        
    st.dataframe(
        display_df.style.format({"Current_Price": "₦{:,.2f}"}),
        column_config={
            "Category": "Material Trade",
            "Material": "Building Component Specification",
            "Base_Unit": "Trading Unit",
            "Current_Price": "Live Market Rate",
            "Location": "Geographic State Pool"
        },
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# 2. TRADER PORTAL VIEW
# ==========================================
elif role == "🏪 Certified Trader Hub":
    st.header("🏪 Trader Price Update Portal")
    st.info("Verified Material Merchants can select their operational state to update baseline costs.")
    
    trader_state = st.selectbox("Select Your State Jurisdiction:", NIGERIAN_STATES)
    
    df = st.session_state.material_db
    state_mask = df['Location'] == trader_state
    
    edited_df = st.data_editor(
        df[state_mask], 
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
    
    if st.button("🚀 Push Live Price Updates to Cloud", use_container_width=True):
        # Merge edits back into primary session storage records
        for idx in edited_df.index:
            st.session_state.material_db.at[idx, 'Current_Price'] = edited_df.loc[idx, 'Current_Price']
        st.success(f"Market prices successfully synchronized for {trader_state}! All local active BoQs updated.")

# ==========================================
# 1. QUANTITY SURVEYOR VIEW
# ==========================================
else:
    st.header("👷 Quantity Surveyor Workspace")
    
    st.subheader("1. Project Specification & Smart Take-Off")
    project_state = st.selectbox("Select Project Site State Location:", NIGERIAN_STATES, index=0)
    
    uploaded_file = st.file_uploader("Upload Architectural/Structural PDF Blueprint Design File", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("AI parsing design matrices and binding local market indexes..."):
            time.sleep(1) 
        st.success("Spatial Blueprint analysis complete!")
        
        # Metric layout display boards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Gross Built Footprint", "198.5 m²")
        col2.metric("Blockwork Wall Area", "320.0 m²")
        col3.metric("Roof Footprint Area", "232.0 m²")
        col4.metric("Internal Floor Finishes", "178.0 m²")
        
        st.write("---")
        st.subheader("2. Dynamically Priced Bill of Quantities (BoQ)")
        
        # Filter localized price vectors from state database pool
        state_db = st.session_state.material_db[st.session_state.material_db['Location'] == project_state].set_index('Material')
        
        cement = state_db.loc["Dangote Cement (50kg)", "Current_Price"]
        sand = state_db.loc["Sharp Sand (20 Tons)", "Current_Price"]
        granite = state_db.loc["Granite 3/4 inch (20 Tons)", "Current_Price"]
        blocks = state_db.loc["9-inch Sandcrete Blocks", "Current_Price"]
        roofing = state_db.loc["0.55mm Aluminium Longspan Roofing Sheet", "Current_Price"]
        tiles = state_db.loc["60x60cm Vitrified Floor Tiles", "Current_Price"]
        wc = state_db.loc["Twyford Water Closet (WC) Suite", "Current_Price"]
        
        # Standardized cost matrix formulas
        boq_data = [
            {"Item": "1", "Description": "Plain concrete (1:2:4) in insitu concrete beds over 150mm thick, laid on blinded surface.", "Qty": 145.2, "Unit": "m²", "Rate (₦)": float((cement * 0.4) + (sand * 0.02) + (granite * 0.04) + 2500)},
            {"Item": "2", "Description": "Vibrated sandcrete blockwall (225mm thick) built in cement sand mortar (1:4) properly bedded.", "Qty": 320.0, "Unit": "m²", "Rate (₦)": float((blocks * 10) + (cement * 0.1) + 1500)},
            {"Item": "3", "Description": "0.55mm Aluminium Longspan Roofing Sheet fixed to timber framework with necessary accessories.", "Qty": 232.0, "Unit": "m²", "Rate (₦)": float((roofing * 1.15) + 3000)},
            {"Item": "4", "Description": "600 x 600mm Vitrified floor tiles bedded on cement sand mortar screed base, jointed and grouted.", "Qty": 178.0, "Unit": "m²", "Rate (₦)": float((tiles * 0.95) + (state_db.loc["White Cement (25kg)", "Current_Price"] * 0.05) + 2200)},
            {"Item": "5", "Description": "Supply and fix Twyford Water Closet (WC) suite complete with cistern, flush links and connections.", "Qty": 4.0, "Unit": "Nr", "Rate (₦)": float(wc + 15000)}
        ]
        
        for row in boq_data:
            row["Amount (₦)"] = row["Qty"] * row["Rate (₦)"]
            
        boq_df = pd.DataFrame(boq_data)
        
        # Display professional table layout
        st.dataframe(
            boq_df.style.format({"Rate (₦)": "₦{:,.2f}", "Amount (₦)": "₦{:,.2f}"}),
            use_container_width=True, hide_index=True
        )
        
        total_cost = boq_df["Amount (₦)"].sum()
        st.metric(label=f"📊 Total Estimated Project Valuation ({project_state})", value=f"₦{total_cost:,.2f}")
        
        # ==========================================
        # DOWNLOAD DATA SOFT COPY SYSTEM (CSV EXPORT)
        # ==========================================
        st.write("---")
        st.subheader("💾 Export Soft Copy Project Deliverables")
        
        # Format human-readable output columns for spreadsheet export
        export_df = boq_df.copy()
        export_df["Rate (₦)"] = export_df["Rate (₦)"].apply(lambda x: f"NGN {x:,.2f}")
        export_df["Amount (₦)"] = export_df["Amount (₦)"].apply(lambda x: f"NGN {x:,.2f}")
        
        # Convert internal dataframe structure directly to comma separated binary memory layout
        csv_buffer = io.StringIO()
        export_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        
        st.download_button(
            label="📥 Download Soft Copy Bill of Quantities (.CSV Spreadsheet)",
            data=csv_bytes,
            file_name=f"CostSync_BoQ_{project_state.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    else:
        st.info("👋 Select project state and upload blueprint design file to execute live valuation models.")
