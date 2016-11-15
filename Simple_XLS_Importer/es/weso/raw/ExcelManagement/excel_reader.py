import os.path
import xlrd

class XslReader(object):
    
    def __init__(self):
        pass

    def load_metadata_sheet(self, file_path):
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_name("metadata")

        data_dictionary = {}
	data_dictionary["org_acronym"] = worksheet.cell_value(0, 1).decode("UTF-8")
	data_dictionary["dataset_internal_id"] = worksheet.cell_value(1, 1).decode("UTF-8")
	data_dictionary["indicator_internal_id"] = self._get_string_from_cell_value(worksheet.cell_value(2, 1))
	data_dictionary["read_as"] = worksheet.cell_value(3, 1).decode("UTF-8")

        return data_dictionary

    def load_xsl_indicator_country_year_value(self, file_path):
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_name("data")
        indicator_col = 0
        country_col = 1
        year_col = 2
        value_col = 3
        note_col = 4

        data_array = []
        for curr_row in range (0, worksheet.nrows):
            indicator = worksheet.cell_value(curr_row, indicator_col).encode("UTF-8")
            country = worksheet.cell_value(curr_row, country_col).encode("UTF-8")
            year = self._get_string_from_cell_value(worksheet.cell_value(curr_row, year_col)) #float
            if worksheet.cell_type(curr_row, value_col) == xlrd.XL_CELL_TEXT:  # text cell
                value = worksheet.cell_value(curr_row, value_col).encode("UTF-8");
            else:
		value = self._get_value_from_cell(worksheet.cell_value(curr_row, value_col))
            # The note is optional
	    note = None
            if (worksheet.ncols >= (note_col+1)) and (worksheet.cell_type(curr_row, note_col) != xlrd.XL_CELL_EMPTY):  # empty cell
                note = worksheet.cell_value(curr_row, note_col).encode("UTF-8");

            obs = {'indicator': indicator, 'country': country, 'year': year, 'value': value}
	    if (note is not None):
		obs.update({'note': note})
            data_array.append(obs)

	# TODO not add None values. Add log
        return data_array


    def load_xsl_country_year_value(self, file_path):
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_name("data")
        
        country_col = 0
        year_col = 1
        value_col = 2
        note_col = 3

        data_array = []
        for curr_row in range (0, worksheet.nrows):
            country = worksheet.cell_value(curr_row, country_col).encode("UTF-8")
            year = self._get_string_from_cell_value(worksheet.cell_value(curr_row, year_col)) #float
            if worksheet.cell_type(curr_row, value_col) == xlrd.XL_CELL_TEXT:  # text cell
                value = worksheet.cell_value(curr_row, value_col).encode("UTF-8");
            else:
		value = self._get_value_from_cell(worksheet.cell_value(curr_row, value_col))
            # The note is optional
	    note = None
            if (worksheet.ncols >= (note_col+1)) and (worksheet.cell_type(curr_row, note_col) != xlrd.XL_CELL_EMPTY):  # empty cell
                note = worksheet.cell_value(curr_row, note_col).encode("UTF-8");

            obs = {'country': country, 'year': year, 'value': value}
	    if (note is not None):
		obs.update({'note': note})
            data_array.append(obs)

	# TODO not add None values. Add log
        return data_array

    def load_xsl_multiple_columns_by_year(self, file_path):
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_name("data")
        
        data_matrix = [[0 for x in xrange(worksheet.ncols)] for x in xrange(worksheet.nrows)]
        
        for curr_row in range (0, worksheet.nrows):
            for curr_col in range (0, worksheet.ncols):
                #print "%s,%s   ---- %s" %(curr_row, curr_col, worksheet.cell_value(curr_row, curr_col))
                if worksheet.cell_type(curr_row, curr_col) == 1:  # text cell
                    data_matrix[curr_row][curr_col] = worksheet.cell_value(curr_row, curr_col).encode("UTF-8");
                else:
		    data_matrix[curr_row][curr_col] = self._get_value_from_cell(worksheet.cell_value(curr_row, curr_col))
                     
        return data_matrix

    @staticmethod
    def _get_value_from_cell(cell_value):
      if cell_value == "":
	 return None
      if cell_value.is_integer(): #integer
         return int(cell_value)
      else: #float
         return float(cell_value)

    @staticmethod
    def _get_string_from_cell_value(cell_value):
	# in case the cell is read as float, because there is only numbers
        if isinstance(cell_value, float):
	   if cell_value.is_integer():
              return str(int(cell_value))
           else:
              return str(cell_value)
        else:
	   return cell_value.decode("UTF-8")
