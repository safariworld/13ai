/*
	Large-Scale Sparse Matrix

	Author:   Steffen Rendle, http://www.libfm.org/
	modified: 2012-06-08

	Copyright 2011-2012 Steffen Rendle, see license.txt for more information
*/

#ifndef FMATRIX_H_
#define FMATRIX_H_

#include <limits>
#include <vector>
#include <assert.h>
#include <iostream>
#include <fstream>
#include "../util/random.h"



const uint FMATRIX_EXPECTED_FILE_ID = 2;

template <typename T> struct sparse_entry {
    uint id;
    T value;
};
	
template <typename T> struct sparse_row {
	sparse_entry<T>* data;
	uint size;
};

struct file_header {
	uint id;
	uint float_size;
	uint64 num_values;
	uint num_rows;
	uint num_cols;
}; 

template <typename T> class LargeSparseMatrix {
	public:
		virtual void begin() = 0; // go to the beginning
		virtual bool end() = 0;   // are we at the end?
		virtual void next() = 0; // go to the next line
		virtual sparse_row<T>& getRow() = 0; // pointer to the current row 
		virtual uint getRowIndex() = 0; // index of current row (starting with 0)
		virtual uint getNumRows() = 0; // get the number of Rows
		virtual uint getNumCols() = 0; // get the number of Cols
		virtual uint64 getNumValues() = 0; // get the number of Values
		

		void saveToBinaryFile(std::string filename) {
			std::cout << "printing to " << filename << std::endl; std::cout.flush();
			std::ofstream out(filename.c_str());
			if (out.is_open()) {
				file_header fh;
				fh.id = FMATRIX_EXPECTED_FILE_ID;
				fh.num_values = getNumValues();
				fh.num_rows = getNumRows();
				fh.num_cols = getNumCols();
				fh.float_size = sizeof(T);
				out.write(reinterpret_cast<char*>(&fh), sizeof(fh));
				for (begin(); !end(); next()) {
					out.write(reinterpret_cast<char*>(&(getRow().size)), sizeof(uint));
					out.write(reinterpret_cast<char*>(getRow().data), sizeof(sparse_entry<T>)*getRow().size);
				}
				out.close();
			} else {
				throw "could not open " + filename;
			}
		}

		void saveToTextFile(std::string filename) {
			std::cout << "printing to " << filename << std::endl; std::cout.flush();
			std::ofstream out(filename.c_str());
			if (out.is_open()) {
				for (begin(); !end(); next()) {
					for (uint i = 0; i < getRow().size; i++) {
						out << getRow().data[i].id << ":" << getRow().data[i].value;
						if ((i+1) < getRow().size) {
							out << " ";
						} else {
							out << "\n";
						}
					}
				}
				out.close();
			} else {
				throw "could not open " + filename;
			}
		}
};

template <typename T> class LargeSparseMatrixHD : public LargeSparseMatrix<T> {
	protected:
		DVector< sparse_row<T> > data;
		DVector< sparse_entry<T> > cache;
		std::string filename;
		
		std::ifstream in;

		uint64 position_in_data_cache;
		uint number_of_valid_rows_in_cache;
		uint64 number_of_valid_entries_in_cache;
		uint row_index;

		uint num_cols;
		uint64 num_values;
		uint num_rows;	

		void readcache() {
			if (row_index >= num_rows) { return; }
			number_of_valid_rows_in_cache = 0;
			number_of_valid_entries_in_cache = 0;
			position_in_data_cache = 0;
			do {
				if ((row_index + number_of_valid_rows_in_cache) > (num_rows-1)) {
					break;
				}
				if (number_of_valid_rows_in_cache >= data.dim) { break; }

				sparse_row<T>& this_row = data.value[number_of_valid_rows_in_cache];
				
				in.read(reinterpret_cast<char*>(&(this_row.size)), sizeof(uint));
				if ((this_row.size + number_of_valid_entries_in_cache) > cache.dim) {
					in.seekg(- (long int) sizeof(uint), std::ios::cur);
					break;
				}

				this_row.data = &(cache.value[number_of_valid_entries_in_cache]);
				in.read(reinterpret_cast<char*>(this_row.data), sizeof(sparse_entry<T>)*this_row.size);
			
				number_of_valid_rows_in_cache++;					
				number_of_valid_entries_in_cache += this_row.size;
			} while (true);
	
		}	
	public:
		LargeSparseMatrixHD(std::string filename, uint64 cache_size) { 
			this->filename = filename;
			in.open(filename.c_str());
			if (in.is_open()) {
				file_header fh;
				in.read(reinterpret_cast<char*>(&fh), sizeof(fh));
				assert(fh.id == FMATRIX_EXPECTED_FILE_ID);
				assert(fh.float_size == sizeof(T));
				this->num_values = fh.num_values;
				this->num_rows = fh.num_rows;
				this->num_cols = fh.num_cols;				
				//in.close();
			} else {
				throw "could not open " + filename;
			}

			if (cache_size == 0) {
				cache_size = std::numeric_limits<uint64>::max();
			}
			// determine cache sizes automatically:
			double avg_entries_per_line = (double) this->num_values / this->num_rows;
			uint num_rows_in_cache;
			{
				uint64 dummy = cache_size / (sizeof(sparse_entry<T>) * avg_entries_per_line + sizeof(uint));
				if (dummy > static_cast<uint64>(std::numeric_limits<uint>::max())) {
					num_rows_in_cache = std::numeric_limits<uint>::max();
				} else {
					num_rows_in_cache = dummy;
				}
			}
			num_rows_in_cache = min(num_rows_in_cache, this->num_rows);
			uint64 num_entries_in_cache = (cache_size - sizeof(uint)*num_rows_in_cache) / sizeof(sparse_entry<T>);
			num_entries_in_cache = min(num_entries_in_cache, this->num_values);
			std::cout << "num entries in cache=" << num_entries_in_cache << "\tnum rows in cache=" << num_rows_in_cache << std::endl;

			cache.setSize(num_entries_in_cache);
			data.setSize(num_rows_in_cache);
		}
//		~LargeSparseMatrixHD() { in.close(); }

		virtual uint getNumRows() { return num_rows; };
		virtual uint getNumCols() { return num_cols; };
		virtual uint64 getNumValues() { return num_values; };

		virtual void next() {
			row_index++;
			position_in_data_cache++;
			if (position_in_data_cache >= number_of_valid_rows_in_cache) {
				readcache();
			}
		}

		virtual void begin() {
			if ((row_index == position_in_data_cache) && (number_of_valid_rows_in_cache > 0)) {
				// if the beginning is already in the cache, do nothing
				row_index = 0;
				position_in_data_cache = 0;
				// close the file because everything is in the cache
				if (in.is_open()) {
					in.close();
				}
				return;
			}
			row_index = 0;
			position_in_data_cache = 0;
			number_of_valid_rows_in_cache = 0;
			number_of_valid_entries_in_cache = 0;
			in.seekg(sizeof(file_header), std::ios_base::beg);
			readcache();
		}

		virtual bool end() { return row_index >= num_rows; }

		virtual sparse_row<T>& getRow() { return data(position_in_data_cache); }
		virtual uint getRowIndex() { return row_index; }
	
	
};

