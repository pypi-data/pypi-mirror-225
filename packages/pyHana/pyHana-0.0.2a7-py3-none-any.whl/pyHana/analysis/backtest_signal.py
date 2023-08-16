import pandas  as pd

def MACD(df, window_slow, window_fast, window_signal):
    macd = pd.DataFrame()
    macd['ema_slow'] = df['종가'].ewm(span=window_slow).mean()
    macd['ema_fast'] = df['종가'].ewm(span=window_fast).mean()
    macd['macd'] = macd['ema_slow'] - macd['ema_fast']
    macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
    macd['diff'] = macd['macd'] - macd['signal']
    macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
    macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
    
    return macd

def get_macd_trade_signal(macd):
    sig_list = []
    for idx, diff in enumerate(macd['diff']):
        if idx == 0:
            if diff > 0:
                sig_buy = 1
            elif diff < 0:
                sig_buy = -1
            else:
                sig_buy = -1

            sig_list.append(' ')
        else:
            if diff * sig_buy < 0:
                if diff > 0:
                    sig_buy = 1
                    sig_list.append('B')                
                else:
                    sig_buy = -1
                    sig_list.append('S')                
            else:
                sig_list.append(' ')       
    
#     for i in sig_list:
#         print(i)
    
    return sig_list