# Đối chiếu phản hồi xưởng Việt Nam — 13/10/2026

**Kết luận:** phản hồi cho thấy xưởng có giới hạn gia công lớn hơn một số khe đồng trong thiết kế. Kích thước via được đo từ bộ hiện tại lại đáp ứng các con số trong tin nhắn, nên cần xác nhận đúng phiên bản file và tọa độ lỗi trước khi đổi via. Chưa có cơ sở kết luận tất cả nhà sản xuất ở Việt Nam không thể làm.

## File thực tế đã đọc

- `export/PCB-nho-Gerber.zip`: một thiết kế cell, SHA256 `2ea2799ef49277b3fa4715836aaffa22e2dab55b275bdee8b30b0552f61b34d6`.
- `export/PCB-to-PCBA.zip`: gói bo lớn có thư mục `Gerber/`, BOM và centroid; SHA256 `9039f242e23edbb327b34704540238b96dd4e63baafa3cb7c069b67edca2cefd`.
- Nguồn bố trí được đối chiếu: `export/PCB-source-KiCad/Braille-Cell.kicad_pcb` và `Braille-Evaluation.kicad_pcb`.

ZIP hiện tại giải nén/CRC bình thường. Đọc Gerber trực tiếp thấy flash đồng tròn Ø0,7564 mm trên cả hai mặt, đối chiếu Excellon lỗ Ø0,35 mm: bo nhỏ có 15 lỗ loại này (12 điểm hàn cuộn + 3 via chuyển lớp), bo lớn có 183 via. Đây không phải kết luận chỉ dựa vào README.

## Đối chiếu từng yêu cầu

| Hạng mục | File hiện tại | Xưởng trong ảnh | Đánh giá |
|---|---|---|---|
| Lỗ via | Ø0,35 mm | Tối thiểu Ø0,30 mm | Đáp ứng kích thước danh nghĩa |
| Đồng ngoài via | Ø0,7564 mm | Một xưởng: lớn hơn lỗ ít nhất 0,4 mm; xưởng khác: lỗ 0,3 cần đồng ngoài ≥0,65 mm | Chênh đường kính hiện tại 0,4064 mm, đáp ứng cả hai cách nêu này |
| Vòng đồng mỗi bên | (0,7564−0,35)/2 = 0,2032 mm | Quy tắc chênh đường kính 0,4 tương đương vòng mỗi bên 0,2 mm | Đáp ứng danh nghĩa, cần xác nhận cách xưởng định nghĩa drill/finished hole |
| Bề rộng track nhỏ nhất, bo nhỏ | 0,2032 mm | ≥0,20 mm | Đáp ứng danh nghĩa; gần giới hạn |
| Bề rộng track nhỏ nhất, bo lớn | 0,3048 mm | ≥0,20 mm | Đáp ứng danh nghĩa |
| Khe track khác net cùng lớp, bo nhỏ | Đo nhỏ nhất 0,1524 mm | ≥0,20 mm hoặc ≥0,35 mm | Không đáp ứng hai mức này |
| Khe track khác net cùng lớp, bo lớn | Đo nhỏ nhất 0,2032 mm | ≥0,20 mm hoặc ≥0,35 mm | Riêng track–track đạt 0,20; không đạt 0,35. Chưa bao gồm pad và zone |
| Header pitch 1,27 mm | Pad rộng 1,108 mm → khe danh nghĩa 0,162 mm | Một xưởng cho ngoại lệ cục bộ 0,15 mm; xưởng kia chưa nói có ngoại lệ | Cần xác nhận xưởng chấp nhận vùng header; mức 0,35 áp dụng mọi nơi sẽ cần sửa cả footprint/đấu nối |

Script đo được 15 cặp đoạn track ở bo nhỏ dưới khe 0,20 mm; 24 cặp dưới 0,35 mm. Bo lớn có 332 cặp đoạn track dưới 0,35 mm và 184 cặp via–track dưới 0,35 mm. Đây là số cặp hình học, không phải số vị trí sửa độc lập. Một vùng có thể tạo nhiều cặp. Khoảng cách vòng đồng via tới track khác net nhỏ nhất: bo nhỏ 0,2314 mm, bo lớn 0,2032 mm.

Đây là phép đo giới hạn phạm vi: **không phải DRC đầy đủ**. Chưa đo toàn bộ pad, zone, các cổ đồng nhỏ, mask và dung sai sản xuất theo quy trình xưởng. Không tuyên bố bo lớn đã đạt DFM chỉ từ track–track ≥0,20 mm.

## Con số 0,022 mm trong ảnh

Ảnh không có tọa độ, tên layer, net hoặc báo cáo DFM. Chưa thể xác định 0,022 mm đang đo khe đồng giữa hai net, một đoạn hình học nhỏ, hay một phần của phép đo đường chéo. Không tìm thấy khe track–track khác net cùng lớp 0,022 mm trong phép đo hiện tại. Không coi điều này là chứng minh ảnh sai; cũng không sửa file theo con số đó khi chưa định vị được.

