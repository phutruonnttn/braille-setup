# Lõi ferrite thay thế cho Braille — nghiên cứu ngày 12/10/2026

**Kết quả:** có hai mã tiêu chuẩn cùng kích thước và ba đầu mối châu Á đáng hỏi mua mẫu. Chưa xác minh được sản phẩm thay thế vừa có sẵn tại Singapore, vừa bán lẻ số lượng nhỏ, vừa chạy tương đương trong cơ cấu Braille. Các lựa chọn dưới đây là ứng viên thử nghiệm hoặc đầu mối hỏi hàng; chưa phải linh kiện thay thế đã được phê duyệt.

Theo email bạn cung cấp, Fair-Rite Asia xác nhận không có hàng để lấy tại Singapore; MOQ/SOQ thông thường 6.000 chiếc, đơn nhỏ tùy tồn kho Mỹ, vận chuyển Ex-Factory và đề nghị khách tự thu xếp courier. Vì vậy, hỏi tiếp văn phòng này không giải quyết được yêu cầu mua sẵn nội địa hiện tại.

## Ràng buộc của bộ đang làm

- 4 cell × 6 lõi = **24 lõi sử dụng**. Có thể hỏi 3–6 mẫu để thử trước, sau đó 30–50 chiếc tính cả dự phòng.
- Lõi gốc: thanh ferrite mềm đặc, không phủ, **Ø1,00 ±0,025 × 10,00 ±0,30 mm**, NiZn material 67. [Fair-Rite 3067990831](https://fair-rite.com/product/antennarfid-rods-3067990831/).
- PCB nhỏ có sáu lỗ lõi Ø1,10 mm theo [kiểm tra file nguồn](../pcb-audit/README-kiem-tra-PCB.md). Thanh Ø1,2/1,5/2 mm cần sửa PCB và kiểm tra lại cơ khí, cuộn dây, jig quấn và khoảng cách tới nam châm.
- Đúng đường kính và chiều dài chỉ xác nhận hình học danh nghĩa; chưa xác nhận lực lật cam, nhiệt độ hay độ tin cậy.

## Những vật liệu/mã đáng thử

| Lựa chọn | Hình học | Vật liệu; độ từ thẩm ban đầu | Độ từ thẩm thanh µROD | Kết luận |
|---|---|---|---:|---|
| [3067990831 — gốc](https://fair-rite.com/product/antennarfid-rods-3067990831/) | Ø1 × 10 mm | NiZn 67; µi 40 | 22 | Mốc so sánh đã được tác giả dùng |
| [3061990831](https://fair-rite.com/product/antennarfid-rods-3061990831/) | Cùng kích thước và dung sai với lõi gốc | NiZn 61; µi 125 | 35 | Ưu tiên thử trong hai mã cùng hình học; chưa có nguồn châu Á được xác nhận |
| [3078990831](https://fair-rite.com/product/antennarfid-rods-3078990831/) | Cùng kích thước và dung sai với lõi gốc | MnZn 78; µi 2300 | 48 | Tính chất khác đáng kể, chỉ mua mẫu để đánh giá |
| [Tomita 6D8](https://www.tomita-electric.com/en/material/std-ni/) | **Chưa xác nhận có thanh Ø1 × 10 mm** | NiZn; µiac 73 | Chưa có | Là tên vật liệu để hỏi hãng, không phải mã thanh bán sẵn |

µi và µROD là hai đại lượng khác nhau. Không thể suy ra lực tác động tăng theo tỷ lệ 2300/40 khi đổi sang material 78. Với cơ cấu có nam châm vĩnh cửu và cuộn kích bằng xung, cần đo đáp ứng thực tế. Đây là nhận định kỹ thuật, không phải kết quả thử các vật liệu thay thế.

Lý do đưa Tomita 6D8 vào danh sách hỏi: NiZn có µiac 73 và Hc 240 A/m; lõi gốc có Hc 3 Oe, tương đương khoảng 239 A/m. Sự gần nhau của vài thông số **không chứng minh tương đương**; điều kiện đo, đường cong từ hóa, hình học và lực hút cam vẫn cần đánh giá. Không tự tạo mã hàng kiểu “6D8-R-1X10”.

## Đầu mối 1 — Infantron tại Singapore / Tomita Electric

[Infantron](https://infantron.net/) công bố phân phối ferrite Tomita Electric và linh kiện từ tùy chỉnh.

- Email: **sales@infantron.net**
- Điện thoại: **+65 6299 3900**
- Địa chỉ: **Blk 996 Bendemeer Road, #06-07, B-Central, Singapore 339944**.

Bằng chứng hãng làm được đường kính nhỏ: [catalog thanh Tomita](https://www.tomita-electric.com/en/item/r_ra-type-cores/) có **4D4-R-1X4.8**, Ø1,0 ±0,05 mm, dài 4,8 ±0,2 mm. Mã này quá ngắn để thay trực tiếp. Catalog công khai chưa cho thấy thanh Ø1 × 10 mm. [Tomita](https://www.tomita-electric.com/en/itemcat/ferrite/) công bố sản xuất ferrite tại Nhật và Trung Quốc.

Hỏi thanh Ø1 × 10 mm bằng 6D8 hoặc NiZn phù hợp do hãng đề xuất, từ hàng mẫu/khuôn sẵn; yêu cầu datasheet và nơi xuất hàng. Chưa biết họ nhận 3–6 mẫu hay 30–50 chiếc, có phí tooling hay không. **Chỉ tới địa chỉ khi họ xác nhận hàng và cho tự lấy.**

## Đầu mối 2 — Golden Eagle, Trung Quốc / Thái Lan

Hãng quảng bá [cuộn RFID dùng lõi thanh cỡ nhỏ](https://www.inductor-coil.com/for-tiny-rfid-induction-components-mini-rod-core-air-core-inductive-coil-high-frequency-inductor-with-metal-end-cap-terminals-product/), nên đáng hỏi nguồn lõi thô trước khi quấn. Kích thước cuộn hoàn chỉnh trong quảng cáo không xác nhận đường kính lõi bên trong.

- Email: **sales@goldeneagle-cn.com**
- Điện thoại quốc tế: **+86 769 83517380**
- [Liên hệ chính thức](https://www.inductor-coil.com/contact-us/) có địa chỉ Dongguan, Trung Quốc và Samut Sakhon, Thái Lan; hãng có [trang nhà máy Thái Lan](https://www.inductor-coil.com/thailand-factory/).

Hỏi rõ **lõi rời, chưa quấn**, Ø1 × 10 mm, ferrite mềm NiZn, vật liệu có datasheet; mua mẫu trước. Chưa có bằng chứng họ bán lõi rời đúng kích thước, có tồn kho hoặc nhận MOQ nhỏ. Địa chỉ nhà máy không chứng minh đơn này sẽ xuất từ đó.

## Đầu mối 3 — Superworld tại Singapore

[Danh mục hãng](https://www.superworld.com.sg/our-products/family/) có transponder coil và nhiều linh kiện từ. Có thể hỏi lõi mẫu từ nguồn sản xuất hiện có.

- Email: **sales@superworld.com.sg**
- Điện thoại: **+65 6298 2866**
- Địa chỉ: **16 New Industrial Road, #06-01 to 08, Hudson TechnoCentre, Singapore 536204**.

Chưa tìm thấy mã lõi thô Ø1 × 10 mm được công bố. Đây là đầu mối kỹ thuật để hỏi, chưa phải shop có hàng bán lẻ.

## Những hướng đã kiểm tra nhưng chưa đủ cơ sở đặt

| Nguồn / lựa chọn | Kết quả và lý do chưa chọn |
|---|---|
| [LCSC C22245444 — 3078990831](https://www.lcsc.com/product-detail/Accessories-Inductors-Transformers_Fair-Rite-Products-3078990831_C22245444.html) | Listing truy xuất trong lần nghiên cứu báo hết hàng; lần mở lại URL rút gọn bị lỗi. Chưa xác nhận tồn kho trực tiếp lúc checkout. |
| [JLCPCB C22245444](https://jlcpcb.com/partdetail/Fair_RiteProducts-3078990831/C22245444) | Listing báo stock 0. Dịch vụ preorder của trang dành cho tồn kho lắp PCBA, không giao linh kiện rời; không coi là cách mua lõi để tự quấn. |
| [RS 467-3999, 3078990821](https://sg.rs-online.com/web/p/ferrite-cores/4673999) | Ø0,75 × 7,5 mm; sai hình học. Kết quả tồn kho được lập chỉ mục không nhất quán, chưa xác nhận hàng Singapore. |
| [Mouser 3061990831](https://www.mouser.ca/en/ProductDetail/Fair-Rite/3061990831?qs=aTFcLA2DbqsMe9wDxh%252BNqg%3D%3D) | Có listing mã cùng kích thước, nhưng chưa có bằng chứng đơn sẽ xuất từ châu Á. Không giải quyết yêu cầu tránh ship Mỹ. |
| Ferroxcube ROD1/10-4B1 | Chỉ thấy tên trong catalog bên thứ ba. Chưa xác nhận bằng datasheet hãng và nơi có hàng; không đưa vào đề xuất mua. [Danh mục hãng đã kiểm tra](https://www.ferroxcube.com/de-DE/products_ferroxcube/detail/emi/rod_core). |
| [Magnet-Tech](https://www.magnet-tech.com/core/NiZn/r.htm), [Magason](https://www.magason-tech.com/magnetic-core/nizn-ferrite-core/wound-ferrite-rod-antenna-coil.html) | Các mã nhỏ đã tìm thấy bắt đầu khoảng Ø1,2 mm; không vừa lỗ lõi PCB hiện tại. Hàng tùy chỉnh vẫn cần báo giá/MOQ. |
| Taobao / 1688 / Shopee | Chưa xác minh được listing đúng thanh mềm đặc Ø1 × 10 mm, có thông tin vật liệu. Khả năng truy cập/tìm kiếm sàn bị giới hạn; không kết luận sàn hoàn toàn không có hàng. |

Từ khóa: `镍锌铁氧体 实心磁棒 1×10mm`, `软磁铁氧体 圆棒 直径1mm 长10mm`, `微型 RFID 磁棒 磁芯`. Cần người bán xác nhận **đường kính ngoài của lõi**, không phải lỗ trong hạt ferrite hoặc đường kính dây quấn. Nam châm ferrite vĩnh cửu và hạt chống nhiễu rỗng không phải loại đang tìm.

## Có nên dùng thép/kẹp giấy hoặc lõi to hơn?

Tác giả đã thử lõi thép kẹp giấy 1 mm và ghi nhận nóng cuộn dây, cam bị lực hút giữ lại; khi đổi ferrite, cơ cấu chạy mát hơn và thời gian refresh giảm từ 200 xuống 50 ms. [Nhật ký thử nghiệm của tác giả](https://hackaday.io/project/191181-electromechanical-refreshable-braille-module/log/224226-updated-winding-jig-for-ferrite-cores-vs-steel-cores).

Vì vậy không coi thép là thay thế đã được chứng minh cho bộ hoàn chỉnh. Không tự khoan rộng PCB để nhét thanh 1,2–2 mm: phải kiểm tra đường đồng, CAD, cuộn dây và khoảng hở trước. Cũng chưa có cơ sở nối hai thanh 4,8 mm bằng keo để coi như một thanh 10 mm liên tục.

## Cách tiến hành khi nhận được mẫu

1. Đo đường kính, chiều dài; kiểm tra lắp thử trong PCB, jig và vỏ in, không ép lõi.
2. Quấn một cuộn theo hình học đang dùng; ghi số vòng, chiều dài quấn và điện trở DC. Không tự chọn điện áp/dòng mới chỉ từ µi.
3. Lắp một cam, kiểm tra lật cả hai chiều với điều kiện kích đã được xác nhận cho bộ điều khiển. Theo dõi dòng và nhiệt, tránh vượt giới hạn driver/cuộn dây.
4. Thử sàng lọc khoảng 100 lần đổi trạng thái; ghi số lần không lật, trạng thái giữ và nhiệt. Đây là kiểm tra ban đầu, chưa phải chứng nhận tuổi thọ.
5. Thử một cell đủ sáu chấm trước khi nhân lên bốn cell. Chỉ cập nhật BOM sau khi chọn và thử được vật liệu thực tế.

[Mẫu email tiếng Anh và tin hỏi tiếng Trung](ferrite-alternative-RFQ.txt) đã chuẩn bị để hỏi ba đầu mối. Chưa gửi liên hệ hay đặt hàng.
