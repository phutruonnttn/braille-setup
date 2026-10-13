# Kiểm tra PCB Braille — 12/10/2026

## Kết luận chính

**Không dùng `Braille Module Gerber File.zip` để đặt PCB nhỏ cho một Braille cell.** Bộ ZIP này chứa bo điều khiển lớn, không khớp với `Braille Cell.brd`.

Các ZIP gốc đều giải nén được và vượt qua kiểm tra CRC. Không thấy dấu hiệu tải hỏng. File gốc được giữ nguyên.

Đã tải lại hai ZIP Gerber/PCBA từ link tác giả đăng trong log: cả hai trùng từng byte với bản bạn đã tải. Lỗi nhầm Gerber vì vậy có ngay trong bộ tác giả công bố, không phải do bạn tải sai hoặc file hỏng khi tải.

| Hạng mục | Nguồn đúng / nội dung thực tế | Kích thước đường viền |
| --- | --- | --- |
| PCB nhỏ cho một cell, 6 cuộn dây | `Braille Cell Eagle Source Files.zip` → `Braille Cell.brd` + `.sch` | 7,620 × 29,718 mm |
| PCB lớn điều khiển tối đa 8 cell | `Braille Evaluation Board Eagle Source Files.zip`; Gerber nằm bên trong `Braille Evaluation Board PCBA Files.zip` | 98,01225 × 89,6112 mm |
| ZIP mang tên `Braille Module Gerber File.zip` | Thực tế chứa thiết kế bo lớn | 98,01225 × 89,6112 mm |

Kích thước trên tính từ tâm đường viền layer 20 của Eagle. Đây chưa phải kiểm tra dung sai lắp ghép với CAD V12.

## Bằng chứng nhầm bộ Gerber

So sánh `Braille Module Gerber File.zip` với ZIP `Braille Evaluation Board Gerber files.zip` nằm trong bộ PCBA:

- GTL và GBL (đồng mặt trên/dưới): giống từng byte.
- GKO (đường viền): giống từng byte.
- GTS và GBS (solder mask): giống từng byte.
- GTP và GBP (paste): giống từng byte.
- GBO: giống từng byte.
- XLN (khoan): giống sau khi bỏ dòng thời gian xuất file.
- GTO (silkscreen trên): có khác biệt; không làm thay đổi kết luận về đường đồng, khoan và kích thước bo.
- `gerber_job.gbrjob` trong ZIP Module cũng ghi kích thước 98,01225 × 89,6112 mm, hai lớp đồng.

Do đó bộ tải về hiện có **chưa cung cấp đúng Gerber sẵn dùng của PCB nhỏ**. Cần xuất lại từ đúng `Braille Cell.brd`, hoặc gửi file Eagle này cho xưởng có khả năng xuất CAM.

## PCB nhỏ: những điểm cần đối chiếu khi xuất CAM

Đọc trực tiếp file nguồn cho thấy:

- Một footprint BRAILLE-6, 12 net riêng tương ứng 12 đầu dây của 6 coil.
- Hai cụm header 2×3, pitch 1,27 mm; drill pad header 0,6 mm.
- 6 lỗ lõi ferrite Ø1,1 mm; ngoài ra có 2 lỗ Ø2,1 mm và 2 lỗ Ø1,6 mm trong phần plain/hole.
- 15 via, drill Ø0,35 mm. 12 via đặt cạnh lõi phục vụ hàn coil, 3 via còn lại chuyển lớp đường mạch.
- Đường mạch nhỏ nhất được khai báo trong các signal là 0,2032 mm.
- Không có wire layer 19 trong file. Điều này không thay thế kiểm tra kết nối và DRC trong phần mềm PCB.

Để xuất bộ đặt hàng, dùng EAGLE/CAM hoặc phần mềm có thể import EAGLE XML rồi xuất Gerber và Excellon. Kiểm tra kết quả trong Gerber viewer độc lập:

