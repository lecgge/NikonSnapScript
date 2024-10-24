from asyncio import Timeout
from time import sleep



from tools import culatePoint

#
# # 使用Chrome浏览器打开页面
# driver = Chromium().latest_tab
# driver.get('https://wj.qq.com/s2/14502829/j46e/')  # 将这里的URL替换为你想要访问的实际网址
#
# # 等待页面加载完成
# driver.page_load_timeout = 30  # 设置页面加载超时时间（秒）
# sleep(10)
#
# # 查找class为'page-btn'的元素
# page_button = driver.ele('css:.page-btn')
#
# # 如果找到了按钮，则点击
# if page_button:
#     print("找到class为'page-btn'的按钮")
#     page_button.click()
# else:
#     print("没有找到class为'page-btn'的按钮")
#
# # 查找 class 为 'pe-image' 的 span 元素
# span_element = driver.ele('css:span.pe-image')
# img_src = ""
# # 如果找到了 span 元素
# if span_element:
#     # 在 span 元素中查找 img 标签
#     img_element = span_element.ele('css:img')
#
#     # 如果找到了 img 标签
#     if img_element:
#         # 获取 img 标签的 src 属性
#         img_src = img_element.attr('src')
#         print(f"图片的 URL 是: {img_src}")
#     else:
#         print("没有找到 span 中的 img 标签")
# else:
#     print("没有找到 class 为 'pe-image' 的 span 元素")
#

img_src = "https://wj.gtimg.com/uploadImages/2024-10-23/202410231859206718d708cfbb3.jpg"
# 使用 requests 获取图片内容
# response = requests.get(img_src)
# response.raise_for_status()  # 检查请求是否成功

print(culatePoint('1.png'))