print("โปรแกรมคำนวณคะแนนรวมระดับเกรด")

point1 = int(input("คะแนนวิชา 1 "))
point2 = int(input("คะแนนวิชา 2 "))
point3 = int(input("คะแนนวิชา 3 "))

totall_point = point1 + point2 + point3
average = totall_point/3
if totall_point < 60:
    print("คะแนนรวมของคุณ = ", totall_point)
    print("คะแนนเฉลี่ยสามวิชา = ", average, "คะแนน")
    print("ควนปรับปรุง")
elif average < 80:
    print("คะแนนเฉลี่ยสามวิชา = ", average, "คะแนน")
    print("ผ่าน")
elif average > 80:
    print("คะแนนเฉลี่ยสามวิชา = ", average, "คะแนน")
    print("ดีเยี่ยม")