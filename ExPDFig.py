import fitz  # PyMuPDF
import os
import sys

def extract_images():
    # 1. 从控制台获取路径
    # 使用 strip() 去掉空格，strip('"') 去掉拖入文件时可能自带的双引号
    path_input = input("请输入 PDF 文件的完整路径（或直接把文件拖进来）: ").strip().strip('"').strip("'")
    
    if not os.path.exists(path_input):
        print(f"❌ 错误：找不到文件，请检查路径是否正确：{path_input}")
        return

    if not path_input.lower().endswith(".pdf"):
        print("❌ 错误：该文件似乎不是 PDF 格式。")
        return

    # 2. 提取文件名和创建文件夹
    base_name = os.path.basename(path_input)
    pdf_name = os.path.splitext(base_name)[0]
    output_folder = pdf_name

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📂 已创建输出目录: {output_folder}")

    # 3. 开始处理 PDF
    try:
        pdf_document = fitz.open(path_input)
        total_pages = len(pdf_document)
        img_count = 0

        print(f"🚀 正在处理: {base_name} (共 {total_pages} 页)...")

        for page_num in range(total_pages):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # 命名格式：pdf名字_页数_序号
                image_filename = f"{pdf_name}_{page_num + 1}_{img_index}.{image_ext}"
                image_filepath = os.path.join(output_folder, image_filename)

                with open(image_filepath, "wb") as f:
                    f.write(image_bytes)
                
                img_count += 1

        pdf_document.close()
        print("-" * 30)
        print(f"✅ 任务完成！")
        print(f"输出文件名格式：：")
        print(f"PDF文件名_页码_当页图片序号.图片后缀")
        print(f"📸 成功提取 {img_count} 张图片。")
        print(f"📍 图片保存位置: {os.path.abspath(output_folder)}")

    except Exception as e:
        print(f"💥 运行过程中出错: {e}")

if __name__ == "__main__":
    extract_images()
    # 防止程序运行完直接闪退，方便查看结果
    input("\n按回车键退出程序...")
