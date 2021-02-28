import numpy as np

'''
Class to decode code bars in the standard UPC-A.
These type of code bars contains 95 bits, and 12 digits coded. Each of these
digits are coded using 7 bits. The definition of each bit is done in construction.
The code is done in such a way that it is possible to detect if the code is
being read from left to right, or from right to left.

The code is composed as this:
    - 3 bits for the starting character
    - 42 bits that belongs to the first part of the code
    - 5 bits that defines the middle of the code
    - 42 bits that belongs to the second part of the code
    - 3 bits for the ending character

The way to detect the orientation is using the codes defined on construction.
The first 42 bits of the code are coded as digits with an ODD number of 1s on it.
Also, each digit code starts with 0 and ends with 1.
The second part of the code contains digits coded in such a way that each code
has an even number of 1s on it, and each code starts with 1, and it ends with 0.

The decoder expects the bar code to start with 1s (black values). It counts how
many pixels have this bar. This number will define the width of a bit in the code
bar.

Then, it will check the first number, after the starting code, and see if the
number has an even or an odd number of 1s. This will define the orientation
(if we have to read from left to right or from right to left).

Then, we check the presence of the starting, central and ending codes.
If all this is correct, we retrieve the codes directly, and we run the error check
formula.

If the codes have been retrieved correctly, and the error check is OK, then we
print the decoded value.
'''
class BarCode:
    def __init__(self):
        '''
        Constructor. In this class we initialize the different codes that we can
        find on each side of the bar code (odd side and even side).

        We also define the start, central and end bits sequence.
        '''
        # This dictionary holds the different codes we can find in the odd side.
        self.odd_number_dict = {}
        # The key values are the different codes we can read from the bar code.
        # The value is the equivalent int number
        self.odd_number_dict[13] = 0
        self.odd_number_dict[25] = 1
        self.odd_number_dict[19] = 2
        self.odd_number_dict[61] = 3
        self.odd_number_dict[35] = 4
        self.odd_number_dict[49] = 5
        self.odd_number_dict[47] = 6
        self.odd_number_dict[59] = 7
        self.odd_number_dict[55] = 8
        self.odd_number_dict[11] = 9

        # This dictionary holds the different codes we can find in the even side.
        self.even_number_dict = {}
        # The key values are the different codes we can read from the bar code.
        # The value is the equivalent int number
        self.even_number_dict[114] = 0
        self.even_number_dict[102] = 1
        self.even_number_dict[108] = 2
        self.even_number_dict[66] = 3
        self.even_number_dict[92] = 4
        self.even_number_dict[78] = 5
        self.even_number_dict[80] = 6
        self.even_number_dict[68] = 7
        self.even_number_dict[72] = 8
        self.even_number_dict[116] = 9

        # We define the start, central and end sequence: 101 - 01010 - 101, respectively.
        self.start_seq_digit = 5
        self.central_digit = 10
        self.end_seq_digit = 5

    def detected_code_error_check(self, numbers, module_check_digit):
        '''
        Run the error check formula. We take the numbers in the even positions,
        we sum them, and we multiply this result by 3. Then we sum the even numbers.
        These two results are summed together with the module check digit.

        If this final result is a multiply of 10, the error check has been passed.

        Args:
            numbers: NumPy array with the numbers of the code. The first 6 numbers
                belong to the odd side, and the other 5 belong to the even part.

            module_check_digit: This is the last value detected in the even part of the code.
                This value has been extracted from the detected digits before entering
                into this function. In other words, this value must not be present
                in the numbers list.
        Returns:
            True if the code is correct.
        '''
        odd_idx = np.arange(0, numbers.size, 2, dtype=np.uint8)
        even_idx = np.arange(1, numbers.size, 2, dtype=np.uint8)

        modulus_equation = int((np.sum(3.0 * numbers[odd_idx]) + np.sum(numbers[even_idx])) + module_check_digit)
        return not bool(modulus_equation % 10)

    def check_orientation(self, first_digit_detected):
        '''
        It checks if the detected digit corresponds to a number in the even
        section, or the odd section. This value defines if the code have to be
        read from left to right (if the number has an odd amount of 1s), or from
        right to left (if the number has an even amount of 1s).

        Only the first seven digits are taken into account.

        Args:
            first_digit_detected: Set of 7 bits read after the starting sequence
                code.

        Returns:
            True if the orientation is correct (we can read from
            left to right). False if the code is inversed (we have to read
            from right to left)
        '''
        ones_counter = 0
        for i in range(7):
            mask = 1 << i
            if first_digit_detected & mask:
                ones_counter += 1
        return bool(ones_counter % 2)

    def extract_bit(self, bar):
        '''
        Check the bits in a bar. All the elements in the bar must be equal.
        If it is not the case, a ValueError exception is thrown.

        Args:
            bar:  with the bits that compose a bar bit.

        Returns:
            If all the bar values are the same, this function returns its value.
        '''
        bar_width = len(bar)
        last_bit = bar[0]
        for i in range(1, bar_width):
            if last_bit != bar[i]:
                raise ValueError("Bad formed code bar. For the bar_width {}, we found that a single bar have different values inside".format(bar_width))
        return last_bit

    def extract_bits(self, bits, bar_width):
        '''
        Create an array with the bits of the bar code. This function is required
        since each bar can have a width of N pixels, so we need to
        consider that N pixels belongs to a single bit.

        Args:
            bits: Pixels with the values of the code bar.
            bar_width: This value contains the amount of pixels that a single bar has.

        Returns:
            NumPy array with the bits retrieved from the input pixel values.
        '''
        amount_bits = int(bits.size / bar_width)
        bits_list = []
        print("Amount of detected bits: {}".format(amount_bits))
        assert(amount_bits == 95)
        for i in range(amount_bits):
            start = i * bar_width
            end = (i + 1) * bar_width
            retrieved_bit = self.extract_bit(bits[start:end])
            bits_list.append(retrieved_bit)

        return np.array(bits_list, dtype=np.uint8)

    def extract_code(self, bits):
        '''
        Convert the detected bits from the code bar into integer digits.
        This convertion considers that a single code contains 7 bits.

        The input sequence must not contain the start, central and end codes.

        Args:
            bits: List with detected bits from the bar code. The digits are
                read from left to right, considering that a code is composed
                by 7 bits.

        Returns:
            NumPy array filled with integers. Each integer corresponds to one
            code contained in the bars code.
        '''
        digits = []
        bits_per_digit = 7
        amount_digits = int(bits.size / bits_per_digit)
        for i in range(amount_digits):
            start_index = i * bits_per_digit
            end_index = (i + 1) * bits_per_digit
            number = bits[start_index:end_index]
            detected_digit = number[0]

            for j in range(1, number.size):
                detected_digit = detected_digit << 1
                detected_digit += number[j]
            digits.append(detected_digit)
        return np.array(digits)

    def check_start_center_end_bits(self, bits):
        '''
        Check if the bar codes is correctly detected. The detected code
        must contain the start, central and end code (101 - 01010 - 101, respectively),
        placed at the beginning, at the bit 43 and at the end, respectively.

        Args:
            bits: List with the detected bits. Each position corresponds to
                one bit placed in the bars code.

        Returns:
            True if the start, central, and end sequences are present in the right
            positions. False in any other case.
        '''
        start_sequence_cond = bits[0] == 1 and bits[1] == 0 and bits[2] == 1
        print("Start sequence condition: {}".format(start_sequence_cond))
        central_sequence_cond = bits[43] == 0 and bits[44] == 1 and bits[45] == 0 and bits[46] == 1 and bits[47] == 0
        print("Central sequence condition: {}".format(central_sequence_cond))
        end_sequence_cond = bits[-1] == 1 and bits[-2] == 0 and bits[-3] == 1
        print("End sequence condition: {}".format(end_sequence_cond))
        return start_sequence_cond and central_sequence_cond and end_sequence_cond

    def correct_orientation(self, code_bar_bits, bar_width):
        '''
        We correct the orientation, checking the first code. We consider that the
        start sequence is present in the first three bits of the code, so the
        first number is between the bits 3 and 10. We check the amount of
        ones present in this number:
            - If the amount of 1s is odd, the number is read
        from left to right.
            - If the amount of 1s is even, the number is read from right to left.

        Args:
            code_bar_bits: NumPy array with a line of pixels that belongs to
                the bars code. In this array, each bar is coded with more than
                one pixel. Each bar is formed with as many bits as the bar_width
                parameters says.
            bar_width: Integer that tells how many pixels belongs to a singe bar.

        Returns:
            NumPy array with the pixels oriented to be read from left to right.
            If the input array can be read from left to right, then this input
            is copied in the output. If it is not the case, we flip the input
            array and we provide it as output.
        '''
        bits_list = []
        for i in range(3, 10):
            start = i * bar_width
            end = (i + 1) * bar_width
            retrieved_bit = self.extract_bit(code_bar_bits[start:end])
            bits_list.append(retrieved_bit)

        np_bits = np.array(bits_list)

        # We check the orientation of the bar code (from left to right,
        # or from right to left)
        detected_first_digit = np_bits[0]

        for i in range(1, np_bits.size):
            detected_first_digit = detected_first_digit << 1
            detected_first_digit += np_bits[i]

        print("First detected number: {}".format(detected_first_digit))

        if not self.check_orientation(detected_first_digit):
            print("Reversing the Bar code orientation")
            code_bar_bits = np.flip(code_bar_bits)

        return code_bar_bits

    def convert_odd_numbers(self, codes):
        '''
        Convert numbers from the odd side of the code into decimal digits.

        Args:
            codes: List of integer numbers, with the detected codes from the
                bars code pixels. These codes corresponds to the side that
                contains an odd amount of 1s on their binary representation

        Returns:
            NumPy array with the corresponding decimal digits.
        '''
        output_code = []
        for code in codes:
            decoded_value = self.odd_number_dict.get(code)
            if not decoded_value is None:
                output_code.append(decoded_value)
            else:
                raise ValueError("The decoded odd value {} is not a possible value".format(code))
        return np.array(output_code)

    def convert_even_numbers(self, codes):
        '''
        Convert numbers from the even side of the code into decimal digits.

        Args:
            codes: List of integer numbers, with the detected codes from the
                bars code pixels. These codes corresponds to the side that
                contains an even amount of 1s on their binary representation

        Returns:
            NumPy array with the corresponding decimal digits.
        '''
        output_code = []
        for code in codes:
            decoded_value = self.even_number_dict.get(code)
            if not decoded_value is None:
                output_code.append(decoded_value)
            else:
                raise ValueError("The decoded even value {} is not a possible value".format(code))
        return np.array(output_code)

    def convert_code_into_str(self, code):
        '''
        Convert a list of decimal numbers into a string.

        Args:
            code: List of integer numbers

        Returns:
            Single string, with all the integer numbers joined one after the
            other one.
        '''
        string_ints = [str(x) for x in code]
        return "".join(string_ints)

    def decode(self, code_bar_bits):
        '''
        Decode a bars code into a list of decimal numbers. Only the bars coded
        in the UPC-A.

        Args:
            code_bar_bits: NumPy array that corresponds to a line of pixels that
                contains the code bars. Only two pixel values are allowed: 0 or
                1. The line must start with 1, and be the start code bar.

        Returns:
            String with the detected code. If any step in the detection fails,
            an empty string is returned.
        '''
        print("Received bits from the image: {}".format(code_bar_bits))

        bar_width = 0
        code = ""

        for i in range(code_bar_bits.size):
            if 1 == code_bar_bits[i]:
                bar_width += 1
            else:
                break

        print("Detected bar width: {}".format(bar_width))

        if bar_width:
            corrected_code_bar_bits = self.correct_orientation(code_bar_bits, bar_width)
            # Based on the bar_width parameter, we extract all the bits in the sequence.
            bits = self.extract_bits(corrected_code_bar_bits, bar_width)
            # We check the presence of the start, central and end sequence in the code
            if self.check_start_center_end_bits(bits):
                odd_side_bits = bits[3:45]
                even_side_bits = bits[50:92]

                odd_side_numbers = self.extract_code(odd_side_bits)
                even_side_numbers = self.extract_code(even_side_bits)

                decoded_odd_values = self.convert_odd_numbers(odd_side_numbers)
                decoded_even_values = self.convert_even_numbers(even_side_numbers)

                # We remove the modulus check digit from the sequence
                modulus_digit = decoded_even_values[-1]
                decoded_even_values = decoded_even_values[0:-1]

                numbers = np.concatenate((decoded_odd_values, decoded_even_values))
                print("Decoded digits: {}".format(numbers))

                if self.detected_code_error_check(numbers, modulus_digit):
                    code = self.convert_code_into_str(numbers)
                    print("Check code correct!")
                    print("The detected code is: {}".format(code))
                else:
                    print("ERROR: Check code incorrect!")
            else:
                print("ERROR: The start, central and end sequence are incorrect! Aborting")
        else:
            print("ERROR! We could not detect the bar width!")

        return code