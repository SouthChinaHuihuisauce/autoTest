# save_auth.py
from playwright.sync_api import sync_playwright


def save_auth_state():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 打开你的登录页
        page.goto("https://console.saas.aiwa.top/sales_web/auth/signin")

        # 手动输入账号、密码、验证码，并完成登录
        input("请在浏览器中手动完成登录，然后按 Enter 键继续...")

        # 登录成功后，等待页面跳转稳定
        page.wait_for_url("**/sales_web**", timeout=0)

        # 保存状态
        context.storage_state(path="auth.json")
        print("认证状态已成功保存到 auth.json")
        browser.close()


if __name__ == "__main__":
    save_auth_state()