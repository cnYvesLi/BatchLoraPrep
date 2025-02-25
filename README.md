# Image Preprocessing and Tagging Service

这是一个基于ViT（Vision Transformer）模型的图像标注服务，可以自动为图像生成相关标签和描述。

## 功能特点

- 支持多种图像格式的处理
- 自动生成图像标签和描述
- 基于ViT模型的高精度识别
- Web界面支持，易于使用
- 支持标签概率显示
- 支持角色标签特殊处理

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/your-username/image-preprocessing.git
cd image-preprocessing
```

2. 创建并激活虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install flask onnxruntime numpy pillow
```

4. 下载模型文件：

模型文件较大，未直接包含在代码仓库中。请从以下链接下载模型文件：
- [wd-vit-tagger-v3.onnx](https://huggingface.co/SmilingWolf/wd-vit-tagger-v3/blob/main/model.onnx)
- [wd-vit-tagger-v3.csv](https://huggingface.co/your-username/image-preprocessing/resolve/main/wd-vit-tagger-v3.csv)

下载后将文件放置在项目的 `models` 目录下。

## 使用方法

1. 启动服务：
```bash
python app.py
```

2. 打开浏览器访问：`http://localhost:5000`

3. 上传图片并获取标签结果

## API 说明

### 生成标签

- 端点：`/api/generate-tags`
- 方法：POST
- 参数：
  - image: 图片文件（multipart/form-data）
- 返回：JSON格式的标签信息

```json
{
    "tags": {
        "tags": [...],
        "all_probabilities": [...],
        "probabilities": [...]
    }
}
```

## 项目结构

```
image-preprocessing/
├── app.py              # 主应用程序
├── main.html           # Web界面
├── models/            # 模型文件目录
│   ├── wd-vit-tagger-v3.onnx
│   └── wd-vit-tagger-v3.csv
├── requirements.txt    # 项目依赖
└── README.md          # 项目说明
```

## 技术栈

- Python 3.7+
- Flask
- ONNX Runtime
- NumPy
- Pillow
