**Kimball's Framework (Dimensional Modeling)** là phương pháp luận (methodology) do **Ralph Kimball** (cùng Margy Ross) phát triển, trình bày chi tiết trong cuốn sách nổi tiếng *The Data Warehouse Toolkit*. Phương pháp này ra đời nhằm giúp việc truy vấn dữ liệu kinh doanh trở nên dễ hiểu hơn và tăng tốc độ xử lý báo cáo trong các hệ thống Data Warehouse

Đây được xem là bộ chuẩn mực phổ biến nhất cho việc thiết kế Data Warehouse hiện đại.

---

### Các đặc điểm chính của Kimball's Framework

#### 1. Phương pháp tiếp cận Bottom-up (Từ dưới lên)

Xây dựng kho dữ liệu dựa trên các quy trình nghiệp vụ cụ thể (*Business Processes*) trước (như bán hàng, quản lý kho, chăm sóc khách hàng), sau đó hợp nhất lại thành Kho dữ liệu tổng thể thông qua các **Conformed Dimensions** (chiều dùng chung như Ngày tháng, Khách hàng).

#### 2. Quy trình thiết kế 4 bước (4-Step Dimensional Design Process)

* **Bước 1: Chọn quy trình nghiệp vụ (Select the business process):** Xác định hoạt động cần phân tích (ví dụ: Quy trình đặt hàng).
* **Bước 2: Xác định mức độ chi tiết (Declare the grain):** Xác định 1 dòng trong bảng Fact đại diện cho cái gì (ví dụ: Mỗi dòng đại diện cho 1 sản phẩm trong 1 hóa đơn).
* **Bước 3: Xác định các chiều (Identify the dimensions):** Trả lời các câu hỏi Ai? Cái gì? Ở đâu? Khi nào? Tại sao?
* **Bước 4: Xác định các chỉ số (Identify the facts):** Các số liệu cần tính toán (ví dụ: Tổng tiền, Số lượng, Tiền giảm giá).

#### 3. Hai thành phần cốt lõi: Fact Tables & Dimension Tables (Star Schema)

Mô hình chiều kết nối hai thành phần cơ bản để tạo thành mô hình hình sao (**Star Schema**) – với Fact table nằm ở trung tâm và các Dimension table tỏa ra xung quanh:

**Bảng Sự kiện (Fact tables):**
* **Bản chất:** Đóng vai trò như các **động từ** (*Verbs*), ghi lại các sự kiện nghiệp vụ hoặc đo lường hoạt động thực tế (ví dụ: *"Một đơn hàng được đặt"*, *"Một giao dịch chuyển tiền đã xảy ra"*).
* **Nội dung:** Chứa các chỉ số định lượng có thể đo lường/tính toán (doanh số, số lượng sản phẩm, thời gian xử lý) cùng với các khóa ngoại (*foreign keys*) để liên kết tới các Dimension tables.


**Bảng Chiều (Dimension tables):**
* **Bản chất:** Đóng vai trò như các **danh từ** (*Nouns*), cung cấp ngữ cảnh chi tiết xung quanh các sự kiện ở Fact table (trả lời cho các câu hỏi: *Ai mua? Mua sản phẩm gì? Vào thời gian nào? Ở đâu?*).
* **Nội dung:** Chứa các thông tin mô tả chi tiết mang tính định tính (tên khách hàng, danh mục sản phẩm, địa chỉ chi nhánh).



> **Lưu ý:** Khác với dạng chuẩn 3 (3NF), mô hình chiều chấp nhận sự dư thừa dữ liệu (*redundancy*) nhất định để đổi lấy sự đơn giản, dễ hiểu cho người dùng cuối và tối ưu tốc độ truy vấn.

#### 4. Mô hình nhà bếp (The Kitchen Analogy) về luồng dữ liệu

Kimball sử dụng hình ảnh một nhà bếp hàng ăn để mô tả luồng di chuyển của dữ liệu:

* **Pantry (Khu lưu trữ / Staging Area):** Nơi chứa dữ liệu thô vừa lấy về. Chưa cho người dùng nghiệp vụ truy cập.
* **Kitchen (Khu chế biến / Processing Area):** Nơi các Data Engineer & Analytics Engineer làm sạch, chuyển đổi và mô hình hóa dữ liệu. Tập trung vào hiệu năng và chuẩn mực xử lý.
* **Dining Hall (Phòng ăn / Presentation Area):** Nơi cung cấp dữ liệu đã hoàn thiện, sẵn sàng để tiêu thụ dưới dạng các **Fact & Dimension tables** cho người dùng phân tích hoặc đưa lên BI Tool (Looker Studio, Power BI, Tableau).
---

Trước đây, việc áp dụng Kimball Framework (Dimensional Modeling) chủ yếu do Data Warehouse Engineer / ETL Developer đảm nhận, kết hợp chặt chẽ với Business Intelligence (BI) Developer / Data Analyst.

Sự phân chia trách nhiệm thời điểm đó diễn ra như sau:

