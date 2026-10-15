import os
from flask import Flask, request, jsonify

app = Flask(name)

def bubble_sort_steps(arr):
"""
버블 정렬(Bubble Sort) 알고리즘을 수행하며,
정렬되는 모든 단계를 기록하여 반환하는 함수.

인자:
    arr (list): 정렬할 숫자들이 담긴 리스트
반환:
    dict: 초기 상태, 각 단계별 배열 상태 및 비교/교환 인덱스 정보, 최종 결과
"""
n = len(arr)
steps = []
# 복사본 생성하여 원본 보호
current_arr = list(arr)

# 초기 상태 기록
steps.append({
    "array": list(current_arr),
    "comparing": [],
    "swapped": False,
    "message": "초기 배열 상태입니다."
})

for i in range(n):
    swapped = False
    for j in range(0, n - i - 1):
        # 비교하는 두 원소 기록
        comparing_indices = [j, j + 1]
        
        if current_arr[j] > current_arr[j + 1]:
            # 값 교환 (Swap)
            current_arr[j], current_arr[j + 1] = current_arr[j + 1], current_arr[j]
            swapped = True
            steps.append({
                "array": list(current_arr),
                "comparing": comparing_indices,
                "swapped": True,
                "message": f"인덱스 {j} ({current_arr[j+1]})와 {j+1} ({current_arr[j]})의 값이 교환되었습니다."
            })
        else:
            steps.append({
                "array": list(current_arr),
                "comparing": comparing_indices,
                "swapped": False,
                "message": f"인덱스 {j} ({current_arr[j]})와 {j+1} ({current_arr[j+1]})는 정렬되어 있어 교환하지 않습니다."
            })
    
    # 만약 이번 루프에서 교환이 전혀 없었다면 이미 정렬 완료된 상태
    if not swapped:
        break
        
return steps


@app.route("/", methods=["GET"])
def health_check():
"""클라우드 런 헬스 체크 엔드포인트"""
return jsonify({"status": "healthy", "message": "Bubble Sort Cloud Run Server is running!"}), 200

@app.route("/sort", methods=["POST"])
def sort_endpoint():
"""
버블 정렬 수행을 요청받는 API 엔드포인트.
JSON 바디 예시: {"array": [64, 34, 25, 12, 22, 11, 90]}
"""
try:
data = request.get_json()
if not data or "array" not in data:
return jsonify({"error": "Invalid input, 'array' field is required."}), 400

    input_array = data["array"]
    if not isinstance(input_array, list) or not all(isinstance(x, (int, float)) for x in input_array):
        return jsonify({"error": "'array' must be a list of numbers."}), 400
        
    # 버블 정렬 단계별 시뮬레이션 실행
    sorting_steps = bubble_sort_steps(input_array)
    
    return jsonify({
        "success": True,
        "original": input_array,
        "steps": sorting_steps,
        "complexity": {
            "time": "O(n^2)",
            "space": "O(1)"
        }
    }), 200
    
except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 500


if name == "main":
# Cloud Run 환경 변수 PORT를 사용하며, 기본값은 8080
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
