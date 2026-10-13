# Bộ đặt PCB: 4 cell nhỏ + 1 bo điều khiển lớn

Đã xuất mới bằng **KiCad 10.0.6** từ đúng nguồn Eagle và đọc lại các lớp Gerber/Excellon bằng **gerbonara**. File gốc trong thư mục dự án không bị ghi đè.

## Gửi những file nào

| Đơn hàng | Số PCB thành phẩm | File gửi xưởng |
| --- | ---: | --- |
| PCB nhỏ cho một cell | **4** | `Braille-Cell-Gerbers.zip` |
| PCB lớn điều khiển 8 cell | **1** | `Braille-Evaluation-Gerbers.zip` |
| Lắp SMD cho bo lớn, nếu đặt PCBA | **1 bộ / 72 linh kiện** | `bom/Evaluation-BOM-SMD.csv` + `assembly/Evaluation-Top-Centroid.csv`, hoặc gói `Braille-Evaluation-PCBA.zip` |

PCB nhỏ là **một thiết kế lặp lại 4 lần**, chưa ghép thành panel. Xưởng có thể panelize theo quy trình của họ. Nếu xưởng có MOQ 5, số lượng báo giá có thể lớn hơn 4; không thay đổi thiết kế để ép số lượng.

**Không dùng lại ZIP Module bị nhầm của tác giả. Không trộn centroid cũ với Gerber mới.**

## Thông số gia công

- Hai lớp đồng, FR-4, độ dày danh nghĩa 1,6 mm, đồng 1 oz là cấu hình dự kiến cho cả hai bo. Độ dày gốc của bo lớn được ghi là 1,57 mm; 1,6 mm là giá trị danh nghĩa sử dụng cho bộ xuất mới. Chưa xác minh dung sai lắp của phần cơ khí đã in; PCB nhỏ cần đúng độ dày phù hợp với chi tiết của bạn.
- PCB nhỏ: **7,620 × 29,718 mm**, tính theo tâm đường outline. PCB lớn: **98,01225 × 89,6112 mm**.
- Đường viền Gerber có bề rộng nét 0,2032 mm kế thừa Eagle. Gia công theo **tâm đường viền**, không lấy biên ngoài nét làm kích thước bo. Metadata kích thước trong job file đã được hiệu chỉnh theo tâm outline đã kiểm chứng.
- Clearance đồng được kiểm tra ở **0,1524 mm (6 mil)**; khoảng cách đồng–mép bo **0,30 mm**; khoảng cách đồng–lỗ **0,20 mm**. Xưởng cần hỗ trợ các mức này. Đây là quy tắc theo hình học thiết kế, chưa phải xác nhận DFM của một xưởng cụ thể.
- Dữ liệu khoan được tách rõ PTH và NPTH. PCB nhỏ: 27 lỗ mạ + 10 lỗ không mạ. PCB lớn: 325 lỗ mạ + 4 lỗ không mạ.
- **12 lỗ hàn coil trên PCB nhỏ phải để lộ đồng cả hai mặt**; không tent/plug/fill các lỗ này. Ba via chuyển lớp còn lại giữ tenting.
- Header có pitch **1,27 mm**, drill hoàn thiện **0,60 mm**. Chọn pin phù hợp, chẳng hạn chân vuông 0,40 mm của loại header gốc; tránh tự đổi sang header 2,54 mm hoặc chân lớn hơn.
- Đã giảm solder mask expansion riêng quanh header 1,27 mm và terminal coil xuống 0,025 mm để không nhập các cửa sổ mask của chân khác net. Giữ cấu hình này khi xưởng chuẩn bị CAM.

## BOM đã sửa

- C1–C5 = **100 nF**, C6 = **1 µF**; đã bỏ toàn bộ mô tả 9 pF gây nhầm. Tụ 0603, X7R, điện áp tối thiểu 25 V.
- R1 = **1 kΩ**, chọn **Bourns 3362P-1-102LF**; R3 = **240 Ω**.
- Đã bổ sung **J2** bị thiếu vào danh sách phần hàn tay; J2/J3 là đầu nối 1×2, pitch 2,54 mm.
- IC1/IC4 dùng **TBD62083AFG,EL**, đúng loại sink DMOS được tác giả nêu trong log. Đã đối chiếu pinout Toshiba với symbol TD62083 trong Eagle: pin 9 GND, pin 10 COMMON, output 1 tại pin 18. Footprint SOP-18, pitch 1,27 mm.
- Q1/Q2 dùng **TBD62783AFG,EL**, source DMOS; pin 9 VCC, pin 10 GND. Không đổi nhầm FG thành FNG/SSOP hoặc PG/DIP.
- U2 chọn **TI LM317AEMP/NOPB**, SOT-223, ADJ/OUT/IN = chân 1/2/3 và tab = OUT. Dòng/độ nóng thực tế phụ thuộc tản nhiệt và tải coil.
- Đã tách logo, module Braille, Arduino Nano, trimmer và đầu nối ra khỏi BOM cho máy gắp SMT. BOM SMD có đúng **72 designator**, khớp file centroid mới.
- Giữ đầy đủ 56 BAV99 và toàn bộ driver/decoder trên bo lớn; 4 cell chỉ chiếm **U$1–U$4**, U$5–U$8 để trống. Không cần cắt bớt mạch driver.

`Evaluation-BOM-Corrected.csv` gồm phần SMT và phần hàn tay trên bo lớn. `Evaluation-BOM-SMD.csv` chỉ dùng cho SMT; `Evaluation-BOM-Hand-Assembly.csv` dùng cho trimmer, jack, Nano, đầu nối và socket. `Four-Cells-BOM.csv` ghi vật tư cho đúng 4 module, kể cả các chi tiết đã in.

