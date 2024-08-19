import streamlit as st
import os
import cv2
from text_renderer.config import get_cfg
from text_renderer.render import Render
from example_data.deepctrl import get_configs
from pathlib import Path

# 设置页面标题
st.set_page_config(page_title="文本图像生成器")

# 标题
st.title("文本图像生成器")

# 用户输入
text = st.text_input("请输入要渲染的文本：")

# 添加效果选择
effects_options = [
    ("Line", "在文本周围添加线条"),
    ("DropoutRand", "随机丢弃像素"),
    ("DropoutVertical", "垂直方向随机丢弃"),
    ("DropoutHorizontal", "水平方向随机丢弃"),
    ("Padding", "添加内边距"),
    ("Emboss", "浮雕效果"),
    ("MotionBlur", "运动模糊"),
    ("Curve", "曲线变换")
]

selected_effects = st.multiselect(
    "选择要应用的效果:",
    [effect[0] for effect in effects_options],
    format_func=lambda x: f"{x} - {dict(effects_options)[x]}"
)

# 添加透视变换参数的输入
st.header("透视变换设置")
perspective_x = st.number_input("X轴透视变换强度", value=20.0, min_value=0.0, max_value=100.0, step=1.0)
perspective_y = st.number_input("Y轴透视变换强度", value=20.0, min_value=0.0, max_value=100.0, step=1.0)
perspective_z = st.number_input("Z轴透视变换强度", value=1.5, min_value=0.0, max_value=10.0, step=0.1)

if st.button("生成图像"):
    if text:
        # 获取配置
        configs = get_configs(text, selected_effects, perspective_x, perspective_y, perspective_z)
        
        # 创建Render对象
        render = Render(configs[0].render_cfg)
        
        # 从配置中获取要生成的图片数量
        num_images = configs[0].num_image
        
        # 生成多张图像
        images = []
        labels = []
        for _ in range(num_images):
            image, label = render()
            if image is not None:
                images.append(image)
                labels.append(label)
        
        if images:
            # 显示生成的图像
            for i, (image, label) in enumerate(zip(images, labels)):
                # 将图像从BGR转换为RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # 显示生成的图像
                st.image(image_rgb, caption=f"生成的图像 {i+1} - 文本: {label}", use_column_width=True)
                
                # 保存图像
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                image_path = output_dir / f"{label}_{i+1}.png"
                cv2.imwrite(str(image_path), image)
            
            st.success(f"已生成 {len(images)} 张图像并保存至 output 目录")
        else:
            st.error("图像生成失败")
    else:
        st.warning("请输入要渲染的文本")

# # 显示已生成的图像
# st.header("已生成的图像")
# output_dir = Path("output")
# if output_dir.exists():
#     image_files = list(output_dir.glob("*.png"))
#     if image_files:
#         for image_file in image_files:
#             image = cv2.imread(str(image_file))
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             st.image(image_rgb, caption=f"文件名: {image_file.name}", use_column_width=True)
#     else:
#         st.info("暂无生成的图像")
# else:
#     st.info("暂无生成的图像")