template <typename T> class LargeSparseMatrixMemory : public LargeSparseMatrix<T> {
	protected:
		 uint index;
	public:
		DVector< sparse_row<T> > data;
		uint num_cols;
		uint64 num_values;
		virtual void begin() { index = 0; };
		virtual bool end() { return index >= data.dim; }
		virtual void next() { index++;}
		virtual sparse_row<T>& getRow() { return data(index); };
		virtual uint getRowIndex() { return index; };
		virtual uint getNumRows() { return data.dim; };
		virtual uint getNumCols() { return num_cols; };
		virtual uint64 getNumValues() { return num_values; };

//		void loadFromTextFile(std::string filename);
};
/*
template <typename T> void LargeSparseMatrixMemory<T>::loadFromTextFile(std::string filename) {
	uint64 num_rows = 0;
	uint64 num_values = 0;
	uint64 num_feature = 0;
	bool has_feature = false;
	
	// (1) determine the number of rows and the maximum feature_id
	{
		std::ifstream fData(filename.c_str());
		if (! fData.is_open()) {
			throw "unable to open " + filename;
		}
		token_reader fData2(&fData);
		while (fData2.ch != 0) {
			if (fData2.isNewLine(fData2.ch)) {
				num_rows++;
			} else {
				uint64 _feature = fData2.readInt();
				num_feature = std::max(_feature, num_feature);
				fData2.readFloat();
				num_values++;	
				has_feature = true;
			}
		}	
		fData.close();
	}
	if (has_feature) {	
		num_feature++; // number of feature is bigger (by one) than the largest value
	}
	std::cout << "num_rows=" << num_rows << "\tnum_values=" << num_values << "\tnum_features=" << num_feature << std::endl;
	data.setSize(num_rows);
	
	this->num_cols = num_feature;
	this->num_values = num_values;

	MemoryLog::getInstance().logNew("data_float", sizeof(sparse_entry<T>), num_values);			
	sparse_entry<T>* cache = new sparse_entry<T>[num_values];
	
	// (2) read the data
	{
		std::ifstream fData(filename.c_str());
		if (! fData.is_open()) {
			throw "unable to open " + filename;
		}
		uint64 row_id = 0;
		uint64 cache_id = 0;
		data.value[row_id].data = &(cache[cache_id]);
		data.value[row_id].size = 0;
		token_reader fData2(&fData);
		while (fData2.ch != 0) {
			if (fData2.isNewLine(fData2.ch)) {
				row_id++;
				assert(row_id < num_rows);
				data.value[row_id].data = &(cache[cache_id]);
				data.value[row_id].size = 0;
			} else {
				assert(cache_id < num_values);
				cache[cache_id].id = fData2.readInt();
				cache[cache_id].value = fData2.readFloat();
				cache_id++;
				data.value[row_id].size++;
			}
		}	

		fData.close();
		
		assert(num_rows == row_id);
		assert(num_values == cache_id);		
	}	
}*/





#endif /*FMATRIX_H_*/
