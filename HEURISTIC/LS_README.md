# nhập input 
N, M, t, g, s, c
# kiểm tra ràng buộc: is_valid_assignment
# khởi tạo nghiệm ban đầu: initialize_solution
Sắp xếp các lớp theo số tiết giảm dần (ưu tiên xếp lớp dài trước)

Duyệt tất cả slot thời gian và phòng để xếp lớp vào nếu không vi phạm:
- Sức chứa phòng học
- Ràng buộc giáo viên
- Tránh trùng thời gian
# Tạo các nghiệm lân cận: generate_neighbors
Từ một nghiệm hiện tại, tạo ra các nghiệm lân cận:
- Di chuyển slot: Thay đổi thời gian của lớp trong cùng phòng
- Di chuyển phòng: Chuyển lớp sang phòng khác
- Hoán đổi lớp: Hoán đổi thời gian và phòng của hai lớp nếu không vi phạm ràng buộc
# Tính điểm nghiệm: calculate_score
Tính số lớp xếp được trong nghiệm
# Local Search: local_search_run
Từ nghiệm ban đầu, duyệt qua các nghiệm lân cận để tìm nghiệm tốt hơn

Dừng nếu:
- Không cải thiện sau 'no_improve_limit' lần lặp
- Vượt quá số lần lặp 'max_iterations'
# Chạy song song: local_search
Chạy nhiều Local Search song song bằng multiprocessing

Chọn nghiệm tốt nhất từ các kết quả
# in ra output


# ưu điểm:
- Khả năng mở rộng: Tăng khả năng tìm kiếm nghiệm tốt hơn nhờ Local Search và multiprocessing
- Hiệu quả: Tối đa hóa số lớp được xếp trong thời khóa biểu
- Linh hoạt: Dễ dàng thay đổi ràng buộc hoặc mục tiêu
# nhược điểm:
- Tốn thời gian: Local Search có thể chậm nếu không tối ưu hóa tốt
- Nghiệm cục bộ: Có thể dừng ở nghiệm cục bộ mà không tìm được nghiệm tối ưu toàn cục
