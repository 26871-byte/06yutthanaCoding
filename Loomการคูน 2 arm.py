print("โปรแกรมรับแม่สูตรคูน")

star = int(input("เริ่มต้นแม่สูตรคูน"))
stop = int(input("สิ้นสุดแม่สูตรคูน"))

for i in range(star,stop+1):
    print ("\nตารางแม่สูตรคูน")
    for k in range(1,13):
     print (i,"x",k ,"=",i*k)
 
print("ยุทธนา ดรุณพันธ์\n4/4 เลขที่6")