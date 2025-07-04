from fastapi import FastAPI, HTTPException, Body
from processingdata import PDFsProcess
import summary as sum
import json
import os
import re

app = FastAPI()
app.config = {"JSON_AS_ASCII": False}

model = sum.Summary()

def is_url(string: str) -> bool:
    return re.match(r'^https?://', string.strip()) is not None

@app.post("/summarize_pdf")
async def summarize_pdf(source: str = Body(..., embed=True)):
    try:
        if not source:
            raise HTTPException(status_code=400, detail="Thiếu trường 'source' trong nội dung yêu cầu.")

        # Xử lý input là URL hoặc đường dẫn cục bộ
        data_obj = PDFsProcess(source)

        tt1, tt2 = data_obj.load_pdf()
        if tt1 and tt2:
            dt = data_obj.read_text()
            summary = model.summary_content(dt)

            return {"response": summary}

        elif not tt1 and not tt2:
            raise HTTPException(
                status_code=400,
                detail=f"Tệp PDF từ '{source}' không tồn tại hoặc không thể truy cập. "
                       f"Vui lòng kiểm tra lại đường dẫn hoặc quyền truy cập."
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Tệp PDF có thể là file scan ảnh hoặc tài liệu bằng ngôn ngữ không hỗ trợ. "
                    "Hệ thống chỉ xử lý file PDF có nội dung văn bản có thể sao chép được. "
                    "Vui lòng kiểm tra định dạng file."
                )
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Đã xảy ra lỗi trong quá trình xử lý yêu cầu.",
                "chi_tiet": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
