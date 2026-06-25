print("โปรแกรมตรวจจับความเร็วรถ")
score1 = int(input("คะแนนความเร็วรถ1 "))

totall = score1 
average = totall /3

if average < 80:
    
    print ("ปลอดภัย")
elif average > 81 < 100:
    print ("เตือน")
elif average > 101 < 120:
    print ("เสี่ยงถูกปรับ")
else :
    print ("ผิดกฏหมายปรับทันที")
