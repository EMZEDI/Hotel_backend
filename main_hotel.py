# author: Shahrad Mohammadzadeh
# ID:260955645
 
# importing and constants
from room import Room, MONTHS, DAYS_PER_MONTH
from reservation import Reservation
 
import random, copy, datetime, os, doctest
 
 
class Hotel:
    """
    Instance attributes: name (a string), rooms (a list of Room objects), reservations (a dictionary
    mapping integers, i.e. booking numbers, to Reservation objects).
    """
    def __init__(self, name, room_list = [], reservation_dict = {}):
        """(Hotel, str, list, dict)->Hotel
        """
        # given the inputs we add the values (in two cases using deep copy) to the attributes
        
        self.name = name
        
        # now use deep copy for the last two
        self.rooms = copy.deepcopy(room_list)
        self.reservations = copy.deepcopy(reservation_dict)
        
        
    def make_reservation(self, name, room_type, check_in, check_out):
        """(Hotel, str, str, date, date)->int
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        1953400675629
        >>> print(h.reservations[1953400675629])
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        # check the availability
        # by looping through the list of rooms
        for room in self.rooms:
            
            # if the room is available in the given dates
            # and its the first room
            if room.is_available(check_in, check_out):
                reserve = Reservation(name, room, check_in, check_out)
                
                # update the attribute
                self.reservations[reserve.booking_number] = reserve
                
                # return the booking num
                return reserve.booking_number
            
        # if nothing happens in the for loop then we rasie an assertionerror
        raise AssertionError('no room available')
        
    
    def get_receipt(self, booking_num_list):
        """(Hotel, list)->float
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.get_receipt([num1])
        560.0
        >>> date3 = datetime.date(2021, 6, 5)
        >>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
        >>> h.get_receipt([num1, num2])
        2375.0
        >>> h.get_receipt([123])
        0.0
        """
        total_price = 0.0
        
        # iterate through all booking numbers
        for booking_num in booking_num_list:
            
            # check the availability of the booking numbers
            if booking_num in self.reservations:
                
                # find the room object associated to the booking number
                room = self.reservations[booking_num].room_reserved
                
                # find the differernce between check in and check out date
                diff = self.reservations[booking_num].check_out - self.reservations[booking_num].check_in
                
                # find the price of the room
                price = room.price
                
                # since its a timedelta obj
                total_price += ((diff.days) * price)
                
        return total_price
        
        
        
    def get_reservation_for_booking_number(self, booking_num):
        """(Hotel, int)->Reservation
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        # check if the booking num is in the dict (as a key) or not
        if booking_num in self.reservations:
            return self.reservations[booking_num]
        
        # if not
        return None
        
            
    
    def cancel_reservation(self, booking_num):
        """(Hotel, int)->void
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        
        # check the membership of the booking number in the dictionary
        if booking_num in self.reservations:
            
            
            # make available the room
            # first find the room from the reference/reservation dictionary
            # initially find the reservation
            res = self.get_reservation_for_booking_number(booking_num)
            room = res.room_reserved
            
            # iterate through the days from the check_in till check_out and make everyday available
            initial_date = res.check_in
            last_date = res.check_out
            diff = datetime.timedelta(1)
            
            while initial_date < last_date:
                
                # make available each date
                room.make_available(initial_date)
                initial_date = initial_date + diff
            
    
            # in this case, remove the key value pair
            del self.reservations[booking_num]
    
    
    def get_available_room_types(self):
        """(Hotel)->list
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> types = h.get_available_room_types()
        >>> types.sort()
        >>> types
        ['Queen', 'Twin']
        """
    
        # iterate through the list of the rooms of the hotel and add the types into
        # a new list and finally return that
        final_list = []
        for room in self.rooms:
            
            if room.room_type not in final_list:
                final_list.append(room.room_type)
                
        return final_list
            
    
    
    @staticmethod
    def load_hotel_info_file(file_path):
        """(str)->tuple
        >>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> hotel_name
        'Overlook Hotel'
        >>> print(len(rooms))
        500
        >>> print(rooms[236])
        Room 237,Twin,99.99
        """
        
        # open the file from the given file path and read the hotels name and other info
        file_obj = open(file_path, 'r')
        file_info = file_obj.read()
        file_obj.close()
        
        # add strip method to remove any unwanted space
        file_info = file_info.strip()
        
        # add the substrings to a new list
        full_info_list = file_info.split('\n')
        
        
        # name will be the first element of the list
        name = full_info_list[0].strip()
        
        final_list = []
        # for the rest of the elements the method, strips them with ('Room ')and
        # adds the splitted list of each element (with (',')) to the
        # inputs of room object, and adds the room to the final list
        
        for index in range(1, len(full_info_list)):
            
            element = full_info_list[index]
            
            
            
            # strip with Room
            element = element.strip('Room ')
            
            # add the inputs of room object with split method
            sub_temp_list = element.split(',')
            temp_room = Room(sub_temp_list[1], int(sub_temp_list[0]), float(sub_temp_list[2]))
            
            # add the temp room to the final list
            final_list.append(temp_room)
            
        return (name, final_list)
        
    
    def save_hotel_info_file(self):
        """(Hotel)->void
        >>> r1 = Room("Double", 101, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> h.save_hotel_info_file()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 101,Double,99.99\\n'
        >>> fobj.close()
        """
        # find the name of the hotel
        hotel_name = self.name
        
        # create the hotel folder
        # first copy and lowercase all the substrings of the string of the hotel name
        folder_name = hotel_name.lower()
        
        name_str = ''
        
        # iterate through the hotels name and add
        for substring in folder_name:
            
            if substring == ' ':
                name_str += '_'
                
            else:
                name_str += substring
        
        # add each element of the list to a new string with _s and finalize th foler name str
        folder_final_name = 'hotels/' + name_str + '/hotel_info.txt'
        
        # find the room list of the hotel
        room_lst = self.rooms
        
        # assign a new variable empty string to change later in the iteration
        file_info = hotel_name + '\n'
        
        for room in range(len(room_lst)):
 
                
            file_info += (str(room_lst[room]) + '\n')
                
                
        # after making the file info string, open the new file and write the stuff
        fobj = open(folder_final_name, 'w')
        fobj.write(file_info)
        fobj.close()
        
    
    @staticmethod
    def load_reservation_strings_for_month(folder_name, month, year):
        """(str, str, int)->dict
        >>> name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> h = Hotel(name, rooms, {})
        >>> rsvs = h.load_reservation_strings_for_month('overlook_hotel', 'Oct', 1975)
        >>> print(rsvs[237])
        [(1975, 'Oct', 1, ''), (1975, 'Oct', 2, ''), (1975, 'Oct', 3, ''), (1975, 'Oct', 4, ''), \
        (1975, 'Oct', 5, ''), (1975, 'Oct', 6, ''), (1975, 'Oct', 7, ''), (1975, 'Oct', 8, ''), \
        (1975, 'Oct', 9, ''), (1975, 'Oct', 10, ''), (1975, 'Oct', 11, ''), (1975, 'Oct', 12, ''), \
        (1975, 'Oct', 13, ''), (1975, 'Oct', 14, ''), (1975, 'Oct', 15, ''), (1975, 'Oct', 16, ''), \
        (1975, 'Oct', 17, ''), (1975, 'Oct', 18, ''), (1975, 'Oct', 19, ''), (1975, 'Oct', 20, ''), \
        (1975, 'Oct', 21, ''), (1975, 'Oct', 22, ''), (1975, 'Oct', 23, ''), (1975, 'Oct', 24, ''), \
        (1975, 'Oct', 25, ''), (1975, 'Oct', 26, ''), (1975, 'Oct', 27, ''), (1975, 'Oct', 28, ''), \
        (1975, 'Oct', 29, ''), (1975, 'Oct', 30, '9998701091820--Jack'), \
        (1975, 'Oct', 31, '9998701091820--Jack')]
        """
        # first, create the file name and extension
        name = 'hotels/' + folder_name + '/' + str(year) + '_' + month + '.csv'
        
        # open the csv file to read the stuff
        csv_obj = open(name, 'r')
        
        # read the content
        content = csv_obj.read()
        
        # close the file
        csv_obj.close()
        
        # strip the content
        content = content.strip()
        
        # split each line into new list
        new_list = content.split('\n')
        
        data_list = []
        # iterate thru the list and change each sub
        for sub in new_list:
            data_list.append(sub.split(','))
        
        # dict to be returned later
        final_dict = {}
        
        for sublist in data_list:
            # each time make a new tuple list for a new sub
            tup_list = []
            
            # iterate thru each sub
            for index in range(1, len(sublist)):
                element = sublist[index]
                # update the dict
                if index == 1:
                    final_dict[int(sublist[0])] = [(year, month, index, element)]
                # update the dict
                else:
                    final_dict[int(sublist[0])].append((year, month, index, element))
                       
        return final_dict
 
 
    def save_reservations_for_month(self, month, year):
        """(Hotel, str, int)->void
        >>> random.seed(987)
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> Reservation.booking_numbers = []
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> num = h.make_reservation("Jack", "Double", date1, date2)
        >>> h.save_reservations_for_month('Oct', 2021)
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        
        # check if its leap year
        if (year % 4 == 0 and year % 100 == 0):
            if year % 400 == 0:
                DAYS_PER_MONTH[1] = 29
        elif year % 4 == 0:
            DAYS_PER_MONTH[1] = 29
        
        # make the hotels name
        new_hotel_name = ''
        for substring in self.name.lower():
            if substring == ' ':
                new_hotel_name += '_'
            else:
                new_hotel_name += substring
                
        # first create the csv file
        name = 'hotels/' + new_hotel_name + '/' + str(year) + '_' + month + '.csv'
          
        # open the file to write the content
        csv_obj = open(name, 'w')
 
        final_str = ''
        # iterate thru the lines/rooms and add the info
        for room in self.rooms:
        
            # make a list of days
            list_of_days = ([str(room.room_num)] + ['']*(DAYS_PER_MONTH[MONTHS.index(month)]))
            
            # iterate thru the list of days and  
            for day_num in range(1, len(list_of_days)):
                
                # add the properties to new variables
                date = datetime.date(year, (MONTHS.index(month)) + 1, day_num)
                
                #iterate thru the generated reservation list
                for booking_num in self.reservations:
                    
                    reservation = self.reservations[booking_num]
                    
                    # check if the date we are on, is between the check in/out date of res or not
                    day_between_inout = (reservation.check_in <= date < reservation.check_out)
                    
                    # check if the room type of the res match with the room we are on or not
                    room_match = (room == reservation.room_reserved)
                    
                    if day_between_inout and room_match:
                        short_str = reservation.to_short_string()
                        list_of_days[day_num] += short_str
                        break
            
            # join the elements of the list to the final str plus making a new line
            new_str = ','.join(list_of_days)
            final_str += (new_str + '\n')          
        
        # write and close
        csv_obj.write(final_str)
        csv_obj.close()
        
        # change the leap year to the normal year
        DAYS_PER_MONTH[1] = 28
            
 
 
    def save_hotel(self):
        """(Hotel)->void
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> h.make_reservation("Jack", "Double", date1, date2)
        1953400675629
        >>> h.save_hotel()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 237,Double,99.99\\n'
        >>> fobj.close()
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        # create the name of the folder and check if it exists or not
        name = self.name.lower()
        foldername = ''
        for substring in name:
            if substring == ' ':
                foldername += '_'
            else:
                foldername += substring
                
        folder_root = 'hotels/' + foldername
        
        # check and create the folder if not available
        if not os.path.exists(folder_root):
            
            os.makedirs(folder_root)
            
        # make the text file
        self.save_hotel_info_file()
        
        availability_list = []
        # check if room list of the hotel is empty or not
        if len(self.rooms) != 0 :
            
            for room in self.rooms:
                for key in room.availability:
                    if key not in availability_list:   
                        availability_list.append(key)
                        
            for year, month in availability_list:
                month2 = MONTHS[month - 1]
                self.save_reservations_for_month(month2, year)
                
 
 
    @classmethod
    def load_hotel(cls, name):
        """(Hotel, str)->Hotel
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> hotel = Hotel.load_hotel('overlook_hotel')
        >>> hotel.name
        'Overlook Hotel'
        >>> str(hotel.rooms[236])
        'Room 237,Twin,99.99'
        >>> print(hotel.reservations[9998701091820])
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        """
        # make the hotel complete path name
        path_name = 'hotels/' + name
        
        files_list = os.listdir(path_name)
        
        final_dict = {}
        # iterate thru the names of files and read the data
        for file in files_list:
            
            if file != '.DS_Store':
                
                # first check the text file and extract data
                if file[-4:] == '.txt':
                    hotel_name, room_list = Hotel.load_hotel_info_file(path_name + '/' + file)
 
        
        tuple_dict = {}
        for file2 in files_list:
            
            if (file2 != '.DS_Store') and (file2[-4:] == '.csv'):
                month = file2[-7:-4]
                year = int(file2[:-8])
                my_dict = Hotel.load_reservation_strings_for_month(name, month, year)
                
                for key1 in my_dict:
                    if key1 in tuple_dict:
                        tuple_dict[key1] = tuple_dict[key1] + my_dict[key1]
                    else:
                        tuple_dict[key1] = my_dict[key1]
                        
                # iterate thru the rooms and make them available
                for room in room_list:
                
                    room.set_up_room_availability([month], year)
                    
 
 
        # iterate thru the rooms and make them available
        for room in room_list:
            
            for room_num in tuple_dict:
                if room_num == room.room_num:
                    
                    try:           
                        initial_dict = Reservation.get_reservations_from_row(room, tuple_dict[room_num])
                    except:
                        continue
                    for key in initial_dict:                                
                        final_dict[key] = initial_dict[key]
                
        return cls(hotel_name, room_list, final_dict)                        
                
