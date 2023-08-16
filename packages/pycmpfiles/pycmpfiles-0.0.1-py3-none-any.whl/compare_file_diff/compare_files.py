
def compare_two_files(file1,file2):

    file1 = open("test_2.txt",'r')
    file2 = open("test_3.txt",'r')
    l1=[]
    l2=[]

    for i in file1.readlines():
        l1.append(i.replace("\n",""))

    for j in file2.readlines():
        l2.append(j.replace("\n",""))

    size=0
    size = len(l1) if len(l1)>len(l2) else len(l2)

    def check_index(l,index):
        try:
            l[index]
            return True
        except IndexError:
            return False

    for i,j in zip(range(0,size,1), range(0,size,1)):
        
            try:
                if l1[i] == l2[j]:
                    print(f"Line: {i+1}")
                    print(f"\033[0;32;1m{file1.name}: {l1[i]}")
                    print(f"{file2.name}: {l2[j]}")
                    
                else:
                    print(f"Line: {i+1} ")
                    print(f"\033[0;31;1m{file1.name}: {l1[i]}")
                    print(f"{file2.name}: {l2[j]}")
                    
                print("\033[0;37;10m")
                
            except:
                if check_index(l1, i) == True:
                    print(f"Line: {i+1} ")
                    print(f"\033[0;31;1m{file1.name}: {l1[i]}")
                    print(f"\033[0;31;1m{file2.name}:  ")
                elif check_index(l2, i) == True:
                    print(f"Line: {i+1}")
                    print(f"\033[0;31;1m{file1.name}:  ")
                    print(f"\033[0;31;1m{file2.name}: {l2[j]}")
                print("\033[0;37;10m")