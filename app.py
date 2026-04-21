# test_script.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def auth_page():
    with sync_playwright() as p:
        # 关键：在创建浏览器上下文时，加载之前保存的认证状态
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def test_access_dashboard(auth_page):
    # 直接访问任何需要登录的页面，比如 sales_web
    auth_page.goto("https://console.saas.aiwa.top/sales_web")
    # 添加你的业务断言
    # ...