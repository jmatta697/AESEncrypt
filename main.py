import numpy as np

np.set_printoptions(formatter={'int': hex})


def main():
    plain_text = [0x32, 0x43, 0xf6, 0xa8,
                  0x88, 0x5a, 0x30, 0x8d,
                  0x31, 0x31, 0x98, 0xa2,
                  0xe0, 0x37, 0x07, 0x34]

    key = [0x2b, 0x7e, 0x15, 0x16,
           0x28, 0xae, 0xd2, 0xa6,
           0xab, 0xf7, 0x15, 0x88,
           0x09, 0xcf, 0x4f, 0x3c]

    sbox = [[0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
            [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
            [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
            [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
            [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
            [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
            [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
            [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
            [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
            [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
            [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
            [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
            [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
            [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
            [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
            [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]]

    state_matrix = arrange_plain_text_into_state_matrix(plain_text)
    print("state matrix\n" + str(np.asarray(state_matrix)) + "\n")

    key_matrix = arrange_key_into_matrix(key)
    print("key matrix\n" + str(np.asarray(key_matrix)) + "\n")

    trans_key_to_columns = arrange_key_into_columns(key)
    print("key matrix arranged in columns\n" + str(np.asarray(trans_key_to_columns)) + "\n")

    trans_key_to_rows = key_columns_to_rows(trans_key_to_columns)
    print("key matrix arranged in rows\n" + str(np.asarray(trans_key_to_rows)) + "\n")

    master_key_all_rounds = generate_all_key_columns(trans_key_to_columns, sbox)
    print("master key for all rounds\n" + str(np.asarray(master_key_all_rounds)) + "\n")

    # ------- Encryption steps ------------

    state_matrix = add_key(state_matrix, key_matrix)
    print("added key matrix\n" + str(np.asarray(state_matrix)) + "\n")
    #
    # state_matrix = byte_substitution(state_matrix, sbox)
    # print("byte-sub matrix\n" + str(state_matrix) + "\n")
    #
    # state_matrix = shift_row_transformation(state_matrix)
    # print("row shifted matrix\n" + str(state_matrix) + "\n")
    #
    # state_matrix = mix_columns_transformation(state_matrix)
    # print("mix columns matrix\n" + str(state_matrix) + "\n")

# -----------------------------------------------------------------------------------------------


# arrange list of plain text hex values into 4x4 matrix and output resulting matrix
def arrange_plain_text_into_state_matrix(p_text):
    state_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    char_counter = 0
    for i in range(4):
        for j in range(4):
            state_matrix[j][i] = (p_text[char_counter])
            char_counter += 1
    return state_matrix


def arrange_key_into_matrix(key_list):
    key_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    element_counter = 0
    for i in range(4):
        for j in range(4):
            key_matrix[j][i] = (key_list[element_counter])
            element_counter += 1
    return key_matrix


# before first round
def add_key(st_matrx, key_matrx):
    mult_result = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(len(st_matrx)):
        for j in range(len(key_matrx[0])):
            for k in range(len(key_matrx)):
                mult_result[i][j] += st_matrx[i][k] * st_matrx[k][j]
    return mult_result
    # return np.bitwise_xor(st_matrx, key_matrx)


def byte_substitution(key_added_matrx, s_bx):
    for i in range(len(key_added_matrx)):
        for j in range(len(key_added_matrx[i])):
            high_bit_value = key_added_matrx[i][j] >> 4
            low_bit_value = key_added_matrx[i][j] & 0x0f
            key_added_matrx[i][j] = s_bx[high_bit_value][low_bit_value]
    # for element in np.nditer(key_added_matrx):
    #     high_bit_value = element >> 4
    #     low_bit_value = element & 0x0f
    #     element[...] = s_bx[high_bit_value][low_bit_value]
    return key_added_matrx


def shift_row_transformation(byt_sub_matx):
    row_shifted_matrix = byt_sub_matx
    row_shifted_matrix[0] = byt_sub_matx[0]
    row_shifted_matrix[1] = np.roll(byt_sub_matx[1], -1)
    row_shifted_matrix[2] = np.roll(byt_sub_matx[2], -2)
    row_shifted_matrix[3] = np.roll(byt_sub_matx[3], -3)
    return row_shifted_matrix


def mix_columns_transformation(row_shft_mtrx):
    mix_col_matrx = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    fixed_matrix = [[0x02, 0x03, 0x01, 0x01],
                    [0x01, 0x02, 0x03, 0x01],
                    [0x01, 0x01, 0x02, 0x03],
                    [0x03, 0x01, 0x01, 0x02]]
    for i in range(len(fixed_matrix)):
        for j in range(len(row_shft_mtrx[0])):
            mixed_entry = 0
            for k in range(len(row_shft_mtrx)):
                if fixed_matrix[i][k] == 0x02:
                    raw_product = row_shft_mtrx[k][j] << 1
                elif fixed_matrix[i][k] == 0x03:
                    raw_product = (row_shft_mtrx[k][j] << 1) ^ row_shft_mtrx[k][j]
                else:
                    raw_product = row_shft_mtrx[k][j]
                # check if raw product out of GF(2^8) and mod '1 0001 1011' if so
                if raw_product > 255:
                    product = (raw_product ^ 0b100011011) & 0x0ff
                else:
                    product = raw_product
                mixed_entry ^= product
            if mixed_entry > 255:
                mix_col_matrx[i][j] = (mixed_entry ^ 0b100011011) & 0x0ff
            else:
                mix_col_matrx[i][j] = mixed_entry

    return np.asarray(mix_col_matrx)


def arrange_key_into_columns(key_array):
    column_arranged_key = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    key_array_element_index = 0
    for i in range(4):
        for j in range(4):
            column_arranged_key[i][j] = key_array[key_array_element_index]
            key_array_element_index += 1

    return column_arranged_key


def generate_all_key_columns(orig_key_column_form, s_box):
    master_key_columns = []
    # add first 4 columns to master key
    for col in orig_key_column_form:
        master_key_columns.append(col)

    # generate column numbers 4-40
    for col_num in range(4, 44):
        # do this if column number is NOT multiple of 4
        if col_num % 4 != 0:
            new_col = [0, 0, 0, 0]
            for i in range(4):
                new_col[i] = master_key_columns[col_num - 1][i] ^ master_key_columns[col_num - 4][i]
            master_key_columns.append(new_col)
        else:
            # this will be the resulting new column
            new_col = [0, 0, 0, 0]

            # transform W(col_num - 1) by shifting cyclically up by 1 (-1)
            transformed_col_minus_1 = np.roll(master_key_columns[col_num - 1], -1)
            # replace transformed column minus 1 with s-box values
            s_box_subed = [0, 0, 0, 0]
            s_box_subed_element_counter = 0
            for element in transformed_col_minus_1:
                high_bit_value = element >> 4
                low_bit_value = element & 0x0f
                s_box_subed[s_box_subed_element_counter] = s_box[high_bit_value][low_bit_value]
                s_box_subed_element_counter += 1
            # generate special ith special byte
            special_byte = generate_special_byte(col_num)
            # add special byte to first element in s-box subed array
            top_byte = (s_box_subed[0]) ^ int(special_byte)
            s_box_subed[0] = top_byte
            transformed_col_minus_1 = s_box_subed
            # generate new column - transformed W(i-1) ^ W(i-4)
            for i in range(4):
                new_col[i] = transformed_col_minus_1[i] ^ master_key_columns[col_num - 4][i]
            master_key_columns.append(new_col)

    return master_key_columns


# when current column is a multiple of 4 when building master key, this method generates the special
# bit to add to the top byte of the column
def generate_special_byte(current_col_num):
    raw_special_byte = 0b00000010 ** ((current_col_num - 4) / 4)
    if raw_special_byte > 0xff:
        if current_col_num == 40:
            special_byte = (int(raw_special_byte) ^ 0b1000110110) & 0x0ff
        else:
            special_byte = (int(raw_special_byte) ^ 0b100011011) & 0x0ff
    else:
        special_byte = raw_special_byte
    return special_byte


# transforms column arranged 4X4 matrix into row arranged 4X4 matrix
def key_columns_to_rows(column_arng_key):
    row_arranged_key = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            row_arranged_key[j][i] = column_arng_key[i][j]
    return row_arranged_key


main()


