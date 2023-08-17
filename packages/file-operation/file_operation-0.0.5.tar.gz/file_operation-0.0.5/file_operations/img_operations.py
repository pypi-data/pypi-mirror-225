"""

@Time : 2023/4/9 11:52 
@Author : skyoceanchen
@TEL: 18916403796
@项目：JYairports
@File : img_operations.by
@PRODUCT_NAME :PyCharm
"""
import base64
import qrcode


class ImageOperation(object):
    @staticmethod
    def base64_to_image(base64_data, img_file, ):
        with open(img_file, "wb") as f:
            f.write(base64_data)

    @staticmethod
    def image_to_base64(img_file, ):
        with open(img_file, "rb") as f:
            base64_data = base64.b64encode(f.read())
        return base64_data

    @staticmethod
    def base64_to_base64(base64_data):
        return base64_data

    @staticmethod
    def create_qrcode(text, file_path):
        # text = r"http://139.224.52.79:8089/media/report\\embed_report\\1648622788.pdf"  # 设置URL必须添加http://
        img = qrcode.make(text)
        img.save(file_path)  # 保存图片至本地目录，可以设定路径