1. Đường viền phải khoảng 7,62 × 29,72 mm, có 6 lỗ Ø1,1 mm ở vùng coil và 12 chân header ở hai đầu.
2. Các via hàn đầu coil phải mở solder mask và lộ đồng. Tác giả yêu cầu rõ điều này; không chọn tent/plug toàn bộ via một cách mặc định.
3. Xuất đủ hai mặt đồng, hai mặt solder mask, outline, silkscreen cần dùng và dữ liệu khoan; phân biệt lỗ mạ và không mạ theo thiết kế.
4. Kiểm tra clearance quanh lỗ và mép bo với khả năng gia công của xưởng. Tác giả đã ghi nhận phải nới quy tắc DRC ở những vùng này. Một lô tác giả làm thành công không bảo đảm mọi xưởng đều nhận.
5. Xác nhận độ dày PCB và dung sai lỗ với phần cơ khí đã in. Chưa có kết luận về độ dày thích hợp của PCB nhỏ từ lần kiểm tra này.

Gói `Braille-Cell-correct-Eagle-source.zip` trong thư mục này chỉ chứa đúng nguồn Eagle và library để giao cho xưởng/CAM; **không phải bộ Gerber đã được chứng nhận để sản xuất**.

## Bo lớn: lỗi thông tin trong BOM

CSV BOM có cột Comment/Description của C5/C6 ghi 9 pF, trong khi cột Value và file Eagle ghi:

| Designator | Giá trị cần dùng |
| --- | --- |
| C1–C5 | 0,1 µF (100 nF) |
| C6 | 1 µF |
| R1 | Biến trở 0–1 kΩ, footprint 3362P |
| R3 | 240 Ω |

Tác giả xác nhận giá trị tụ và biến trở trong bình luận ngày 27/01/2024. R3 đọc từ nguồn Eagle/CSV. Vì thế không nên để xưởng chọn linh kiện C5/C6 dựa riêng vào chuỗi “9.0PF”.

Cột LCSC Part # của BOM đang trống. Các mục như BRAILLE-6, Arduino Nano và logo cũng xuất hiện trong BOM nhưng không phải tất cả đều là linh kiện SMT để máy gắp. Cần chốt danh sách linh kiện thực sự lắp, mã hàng và các phần hàn tay trước khi đặt PCBA.

ZIP PCBA bên ngoài chứa BOM, centroid và một ZIP Gerber bên trong. Nếu cổng đặt hàng chỉ nhận Gerber, upload ZIP Gerber bên trong; BOM và centroid được gửi vào các mục tương ứng.

Chưa sửa BOM gốc hoặc chọn linh kiện thay thế; cần kiểm tra đúng mã IC và pinout trước khi đặt lắp ráp.

## Đối chiếu bảng của bạn và video

Đọc được Google Sheets `Braille 3D`, gồm các tab Braille, Coil Winding Tool, 3D Print và Order. Trong Order đang có Braille PCB ×2 và Larger PCB ×1. Hai mục này cần hai bộ thiết kế riêng.

Đã lấy metadata video và xem storyboard/khung hình mẫu: khoảng 1:36–1:42 có PCB nhỏ và thao tác coil; khoảng 3:02 có bo điều khiển lớn. Không lấy được transcript tự động; không tuyên bố đã nghe hoặc kiểm tra từng khung hình của toàn video.

## Nguồn

- Dự án: https://hackaday.io/project/191181-electromechanical-refreshable-braille-module
- Thiết kế PCB, yêu cầu mở solder mask ở via: https://hackaday.io/project/191181/log/223535-pcb-design-of-braille-cell-evaluation-board
- Log gia công và giới hạn DRC: https://hackaday.io/project/191181/log/223649-braille-module-driver-pcbs
- Hướng dẫn lắp: https://hackaday.io/project/191181/instructions
- Video: https://www.youtube.com/watch?v=BXi1tG78AW4
- Bảng của bạn (chỉ đọc): https://docs.google.com/spreadsheets/d/1n8VOP-WUzwAJ5pPl9g75yRddvFoka2YRsmup5m-X4bY/edit

## Phạm vi xác minh

Đã kiểm tra tính toàn vẹn ZIP, so sánh các lớp Gerber, phân tích XML Eagle và đối chiếu tài liệu tác giả. Chưa chạy DRC/ERC trong EAGLE/KiCad, chưa thử phần cứng, chưa xác minh toàn bộ dung sai CAD–PCB, chưa xuất lại CAM. Lỗi nhầm bộ Gerber và mâu thuẫn BOM đã có bằng chứng trực tiếp; chưa đủ cơ sở kết luận toàn bộ mạch không có lỗi điện.
