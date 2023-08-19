from openxlab.model.handler.download_file import download, download_from_url
from openxlab.model import init


# inference("mmocr/SVTR", ['./demo_text_ocr.jpg'])
# download("dongxiaozhuang/digo_01", "model_1", overwrite=False)
# download("alvin123/digo_01", "model_1", overwrite=False)
# download("thomas-yanxin/MindChat-InternLM-7B", "config.json", overwrite=False)
# download("dongxiaozhuang/digo_01", "mm", overwrite=True)
# download("dongxiaozhuang/yy_001", "model_1", overwrite=True)
download_from_url("https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors", overwrite=True)
# download_from_url("https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/model_index.json", overwrite=True)
# init()

