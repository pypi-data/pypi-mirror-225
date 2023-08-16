import pandas    as pd
import random
from   ..innerIO import stockInfo  as sd


def backtesting(maxItemNum = 20, cashAmt = 100000000, sDt = '00000101', eDt = '99991231',
                taxRatio = 0.2, expenseRatio = 0.015, 
                holdDays = 20, 
                cutoffRatio = 0, # 손절 수익률 (-100 <= x <0)
                profitRatio = 0, # 익절 수익률 (0 < x)
                dayMaxTradeNum = 2, dfSign=[], dfTradeList=[], parallelInd=''
                ):
    dfBuySign  = dfSign[ (dfSign['일자'] >= sDt) & (dfSign['일자'] <= eDt) & (dfSign['Signal'] == 'B')]
    dfSellSign = dfSign[ (dfSign['일자'] >= sDt) & (dfSign['일자'] <= eDt) & (dfSign['Signal'] == 'S')]
    
    dfItemCnt = dfBuySign.groupby("일자").agg( 종목수=("종목코드", "count") ).reset_index()

    invItemList = []  # 투자 진행 종목의 종료일자 - 다음 투자를 위해
    simulRes = []     # 투자 결과 리스트 저장

    while(len(dfItemCnt) > 0):
        curDt = dfItemCnt['일자'][0]

        # 투자일 경과 건 투자진행 종목 리스트에서 삭제
        i = 0
        while i < len(invItemList) and invItemList[i] < curDt:
            i += 1
        if i >= 0:
            invItemList = invItemList[i:]

        # maxItemNum 개의 종목에 투자금액 1/N 분배 (이미 투자진행중인 건은 잔존 현금의 투자금액 분배 시 제외)
        ##  cashAmt가 아니라 해당 일자까지 투자한 금액, 회수한 금액을 감안한 여유 자금 재계산 필요
        dfTemp = pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                                 '매도일자','매도가격','매도금액','매도비용','현금잔액','투자손익'])    
        dfTemp = dfTemp[dfTemp['매도일자'] >= curDt]

        maxInvAmt = (cashAmt - dfTemp['매도금액'].sum() + dfTemp['매도비용'].sum()) / ( maxItemNum - len(invItemList) )


        # 해당 일자에 대한 투자 대상종목 수 계산
        curInvItemNum =  min (maxItemNum - len(invItemList), dayMaxTradeNum )

    #     print('\n', cashAmt, maxInvAmt, curInvItemNum)

        dList = dfBuySign[dfBuySign['일자']==curDt][['종목코드','종목명']].values.tolist()
        if len(dList) > curInvItemNum:
            random.shuffle(dList)
            dList = dList[:curInvItemNum]

        for x in dList:
            if dfTradeList == []:
                tradeList = sd.ReadStockTrade(x[0])
            else:
                tradeList = dfTradeList[x[0]]

            # 매입일자 및 가격 구하기
            buyDt = curDt
            buyPrice = int(tradeList[tradeList['일자']==buyDt]['종가'].values[0])

            # 매도일자 및 가격 구하기
            buyIdx = tradeList.index[tradeList['일자']==buyDt].values[0]            
            hDays = holdDays
            
            dfTemp = dfSellSign[(dfSellSign['종목코드']==x[0])&(dfSellSign['일자']>curDt)].reset_index()
            if len(dfTemp) > 0:
                sellDt = dfTemp.iloc[0]['일자']
            else:
                sellDt = '99991231'

            for ii in range(1, holdDays + 1):
                # if  (buyIdx + holdDays) < len(tradeList):
                if  (buyIdx + ii) < len(tradeList):
                    if  cutoffRatio < 0 and int(tradeList['종가'].iloc[buyIdx + ii]) <= buyPrice * (100 + cutoffRatio) / 100  or \
                        profitRatio > 0 and int(tradeList['종가'].iloc[buyIdx + ii]) >= buyPrice * (100 + profitRatio) / 100  or \
                        tradeList['일자'].iloc[buyIdx + ii] == sellDt :
                            
                        hDays = ii
                        break
                else:
                    break

            if (buyIdx + hDays) >= len(tradeList):
                continue

            sellDt = tradeList['일자'].iloc[buyIdx + hDays]            
            sellPrice = int(tradeList[tradeList['일자']==sellDt]['종가'].values[0])

            #######################################################
            # 매수/매도 거래내역 만들기
            #######################################################
            
            # 주식수량
            buyCnt = int(maxInvAmt / buyPrice)

            # 매입계산
            buyAmt = buyCnt * buyPrice * (-1)
            buyExpense = int(buyAmt * expenseRatio / 100)

            # 매도계산
            sellAmt = buyCnt * sellPrice
            sellExpense = int(sellAmt * taxRatio / 100) * (-1) + int(sellAmt * expenseRatio / 100) * (-1)

            # 보유현금 계산
            deltaAmt = buyAmt + buyExpense + sellAmt + sellExpense
            cashAmt += deltaAmt
    # 
            # 매도, 매수 결과
            simulRes.append( x + [buyCnt, buyDt, buyPrice, buyAmt, buyExpense, sellDt, sellPrice, sellAmt, sellExpense, cashAmt, deltaAmt] )

            invItemList.append(sellDt)

        invItemList.sort()

        if len(invItemList) >= maxItemNum:
            # 보유 종목 갯수가 max인 경우, 보유종목의 최초 매도일자 이후로 이동
            dfItemCnt = dfItemCnt[ dfItemCnt['일자'] > invItemList[0]            ] [['일자','종목수']].reset_index()
        else:
            # 추가 매수 가능한 경우, 다음 시그널 발생일로 이동
            dfItemCnt = dfItemCnt[ dfItemCnt['일자'] > dfItemCnt['일자'].iloc[0] ] [['일자','종목수']].reset_index()

        if parallelInd != 'Y':
            print('\r' + invItemList[0], end='')

    return pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용','매도일자','매도가격','매도금액','매도비용','현금잔액', '투자손익'])    


def get_earn_ratio(df, sig_list):
    i = 0
    earn_ratio = 100
    buy_idx = -1
    sell_idx = -1
                   
    while(i < len(df)):
        while( i < len(df) ):
            if sig_list[i] == 'B':
                buy_idx = i
                break
            else:
                i += 1

        while( i < len(df) ):
            if sig_list[i] == 'S':
                sell_idx = i 
                earn_ratio *= (df['종가'].iloc[sell_idx] / df['종가'].iloc[buy_idx])

                break
            else:
                i += 1
    
    if buy_idx > sell_idx and buy_idx < (len(df) - 1):
        sell_idx = len(df) - 1
        earn_ratio *= (df['종가'].iloc[sell_idx] / df['종가'].iloc[buy_idx])

    return (earn_ratio - 100)