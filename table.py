import pandas as pd
import os
import re
# Đường dẫn đến folder chứa các file
result_path = "./RESULT2/CP"  # Thay thế bằng đường dẫn thực tế

# Tạo một list để lưu trữ dữ liệu
data = []

# Duyệt qua từng file trong folder
for filename in sorted(os.listdir(result_path), key=lambda x: int(re.findall(r'\d+', x.split('_')[-1])[0])):
    if filename.startswith("result_test") and filename.endswith(".txt"):
        with open(os.path.join(result_path, filename), 'r') as f:
            for line in f:
                if "Number of tasks scheduled:" in line:
                    num_tasks = int(line.split(":")[1].strip())
                elif "Solver run time:" in line:
                    solver_time = float(line.split(":")[1].strip().split(" ")[0])
            data.append([filename, num_tasks, solver_time])

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data, columns=['File', 'Number of tasks', 'Solver run time'])
df.to_csv("./RESULT2/CP/result.csv", index=False)
# Hiển thị DataFrame
print(df) 