Nên yêu cầu xưởng xác nhận tên ZIP đã mở, lớp đồng F.Cu/B.Cu và tọa độ X/Y của từng lỗi; cần biết lỗi là track–track, via–track, pad–track, pad–pad, soldermask hay cổ đồng cùng net. Nếu họ đo khác file đang có, so sánh đúng phiên bản trước.

## Vì sao lần xuất trước vẫn có thể bị xưởng từ chối?

Bộ trước được xuất/kiểm tra theo khoảng cách đồng **0,1524 mm (6 mil)** và cấu trúc gốc. Báo cáo DRC lưu trong dự án có 0 lỗi mức error và 0 kết nối thiếu dưới các quy tắc đó; đây không phải chứng nhận đáp ứng các quy tắc mới 0,20/0,35 mm. Kiểm tra CRC và xuất Gerber đúng định dạng cũng không thay thế DFM của nhà máy.

## Các hướng xử lý

1. **Xác nhận đúng file trước.** Via hiện tại đã đủ lớn theo tin nhắn. Chỉ tăng via nếu xưởng đưa yêu cầu khác hoặc chỉ ra lỗi cụ thể; tăng vòng đồng có thể làm khe tới mạch bên cạnh nhỏ hơn.
2. **Nếu muốn làm tại xưởng chấp nhận khe 0,20 mm:** có thể đặt bộ quy tắc 0,20 mm, giữ ngoại lệ 0,15 mm ở footprint/pad cố định mà xưởng xác nhận, rồi sửa các khe thực sự vi phạm. Bo nhỏ có mật độ cao nên vẫn cần kiểm tra khả năng đi lại đường và vùng quanh lỗ ferrite. Bo lớn có track–track đạt 0,20 nhưng vẫn cần DRC toàn bộ pad/zone.
3. **Nếu xưởng bắt 0,35 mm cho toàn bộ đường đi:** đây là thay đổi layout đáng kể, không giải quyết bằng tăng via. Giữ nguyên net điện; di chuyển/đi lại các đường, kiểm tra header, lỗ lắp và vị trí kết nối. Nếu đổi vị trí linh kiện bo lớn, xuất lại centroid. Nếu đổi kích thước bo hoặc header bo nhỏ, đối chiếu và có thể phải in lại cơ khí.
4. **Gửi xưởng khác có khả năng phù hợp để họ DFM trước khi chốt.** Ví dụ [JLCPCB công bố](https://jlcpcb.com/capabilities/Capabilities) PCB 2 lớp 1 oz hỗ trợ track/space 0,10/0,10 mm và via nhỏ hơn cấu hình hiện tại. Tuy nhiên PTH, mask, khoảng cách lỗ tới track và pad phải xét riêng; công bố năng lực không xác nhận họ chắc chắn nhận nguyên bộ này. Có thể sản xuất bo trống ở nơi khác rồi thuê xưởng Việt Nam sourcing/lắp ráp bo lớn nếu họ nhận bo khách cấp.

Ưu tiên thực tế: xác nhận file và lấy DFM cụ thể; nếu chọn xưởng Việt Nam, ưu tiên mức khe 0,20 mm có ngoại lệ pad cố định 0,15 mm được xác nhận. Chưa chỉnh copper hay tạo Gerber thay thế trong lần đối chiếu này.

## Tin nhắn gửi xưởng

> Anh giúp em xác nhận đang kiểm tra PCB-nho-Gerber.zip và phần Gerber trong PCB-to-PCBA.zip bản em gửi mới nhất nhé. Em kiểm tra file khoan/Gerber hiện tại thấy via có lỗ 0,35 mm, đồng ngoài 0,7564 mm, vòng đồng mỗi bên 0,2032 mm. Track nhỏ nhất bo nhỏ 0,2032 mm, bo lớn 0,3048 mm.
>
> Thiết kế có một số khe đồng dưới 0,20 mm và pad header pitch 1,27 mm có khe khoảng 0,162 mm. Anh cho em xin ảnh lỗi có tọa độ X/Y, lớp đồng và loại lỗi cụ thể, nhất là chỗ đo 0,022 mm, để em sửa đúng vị trí.
>
> Nhờ anh xác nhận mức khoảng cách xưởng yêu cầu là 0,20 hay 0,35 mm; vùng pad/header cố định có được chấp nhận 0,15 mm không? Em sẽ dùng mức xưởng xác nhận để sửa và gửi lại bộ kiểm tra, rồi mới chốt sản xuất.

Kết quả máy đọc: [JSON đo hình học](vn-dfm-2026-10-13.json). Script tái tạo: [vn-dfm-2026-10-13.py](vn-dfm-2026-10-13.py).
