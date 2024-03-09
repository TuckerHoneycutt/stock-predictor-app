import streamlit as st
import pandas as pd
import datetime
from scipy import stats
import yfinance as yf

def initialize_paths():
    now = datetime.datetime.now()
    return now

def load_ticker_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="max")
    return hist

def calculate_djia_delta(df_DJIA):
    for ii in range(1, len(df_DJIA.index)):
        DJI_Close_yesterday = float(df_DJIA['Close'][ii-1])
        DJI_Close_today = float(df_DJIA['Close'][ii])
        df_DJIA.at[df_DJIA.index[ii], 'DJI_DeltaPct'] = DJI_Close_today / DJI_Close_yesterday
    return df_DJIA

def calculate_1day_metrics(data, dX):
    dX['Open'] = data.Open
    dX['High'] = data.High
    dX['Low'] = data.Low
    dX['Close'] = data.Close
    dX['Average'] = (data.High + data.Low) / 2.
    dX['Range'] = data.High - data.Low
    convert_array = [int(val) for val in data['Volume']]
    dX['Volume'] = convert_array
    return dX

def calculate_trend_averages(data, dX):
    dX = calculate_ta5(data, dX)
    dX = calculate_ta10(data, dX)
    dX = calculate_ta20(data, dX)
    dX = calculate_ta60(data, dX)
    dX = calculate_ta_ratios(dX, data)
    return dX

def calculate_ta5(data, dX):
    for ii in range(4, len(data.index)):
        day_index = range(ii-3, ii+2)
        Values_5days = dX['Average'][ii-4:ii+1]
        M, b, r, p, err = stats.linregress(day_index, Values_5days)
        Pred_tomorrow = M * (ii+2) + b
        dX.at[data.index[ii], 'TA5'] = Pred_tomorrow
    return dX

def calculate_ta10(data, dX):
    for ii in range(9, len(data.index)):
        day_index = range(ii-8, ii+2)
        Values_10days = dX['Average'][ii-9:ii+1]
        M, b, r, p, err = stats.linregress(day_index, Values_10days)
        Pred_tomorrow = M * (ii+2) + b
        dX.at[data.index[ii], 'TA10'] = Pred_tomorrow
    return dX

def calculate_ta20(data, dX):
    for ii in range(19, len(data.index)):
        day_index = range(ii-18, ii+2)
        Values_20days = dX['Average'][ii-19:ii+1]
        M, b, r, p, err = stats.linregress(day_index, Values_20days)
        Pred_tomorrow = M * (ii+2) + b
        dX.at[data.index[ii], 'TA20'] = Pred_tomorrow
    return dX

def calculate_ta60(data, dX):
    for ii in range(59, len(data.index)):
        day_index = range(ii-58, ii+2)
        Values_60days = dX['Average'][ii-59:ii+1]
        M, b, r, p, err = stats.linregress(day_index, Values_60days)
        Pred_tomorrow = M * (ii+2) + b
        dX.at[data.index[ii], 'TA60'] = Pred_tomorrow
    return dX

def calculate_ta_ratios(dX, data):
    for ii in range(9, 19):
        dX.at[data.index[ii], 'TA5_10'] = dX.TA5[ii] / dX.TA10[ii]
    for ii in range(19, 59):
        dX.at[data.index[ii], 'TA5_10'] = dX.TA5[ii] / dX.TA10[ii]
        dX.at[data.index[ii], 'TA10_20'] = dX.TA10[ii] / dX.TA20[ii]
    for ii in range(59, len(data.index)):
        dX.at[data.index[ii], 'TA5_10'] = dX.TA5[ii] / dX.TA10[ii]
        dX.at[data.index[ii], 'TA10_20'] = dX.TA10[ii] / dX.TA20[ii]
        dX.at[data.index[ii], 'TA20_60'] = dX.TA20[ii] / dX.TA60[ii]
    return dX

def calculate_streak_metrics(data, dX):
    dX['Streak_Low'] = 0
    dX['Streak_High'] = 0
    for ii in range(6, len(data.index)):
        dX = calculate_low_streaks(data, dX, ii)
        dX = calculate_high_streaks(data, dX, ii)
    return dX

