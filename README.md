# twitter-igor

## To Get Data
- add your .env
- `cd src`
- `python main.py`

## To Display Data
- `cd src`
- `streamlit run app.py`

### To Display Data (Custom)
```
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
```