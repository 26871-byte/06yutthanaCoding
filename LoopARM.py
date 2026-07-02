import random

number = random.randint(1, 100)
count = 0

while True:
    guess = int(input("ทายเลข 1-100: "))
    count += 1

    if guess == number:
        print("ทายถูก!")
        print("คุณใช้ไป", count, "ครั้ง")
        break
    elif guess > number:
        print("มากเกินไป")
    else:
        print("น้อยเกินไป")