def calculate_low_streaks(data, dX, ii):
    if (data.Low[ii] > data.Low[ii-1]) and (data.Low[ii-1] > data.Low[ii-2]):
        dX.at[data.index[ii], 'Streak_Low'] = 2
        if (data.Low[ii-2] > data.Low[ii-3]):
            dX.at[data.index[ii], 'Streak_Low'] = 3
            if (data.Low[ii-3] > data.Low[ii-4]):
                dX.at[data.index[ii], 'Streak_Low'] = 4
                if (data.Low[ii-4] > data.Low[ii-5]):
                    dX.at[data.index[ii], 'Streak_Low'] = 5
                    if (data.Low[ii-5] > data.Low[ii-6]):
                        dX.at[data.index[ii], 'Streak_Low'] = 6
    elif (data.Low[ii] < data.Low[ii-1]) and (data.Low[ii-1] < data.Low[ii-2]):
        dX.at[data.index[ii], 'Streak_Low'] = -2
        if (data.Low[ii-2] < data.Low[ii-3]):
            dX.at[data.index[ii], 'Streak_Low'] = -3
            if (data.Low[ii-3] < data.Low[ii-4]):
                dX.at[data.index[ii], 'Streak_Low'] = -4
                if (data.Low[ii-4] < data.Low[ii-5]):
                    dX.at[data.index[ii], 'Streak_Low'] = -5
                    if (data.Low[ii-5] < data.Low[ii-6]):
                        dX.at[data.index[ii], 'Streak_Low'] = -6
    return dX

def calculate_high_streaks(data, dX, ii):
    if (data.High[ii] > data.High[ii-1]) and (data.High[ii-1] > data.High[ii-2]):
        dX.at[data.index[ii], 'Streak_High'] = 2
        if (data.High[ii-2] > data.High[ii-3]):
            dX.at[data.index[ii], 'Streak_High'] = 3
            if (data.High[ii-3] > data.High[ii-4]):
                dX.at[data.index[ii], 'Streak_High'] = 4
                if (data.High[ii-4] > data.High[ii-5]):
                    dX.at[data.index[ii], 'Streak_High'] = 5
                    if (data.High[ii-5] > data.High[ii-6]):
                        dX.at[data.index[ii], 'Streak_High'] = 6
    elif (data.High[ii] < data.High[ii-1]) and (data.High[ii-1] < data.High[ii-2]):
        dX.at[data.index[ii], 'Streak_High'] = -2
        if (data.High[ii-2] < data.High[ii-3]):
            dX.at[data.index[ii], 'Streak_High'] = -3
            if (data.High[ii-3] < data.High[ii-4]):
                dX.at[data.index[ii], 'Streak_High'] = -4
                if (data.High[ii-4] < data.High[ii-5]):
                    dX.at[data.index[ii], 'Streak_High'] = -5
                    if (data.High[ii-5] < data.High[ii-6]):
                        dX.at[data.index[ii], 'Streak_High'] = -6
    return dX

def calculate_jump_gap_metrics(data, dX):
    for ii in range(1, len(data.index)):
        if data.Low[ii] > data.High[ii-1]:
            dX.at[data.index[ii], 'JumpUp'] = 1
        elif data.High[ii] < data.Low[ii-1]:
            dX.at[data.index[ii], 'JumpDown'] = 1
        elif data.Open[ii] > data.High[ii-1]:
            dX.at[data.index[ii], 'GapUp'] = 1
        elif data.Open[ii] < data.Low[ii-1]:
            dX.at[data.index[ii], 'GapDown'] = 1
    return dX

def calculate_relational_metrics(data, dX, df_DJIA):
    dX['Close_PctOfRange'] = (data.Close - data.Low) / dX.Range
    dX['Close_TA5'] = data.Close / dX.TA5
    dX['Close_TA10'] = data.Close / dX.TA10
    dX['Close_TA20'] = data.Close / dX.TA20
    dX['Close_TA60'] = data.Close / dX.TA60
    dX['Close_TA5_TA10'] = data.Close / dX.TA5_10
    dX['DowDelta'] = df_DJIA.DJI_DeltaPct
    return dX

def calculate_multiday_metrics(data, dX):
    for ii in range(len(data.index)):
        dX.at[data.index[ii], 'H5'] = data.iloc[ii+1:ii+6]['High'].max()
        dX.at[data.index[ii], 'H10'] = data.iloc[ii+1:ii+11]['High'].max()
        dX.at[data.index[ii], 'H20'] = data.iloc[ii+1:ii+21]['High'].max()
    return dX

def calculate_metrics(data, df_DJIA):
    dX = pd.DataFrame()
    dX = calculate_1day_metrics(data, dX)
    dX = calculate_trend_averages(data, dX)
    dX = calculate_streak_metrics(data, dX)
    dX = calculate_jump_gap_metrics(data, dX)
    dX = calculate_relational_metrics(data, dX, df_DJIA)
    dX = calculate_multiday_metrics(data, dX)
    return dX

def main():
    st.title("Stock Data Analysis")
    ticker_input = st.text_input("Enter stock ticker symbol(s):", "")
    submit_button = st.button("Submit")

    if submit_button:
        tickers = [ticker.strip().upper() for ticker in ticker_input.split()]

        for ticker in tickers:
            data = load_ticker_data(ticker)
            data = calculate_djia_delta(data)

            dX = calculate_metrics(data, data)

            now = initialize_paths()
            file_path = f"stock_data_{ticker}_{now.strftime('%Y%m%d_%H%M%S')}.csv"
            dX.to_csv(file_path)
            st.success(f"Data for {ticker} saved to {file_path}")

if __name__ == "__main__":
    main()
