# Bắt đầu nhanh (Tiếng Việt)

Trang này là bản tóm tắt một trang cho người mới. Hướng dẫn chi tiết bằng tiếng Anh nằm trong [docs](.) — hãy dùng các trang đó khi cần xem kỹ từng bước.

## Yêu cầu hệ thống

| | Tối thiểu | Ghi chú |
|---|---|---|
| Hệ điều hành | **Windows 10 hoặc 11, 64-bit** | **Windows XP không chạy được** — xem bên dưới |
| CPU | 4 nhân, hỗ trợ SSE4.2 | Blender 4.5 không khởi động nếu thiếu SSE4.2 |
| RAM | 8 GB | 16 GB thoải mái hơn |
| GPU | OpenGL 4.3, 2 GB VRAM | NVIDIA RTX render Cycles nhanh hơn; không có GPU vẫn render bằng CPU |
| Ổ đĩa | ~2 GB trống | Blender ~1 GB sau khi giải nén |
| Phần mềm | OpenCode đã cài và đã đăng nhập | Git và uv sẽ được cài trong hướng dẫn |

### Vì sao Windows XP không chạy được

- Blender 4.5 yêu cầu Windows 64-bit (8.1 trở lên; khuyến nghị Windows 10/11), CPU SSE4.2 và OpenGL 4.3. Bản Blender cuối cùng chạy trên XP là 2.76 (năm 2014).
- JewelCraft 3.0.1 yêu cầu Blender 4.5+.
- Addon MCP-for-Blender yêu cầu Blender 3.0+.
- OpenCode yêu cầu Windows 10/11 64-bit.

Không có cách ghép các phiên bản cũ để chạy đủ quy trình này trên XP. Cần chuyển sang máy Windows 10/11 64-bit (hoặc Remote Desktop vào một máy như vậy).

## Cài đặt trong 6 bước

Mở **Windows PowerShell** và chạy:

```powershell
# 1. Tải repository
cd D:\
git clone https://github.com/hhoangdo/JewelryDesignTest.git
cd JewelryDesignTest

# 2. Cài Blender, JewelCraft và MCP addon
#    Làm theo trang docs\02-install.md (có lệnh cụ thể và mã SHA256)

# 3. Kiểm tra máy
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1

# 4. Tạo dự án mới
powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name first-ring

# 5. Mở Blender và mở file
#    D:\JewelryDesignTest\projects\first-ring\ring.blend
#    Trong Blender: nhấn N để thấy tab MCP for Blender và JewelCraft

# 6. Mở OpenCode tại thư mục gốc của repo
cd D:\JewelryDesignTest
opencode
```

Sau đó dán prompt (tiếng Việt hoặc tiếng Anh đều được):

> Mở `projects/first-ring/ring.blend`. Hãy tạo một chiếc nhẫn solitaire: size US 7 (đường kính trong 17.3 mm), đá chủ 5 mm round brilliant, 6 chấu, vàng vàng, bản nhẫn rộng 2 mm. Dùng collection `GEMS` và `METAL`. Lưu từng script vào `projects/first-ring/scripts/`, lưu file vào `projects/first-ring/ring.blend`, và không sửa template hay example.

## Quy trình làm việc

1. **Mô tả** chiếc nhẫn bằng lời.
2. AI viết script Python (`bpy`) và gửi qua MCP xuống Blender.
3. AI dùng `look` để chụp màn hình và tự kiểm tra mô hình.
4. Bạn xem ảnh, nhận xét **một tham số mỗi lần**.
5. Khi hài lòng, yêu cầu render 1000×1000 vào `projects/<tên>/renders/hero.png`.

## Tái tạo mẫu solitaire

Mẫu có sẵn trong `example-solitaire/`:

- `ring.blend` — mô hình hoàn chỉnh.
- `renders/hero.png` — ảnh render mẫu.
- `reference/target.jpg` — ảnh tham chiếu.
- `scripts/` — 5 script tái tạo mô hình.

Có hai cách:

- **Chạy lại script** (nhanh, kiểm tra cài đặt): tạo project `replay-check`, copy 5 script vào, mở Blender và chạy lần lượt `build_band.py` → `build_gem.py` → `build_head.py` → `studio_render.py` → `verify_scene.py`.
- **Để AI làm lại** (bài tập thực tế): tạo project `my-solitaire`, mở Blender, đính kèm ảnh `reference/target.jpg` và dán prompt trong `example-solitaire/prompt.md`.

Chi tiết đầy đủ: [5. Recreate the example](05-recreate-example.md).

## Lưu ý quan trọng

- **Đơn vị:** scene dùng `scale_length = 1.0`, hiển thị milimét. Kích thước thiết kế tính bằng mm rồi chia 1000 khi đưa vào Blender. Nếu mô hình nhỏ hơn 1000 lần, kiểm tra lại `scale_length`.
- **Safe mode:** AI chỉ được dùng `bpy`, `math`, `mathutils`; không đọc/ghi file tùy ý và không sửa preferences.
- **Đây là mô hình hình ảnh**, không phải chứng nhận sản xuất/đúc. Muốn làm nhẫn thật, cần kiểm tra dung sai và kỹ thuật riêng.
- **`projects/` được Git bỏ qua** — công việc của bạn không bị đẩy lên repo.

## Khi gặp lỗi

Xem [Troubleshooting](TROUBLESHOOTING.md) hoặc chạy lại:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1
```

Các lỗi thường gặp: `spawn uvx ENOENT`, cổng 9876 bận, OpenCode không thấy tool Blender, render ra ảnh trắng.
