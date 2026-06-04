# #打开文件
# f = open("resources/123.txt", "r", encoding="utf-8")
#
# #读取文件
# file = f.read()
# print(file)
#
# #关闭文件
# f.close()


#打开文件
# f = open("resources/123.txt", "w", encoding="utf-8")
#
# #写入文件
# try :
#     f.write("静夜思（李白）\n\n")
#     f.write("床前明月光\n")
#     f.write("疑似地上霜\n")
#     f.write("举头望明月\n")
#     f.write("低头思故乡")
#
# #关闭文件
# finally:
#     f.close()



#方式一：防止出现异常，使用try...finally
# 打开文件
f = open("resources/123.txt", "w", encoding="utf-8")

#写入文件
try :
    f.write("静夜思（李白）\n\n")
    f.write("床前明月光\n")
    f.write("疑似地上霜\n")
    f.write("举头望明月\n")
    f.write("低头思故乡")

#关闭文件
finally:
    f.close()

#方式二：防止出现异常，使用with(with会自动进行资源释放)
with open("resources/123.txt", "w", encoding="utf-8") as f:
    f.write("静夜思（李白）\n\n")
    f.write("床前明月光\n")
    f.write("疑似地上霜\n")
    f.write("举头望明月\n")
    f.write("低头思故乡")


