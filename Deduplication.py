import xlrd
import os

# 两个模式，一个是去除M1的重复值，一个是去除撞密cookie的重复值


def drop_duplicate():
    # 读取原始数据
    source = {}
    for file in os.listdir("."):
        if "xlsx" == file.rsplit(".", 1)[1]:
            workbook = xlrd.open_workbook(file)
            table = workbook.sheet_by_index(0)
            lines = table.nrows
            for i in range(lines):
                data = table.row_values(i)
                source[data[0]] = data[1]
            break

    if not source:
        print("没有找到原始数据，程序退出.")
        return False
    print("原始数据:{}行".format(len(source)))
    result = set({})
    for file in os.listdir("."):
        print(file)
        if "txt" == file.rsplit(".", 1)[1]:
            # 先读取一行数据对文件进行判断
            test = open(file, encoding="utf-8").readline()
            if len(test.split("\t")) == 4:
                # 过检存数据
                print("存在过检存数据\n")
                for i in open(file, encoding="utf-8").readlines():
                    try:
                        result.add(i.split("\t")[1])
                    except:
                        pass
            elif len(test.split("\t")) == 3:
                # cookie失败数据
                print("存在撞密cookie失败数据\n")
                for i in open(file, encoding="utf-8").readlines():
                    try:
                        result.add(i.split("\t")[0])
                    except:
                        pass
            elif len(test.split("\t")) > 5:
                # cookie成功数据
                print("存在撞密cookie成功数据\n")
                for i in open(file, encoding="utf-8").readlines():
                    try:
                        result.add(i.split("\t")[2])
                    except:
                        pass

    # 从原始数据中删除重复值
    for i in result:
        if i in source:
            source.pop(i)
        else:
            print(i)

    print("去除重复后剩余 {} 条".format(len(source)))
    with open("./remain.txt", "w+", encoding="utf-8") as f:
        for k, v in source.items():
            f.write("{}\t{}\n".format(k, v))


info = """-------------------------------------------------------------------
原始数据Excel格式为: 账号和密码 两列. 结果文件不需要做更改, 程序自动读取.
去重后的数据会写入到 remain.txt 文件中, 去重会把原始数据中的重复值也去除.
-------------------------------------------------------------------
"""

print(info)
input("按回车开始:\n")
try:
    drop_duplicate()
except Exception as e:
    print("程序出错: ", e)
input("按回车结束:\n")
