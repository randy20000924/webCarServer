import json
import sys
import os
import time


#檔案位置必須在cars且檔名為daily_{日期}_{代號}_{編號}.json的格式
#會自動寫入public/carDatas並自動分類

start = 0
def prograssbar(current, scale, dur, filename): #顯示進度條
    global start
    dur = start + dur
    a = "*" * int(current/scale*30)
    b = "." * (30 - int(current/scale*30))
    c = (current / scale) * 100
    sys.stdout.flush()
    print("\r{:^3.0f}%[{}->{}] ({}/{}) {:.2f}s {}".format(c,a,b,current,scale,dur, filename),end = "")
    



if __name__ == '__main__':
    dirPath = r"./cars"
    problemList = []
    result = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]#檢查json檔
    for curfile,file in enumerate(result):
        start = time.perf_counter()
        problem = False
        
        
        if file.split('.')[1]=='json':      #對json物件轉成dictionary
            try:
                d = ''
                with open(f'./cars/{file}','r', encoding="utf-8") as f:
                   d = json.load(f)
            except KeyboardInterrupt:
                print('\nKeyboardInterrupt stop')
                exit()

            except:
                #print(f"\nfile {file} not a json file")
                problemList.append({file, "not a json file"})
                continue
            data = []
            for index, i in enumerate(d['Items']):#將主要數據寫入item
                try:
                    item = {f"{index}":[
                                            {"timestamp":int(i['timestamp']['N'])},
                                            {"Longitude":float(i['GPS']['M']['Longitude']['N'])},
                                            {"Latitude":float(i['GPS']['M']['Latitude']['N'])},
                                            {"Velocity":float(i['Vehicle']['M']['Velocity']['N'])}
                                        ]}
                except:
                    try:
                        item = {f"{index}":[
                                                {"timestamp":int(i['timestamp']['N'])},
                                                {"Longitude":float(i['GPS']['M']['Longitude']['N'])},
                                                {"Latitude":float(i['GPS']['M']['Latitude']['N'])},
                                                {"Velocity":0 if float(i['Vehicle']['M']['Velocity']['NULL']) else -1}
                                            ]}
                    except:
                        problem = True
                        problemList.append({file, "parse file wrong"})
                        break
                
                data.append(item)
            if problem:
                continue


            carNum = file.split("_")[3].split(".")[0]
            fileNum = file.split("_")[3].split(".")[0]
            date = file.split("_")[1]


            if not os.path.exists('./public/carDatas'):#創建路徑
                os.mkdir("./public/carDatas")
            if not os.path.exists(f"./public/carDatas/{fileNum}"):
                os.mkdir(f"./public/carDatas/{fileNum}")


            with open(f'./public/carDatas/{fileNum}/{carNum}_{date}.json','w', encoding="utf-8") as f:  
                f.write(str({f'{file.split("_")[3].split(".")[0]}':data}).replace("'", '"'))#寫檔


            dur = time.perf_counter() - start
            prograssbar(curfile+1, len(result), dur, result[curfile])


    if len(problemList) > 0:
        print(f'\nThese datas have somthing wrong ): {problemList}')
    print("\n----Done")