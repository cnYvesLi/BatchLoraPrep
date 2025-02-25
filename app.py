from flask import Flask, request, jsonify, send_file
import onnxruntime as ort
import numpy as np
from PIL import Image
import io
import os
import csv

app = Flask(__name__, static_url_path='/')

@app.route('/tagger.js')
def serve_js():
    return send_file(os.path.join(os.path.dirname(__file__), 'tagger.js'))


class ImageTagger:
    def __init__(self):
        self.model = None
        self.session = None
        self.modelLoaded = False
        self.tags = []

    def load_model(self):
        try:
            model_path = 'models/wd-vit-tagger-v3.onnx'
            csv_path = 'models/wd-vit-tagger-v3.csv'
            self.model = ort.InferenceSession(model_path)
            
            # 加载标签映射文件
            self.tags = []
            self.tag_categories = []
            if os.path.exists(csv_path):
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # 跳过标题行
                    for row in reader:
                        self.tags.append(row[1])  # 第二列是标签名
                        self.tag_categories.append(row[2] if len(row) > 2 else '0')  # 第三列是标签类别
            
            self.modelLoaded = True
            print('Model and tags loaded successfully')
        except Exception as error:
            print('Error loading model or tags:', error)
            raise error

    def preprocess_image(self, image):
        # 调整图片大小到模型要求的尺寸
        size = 448
        # 计算缩放比例，保持长宽比
        width, height = image.size
        ratio = size / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # 使用LANCZOS重采样方法调整图片大小
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # 创建白色背景的正方形画布
        new_image = Image.new('RGB', (size, size), (255, 255, 255))
        
        # 将调整后的图片居中粘贴
        paste_x = (size - new_width) // 2
        paste_y = (size - new_height) // 2
        new_image.paste(image, (paste_x, paste_y))

        # 转换为numpy数组并调整格式
        img_array = np.array(new_image)
        # 转换为BGR格式（从RGB格式）
        img_array = img_array[...,::-1]
        # 转换为float32类型
        img_array = img_array.astype(np.float32)
        # 添加batch维度
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def generate_tags(self, image_data, threshold=0.35, character_threshold=0.85):
        if not self.modelLoaded:
            self.load_model()

        try:
            # 预处理图片
            input_tensor = self.preprocess_image(image_data)
            # 运行推理
            outputs = self.model.run(None, {'input': input_tensor})
            probs = outputs[0][0]

            # 获取高于阈值的标签
            tags = []
            print(f"\n原始概率值数量: {len(probs)}")
            print("处理标签中...")

            # 记录所有概率值用于返回给前端
            all_probabilities = []
            for idx, prob in enumerate(probs):
                tag_name = self.tags[idx] if idx < len(self.tags) else f'tag_{idx}'
                category = self.tag_categories[idx] if idx < len(self.tag_categories) else '0'
                
                # 保存所有概率值
                all_probabilities.append({
                    'tag': tag_name,
                    'probability': float(prob),
                    'category': category
                })
                
                # 打印原始数据
                if prob > min(threshold, character_threshold):
                    print(f"标签 {tag_name}: 概率={prob:.4f}, 类别={category}")
                
                # 角色标签使用更高的阈值
                # 确保标签以逗号结尾
                formatted_tag = tag_name if tag_name.endswith(',') else tag_name + ','
                if category == '4' and prob > character_threshold:
                    tags.append({'tag': formatted_tag, 'probability': float(prob), 'is_character': True})
                elif prob > threshold:
                    tags.append({'tag': formatted_tag, 'probability': float(prob), 'is_character': False})

            # 按概率排序
            tags.sort(key=lambda x: x['probability'], reverse=True)
            print(f"\n筛选后的标签数量: {len(tags)}")
            print("最终返回的标签:")
            for tag in tags:
                print(f"{tag['tag']}: {tag['probability']:.4f} ({'角色' if tag['is_character'] else '普通'})")
            
            # 返回包含所有概率值的结果
            return {
                'tags': tags,
                'all_probabilities': sorted(all_probabilities, key=lambda x: x['probability'], reverse=True),
                'probabilities': all_probabilities  # 添加所有概率值到返回结果中
            }
        except Exception as error:
            print('Error generating tags:', error)
            raise error

# 创建标注器实例
tagger = ImageTagger()

@app.route('/')
def index():
    return send_file('main.html')

@app.route('/api/generate-tags', methods=['POST'])
def generate_tags():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    try:
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))
        tags = tagger.generate_tags(image)
        return jsonify({'tags': tags})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)