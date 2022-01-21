import json
import os
import sys


def folderCheck(infolder, addfolder, outfolder):
    # input폴더 체크
    if os.path.isdir(infolder) != True:
        print('"input" 폴더가 없습니다.')
        os.system("pause")
        sys.exit()
    # input_add폴더 체크
    if os.path.isdir(addfolder) != True:
        print('"input_add" 폴더가 없습니다.')
        os.system("pause")
        sys.exit()
    # output폴더 체크, 없을 시 생성
    if os.path.isdir(outfolder) != True:
        print('"output" 폴더가 없습니다. 폴더를 생성합니다.')
        os.mkdir(outfolder)
        print('"output" 폴더 생성 완료!')


def makeInputList(inDir, inAddDir):
    try:
        inDirList = [name[:-5] for name in os.listdir(inDir)]
        inAddDirList = [name[:-5] for name in os.listdir(inAddDir)]
        # 리턴용 임시 리스트
        returnDirList = []
        returnAddDirList = []
        for a in range(len(inDirList)):
            for b in range(len(inAddDirList)):
                # main파일과 add파일 순서대로 리스트에 추가
                if inDirList[a] + "_add" == inAddDirList[b]:
                    returnDirList.append(inDirList[a])
                    returnAddDirList.append(inAddDirList[b])
        print(f"변경할 파일 목록: {returnDirList}")
        return returnDirList, returnAddDirList
    except Exception as e:
        print(f"에러가 발생했습니다. 혹시 _add를 추가하지 않으셨나요?")
        print(f"에러메세지: {e}")
        os.system("pause")
        sys.exit()


def changeData(Filename, Data, addData):
    print(f"{Filename} 변경 작업 시작...")
    tempEditlist = []
    tempErrorlist = []
    try:
        for j in range(len(addData)):
            for i in range(len(Data)):
                if addData[j]["name"] == Data[i]["name"]:
                    tempEditlist.append(f'{Filename}.json\t:{Data[i]["name"]}')
                    usekeys = list(addData[j].keys())
                    mainkeys = list(Data[i].keys())
                    if "id" in usekeys:
                        usekeys.remove("id")
                    if "id" in mainkeys:
                        mainkeys.remove("id")
                    print(f'[작업] 항목: {addData[j]["name"]}\t변경사항: {usekeys}')
                    for key in usekeys:
                        if key not in mainkeys:
                            print(f"[에러] 추가파일에 있으나 메인에 없는 항목: {key}")
                            temperror = (
                                f'{Filename}.json\t:{addData[j]["name"]}\t:{key}'
                            )
                            tempErrorlist.append(temperror)
                            continue
                        Data[i][key] = addData[j][key]
        return Data, tempEditlist, tempErrorlist
    except Exception as e:
        print("변경 작업 중 에러가 발생했습니다.")
        print("에러 메세지: " + e)
        os.system("pause")
        sys.exit()


def mainStart(input_dir, input_add_dir, out_txt):
    lista, listb = makeInputList(input_dir, input_add_dir)
    editDatas = []
    errorDatas = []
    for n in range(len(lista)):
        with open(f"./input/{lista[n]}.json") as mj:
            try:
                mainData = json.load(mj)
            except Exception as e:
                print(f"{lista[n]}.json 파일을 읽어오는 데 문제가 발생하였습니다.")
                print(f"파일이 없거나, 내용/형식에 문제가 있습니다.")
                print(f"에러 메세지: {e}")
                os.system("pause")
                sys.exit()
        with open(f"./input_add/{listb[n]}.json") as ij:
            try:
                inputData = json.load(ij)
            except Exception as e:
                print(f"{listb[n]}.json 파일을 읽어오는 데 문제가 발생하였습니다.")
                print(f"파일이 없거나, 내용/형식에 문제가 있습니다.")
                print(f"에러 메세지: {e}")
                os.system("pause")
                sys.exit()

        mainData, editData, errorData = changeData(lista[n], mainData, inputData)
        for edata in editData:
            editDatas.append(edata)
        for erdata in errorData:
            errorDatas.append(erdata)

        with open(f"./output/{lista[n]}.json", "w") as oj:
            json.dump(mainData, oj, indent=4)
        print(f"{lista[n]}.json 데이터 수정 완료!")

    with open(out_txt, "w", encoding="utf-8-sig") as er:
        er.write("수정된 데이터 목록:\n")
        for info in editDatas:
            er.write(info)
            er.write("\n")
        er.write("\n")
        er.write("에러난 데이터 목록:\n")
        for errorinfo in errorDatas:
            er.write(errorinfo)
            er.write("\n")


if __name__ == "__main__":
    input_dirr = "./input"
    input_add_dirr = "./input_add"
    output_dirr = "./output"
    output_txtt = "./result.txt"
    print("귀곡팔황용 모드식 json 수정 프로그램")
    print("Snowyegret / 버전: 0.0.5")
    print("프로그램 시작")
    folderCheck(input_dirr, input_add_dirr, output_dirr)
    mainStart(input_dirr, input_add_dirr, output_txtt)
    print("작업을 완료했습니다!")
    os.system("pause")
    sys.exit()
