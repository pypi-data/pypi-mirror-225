import os
import time

class Controller:

    def __init__(self):
        self._optionsList = list()
        self._optionListLength = 0
        self.userInput = ''

    def addOption(self, option: str, funcLink) -> None:
        self._optionsList.append( [option, funcLink] )
        self._optionListLength = len(self._optionsList)
    
    def removeOption(self, option: str) -> None:
        for index, item in enumerate(self._optionsList):
            if item[0] == option:
                del self._optionsList[index]
        self._optionListLength -= 1

    def get_optionListLength(self):
       return self._optionListLength
    
    def get_options(self):
        return [item[0] for item in self._optionsList]
    
    def clearOptions(self):
        self._optionsList.clear()
        self._optionListLength = len(self._optionsList)

    def printOptions(self):
        for index, item in enumerate(self._optionsList):
            print(f'{index + 1}. {item[0]}')
    
    def runFunc(self, id: int):
        self._optionsList[id - 1][1]()

    def runLoop(self):
        self._optionListLength = len(self._optionsList)
        while self.userInput != str(self._optionListLength +1):

            print("Enter one of the options: \n")
            self.printOptions()
            print(f"{len(self._optionsList)+1}. Quit")
            self.userInput = input("\n> ")

            if self.userInput == str(self._optionListLength + 1):
                os.system("cls")
                break
            
            elif self.userInput.isnumeric() and 0 < int(self.userInput) <= self._optionListLength:
                os.system("cls")
                self.runFunc(int(self.userInput))

            else:
                os.system("cls")

                print(f"\nOption \"{self.userInput}\" does not exist, please try again.")
                time.sleep(3)

                os.system("cls")