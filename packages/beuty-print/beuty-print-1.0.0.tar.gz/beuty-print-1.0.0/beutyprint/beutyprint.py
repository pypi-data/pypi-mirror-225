
from colorama import Fore, Back, Style

LEFT = 0
RIGHT = 1
CENTER = 2

class BeutySpan():
    def __init__(self, textColor = '', textPadding : int= 0, textPaddingDirection : int = RIGHT, textBackgroundColor= '', textStyle :str = '', l_sep : str= '[ ', r_sep: str = ' ]', defaultColor:str = None):
        self.textColor = textColor
        self.textPadding = textPadding
        self.textPaddingDirection = textPaddingDirection
        self.textBackgroundColor = textBackgroundColor
        self.textStyle = textStyle
        self.l_sep = l_sep
        self.r_sep = r_sep
        self.defaultColor = defaultColor

class BeutyPrint():

    def __init__(self, format: list[BeutySpan] = [BeutySpan()], defaultColor = Style.RESET_ALL):
        self.formatRules = format
        self.defaultColor = defaultColor

    def setDefaultFormat(self, format: list[BeutySpan]):
        self.formatRules = format

    def setDefaultColor(self, color):
        self.defaultColor = color

    def getFormatted(self, format: list[BeutySpan], messagesList : list):
        formattedString = ''
        formatIdx = 0

        for msg in messagesList:
            if formatIdx >= len(format):
                formatIdx = 0

            span = format[formatIdx]

            if span.defaultColor == None:
                span.defaultColor = self.defaultColor
            
            formattedString += f"{span.defaultColor}{span.l_sep}{span.textColor}{span.textBackgroundColor}{span.textStyle}"
            
            if span.textPaddingDirection == RIGHT:
                formattedString += f"{str(msg) :<{span.textPadding}}"
            elif span.textPaddingDirection == LEFT:
                formattedString += f"{str(msg) :>{span.textPadding}}"
            else:
                formattedString += f"{str(msg).center(span.textPadding)}"
            
            formattedString += f"{span.defaultColor}{span.r_sep}"
            formatIdx += 1

        return formattedString

    def printUsingFormat(self, format: list[BeutySpan], messagesList : list, end = '\n'):
        print(self.getFormatted(format, messagesList), end=end)
    

    def print(self, messagesList : list, end='\n'):
        if type(messagesList) == str:
            self.printUsingFormat(self.formatRules, [messagesList], end)
        else:
            self.printUsingFormat(self.formatRules, messagesList, end)

    