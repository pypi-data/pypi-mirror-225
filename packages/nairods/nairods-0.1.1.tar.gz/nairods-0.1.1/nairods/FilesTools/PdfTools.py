#! /usr/bin/env python
# -*-coding:utf-8-*-
import datetime
import os
import fitz


# fitz就是 pip install PyMuPDF==1.18.7


#  关于pdf 操作的一些工具

class PdfCurd(object):
    """
    pdf 转换
    """

    def __init__(self):
        pass

    def pdf_pic(self, pdf_path, pic_path):
        """
        pdf 转化为图片
        单个文件
        """

        start_time = datetime.datetime.now()  # 开始时间
        print(f"pic_path={pic_path}")
        pdf_doc = fitz.open(pdf_path)
        for pg in range(pdf_doc.pageCount):
            page = pdf_doc[pg]
            rotate = int(0)
            zoom_x = 1.33333333  # 等比例放大
            zoom_y = 1.33333333
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            if not os.path.exists(pic_path):
                os.makedirs(pic_path)
            pg  = f"{pdf_path.split('.')[0]}_{pg}"
            pix.writePNG(f"{pic_path}{os.sep}{pg}.png")
        end_time = datetime.datetime.now()
        print(f'运行时间时间:{(end_time - start_time).seconds}s')


# if __name__ == "__main__":
#     PC = PdfCurd()
#     pdf_path = 'demo.pdf'
#     pic_path = './pic'
#     PC.pdf_pic(pdf_path, pic_path)