Các cột LCSC không được điền bằng mã đoán. Xưởng có thể chọn linh kiện thụ động theo thông số và gán mã kho tương ứng. **J1 cần xưởng đối chiếu hình footprint trước khi chọn jack**: nguồn gốc dùng ba lỗ tròn Ø1 mm, không phải mọi jack cùng cỡ đầu cắm đều có chân phù hợp. Bản xem footprint có trong `previews/J1-footprint.svg`.

## Vật tư cho 4 cell

- 24 coil tự quấn; 24 lõi ferrite Fair-Rite 3067990831; 24 nam châm Ø1 × 0,5 mm N52.
- 8 male header 2×3, pitch 1,27 mm trên 4 PCB nhỏ.
- 8 female socket 2×3, pitch 1,27 mm trên bo lớn nếu dùng kết nối tháo rời cho 4 cell. Socket là phương án kết nối đề xuất; cần xác nhận chiều cao ăn khớp với header đã mua. Có thể hàn trực tiếp chân module nếu không dùng socket.
- 24 cam, 24 dot, 4 upper và 4 lower theo CAD V12.

Nếu bạn vẫn mua theo bảng cũ với **20 nam châm và 12 lõi ferrite**, lượng đó thiếu **4 nam châm và 12 lõi** cho 4 cell. Các số trên chưa cộng linh kiện dự phòng.

## Thay đổi trong file PCB

1. PCB nhỏ: giữ nguyên đường đồng, vị trí header, lỗ và outline. Chuyển 12 via dùng để hàn coil thành pad PTH có cùng vị trí, cùng đường kính đồng và khoan; bảo đảm lộ đồng trên mask. Ba via chuyển lớp giữ nguyên.
2. Hai bo: giảm expansion mask riêng quanh header 1,27 mm để giữ web mask giữa các chân.
3. Bo lớn: mô hình hóa đúng tab OUT của LM317 bằng pad số 2 nối nội bộ với chân OUT. Gán cùng net và cho phép hai pad chung số nối qua thân linh kiện; không thêm dây nối sai hoặc nối tab xuống GND.
4. Bo lớn: dùng kết nối đồng đặc tại pad GND của Nano thay cho thermal chỉ còn một spoke khi refill trong KiCad.
5. Chuyển 19 nét đồ họa footprint không được importer gán layer sang F.Fab; đây là nét tài liệu, không phải đồng hay đường cắt.
6. Xuất lại centroid từ tâm bao các pad SMD, cùng gốc tọa độ với Gerber và khoan. File `KiCad-footprint-origins.csv` chỉ là dữ liệu tham chiếu nguồn, **không phải centroid gửi máy gắp**.

Centroid cũ của tác giả ghi C5 khoảng (40,14; 82,14) mm và C6 (40,14; 79,97) mm, trong khi nguồn Eagle hiện tải được đặt chúng lần lượt ở (40,13835; 82,77860) và (39,50335; 80,60055) mm. Đây là một lý do cụ thể cần dùng centroid mới.

## Kết quả kiểm tra

- PCB nhỏ: **0 violation, 0 unconnected item** với các quy tắc nêu trên.
- PCB lớn: **0 violation mức error, 0 unconnected item**. Còn **123 warning**: 122 về chữ/đường silk và 1 via N$37 nối trên một lớp. Gerber silk đã trừ phần mask để không in đè lên bề mặt hàn. Cảnh báo chữ nhỏ vẫn còn; không tuyên bố silkscreen hoàn hảo.
- Đã đối chiếu 12 contactref của bo nhỏ và 429 contactref của bo lớn với net gốc Eagle trước sửa; số track/via lúc import khớp nguồn.
- Đã đọc lại Gerber và Excellon bằng parser độc lập, kiểm tra kích thước outline, đủ lớp, số lượng/đường kính lỗ và xác nhận đủ 12 terminal coil lộ đồng trên cả hai mặt mask.
- Có ảnh xem trước render trực tiếp từ Gerber mới trong `previews/`.

Chưa thử phần cứng, chưa xác minh cơ khí với bản in thực tế, chưa nhận DFM của xưởng. DRC tốt không thay thế kiểm tra hoạt động prototype. Xưởng PCBA cần đối chiếu mã hàng và chiều linh kiện trong preview trước chạy máy; file centroid dùng góc theo footprint KiCad, có thể cần hiệu chỉnh theo thư viện máy của xưởng.

## Tái tạo bộ xuất

Các script có trong thư mục này. `prepare_boards.py` chỉ chạy sau khi import lại file gốc; không chạy lần hai trực tiếp trên file đã chuyển coil sang pad. KiCad Python được sử dụng để sửa và kiểm tra parity; `build_bom.py` tạo CSV; `export_centroids.py` xuất vị trí; `verify_gerbers.py` cần gerbonara để đọc lại Gerber.

Nguồn tham khảo:

- Dự án và xác nhận tụ/trimmer của tác giả: https://hackaday.io/project/191181-electromechanical-refreshable-braille-module
- Driver DMOS trong log: https://hackaday.io/project/191181/log/223649-braille-module-driver-pcbs
- Toshiba sink driver: https://toshiba.semicon-storage.com/info/docget.jsp?did=29893&prodName=TBD62083AFG
- Toshiba source driver: https://toshiba-semicon-storage.com/info/TBD62783AFG_datasheet_en_20160511.pdf?did=30523&prodName=TBD62783AFG
- TI LM317A: https://www.ti.com/lit/ds/symlink/lm317a.pdf
- Bourns trimmer: https://www.bourns.com/docs/product-datasheets/3362.pdf
- KiCad CLI: https://docs.kicad.org/10.0/en/cli/cli.html
