# So sánh Gerber PCB nhỏ bạn gửi

File kiểm tra: `Braille-Cell-Small-7.62x29.718mm-Gerber.zip`.
Đối chiếu với: `pcb-order-4cells/Braille-Cell-Gerbers.zip`, là bộ đã dùng để tạo file PCB nhỏ trong export.

## Kết quả xác minh trực tiếp

- ZIP nguyên vẹn, kiểm tra CRC thành công.
- Có đủ hai mặt đồng, hai mặt mask, hai mặt silk, outline và dữ liệu khoan.
- Đọc bằng parser Gerber/Excellon độc lập gerbonara.
- Khi tịnh tiến bản bạn (+20,32; +9,779) mm để cùng gốc với bản mình, toàn bộ hình học đồng trên (79 primitive), đồng dưới (63 primitive) và outline (8 primitive) giống nhau ở độ chính xác xuất 0,000001 mm.
- Cả 37 lỗ đều giống nhau về vị trí và đường kính tại độ chính xác khoan 0,001 mm: 15 lỗ Ø0,35; 12 lỗ Ø0,60; 6 lỗ Ø1,10; 2 lỗ Ø1,60; 2 lỗ Ø2,10.
- Kích thước theo tâm outline thực tế của hai bản đều là **7,620 × 29,718 mm**.

## Khác biệt

| Hạng mục | Bản bạn gửi | Bản mình xuất |
| --- | --- | --- |
| Đồng / outline / vị trí và đường kính lỗ | Giống nhau sau căn gốc | Giống nhau sau căn gốc |
| Gốc tọa độ | X và một số Y âm theo nguồn Eagle | Gốc ở góc trái dưới, tọa độ dương |
| Mask quanh header | Expansion 0,1016 mm; hai cửa sổ liền kề chồng khoảng 0,0412 mm ở đoạn cạnh đối diện | Expansion 0,025 mm; giữ khoảng 0,112 mm mask giữa hai chân header |
| Mask điểm hàn coil | Ø0,7564 mm, bằng đường kính đồng via | Ø0,8064 mm; mở rộng 0,025 mm mỗi bên |
| Via mở mask | Cả 15 via | 12 terminal coil lộ đồng; 3 via chuyển lớp phủ mask |
| Khoan | Một file MixedPlating; có thuộc tính tool đánh dấu PTH/NPTH | Hai file tách PTH và NPTH |
| File job ghi Size | 7,8232 × 29,9213 mm, tính cả độ rộng nét outline | 7,620 × 29,718 mm, đã hiệu chỉnh theo tâm outline |
| Silkscreen | Có nét chữ trên mặt trên | PCB nhỏ không có chữ in |
| Gerber copper pad | Dùng aperture macro cho hình pad bát giác | Dùng region, không cần aperture macro |

Tọa độ âm, aperture macro và file MixedPlating là các cách xuất được phép; bản thân chúng không chứng minh file lỗi. Tuy nhiên cần xưởng hiểu đúng phân loại lỗ. Với file khoan này, Ø0,35/0,60 mm là lỗ mạ; Ø1,10/1,60/2,10 mm là lỗ không mạ, theo các thuộc tính trong file.

Header mở mask nhập nhau là lựa chọn có chủ ý trong README của bạn gửi. Nó không làm thay đổi đường đồng và không đồng nghĩa mạch bị chập. Đổi lại, không còn lớp mask cách giữa các chân ở vùng cửa sổ nhập nhau; bản mình giữ lớp mask đó để hỗ trợ hàn các chân nhỏ.

## Kết luận

Đây là đúng bộ PCB nhỏ, không nhầm bo lớn như ZIP công bố ban đầu. Về mạch đồng và lỗ, bản này tương đương bản mình. Các khác biệt chủ yếu là lớp phủ, chữ, gốc tọa độ và cách đóng gói khoan.

Nếu dùng bản bạn gửi, xưởng cần xác nhận kích thước theo **tâm đường viền 7,620 × 29,718 mm**, không scale bo theo kích thước job 7,8232 × 29,9213; đồng thời đọc đúng lỗ mạ/không mạ. Bản mình đã làm rõ các mục này và giữ web mask giữa chân header.

Chưa chạy DRC từ source của bạn vì chỉ có Gerber, chưa thử phần cứng hoặc nhận DFM từ xưởng. Kết luận hình học dựa trên so sánh các lớp Gerber và khoan thực tế; không chỉ so tên file, ảnh hoặc kích thước ZIP.

Ghi chú thư mục export lúc kiểm tra: hai file đang có tên `PCB-nho-Gerber.zip.txt` và `PCB-to-Gerber.zip.txt`. Nội dung vẫn là ZIP hợp lệ. Nếu xưởng nhận theo đuôi file, cần bỏ `.txt` để gửi dưới dạng `.zip`. Lần kiểm tra này không đổi tên hoặc sửa các file của bạn.
