import pandas as pd
import random
import os

# 1. 파일 불러오기
filename = 'route1.xlsx'

try:
    # 엑셀 파일 로드
    df = pd.read_excel(filename)
    
    # '구분' 컬럼 데이터 추출
    routes = df['구분'].dropna().astype(str).tolist()

    # 2. 연결 관계 분석 (Adjacency List)
    adj = {}

    for r in routes:
        parts = r.split('-')
        if len(parts) < 2:
            continue
        
        start_loc = parts[0].strip()
        end_loc = parts[-1].strip()
        
        if start_loc not in adj:
            adj[start_loc] = []
        
        # {전체경로, 도착지} 저장
        adj[start_loc].append({'route': r, 'end': end_loc})

    # 3. 경로 생성 함수
    def generate_path(target_length, adj_data):
        max_retries = 500
        
        for _ in range(max_retries):
            path = []
            current_node = '차고'
            valid_sequence = True
            
            for i in range(target_length):
                if current_node not in adj_data:
                    valid_sequence = False
                    break
                
                options = adj_data[current_node]
                
                # 마지막 줄이면 반드시 '차고'로 돌아와야 함
                if i == target_length - 1:
                    valid_options = [opt for opt in options if opt['end'] == '차고']
                else:
                    valid_options = options
                    
                if not valid_options:
                    valid_sequence = False
                    break
                
                choice = random.choice(valid_options)
                path.append(choice['route'])
                current_node = choice['end']
            
            if valid_sequence:
                return path
        return None

    # 4. 100개 그룹 생성
    final_output = []
    
    for i in range(100):
        # 1. 실제 운행 줄 수를 13 또는 14 중에서 랜덤 선택
        actual_rows = random.choice([13, 14])
        
        # 2. 경로 생성
        path = generate_path(actual_rows, adj)
        
        if path:
            # 경로 추가
            final_output.extend(path)
            
            # 3. 만약 13줄짜리라면, 남은 1칸을 빈 줄로 채워서 '14칸 고정'을 맞춤
            if len(path) < 14:
                padding = 14 - len(path)
                final_output.extend([''] * padding)
                
            # 4. 그룹 간 간격 7줄 추가
            final_output.extend([''] * 7)
        else:
            print(f"{i+1}번째 그룹 생성 실패")

    # 5. 저장
    output_filename = 'vehicle_log_final.xlsx'
    output_df = pd.DataFrame(final_output, columns=['구분'])
    output_df.to_excel(output_filename, index=False)
    
    print(f"생성 완료! '{output_filename}' 파일에 저장되었습니다.")

except FileNotFoundError:
    print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류 발생: {e}")