from random import randint
import datetime, time
pile = 1
maxpile = 0
npile = 0
face = 1
maxface = 0
nface = 0
exit = False
startTime = time.time()
console = int(input("How Many>"))
print(f"{round(0.5 / console * 100, 2)}% de chance de réussite")
time.sleep(3)

while exit != True:
    if randint(0, 1) == 0:
        print(f"pile {str(pile)} - {maxface} - {maxpile}")
        face = 1
        pile += 1
        if pile == console:
            print(f"Pile > {console}")
            print(f"Temps: {str(datetime.timedelta(seconds=int(round(time.time() - startTime))))}")
            print(f"3/4: {npile}")
            exit = True
        if pile > maxpile:
            maxpile = pile
        if pile > console / 4 * 3:
            npile += 1
    else:
        print(f"face {str(face)} - {maxface} - {maxpile}")
        pile = 1
        face += 1
        if face == console:
            print(f"Face > {console}")
            print(f"Temps: {str(datetime.timedelta(seconds=int(round(time.time() - startTime))))}")
            print(f"3/4: {nface}")
            exit = True
        if face > maxface:
            maxface = face
        if face > console / 4 * 3:
            nface += 1