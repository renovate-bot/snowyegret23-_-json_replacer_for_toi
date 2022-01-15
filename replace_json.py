import json
import os
import sys

mainJson = "main.json"
inputJson = "add_input.json"
outputJson = "main_edited.json"
outputTxt = "result.txt"
editlist = []
errorlist = []

print("""
귀곡팔황 json 수정 프로그램을 시작합니다.
Snowyegret / 버전: 0.0.4
""")
# 0.0.2 변경사항: 각 항목을 for문과 keys를 이용하여 변경토록 수정
#                항목/변경사항을 \t를 이용하여 처리하도록 수정
# 0.0.4 변경사항: 각 항목에 대한 예외 추가 및 에러메세지 출력

# TODO: __main__ 추가 및 "id", "name" 등등 키값을 텍스트 파일에서 불러올 수 있게 변경

with open(mainJson) as mj:
    try:
        mainData = json.load(mj)
        print("메인파일 로드 완료!")
    except Exception as e:
        print("main Json파일에 문제가 발생하였습니다.")
        print("파일이 없거나, 파일 내용에 문제가 있거나, 이름이 올바르지 않습니다.")
        print("메인파일 이름 예시: main.json")
        print("에러 메세지: " + e)
        os.system("pause")
        sys.exit()

with open(inputJson) as ij:
    try:
        inputData = json.load(ij)
        print("추가파일 로드 완료!")
    except Exception as e:
        print("input Json 파일에 문제가 발생하였습니다.")
        print("파일이 없거나, 파일 내용에 문제가 있거나, 이름이 올바르지 않습니다.")
        print("추가파일 이름 예시: add_input.json")
        print("에러 메세지: " + e)
        os.system("pause")
        sys.exit()


print("변경 작업 시작...")
try:
    for j in range(len(inputData)):
        for i in range(len(mainData)):
            if inputData[j]["name"] == mainData[i]["name"]:
                editlist.append(mainData[i]["name"])
                usekeys = list(inputData[j].keys())
                mainkeys = list(mainData[i].keys())
                if "id" in usekeys:
                    usekeys.remove("id")
                if "id" in mainkeys:
                    mainkeys.remove("id")
                print(f'[작업] 항목: {inputData[j]["name"]}\t변경사항: {usekeys}')
                for key in usekeys:
                    if key not in mainkeys:
                        print(f'[에러] 추가파일에 있으나 메인에 없는 항목: {key}')
                        temperror = f'{inputData[j]["name"]}\t:{key}'
                        errorlist.append(temperror)
                        continue
                    mainData[i][key] = inputData[j][key]
except Exception as e:
    print("변경 작업 중 에러가 발생했습니다.")
    print("에러 메세지: " + e)
    os.system("pause")
    sys.exit()
print("변경 작업 완료!")

with open(outputJson, 'w') as oj:
    json.dump(mainData, oj, indent=4)
print("수정된 데이터 생성 완료!")

with open(outputTxt, 'w', encoding="utf-8-sig") as ot:
    ot.write("수정된 데이터 목록:\n")
    for info in editlist:
       ot.write(info)
       ot.write("\n")
    ot.write("\n")
    ot.write("에러난 데이터 목록:\n")
    for errorinfo in errorlist:
        ot.write(errorinfo)
        ot.write("\n")

print(f"수정된 데이터 목록: {editlist}")
os.system("pause")
