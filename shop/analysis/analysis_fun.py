profits=[]
symbols_used=[]
Max_drawdown=[]
winning=[]
Total_trades=[]


def order_to_position(data1):
    pos=[]

    for j in range(1,5):
        # symbols_used=symbols_used_fun()
        for i in range(len(data1)):
            lists=[]
            if data1[i][-1]==j and (data1[i][-2]=='buy'):
                buy_in=data1[i][2]
                symbol=data1[i][1]
                lists.append(symbol)
                lists.append(buy_in)
                lists.append('buy')

                for k in range(i,len(data1)):
                    if data1[k][1]==symbol and data1[k][-2]=='squareoffbuy':
                        sell_in=data1[k][2]
                        lists.append(sell_in)
                        profits.append(((sell_in-buy_in)/buy_in)*100)
                        lists.append(((sell_in-buy_in)/buy_in)*100)
                        lists.append(j)
                        pos.append(lists)
                        break

            elif data1[i][-1]==j and (data1[i][-2]=='sell'):
                sell_in=data1[i][2]
                symbol=data1[i][1]
                lists.append(symbol)
                lists.append(sell_in)
                lists.append('sell')
                for k in range(i,len(data1)):
                    
                    if data1[k][1]==symbol and data1[k][-2]=='squareoffsell':
                        buy_in=data1[k][2]
                        lists.append(buy_in)
                        profits.append(((sell_in-buy_in)/buy_in)*100)
                        lists.append(((sell_in-buy_in)/buy_in)*100)
                        lists.append(j)
                        pos.append(lists)
                        break

    return pos



def winnings(positions):
    lists=[]
    for j in range(1,5):
        profits=0
        losses=0
        for i in range(len(positions)):
            if positions[i][-1]==j:
                if positions[i][-2]>0:
                    profits+=1

                if positions[i][-2]<0:
                    losses+=1

        winning=((profits)/(profits+losses))*100
        lists.append(winning)
    return lists




def symbols_used_fun(orders):
    
    lists=[]
    for j in range(1,5):
        symbol_exempt=[]

        symbol_used_dict={}
        for i in range(len(orders)):
            if orders[i][-1]==j:

                    symbol=orders[i][0]
                    
                    if symbol not in symbol_exempt:
                        symbol_used_dict[symbol]=1
                    symbol_exempt.append(symbol)
                    for k in range(i+1,len(orders)):
                        if orders[k][-1]==j:
                            if orders[k][0]==symbol:
                                symbol_used_dict[symbol]+=1

        lists.append(symbol_used_dict)


    return lists


def total_tr(positions):
    lists=[]
    for j in range(1,5):
        trades=0
        for i in range(len(positions)):
            if positions[i][-1]==j:
                trades+=1
        lists.append(trades)
            
    return lists


def profit(positions):
    lists=[]
    for j in range(1,5):
        profitt=0
        for i in range(len(positions)):
            if positions[i][-1]==j:
                profitt+=positions[i][-2]

        lists.append(profitt)

    return lists


def string(symbol_used):
    # for j in range(len(data2)):
    lists=[]
    for i in range(len(symbol_used)):
        lists.append(str(list(symbol_used.keys())[i])+'_'+str(symbol_used[str(list(symbol_used.keys())[i])]))
    symbol=""
    for i in range(len(lists)):
        
        lists[i]=symbol+'_'+lists[i]
        symbol=lists[i]
    return lists[-1]

def Max_draw(positions):
    return [21,23,34,12]