# author: shahrad mohammadzadeh
# ID:260955645
 
import doctest, datetime, random, os, hotel
import matplotlib.pyplot as plt
 
 
class Booking:
    """
    instance attributes: hotels, which is a list of hotels in the booking
    """
    
    def __init__(self, list_of_hotels):
        """(Booking, list)->void
        """
        self.hotels = list_of_hotels
        
        
    
    @classmethod
    def load_system(cls):
        """(Booking)->Booking
        >>> system = Booking.load_system()
        >>> len(system.hotels)
        2
        >>> system.hotels[0].name
        'The Great Northern Hotel'
        >>> print(system.hotels[0].rooms[314])
        Room 315,Queen,129.99
        """
        # load all the files in the hotels folder
        # iterate through all the folders(diff hotels name) found in the folder named 'hotels'
        # and load each file, do this by using load hotel method which returns a hotel
        # add the hotel to a final hotels list to make a booking with it
        hotel_folder_lst = os.listdir('hotels')
        
        # the main one
        
        hotel_folder_list = []
        for hotel_folder in hotel_folder_lst:
            if hotel_folder != '.DS_Store':
                hotel_folder_list.append(hotel_folder)
        
        hotel_obj_list = []
        # now we have the hotel folder list
        for hotel_name_folder in hotel_folder_list:
            
            # load the hotel
            hotel_obj = hotel.Hotel.load_hotel(hotel_name_folder)
            # add the hotel to the list of hotels
            hotel_obj_list.append(hotel_obj)
            
        return cls(hotel_obj_list)
      
      
      
    
    def menu(self):
        
        # ask the user what to do
        print('Welcome to Booking System')
        print('What would you like to do?')
        print('1        Make a reservation')    
        print('2        Cancel a reservation')
        print('3        Look up a reservation')
        user_operation_choice = input('> ')
        
        # check if the entered input is between 1 and 3 or not
        try:
            user_operation_choice = int(user_operation_choice)
            # based on the user preference, use one of the methods below to operate
            # and after all the operations end, save the hotels
            if user_operation_choice == 1:
                self.create_reservation()
                
                
            elif user_operation_choice == 2:
                self.cancel_reservation()
                
            else:
                self.lookup_reservation()
                
                
            for hotel_final in self.hotels:
                hotel_final.save_hotel()
            
        except:
            
            # secret detection mode
            self.delete_reservations_at_random()
            for hotel_final2 in self.hotels:
                hotel_final2.save_hotel()
        
    
    
    def create_reservation(self):
        """(Booking)->void
        
        """
        
        # prompt the user for their name
        user_name = input('Please enter your name: ')
        
        # iterate thru the list of hotels for the booking and display the name
        # ask for the user preference (which hotel to book)
        print('Hi ' + user_name + '!', 'Which hotel would you like to book?')
        for num, hotel3 in enumerate(self.hotels):
            print(num+1, '       ' + hotel3.name)
        
        user_hotel = self.hotels[(int(input('> ')) - 1)]
        user_hotel_name = user_hotel.name
        user_hotel_room_types = user_hotel.get_available_room_types()
        
        # then display the list of room types of the hotel
        print('Which type of room would you like?')
        for num2, room_type in enumerate(user_hotel_room_types):
            print(num2+1, room_type)
            
        user_room_type = user_hotel_room_types[(int(input('> ')) - 1)]
        
        
        # now ask for check in and check out dates
        check_in_date = input('Enter check-in date (YYYY-MM-DD): ')
        check_out_date = input('Enter check-out date (YYYY-MM-DD): ')
        print('Ok. Making your reservation for a', user_room_type, 'room')
        
        # we have to change the check in and check out string to a datetime object
        
        check_in = datetime.datetime.fromisoformat(check_in_date)
        check_in = datetime.date(check_in.year, check_in.month, check_in.day)
        check_out = datetime.datetime.fromisoformat(check_out_date)
        check_out = datetime.date(check_out.year, check_out.month, check_out.day)
        
        for hotel7 in self.hotels:
            
            if hotel7.name == user_hotel_name:
                
                # finally, make a reservation with the info given and print their booking number and total
                # amount of money owing rounded to two decimal places
                booking_num = hotel7.make_reservation(user_name, user_room_type, check_in, check_out)
                # and get the cost
                cost = round(hotel7.get_receipt([booking_num]), 2)
                
                # print the data
                print('Your reservation number is:', booking_num)
                print('Your total amount due is $'+ str(cost))
                print('Thank you')
        
        
        
    
    def cancel_reservation(self):
        """(Booking)->void
        
        """
        # ask the user to enter their booking number to cancel
        booking_num = int(input('Please enter your booking number: '))
        
        # iterate thru the hotels that we have save in the list of hotels of the object
        # booking that we are working with and cancel the reservation for any of the hotels
        
        message_to_user = 'Could not find a reservation with that booking number.'
        for hotel_obj in self.hotels:
            
            if booking_num in hotel_obj.reservations:
                # now, cancel the reservation
                hotel_obj.cancel_reservation(booking_num)
                # because the booking num is found and deleted, we change the message
                message_to_user = 'Cancelled successfully.'
            
            # if error raises because no reservation object
            else:
                continue
                        
            
        print(message_to_user)
    
    
    def lookup_reservation(self):
        """(Booking)->void
        """
        
        user_ask_booking_num = input('Do you have your booking number(s)? ') 
        user_has_booking_num = (user_ask_booking_num == 'yes')
        user_no_booking_num = (user_ask_booking_num == 'no')
        
        # first condition, when the user has a booking number/s
        if user_has_booking_num:
            try: 
                booking_number_list = []
                booking_num = ''
                # iterate until the user enters 
                while booking_num != 'end':
                    
                    # ask the input from the user
                    booking_num = input('Please enter a booking number (or \'end\'): ')
                    if booking_num != 'end':
                        booking_num = int(booking_num)
                    
                    # create a new list of booking nums and add valid booking number to it everytime
                    if (booking_num != 'end') and (booking_num not in booking_number_list):
                        booking_number_list.append(booking_num)
                        
                # now iterate thru each hotel and see if any room in different dates is reserved
                # with the assiciated booking number or not
                
                for hotel_obj in self.hotels:
                    
                    # also iterate thru the booking num list and check the reservation
                    for booking_num in booking_number_list:
                        reservation = hotel_obj.get_reservation_for_booking_number(booking_num)
                        
                        # check if there is a reservation for real or not
                        if reservation != None:
                            # now, print the data
                            print('Reservation found at hotel', hotel_obj.name)
                            print(reservation)
                            cost = hotel_obj.get_receipt([booking_num])
                            print('Total amount due: $', round(cost,2))
                                                   
            except:
                print('The numbers you entered are not valid :(')
 
            
        # second condition, where the user does not have booking number
        elif user_no_booking_num:
            
            # ask for the user info
            user_name = input('Please enter your name: ')
            hotel_name = input('Please enter the hotel you are booked at: ')
            room_num = int(input('Enter the reserved room number: '))
            check_in_date = input('Enter the check-in date (YYYY-MM-DD): ')
            check_out_date = input('Enter the check-out date (YYYY-MM-DD): ')
            # update check in and check out to datetime objs
            check_in = datetime.datetime.fromisoformat(check_in_date)
            check_in = datetime.date(check_in.year, check_in.month, check_in.day)
            check_out = datetime.datetime.fromisoformat(check_out_date)
            check_out = datetime.date(check_out.year, check_out.month, check_out.day)
            
            break_other_loops = False
            # iterate thru the hotels for the booking objects and find the specific hotel
            for hotel4 in self.hotels:
 
                # check the name
                if hotel4.name == hotel_name:
                    # iterate thru the dictionary of booking num: reservation pairs
                    # and check if the reservationobject is the same as before or not
                    for bookingnum in hotel4.reservations: 
                        rsr_name_ok = (hotel4.reservations[bookingnum].name == user_name)
                        rsr_in_ok = (hotel4.reservations[bookingnum].check_in == check_in)
                        rsr_out_ok = (hotel4.reservations[bookingnum].check_out == check_out)
 
                        if rsr_name_ok and rsr_in_ok and rsr_out_ok:
                            for room in hotel4.rooms:
                                if room_num == room.room_num:
                                    print('Reservation found under booking number ' + str(bookingnum))
                                    print('Here are the details:')
                                    print(hotel4.reservations[bookingnum])
                                    cost = hotel4.get_receipt([bookingnum])
                                    print('Total amount due: $' + str(round(cost, 2)))
                                    break_other_loops = True
                                    break
                                    
                            if break_other_loops:
                                break
                        
                    if break_other_loops:
                        break
                        
                    print('no reservation found with the given info')
 
                    
    
    
    def delete_reservations_at_random(self):
        """(Booking)->void
        >>> random.seed(1338)
        >>> booking = Booking.load_system()
        >>> booking.delete_reservations_at_random()
        You said the magic word!
        >>> len(booking.hotels[1].reservations)
        0
        >>> len(booking.hotels[0].reservations)
        1
        """
        print('You said the magic word!')
        # find a random index to delete
        index = random.randint(0, len(self.hotels) - 1)
        
        # delete all of the reservations
        self.hotels[index].reservations = {}
 
    
    
    def plot_occupancies(self, month):
        """(str)->list
        """
        MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # find the days of the month and add it to x axis list
        month_days = DAYS_PER_MONTH[MONTHS.index(month)]
        
        x_axis = []
        for day_num in range(month_days):
            x_axis.append(day_num)
        # now we have the x axis which is the days
        
        hotels_data_list = {}
        # iterate thru the hotels of the class
        for hotel in self.hotels:
            
            # add the hotel name to be later used
            hotel_name = hotel.name
            x_y_tup = ()
            second_list = [0]*len(x_axis)
            
            # iterate thru each day 
            for day in range(len(x_axis)):
                
                # iterate thru the reservation objs made for the hotel
                for book in hotel.reservations:
                    
                    # make the reservation
                    resrv = hotel.reservations[book]
                    # make a datetime obj
                    date = datetime.date(resrv.check_in.year, MONTHS.index(month) + 1, day + 1)
                    date_ok = (resrv.check_in <= date <= resrv.check_out)
                    if date_ok:
                        second_list[day] += 1
                        
            x_y_tup = (x_axis, second_list)
            hotels_data_list[hotel_name] = x_y_tup
            
        final_list = []
        legend_list = []
        # now we have a hotels data list which is a dict
        # containing the tuples where the first element is list of day nums starting with zero
        # and the second element is a list containing number of reservations named for that day
        # now we apply the matplotlib module methods
        # iterate thru the dictionary and set keys as axis.
        for hotel_name in hotels_data_list:
            days_count_axis = hotels_data_list[hotel_name][0]
            num_of_res_axis = hotels_data_list[hotel_name][1]
            plt.plot(days_count_axis,num_of_res_axis, label = hotel_name)
            plt.xlabel("Day of month", fontsize = 14)
            plt.ylabel("Number of reservations", fontsize = 14)
            legend_list.append(hotel_name)
            final_list.append(hotels_data_list[hotel_name])
            
        plt.title('Occupancies for month ' + month)
        plt.legend(legend_list)
        filename = 'hotel_occupancies_' + month + '.png'
        plt.savefig(filename)
        return final_list    
             
