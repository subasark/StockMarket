# Filtering stocks price below 500
    condition = stock_list['close'] < 500
    stock_list_filtered_df = stock_list[condition]
    # Only Taking NSE code name and Closing Price Of The Stock
    list_close_df = stock_list_filtered_df[['nsecode', 'close']]
    list_close_df.reset_index(drop=True, inplace=True)
    # Converting the DF to List
    nse_cd_list = stock_list_filtered_df['nsecode'].tolist()
    # Appening .NS for Yfinace query
    append_sufix_nsecode = '.NS'
    sufix_list = [sub + append_sufix_nsecode for sub in nse_cd_list]
    # Getting 50D MA Value of The stocks
    # Create an empty DataFrame to store the results
    data = []

    # Iterate through the list of stock names
    for stock_name in sufix_list:
        MV50 = si.get_data(stock_name, interval='1d')['close'][-50:].mean()
        data.append({'Stock': stock_name, 'MV50': MV50})

    # Create a DataFrame from the collected data
    df_MV = pd.DataFrame(data)

    result = list_close_df.join(df_MV)

    result['score'] = ((result['close'] - result['MV50']) / result['MV50']) * 100

    result_top_50 = result.sort_values(by='score', ascending=False).head(30)

    result_list = result_top_50['nsecode'].tolist()

    # Appening .NS for Yfinace query
    append_prefix_tvcode = ' NSE:'
    pre_res = [append_prefix_tvcode + sub for sub in result_list]

    file_path = "D:\list\stocks.txt"

    with open(file_path, "w") as file:
        # Iterate through the list
        for i, item in enumerate(pre_res):
            # Convert list items to strings and write them to the file
            if isinstance(item, list):
                # If the item is a list, join its elements with commas
                file.write(",".join(item))
            else:
                # Otherwise, directly write the item
                file.write(str(item))

            # Add comma unless it's the last element
            if i < len(pre_res) - 1:
                file.write(",")