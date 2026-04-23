import pytest
from playwright.sync_api import sync_playwright, expect
import time


@pytest.fixture(scope="function")
def auth_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        yield page
        context.close()
        browser.close()


def test_add_product_full_success(auth_page):
    """完整测试添加商品流程（填写基本信息并提交）"""
    # 1. 导航到商品列表页
    auth_page.goto("https://console.saas.aiwa.top/sales_web/product/list")
    auth_page.wait_for_load_state("networkidle")

    # 2. 点击“添加商品”按钮
    add_btn = auth_page.get_by_role("button", name="添加商品")
    add_btn.click()

    # 3. 等待抽屉出现
    drawer = auth_page.locator(".n-drawer")

    # 4. 上传商品预览图像（选择第一个 file input，位于基本资料区域）
    upload_input = drawer.locator("#section-basic input[type='file']")  # 或 .first
    upload_input.set_input_files("D:/workspace/clouddao/autoTest/tests/test_data/testProduct.jpg")

    # 等待上传完成（可以根据文件列表状态判断）
    # 示例：等待 n-upload 文件列表中出现“已完成”状态
    # expect(drawer.locator(".n-upload-file-info__status:has-text('done')")).to_be_visible(timeout=15000)

    # 5. 填写商品名称
    name_input = drawer.get_by_placeholder("请输入商品名称")
    name_input.fill("测试咖啡机")

    # 6. 填写商品编码
    code_input = drawer.get_by_placeholder("请输入商品编码")
    code_input.fill("COF-001")

    # 7. 选择商品类型（下拉框）
    type_select = drawer.locator(".n-select").first
    type_select.click()
    # 根据实际显示的文本选择，组件中选项有 Physical, Subscription, Manual, Single
    # 暂时默认
    # option = auth_page.locator(".n-select-option").filter(has_text="服务订阅")
    # option.click()

    # 8. 设置价格
    # 币种选择
    currency_select = drawer.locator(".currency-select")
    currency_select.click()
    # 暂时默认
    # usd_option = auth_page.locator(".n-select-option").filter(has_text="USD")
    # usd_option.click()

    # 金额输入框
    price_input = drawer.locator(".price-input input")
    price_input.fill("129.99")

    # 9. 提交表单（保存按钮）
    save_btn = drawer.get_by_role("button", name="保存")
    save_btn.click()

    # 10. 等待抽屉关闭
    expect(drawer).to_be_hidden(timeout=5000)

    # 11. 验证成功提示
    # success_msg = auth_page.locator(".n-message--success")
    # expect(success_msg).to_be_visible()
    # expect(success_msg).to_contain_text("成功")

    # 12. 验证商品出现在列表中（等待列表刷新）
    auth_page.wait_for_timeout(2000)
    new_product_row = auth_page.locator("tr:has-text('测试咖啡机')")
    expect(new_product_row).to_be_visible()
    # 可选：验证编码和价格
    expect(new_product_row.locator("td").nth(1)).to_have_text("COF-001")
    expect(new_product_row.locator("td").nth(2)).to_have_text("129.99 USD")