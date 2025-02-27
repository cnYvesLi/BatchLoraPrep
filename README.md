# Image Preprocessing and Tagging Service

这是一个基于WD14 Tagger（ViT-based）模型的图像标注服务，可以自动为图像生成相关标签和描述。该项目使用了SmilingWolf的wd-vit-tagger-v3模型，在此特别感谢。

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
git clone https://github.com/cnYvesLi/BatchLoraPrep.git
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
- [wd-vit-tagger-v3.csv](https://huggingface.co/SmilingWolf/wd-vit-tagger-v3/blob/main/selected_tags.csv)

下载后将文件放置在项目的 `models` 目录下。

## 使用方法

1. 启动服务：
```bash
python app.py
```

2. 打开浏览器访问：`http://localhost:5000`

3. 上传图片并获取标签结果
