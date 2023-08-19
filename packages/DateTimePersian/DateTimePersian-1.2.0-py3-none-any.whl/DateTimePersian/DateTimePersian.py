from datetime import *
class DateTimePersian:
    __dayOFmonthE = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    __dayOFmonthP = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    __nameOFmonthP = ['فروردين', 'ارديبهشت', 'خرداد', 'تير', 'مرداد', 'شهريور', 'مهر', 'آبان', 'آذر', 'دي', 'بهمن', 'اسفند']
    __nameOFmonthE = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    __nameOFmonthE_P = ['ژان', 'فوریه', 'مارس', 'آوریل', 'مه', 'ژوئن', 'ژوئیه', 'اوت', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر']
    __nameOfDayP = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
    __nameOfDayE_L = ['Sunday', 'Saturday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    __nameOfDayE_S = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    __yearP = 0
    __monthP = 0
    __dayP = 0
    __yearE = 0
    __monthE = 0
    __dayE = 0
    __hour = 0
    __min = 0
    __sec = 0
    __DATE = True
    __TIME = True

    def __init__(self, DATE = True, TIME = True):
        self.__DATE = DATE
        self.__TIME = TIME
        get_now_date = str(date.today())
        get_now_time = str(datetime.now().strftime("%H:%M:%S %t")).split(':')
        self.__hour = get_now_time[0]
        self.__min = get_now_time[1]
        self.__sec = get_now_time[2]
        split_date = get_now_date.split('-')
        self.__yearE = int(split_date[0])
        self.__monthE = int(split_date[1])
        self.__dayE = int(split_date[2])
        self.C_EtoP(self.__yearE, self.__monthE, self.__dayE)

    def getYearP(self)-> int:
        return self.__yearP
    
    def setYearP(self, year):
        self.__yearP = year

    def getYearE(self)-> int:
        return self.__yearE
    
    def setYearE(self, year):
        self.__yearE = year


    def getMonthP(self)-> int:
        return self.__monthP
    
    def setMonthP(self, month):
        self.__monthP = month


    def getMonthE(self)-> int:
        return self.__monthE
    
    def setMonthE(self, month):
        self.__monthE = month



    def getDayP(self)-> int:
        return self.__dayP
    
    def setDayP(self, day):
        self.__dayP = day

    def getDayE(self)-> int:
        return self.__dayE
    
    def setDayE(self, day):
        self.__dayE = day


    def getHour(self):
        return self.__hour
    
    def setHour(self, hour):
        self.__hour = hour

    def getMin(self):
        return self.__min
    
    def setMin(self, Min):
        self.__min = Min

    def getSec(self):
        return self.__sec
    
    def setSec(self, sec):
        self.__sec = sec

    def getNameDayP(self):
        index = self.__dayP % 7
        return self.__nameOfDayP[index]
    
    def getNameDayE(self, type:str = 'L')->str:
        '''
        This method returns the name of the days of the week as a string.\n
        Use the letter L to get the full name. If you want to get the short name, use the letter S.
        '''
        index = self.__dayE % 7
        if type == 'L':
            return self.__nameOfDayE_L[index]
        elif type == 'S':
            return self.__nameOfDayE_S[index]
        
    def getNameMonthP(self) -> str:
        '''
        Returns the name of the current month in Persian
        '''
        return self.__nameOFmonthP[(self.__monthP - 1)]
    
    def getNameMonthE(self, type:str = 'en') -> str:
        '''
        If you set the type to "en", it will return the name of the month to the Gregorian, and if you set it to "fa", it will return the English month name to translated Persian.
        '''
        if type == 'en':
            return self.__nameOFmonthE[(self.__monthE - 1)]
        elif type == 'fa':
            return self.__nameOFmonthE_P[(self.__monthE - 1)]

    @staticmethod
    def lYear(year):
        '''
            get year type  number of int
            return number of int
        '''
        if 1000 <= year <= 9999:
            return year // 4
        else:
            return "Please enter the correct year."
        
    def today(self, Date = "fa", Type = int):
        get_now_date = str(date.today())
        split_date = get_now_date.split('-')
        if Date == "fa" and Type == int:
            return self.C_EtoP(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        elif Date == "fa" and Type == str:
            get = self.C_EtoP(int(split_date[0]), int(split_date[1]), int(split_date[2]))
            get = get.split('/')
            return f"{get[0]} {self.__nameOFmonthP[int(get[1]) - 1]} {get[2]}"
        elif Date == "en" and Type == int:
            return f"{split_date[0]}/{split_date[1]}/{split_date[2]}"
        elif Date == "en" and Type == str:
            return f"{split_date[0]} {self.__nameOFmonthE[int(split_date[1])-1]} {split_date[2]}"
        
    def C_PtoE(self, Year, Month, Day):
        if(Month > 6 and Day > 30):
            return "The selected day is not in the allowed range."
        DayofDateP = ((Year - 1) * 365) + ((Month - 1) * 31) + Day + ((Year - 1)//4)
        if((Month - 1) > 6):
            DayofDateP -= Month - 7
        DayOfDateE = DayofDateP + 226899
        YearofK = ((Year - 1)//4) + 155
        final_Day_of_Date_E = DayOfDateE - YearofK
        YearE = (final_Day_of_Date_E // 365) + 1
        DayOfMode = final_Day_of_Date_E % 365
        counter = 0
        index = 0
        if(DayOfMode > 31):
            while True:
                DayOfMode = DayOfMode - self.__dayOFmonthE[index]
                counter += 1
                index += 1
                if(DayOfMode <= 31):
                    break
        MonthE = counter + 1
        DayE = DayOfMode
        return f"{YearE}/{MonthE}/{DayE}"
    
    def C_EtoP(self, Year, Month, Day):
        if(Month == 2 and Day > 29):
            return "The selected day is not in the allowed range."
        elif (Month in [4, 6, 9, 11] and Day > 30):
            return "The selected day is not in the allowed range."
        m = 0
        for i in range(Month-1):
            m += self.__dayOFmonthE[i]
        DayofDateP = ((Year - 1) * 365) + m + Day + ((Year - 1)//4)
        DayOfDateE = DayofDateP - 226899
        YearofK = ((Year - 1)//4) - 155
        final_Day_of_Date_E = DayOfDateE - YearofK
        YearE = (final_Day_of_Date_E // 365) + 1
        DayOfMode = final_Day_of_Date_E % 365
        counter = 0
        index = 0
        if(DayOfMode > 31):
            while True:
                DayOfMode = DayOfMode - self.__dayOFmonthP[index]
                counter += 1
                index += 1
                if(DayOfMode <= 31):
                    break
        MonthE = counter + 1
        DayE = DayOfMode
        self.__yearP = YearE
        self.__monthP = MonthE
        self.__dayP = DayE
        return f"{self.__yearP}/{self.__monthP}/{self.__dayP}"
    
    def __str__(self):
        s = ""
        if self.__DATE:
            s+= f"{self.__yearP}/{self.__monthP}/{self.__dayP}"
        if self.__TIME:
            s += f"  {self.__hour}:{self.__min}:{self.__sec}"
        return s





    
