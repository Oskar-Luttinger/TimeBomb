from random import randint
import requests
points=0
gameOver=False

#Frågor vi har nu: math, word, symbol, alphabet

def compare(correct, answer):
    global points
    if (correct==answer):
        points+=1
        print("RÄTT")
        
    else:
        points+=0
        print("FEL")
        
        
def math():
    global points
    a=randint(1,9)
    b=randint(1,9)
    operators=["+","-","*"]
    operator=operators[randint(0,2)]
        
        
    answer=input(f"\nVad är {a} {operator} {b}?: ")
    correct= str(eval(f"{a}{operator}{b}"))
    #print(f"Rätt svar: {correct}")
    compare(correct, answer)
        
def symbol():
    global points
    symbols=["×", "&","^"]
    chosenSymbol=symbols[randint(0,2)]
    symbolString=""
    size=randint(10,20)
    for x in range(size):
        symbolString += symbols[randint(0, 2)] + "    "
        if (x + 1) % 5 == 0:
            symbolString += "\n\n"
    correct = str(symbolString.count(chosenSymbol))


    
    print("\n\n" + symbolString)
    
    answer = str(input(f"Hur många  {chosenSymbol}  är det?: "))
    compare(correct, answer)
    


#för att alla word funktioner ska funka krävs att man installerar requests i packages
def getWord(): 
    url = 'https://random-word-api.vercel.app/api?words=1&length=7' #Anropar ett api som skickar tillbaka ett random engelskt ord på 7 bokstäver :) ville testa om det gick 
    response = requests.get(url) 
    retStr=str(response.json())
    return retStr[2:9] #formaterar ordet lite då man fick tillbaka det lite konstigt. 


def word():
    global points
    chosenWord=getWord()
    reverse=randint(0,1) #slumpar om vi vill ha en reverse fråga eller inte
    if reverse==1: 
        answer=input(f"\nSkriv ordet  {chosenWord}  :  ")
        compare(chosenWord, answer)
    else:
        answer=input(f"\nSkriv ordet  {chosenWord}  BAKLÄNGES:  ") 
        compare(chosenWord[::-1], answer)

def alphabet():
    global points
    alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","Å","Ä","Ö"] #Lägger in alfabetet och en kopia som vi modifierar för att inte få samma bokstav flera gånger
    lettersToUse=alphabet.copy()
    lettersList=[] #Lista för 3 bokstäver som ska va i frågan
    for x in range (3):
        letter=lettersToUse[randint(0, len(lettersToUse)-1)] #Välj en random
        lettersList.append(letter) #Lägg in i listan av 3
        lettersToUse.remove(letter) #Ta bort från bokstavslista
    lettersStr="" #Till sträng för snyggare print
    lettersStr = "  ".join(lettersList)
    answer = input(f"\nVilken av bokstäverna {lettersStr}  kommer först i alfabetet?: ")
    correct = min(lettersList, key=lambda l: alphabet.index(l)) #Det med lägst index i alfabetslistan är rätt svar
    answer=answer.upper()
    compare(correct, answer)
    
while gameOver != True:
    alphabet()
    word()
    math()
    symbol()
    print(f"Poäng: {points}")
        