# author: Shahrad Mohammadzadeh
# ID:260955645
 
# import modules and constants
from room import Room, MONTHS, DAYS_PER_MONTH
import doctest, datetime, random
 
class Reservation:
    """
    Instance attributes: booking_number (an integer), name (a string),
    room_reserved (a Room), check_in (a date), and check_out (a date)
    Class attribute: booking_numbers initialized with an empty list. This
    list will contain the booking numbers generated when reservations are created.
    """
    # class attribute
    booking_numbers = []
 
    def __init__(self, name, room, check_in, check_out, booking_num = None):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-10
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][9]
        False
        """
        # check the availability of the room
        if not room.is_available(check_in, check_out):
            raise AssertionError('room not available')
 
        # add the attributes
        self.name = name
        self.room_reserved = room
        self.check_in =check_in
        self.check_out = check_out
        
        # if the room booking number is not assigned
        # generate a new 13 digit num, the first cant be 0
        
        if booking_num == None:
            
            booking_str = '0'
            
            
            # iterate with a while loop and check if the number exists in the list 
            while int(booking_str) in self.booking_numbers or int(booking_str) == 0:
                
                booking_str = random.randint(1000000000000, 9999999999999)
                        
            # change the updated str to int and add to attribute
            self.booking_number = int(booking_str)
          
        else:
            
            # check the conditions of the entered value of the booking num
            if (booking_num in self.booking_numbers):
                # raise error if the conditions dont apply
                raise AssertionError('booking number used before!')
            
            elif len(str(booking_num)) != 13:
                # raise error if the conditions dont apply
                raise AssertionError('not a valid booking num!')
            else:
                self.booking_number = booking_num
    
        # update the class attribute list
        Reservation.booking_numbers.append(self.booking_number)
        
        # reserve the room
        initial_date = check_in
        
        while initial_date < check_out:
            # reserve the room for each day
            room.reserve_room(initial_date)
            
            # then add up each date by one until reach the last day
            initial_date = initial_date + datetime.timedelta(1)
    
    
    def __str__(self):
        """(Reservation)->str
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation)
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        # return the string representation
        # first change every attribute to their str shape
        booking_num_str = 'Booking number: ' + str(self.booking_number) + '\n'
        name = 'Name: ' + self.name + '\n'
        room =  'Room reserved: ' + str(self.room_reserved) + '\n'
        check_in =  'Check-in date: ' + str(self.check_in) + '\n'
        check_out = 'Check-out date: ' + str(self.check_out)
        
        return booking_num_str + name + room + check_in + check_out
    
 
    def to_short_string(self):
        """(Reservation)->str
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> my_reservation.to_short_string()
        '1953400675629--Mrs. Santos'
        """
        # return the short string representation
        return str(self.booking_number) + '--' + self.name
    
    @classmethod
    def from_short_string(cls, to_short_str, check_in, check_out, room):
        """(Reservation, str, date, date, room)->Reservation
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 4)
        >>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos', date1, date2, r1)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-04
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][3]
        False
        """
        # split the name and the booking number first of all
        booking_name_list = to_short_str.split('--')
        
        # return the class
        return cls(booking_name_list[1], room, check_in, check_out, int(booking_name_list[0]))
 
 
    @staticmethod
    def get_reservations_from_row(room, tup_list):
        """(Room, list)->dict
        >>> random.seed(987)
        >>> Reservation.booking_numbers = [] # needs to be reset for the test below to pass
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(MONTHS, 2021)
        >>> rsv_strs = [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 4, '1953400675629--Jack')]
        >>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
        >>> print(rsv_dict[1953400675629])
        Booking number: 1953400675629
        Name: Jack
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-05
        """
        name_number_to_date = {}
        
        # iterate thru the list of tuples and check the booking numbers 
        for tup in tup_list:
            # if there is a reservation for the date
            if tup[3] != '':
                # take out the booking number
                ref_num_name = tup[3]
                
                # month number and create the date
                mth_num = MONTHS.index(tup[1]) + 1
                date = datetime.date(tup[0], mth_num, tup[2])
                
                if ref_num_name in name_number_to_date:
                    name_number_to_date[ref_num_name] = name_number_to_date[ref_num_name] + [date]
                    
                else:
                    name_number_to_date[ref_num_name] = [date]
                    
                    
        final_dict = {}
        # iterate thru the dict and sort the values lists
        for key in name_number_to_date:
            delt_day = datetime.timedelta(1)
            val = name_number_to_date[key]
            val.sort()
            resr = Reservation(key[15:], room, min(val), max(val) + delt_day, int(key[0:13]))
            final_dict[int(key[0:13])] = resr
            
        return final_dict
 
