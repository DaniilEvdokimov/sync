import sys,os,shutil


source_dir = str(input("Введите путь до каталога: "))
directory = '/media/daniil'
files = os.listdir(directory)
del files[0]
print('Количество флешек:',len(files))
print('Список подключённых флешек: ')
# вывод названий флешек
for i in files:
    print(i)   
name_flash = str(input('Введите имя нужной флешки: '))
dest_dir = f'/media/daniil/{name_flash}/'


def main():
    try:
        checkIfRootDirsExist(source_dir, dest_dir)
        syncDirs(source_dir, dest_dir)
        syncFiles(source_dir, dest_dir)
    except Exception as e:
        print(e)
        print("Ошибка синхронизации!")



def checkIfRootDirsExist(rootDir1, rootDir2) :
    if (not os.path.exists(rootDir1) and not os.path.isdir(rootDir1)) :
        raise Exception(rootDir1 + " не существует")
    if (not os.path.exists(rootDir2) and not os.path.isdir(rootDir2)) :
        raise Exception(rootDir2 + " не существует")



def syncDirs(rootDir1, rootDir2):
    for root1, dirs1, files1 in os.walk(rootDir1):
        for relativePath1 in dirs1 :
            fullPath1 = os.path.join(root1, relativePath1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            if os.path.exists(fullPath2) and os.path.isdir(fullPath2) :
                continue
            if os.path.exists(fullPath2) and os.path.isfile(fullPath2) :
                raise Exception("Не удаётся выполнить синхронизацию каталога." + str(fullPath2) + " должен быть каталог, а не файл!")
            # Случай 1 : конечный каталог не существует
            shutil.copytree(fullPath1, fullPath2)
            print("Каталог " + str(fullPath2) + " скопирован из " + str(fullPath1))
            continue
    for root2, dirs2, files2 in os.walk(rootDir2):
        for relativePath2 in dirs2:
            fullPath2 = os.path.join(root2, relativePath2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if os.path.exists(fullPath1) and os.path.isdir(fullPath1) :
                continue
            if os.path.exists(fullPath1) and os.path.isfile(fullPath1) :
                raise Exception("Не удаётся выполнить синхронизацию каталога." + str(fullPath1) + " должен быть каталог, а не файл!")
            # Случай 2 : исходный каталог не существует
            shutil.copytree(fullPath2, fullPath1)
            print("Каталог " + str(fullPath1) + " скопирован из " + str(fullPath2))
            continue



def syncFiles(rootDir1, rootDir2):
    for root1, dirs1, files1 in os.walk(rootDir1):
        for file1 in files1:
            fullPath1 = os.path.join(root1, file1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            # Случай 1 : файл не существует в конечном каталоге
            if (not os.path.exists(fullPath2)) :
                shutil.copy2(fullPath1, fullPath2)
                print("Файл " + str(fullPath2) + " скопирован из " + str(fullPath1))
                continue
            # Случай 2 : файл исходного каталога является более поздним, чем файл конечного каталога
            file1LastModificationTime = round(os.path.getmtime(fullPath1))
            file2LastModificationTime = round(os.path.getmtime(fullPath2))
            if (file1LastModificationTime > file2LastModificationTime):
                os.remove(fullPath2)
                shutil.copy2(fullPath1, fullPath2)
                print("Файл " + str(fullPath2) + " синхронизирован с " + str(fullPath1))
                continue
            # Случай 3 : файл конечного каталога является более поздним, чем файл иходного каталога
            if (file1LastModificationTime < file2LastModificationTime):
                os.remove(fullPath1)
                shutil.copy2(fullPath2, fullPath1)
                print("Файл " + str(fullPath1) + " синхронизирован с " + str(fullPath2))
                continue
    # Случай 4 : файл существует только в конечном каталоге, а не в исходном
    # Копируем его обратно в исходный каталог
    for root2, dirs2, files2 in os.walk(rootDir2):
        for file2 in files2:
            fullPath2 = os.path.join(root2, file2);
            fullPath1 = fullPath2.replace(rootDir2, rootDir1);
            if (os.path.exists(fullPath1)):
                continue
            shutil.copy2(fullPath2, fullPath1)
            print("Файл " + str(fullPath1) + " скопирован из" + str(fullPath2))



if __name__ == '__main__':
    while True:
        main()