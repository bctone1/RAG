import os
from pypdf import PdfReader, PdfWriter

def split_pdf(filepath, batch_size=10):
    """
    입력 PDF를 여러 개의 작은 PDF 파일로 분할
    """
    reader = PdfReader(str(filepath))
    num_pages = len(reader.pages)
    print(f"총 페이지 수: {num_pages}")

    ret = []
    base = os.path.splitext(str(filepath))[0]

    for start_page in range(0, num_pages, batch_size):
        end_page = min(start_page + batch_size, num_pages) - 1

        output_file = f"{base}_{start_page:04d}_{end_page:04d}.pdf"
        print(f"분할 PDF 생성: {output_file}")

        writer = PdfWriter()
        for i in range(start_page, end_page + 1):
            writer.add_page(reader.pages[i])

        with open(output_file, "wb") as f:
            writer.write(f)

        ret.append(output_file)

    return ret

# 예시
# sample_data = "test.pdf"
# split_files = split_pdf(sample_data, batch_size=10)
