import yfinance as yf
import time
import random
import requests
from yfinance.exceptions import YFRateLimitError
import os

# 代理服务器配置
PROXY = "http://127.0.0.1:10809"  # 替换为您的代理服务器地址和端口

# 设置环境变量方式（全局影响）
os.environ['HTTP_PROXY'] = PROXY
os.environ['HTTPS_PROXY'] = PROXY

def get_stock_data(ticker_symbol, max_retries=5, base_delay=5, use_proxy=True):
    """获取股票数据，包含重试机制和代理支持"""
    # 创建自定义session并配置代理
    session = None
    if use_proxy:
        session = requests.Session()
        session.proxies = {
            'http': PROXY,
            'https': PROXY
        }
        
    for attempt in range(max_retries):
        try:
            # 使用环境变量代理，不再尝试修改内部session
            ticker = yf.Ticker(ticker_symbol)
            
            # 获取股票信息
            info = ticker.info
            return info
        except YFRateLimitError:
            if attempt < max_retries - 1:
                # 指数退避策略，每次等待时间增加
                wait_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"遇到速率限制，等待 {wait_time:.2f} 秒后重试...")
                time.sleep(wait_time)
            else:
                print("达到最大重试次数，无法获取数据")
                raise
        except Exception as e:
            print(f"获取股票数据时发生错误: {type(e).__name__}: {e}")
            raise

try:
    # 测试是否可以通过代理访问Yahoo Finance
    # test_session = requests.Session()
    # test_session.proxies = {'http': PROXY, 'https': PROXY}
    # print("正在测试代理连接...")
    # response = test_session.get("https://finance.yahoo.com", timeout=10)
    # print(f"代理测试结果：状态码 {response.status_code}")
    
    # 获取股票信息，使用代理
    stock_info = get_stock_data("600050.SS", use_proxy=True)
    print("股票信息获取成功:")
    # 只打印部分关键信息，避免输出过多
    keys_to_show = ['shortName', 'symbol', 'sector', 'industry', 'currentPrice', 'marketCap']
    for key in keys_to_show:
        if key in stock_info:
            print(f"{key}: {stock_info[key]}")
        else:
            print(f"{key}: 不可用")
except Exception as e:
    print(f"程序执行失败: {e}")