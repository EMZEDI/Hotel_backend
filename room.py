# author: Shahrad Mohammadzadeh
# ID: 260955645
 
# code for room.py
 
import doctest
import datetime
 
# constants
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
 
 
class Room:
    """
    Instance attributes: room_type (a string), room_num (an int), price (a float), availability,
    (a dictionary mapping tuples of integers representing the year and the month -
    (i.e., (year, month)) to list of booleans).
    
    Class attribute: TYPES_OF_ROOMS_AVAILABLE (a list)
    """
    TYPES_OF_ROOMS_AVAILABLE = ['twin', 'double', 'queen', 'king']
    
    
    def __init__(self, room_type, room_num, price):
        """(Room, str, int, float)->Room
        >>> my_room = Room('Twin', 12345, 100.5)
        >>> my_room.room_type
        'Twin'
        >>> my_room.TYPES_OF_ROOMS_AVAILABLE
        ['twin', 'double', 'queen', 'king']
        >>> my_room2 = Room('double', 12, 150.3)
        >>> my_room2.price
        150.3
        >>> my_room3 = Room('double', 12, 150.3)
        >>> my_room3.price == 100.5
        False
        >>> my_room3.availability
        {}
        >>> my_room3 = Room('double', 12.5, 150.3)
        Traceback (most recent call last):
        AssertionError: not a valid input type
        >>> my_room3 = Room('nothing special', 12, 150.3)
        Traceback (most recent call last):
        AssertionError: room type not available
        >>> my_room3 = Room('queen', 0, 150.3)
        Traceback (most recent call last):
        AssertionError: room number not positive
        >>> my_room3 = Room('queen', 12, -150.3)
        Traceback (most recent call last):
        AssertionError: price is negative
        """
        # input validaitons #1 check the types
        if (type(room_type), type(room_num), type(price)) != (str, int, float):
            raise AssertionError('not a valid input type')
        
        # input validation of the types of the rooms
        if room_type.lower() not in self.TYPES_OF_ROOMS_AVAILABLE:
            raise AssertionError('room type not available')
        
        # input validation of the room number being positive
        if room_num < 1:
            raise AssertionError('room number not positive')
        
        # input validation of the price being negative
        if price < 0:
            raise AssertionError('price is negative')
        
        # assign each instance attribute
        self.room_type = room_type
        self.room_num = room_num
        self.price = price
        self.availability = {}
         
    
    def __str__(self):
        """(Room)->str
        >>> my_room = Room('Twin', 12345, 100.5)
        >>> my_room.__str__()
        'Room 12345,Twin,100.5'
        >>> my_room = Room('Double', 237, 99.99)
        >>> str(my_room)
        'Room 237,Double,99.99'
        >>> my_room = Room('king', 895, 123.9)
        >>> str(my_room)
        'Room 895,king,123.9'
        """
        # return the string made up by the info
        return ('Room ' + str(self.room_num) + ',' + self.room_type + ',' + str(self.price))
    
    
    
    def set_up_room_availability(self, month_list, year):
        """(Room, list, int)->void
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> len(r.availability)
        2
        >>> len(r.availability[(2021, 6)])
        31
        >>> r.availability[(2021, 5)][5]
        True
        >>> print(r.availability[(2021, 5)][0])
        None
        """
        # check if the year is a leaf yr or not/based on the rules
        if ((year % 4 == 0) and (year % 100 == 0)):
            if year % 400 == 0:
                DAYS_PER_MONTH[1] = 29
        elif year % 4 == 0:
            DAYS_PER_MONTH[1] = 29
         
         
        # change the attribute
        # iterate through the month list and pick a month
        bool_list = [None]
        
        for month in month_list:
            
            # count the number of days by getting the index of days per month 
            num_of_days = DAYS_PER_MONTH[MONTHS.index(month)]
            
            # update the bool list each time
            bool_list = bool_list + num_of_days*[True]
            
            # count the month num in the months list
            month_num = MONTHS.index(month) + 1
            
            # add the key value pair to the dict
            self.availability[(year, month_num)] = bool_list
            
            # change back the bool list to [None]
            bool_list = [None]
        
        # change back the year to non-leap
        DAYS_PER_MONTH[1] = 28
        
        
    def reserve_room(self, date):
        """(Room, date)->void
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.reserve_room(date1)
        >>> r.availability[(2021, 6)][20]
        False
        >>> r.availability[(2021, 5)][3] = False
        >>> date2 = datetime.date(2021, 5, 3)
        >>> r.reserve_room(date2)
        Traceback (most recent call last):
        AssertionError: The room is not available at the given date
        """
        # check the input validation
        if self.availability[(date.year, date.month)][date.day] == False:
            raise AssertionError('The room is not available at the given date')
        
        #update the attribute
        self.availability[(date.year, date.month)][date.day] = False
 
 
    def make_available(self, date):
        """(Room, date)->void
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.make_available(date1)
        >>> r.availability[(2021, 6)][20]
        True
        >>> r.availability[(2021, 5)][3] = False
        >>> date2 = datetime.date(2021, 5, 3)
        >>> r.make_available(date2)
        >>> r.availability[(2021, 5)][3]
        True
        """
        
        # update the attribute (easy :)) )
        self.availability[(date.year, date.month)][date.day] = True
        
    
    def is_available(self, check_in, check_out):
        """(Room, date1, date2)->bool
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 5, 25)
        >>> date2 = datetime.date(2021, 6, 10)
        >>> r1.is_available(date1, date2)
        True
        >>> r1.availability[(2021, 5)][28] = False
        >>> r1.is_available(date1, date2)
        False
        """
        # input validaiton of the dates
        diff = check_out - check_in
        
        if diff.days <= 0:
            raise AssertionError('dates do not match')
        
        # check the availability of the rooms
        # first, if the availability is not assigned at first
        if self.availability == {}:
            return False
    
    
        # check the available rooms
        try:
            # sort the availability keys list
            key_list = list(self.availability)
            key_list.sort()
            
            # first, sort the keys of the dict to check yr by yr and mth by mth
            for yr,mth in key_list:
                
                # check if the year and month has passed or not
                yr_not_passed = (check_in.year <= yr <= check_out.year)
                mth_not_passed = (check_in.month <= mth <= check_out.month)
                
                # if months and years not passed
                if yr_not_passed and mth_not_passed:
                    
                    checkout_tuple = (check_out.year, check_out.month)
                    checkin_tuple = (check_in.year, check_in.month)
                    day_count = self.availability[(yr, mth)]
                    last_day = len(day_count)
                    
                    # if we check the vailability in the same month (check in and out)
                    if (yr, mth) == checkin_tuple and (yr, mth) == checkout_tuple:
                        
            
                        # iterate through the days and check the availability
                        for day in range(check_in.day, check_out.day):
                            if self.availability[(yr, mth)][day] != True:
                                return False
                            
                    # when we are in the month of checking in only
                    elif (yr, mth) == checkin_tuple:
                        
            
                        # iterate through the days and check the availability
                        for day in range(check_in.day, last_day):
                            if self.availability[(yr, mth)][day] != True:
                                return False
                            
                            
                    # when we are in the month of checking out only
                    elif (yr, mth) == checkin_tuple:
                        
                        
                        # iterate through the days and check the availability
                        for self.availability[(yr, mth)][day] in range(1, check_out.day):
                            if day != True:
                                return False
                    
            return True
                
            
        except KeyError:
            return False
        
    
    @staticmethod
    def find_available_room(room_list, room_type, check_in, check_out):
        """(list, str, date, date)->Room
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> r2.set_up_room_availability(['May'], 2021)
        >>> r3.set_up_room_availability(['May'], 2021)
        >>> r1.availability[(2021, 5)][8] = False
        >>> r = [r1, r2, r3]
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> my_room == r3
        True
        >>> r3.availability[(2021, 5)][3] = False
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> print(my_room)
        None
        >>> r = Room("King", 110, 120.0)
        >>> r.set_up_room_availability(['Dec'], 2021)
        >>> r.set_up_room_availability(['Jan'], 2022)
        >>> date1 = datetime.date(2021, 12, 20)
        >>> date2 = datetime.date(2022, 1, 8)
        >>> my_room = Room.find_available_room([r], 'Queen', date1, date2)
        >>> print(my_room)
        None
        >>> my_room = Room.find_available_room([r], 'King', date1, date2)
        >>> my_room == r
        True
        """
        
        # input validation of the dates
        diff = check_out - check_in
        
        if diff.days <= 0:
            raise AssertionError('dates do not match')
        
        for room in room_list:
            # check if the room type si valid or not
            # check if the room is available or not
            type_ok = room.room_type == room_type
            available = room.is_available(check_in, check_out)
            
            # return room
            if type_ok and available:
                return room
        
        return None
