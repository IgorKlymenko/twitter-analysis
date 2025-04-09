import streamlit as st
import pandas as pd
import api

api = api.Api()

# Streamlit App
st.title("📊 Download and View Filtered Data")

# Create filter controls in sidebar for better organization
st.sidebar.header("Filter Options")
canadian_selected = st.sidebar.checkbox("Show Canadian", value=False)
founder_selected = st.sidebar.checkbox("Show Founder", value=False)

# Main content area
st.write("Current filters:")
st.write(f"- Canadian: {'✅' if canadian_selected else '❌'}")
st.write(f"- Founder: {'✅' if founder_selected else '❌'}")

# Fetch and display data based on filters
with st.spinner("Fetching data..."):
    # Call RPC to fetch filtered data
    response = api.supabase.rpc(
        "filter_final_data", 
        {"canadian_param": canadian_selected, "founder_param": founder_selected}
    ).execute()
    
    data = response.data
    
    if not data:
        st.info("No data found based on the selected filters.")
    else:
        # Convert to DataFrame for visualization
        df = pd.DataFrame(data)
        
        # Display data count
        st.subheader(f"Found {len(df)} records")
        
        # Display the DataFrame
        st.dataframe(df, use_container_width=True)
        
        # Provide download option with unique key
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"filtered_data_canadian_{canadian_selected}_founder_{founder_selected}.csv",
            mime="text/csv",
            key=f"download_{canadian_selected}_{founder_selected}"
        )