FROM python:3.11-slim

# Cài các gói cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget && \
    rm -rf /var/lib/apt/lists/*

# Làm việc trong thư mục /app
WORKDIR /app

# Clone mã nguồn
RUN git clone https://github.com/caochihai/text-summary-vit5baseX2.git src

# Cài thư viện Python
RUN pip install --no-cache-dir -r src/requirements.txt

# Cài đặt underthesea từ file whl
RUN wget https://files.pythonhosted.org/packages/23/17/8c9b8faa546fc0b1d2c2d95bc3539422946c3614f14db91272b219307c9f/underthesea-6.8.4-py3-none-any.whl \
    && pip install --no-cache-dir underthesea-6.8.4-py3-none-any.whl \
    && rm underthesea-6.8.4-py3-none-any.whl

# Cài gdown bản hỗ trợ download_folder
RUN pip install git+https://github.com/wkentaro/gdown.git

# Tải mô hình
RUN mkdir -p models/chunk_summarizer models/summary_combiner && \
    gdown --folder https://drive.google.com/drive/folders/1GwUytz52fJqREHbjJ3M2zcSnh6y-RnhH -O models/chunk_summarizer && \
    gdown --folder https://drive.google.com/drive/folders/1HcqacpxY3NSRsTPMoTe2oMQM11j6b7D7 -O models/summary_combiner

# Mở cổng
EXPOSE 5000

# Chạy API
WORKDIR /app/src
CMD ["python", "api.py"]
