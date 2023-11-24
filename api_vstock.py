import enum 
import json
import pandas as pd
import vnstock
import ast
from pathlib import Path

# #(Sheet,description,function_name,argument_str)
vnstock_function_list=[
     ['Company Overview','Company Overview','company_overview',"{{'symbol':'{stock_name}'}}"],
     ['Company Profile','Company Profile','company_profile',"{{'symbol':'{stock_name}'}}"],
     ['Company Large ShareHolders','Company Large ShareHolders','company_large_shareholders',"{{'symbol':'{stock_name}'}}"],
     ['Company Fundamental Ratio','Company Fundamental Ratio','company_fundamental_ratio',"{{'symbol':'{stock_name}','mode':''}}"],
     ['Ticker Price Volatility','Ticket Price Volatility','ticker_price_volatility',"{{'symbol':'{stock_name}'}}"],
     ['Company Inside Deals','Company Inside Deals','company_insider_deals',"{{'symbol':'{stock_name}','page_size':500}}"],
     ['Company Subsidiaries','Company Subsidiaries','company_subsidiaries_listing',"{{'symbol':'{stock_name}','page_size':500}}"],
     ['Company Officers','Company Officers','company_officers',"{{'symbol':'{stock_name}','page_size':100}}"],     
     ['Company Events','Company Events','company_events',"{{'symbol':'{stock_name}','page_size':500}}"], 
     ['Company News','Company News','company_news',"{{'symbol':'{stock_name}','page_size':1000}}"],
     ['Report_Balance Sheet','Financial Report - Balance Sheet','financial_report',"{{'symbol':'{stock_name}','report_type':'BalanceSheet','frequency':'Quarterly'}}"],
     ['Report_IncomeStatement','Financial Report - IncomeStatement','financial_report',"{{'symbol':'{stock_name}','report_type':'IncomeStatement','frequency':'Quarterly'}}"],
     ['Report_CashFlow','Financial Report - CashFlow','financial_report',"{{'symbol':'{stock_name}','report_type':'CashFlow','frequency':'Quarterly'}}"],
     ['Flow_Balance Sheet','Financial Flow - Balance Sheet','financial_flow',"{{'symbol':'{stock_name}','report_type':'balancesheet','report_range':'quarterly'}}"],
     ['Flow_IncomeStatement','Financial Flow - IncomeStatement','financial_flow',"{{'symbol':'{stock_name}','report_type':'incomestatement','report_range':'quarterly'}}"],
     ['Flow_CashFlow','Financial Flow - CashFlow','financial_flow',"{{'symbol':'{stock_name}','report_type':'cashflow','report_range':'quarterly'}}"],
     ['Financial Ratio','Financial Ratio','financial_ratio',"{{'symbol':'{stock_name}','is_all':True,'report_range':'quarterly'}}"],
     ['Divident History','Divident History','dividend_history',"{{'symbol':'{stock_name}'}}"],
     ['General Rating','General Rating','general_rating',"{{'symbol':'{stock_name}'}}"],
     ['Business Model Rating','Business Model Rating','biz_model_rating',"{{'symbol':'{stock_name}'}}"],
     ['Business Operation Rating','Business Operation Rating','biz_operation_rating',"{{'symbol':'{stock_name}'}}"],
     ['Financial Health Rating','Financial Health Rating','financial_health_rating',"{{'symbol':'{stock_name}'}}"],
     ['Valuation Rating','Valuation Rating','valuation_rating',"{{'symbol':'{stock_name}'}}"],
     ['Industry Financial Health','Industry Financial Health','industry_financial_health',"{{'symbol':'{stock_name}'}}"],
     ['Stock Evaluation','Stock Evaluation','stock_evaluation',"{{'symbol':'{stock_name}','period':5}}"],
     ['Stock Price Last 3 Months','Stock Price Last 3 Months','stock_historical_data',"{{'symbol':'{stock_name}','resolution':'1','type':'stock','source':'DNSE','start_date':'{last_3_months_date}','end_date':'{today_date}'}}"],
     ['Stock Price In Day','Stock Price In Day','stock_historical_data',"{{'symbol':'{stock_name}','resolution':'1D','type':'stock','source':'DNSE','start_date':'2010-01-01','end_date':'{today_date}'}}"],
     ['Industry Analysis','Industry Analysis','industry_analysis',"{{'symbol':'{stock_name}','lang':'en'}}"],
     ['Stock IntraDay','Stock Intra Day','stock_intraday_data',"{{'symbol':'{stock_name}','page_size':4000}}"],

]

# def create_excel_file(stock_name:str,):

def get_stock_symbol_lst():
    df = vnstock.listing_companies()
    return df

def generate_excelfile(symbol:str, outputfilename:str='output',is_reused:bool=False):

    from datetime import datetime,timedelta

    # Get the current date
    current_date = datetime.now()

    # Format the date as 'YYYY-MM-DD'
    today_date = current_date.strftime('%Y-%m-%d')
    last_3_months_date = (current_date - timedelta(days=90)).strftime('%Y-%m-%d')
    file_full_path = Path(outputfilename)
    file_full_path = file_full_path.parent / f'{file_full_path.stem}_{today_date}.xlsx'
    print(file_full_path)
    if is_reused:
        # Return file if already created
        if file_full_path.is_file(): 
            print('File already created. Do nothing')
            return file_full_path
        
    with pd.ExcelWriter(file_full_path,engine='openpyxl') as writer:
        for fn in vnstock_function_list:
            print(fn[1])
            str = fn[3].format(stock_name=symbol,today_date=today_date,last_3_months_date=last_3_months_date)
            #print(str)
            kwargs = ast.literal_eval(str)
            print(kwargs)
            func = getattr(vnstock,fn[2])
            try:
                df = func(**kwargs)
                df.to_excel(writer,sheet_name=fn[0])
            except Exception as e:
                print(e)

    return file_full_path

def generate_download_excel_files(symbol_lst:list,default_output_folder:Path,is_reused:bool=False) -> list[Path]:
    default_output_folder.mkdir(parents=True, exist_ok=True)
    output_lst = []
    for symbol in symbol_lst:
        output_file_name = default_output_folder / f'{symbol}' 
        print(output_file_name)
        outputfilename = generate_excelfile(symbol=symbol,outputfilename=output_file_name,is_reused=is_reused)
        output_lst.append(outputfilename)
    return output_lst

if __name__ == '__main__':
    #generate_excelfile('TCB')
    #df = get_stock_symbol_lst()
    lst = ['ACB']
    fldr_name = Path.cwd() / 'output'
    generate_download_excel_files(lst,fldr_name,True)