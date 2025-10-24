import requests
import json
import base64

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai/v1"
AI_API_KEY = "sk-gQzgT8AFPvQRBnrsyF-UCA"

# --- Gọi API để tạo hình ảnh ---
url = f"{AI_API_BASE}/images/generations"
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {AI_API_KEY}"
}
data = {
  "model": "imagen-4",
  "prompt": """scene_1_starry_sky": "Digital art, a visually stunning image of abstract glowing data points forming a starry night sky over Vietnam's landscape, from majestic mountains to a serene coastline. Represents the line 'Chạm vào từng con số, thấy cả một trời sao'. Hopeful and epic.",
        "scene_2_smart_city": "Futuristic concept art of a smart city in Vietnam connected by brilliant streams of light to high-tech vertical farms in the countryside. Represents 'thành phố thông minh, là đồng quê kết nối'. Clean, vibrant, and optimistic.",
        "scene_3_gen_z_at_work": "Action shot, energetic, diverse young Vietnamese professionals (Gen Z) collaborating in a modern, sunlit office, coding on transparent screens. A glowing shield icon is visible, symbolizing data security. Represents 'Trí tuệ nhân tạo' and 'lá chắn an toàn'.",
        "scene_4_montage_of_joy": "Photorealistic montage showing the positive outcomes of data technology: a smiling elderly woman video-calling her family, a farmer checking crop data on a tablet in a lush field, a bustling successful small business. Represents 'Là nụ cười của mẹ, là tương lai của cha'.""",
  "n": 4, # Yêu cầu 2 ảnh
}

try:
  response = requests.post(url, headers=headers, data=json.dumps(data))
  response.raise_for_status()

  result = response.json()
  
  # --- Xử lý và lưu từng ảnh ---
  for i, image_obj in enumerate(result['data']):
      b64_data = image_obj['b64_json']
      image_data = base64.b64decode(b64_data)
      
      save_path = f"generated_image_{i+1}.png"
      with open(save_path, 'wb') as f:
          f.write(image_data)
      print(f"Image saved to {save_path}")

except requests.exceptions.RequestException as e:
  print(f"An error occurred: {e}")
  print(f"Response body: {response.text if 'response' in locals() else 'No response'}")