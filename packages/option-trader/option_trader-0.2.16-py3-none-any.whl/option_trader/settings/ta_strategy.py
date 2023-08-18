import pandas_ta as ta

CustomStrategy = ta.Strategy(
    name="Momo and Volatility",
    description="BBANDS, RSI, MACD, MFI, TREND",
    ta=[
        {"kind": "bbands", "length": 20},      
        {"kind": "rsi"},
        {"kind": "macd", "fast": 12, "slow": 26},
        {"kind": "mfi", "period": 14}     
    ]
)      