Data Warehouse Engineer / ETL Developer (tiền thân của Data Engineer):

* **Thiết kế sơ đồ hình sao (Star Schema), bảng Fact và bảng Dimension theo lý thuyết của Ralph Kimball.**

* **Viết các đường ống ETL phức tạp để biến đổi dữ liệu thô và nạp vào data warehouse theo đúng thiết kế.**

BI Developer / Data Analyst (Người phối hợp & khai thác):

* **Làm việc với các bên liên quan (business stakeholders) để định nghĩa các chỉ số kinh doanh.**

* **Phối hợp với team ETL để chốt thiết kế bảng Fact/Dimension, sau đó dùng dữ liệu đó để dựng báo cáo và dashboard.**

Trong mô hình này, Data Engineer thường quá bận rộn với hạ tầng/phần cứng nên không sâu sát bài toán kinh doanh, còn Data Analyst lại thiếu kỹ năng lập trình (như kiểm thử, quản lý phiên bản Git, viết SQL tối ưu). Analytics Engineer ra đời nhằm đảm nhận chính phần Dimensional Modeling này, áp dụng tư duy phần mềm vào công việc làm sạch và mô hình hóa dữ liệu.

---

### Vai trò của Analytics Engineer trong Kimball's Framework

* **Người hiện thực hóa thiết kế của Kimball:** Analytics Engineer chịu trách nhiệm chính trong việc áp dụng **Quy trình 4 bước của Kimball** (Xác định Process $\rightarrow$ Grain $\rightarrow$ Dimensions $\rightarrow$ Facts).
* **Quản lý khu vực "The Kitchen" (Processing Area):** Theo hình ảnh so sánh nhà bếp của Kimball:
* **Staging Area (Pantry):** Chứa dữ liệu thô vừa extract về.
* **Processing Area (Kitchen):** Analytics Engineer chính là "đầu bếp" tại đây. Họ biến dữ liệu thô thành các bảng **Fact** và **Dimension** đã làm sạch, chuẩn hóa và tối ưu hiệu năng.
* **Presentation Area (Dining Hall):** Cung cấp các bảng Star Schema sẵn sàng cho Data Analyst hoặc BI Tools khai thác.

---
Khi xử lý dữ liệu (data proccessing), chúng ta hay sử dụng 2 phương pháp chính:

- ETL (Extract → Transform → Load) — you transform the data before it hits the warehouse. Takes longer to set up because the transformation logic has to be built first, but the data in the warehouse is clean and stable from day one.

- ELT (Extract → Load → Transform) — you load the raw data first, then transform it inside the warehouse. Faster and more flexible. 

ELT đang thống trị và dần thay thế ETL do 4 yếu tố chính sau:

**1.Chi phí đám mây rẻ:** 

Trước đây, dung lượng lưu trữ và khả năng xử lý của các hệ thống Data Warehouse truyền thống vô cùng đắt đỏ. Bạn phải lọc(Extract), làm sạch và thu gọn dữ liệu (Transform) trước khi đẩy vào kho dữ liệu (Load) để tiết kiệm từng chút dung lượng.

Còn hiện tại, với sự ra đời của các Modern Cloud Data Warehouse như Google BigQuery, Snowflake, Amazon Redshift hay Databricks đã làm cho chi phí lưu trữ cực kỳ rẻ. Kiến trúc đám mây cho phép tách biệt giữa Storage (lưu trữ) và Compute (tính toán), giúp bạn dễ dàng đẩy toàn bộ dữ liệu thô vào trước mà không lo tốn kém.

**2. Sức mạnh xử lý vượt trội:** Tận dụng trực tiếp khả năng mở rộng dung lượng tính toán (elastic scaling) cực kỳ mạnh mẽ của Cloud Warehouse để thực hiện biến đổi dữ liệu bằng SQL thay vì phải duy trì máy chủ ETL riêng.

**3. Linh hoạt & bảo toàn dữ liệu gốc:** Dữ liệu thô luôn được lưu lại. Khi qui tắc nghiệp vụ (business logic) thay đổi hoặc logic tính toán sai, chỉ cần sửa SQL và chạy lại biến đổi ngay tại kho mà không cần trích xuất (Extract) lại từ hệ thống nguồn (Source systems).

**4. Hệ sinh thái công cụ hiện đại hỗ trợ:** Các công cụ như Fivetran, Airbyte, Stitch giúp tự động hóa việc kéo dữ liệu thô (Extract/Load) từ hàng trăm nguồn về kho diễn ra tự động và gần như không tốn công sức thiết lập, kết hợp cùng các công cụ biến đổi dữ liệu (Transform) hiện tại cho phép áp dụng các tư duy lập trình phần mềm (Version Control, Testing, Documentation) ngay trong kho dữ liệu. Điều này giúp các Data Analyst chỉ cần dùng kiến thức SQL là đã có thể tự tay làm biến đổi dữ liệu thay vì phải nhờ đến Data Engineer viết code Java/Python phức tạp.

---






