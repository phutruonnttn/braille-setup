# Cập nhật PCB theo DFM xưởng Việt Nam — 13/10/2026

## Yêu cầu đã áp dụng

- Via drill tối thiểu: 0.30 mm.
- Chênh lệch đường kính đồng ngoài và lỗ via tối thiểu: 0.40 mm.
- Track tối thiểu: 0.20 mm.
- Khoảng cách đồng thông thường tối thiểu: 0.20 mm.
- Ngoại lệ pad cố định trong cùng footprint: tối thiểu 0.15 mm.

## Thay đổi thực tế

PCB nhỏ giữ nguyên outline, pad, via, lỗ, net, độ rộng track và UUID. Chỉ tọa
độ đầu/cuối của 44/88 đoạn track được dịch; độ dịch lớn nhất là 0.1147 mm.
Khoảng cách track nhỏ nhất sau sửa là 0.2010 mm. Track vẫn rộng 0.2032 mm.

Via/terminal vẫn dùng drill 0.35 mm và đồng ngoài 0.7564 mm, do đó chênh đường
kính là 0.4064 mm và vòng đồng mỗi bên là 0.2032 mm. Không tăng via vì kích
thước gốc đã đáp ứng con số xưởng đưa ra và tăng thêm sẽ làm giảm clearance.

Hai nhóm header 1.27 mm có pad cố định với khe danh nghĩa 0.162 mm, được kiểm
tra theo ngoại lệ 0.15 mm mà xưởng đã nói có thể chấp nhận.

PCB lớn không đổi routing vì DRC copper theo rule mới không có lỗi.
Ảnh CAM xưởng gửi đang chồng F.Cu (đỏ) và B.Cu (xanh); khoảng cách đo giữa hai
lớp không phải clearance trên cùng một lớp. Bộ Gerber PCB lớn đã được xuất lại
từ source đã áp rule xưởng, thay cho bộ ZIP cũ.

## Kết quả xác minh

- PCB nhỏ: KiCad DRC 0 violation, 0 unconnected item.
- PCB lớn: 0 error-level violation, 0 unconnected item. Còn 123 warning:
  122 warning silkscreen/text và 1 via cố ý chỉ nối trên một lớp.
- PCB lớn: min routed track 0.3048 mm; via drill 0.35 mm; via outer copper
  0.7564 mm, chênh đường kính 0.4064 mm.
- PCB nhỏ: 7.620 x 29.718 mm; min track clearance 0.2010 mm; min track width
  0.2032 mm; min drill 0.35 mm.
- Đọc lại Gerber/Excellon bằng `gerbonara`: đúng outline, đủ lớp, đúng 27 PTH
  và 10 NPTH; đủ 12 terminal coil lộ đồng và mở mask ở cả hai mặt.
- Gerber và drill dùng chung plot origin dương; aperture macro bị tắt để tăng
  tính tương thích với CAM của xưởng.

## File quan trọng

- `source/Braille-Cell.kicad_pcb`: PCB nhỏ sau sửa.
- `verification/Braille-Cell-vn-final.json`: DRC cuối PCB nhỏ.
- `verification/cell-gerber-readback.json`: kiểm tra độc lập sau xuất.
- `previews/cell-vn-top.png`, `cell-vn-bottom.png`: preview từ Gerber.
- `release-vn-020mm/`: bộ ZIP cuối gửi xưởng.

Xưởng vẫn phải chạy DFM trên đúng ZIP cuối và trả lại tọa độ/layer nếu CAM của
họ còn báo lỗi. DRC và Gerber readback không thay thế thử nghiệm phần cứng.
