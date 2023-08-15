# OKN_PY_UPDATER
A python library to be used for live updating the okn data before sending into new version of okn detector.
## Installation requirements and guide
### Anaconda
To install this program, `Anaconda python distributing program` and `Anaconda Powershell Prompt` are needed.  
If you do not have `Anaconda`, please use the following links to download and install:  
Download link: https://www.anaconda.com/products/distribution  
Installation guide link: https://docs.anaconda.com/anaconda/install/  
### PIP install
The library name is called `okn_py_updater`.  
To install `okn_py_updater`, you have to use `Anaconda Powershell Prompt`.   
In `Anaconda Powershell Prompt`:
```
pip install okn_py_updater
```
## Usage
```
example_updater = Updater(`config to be used`, `length of circular buffer`, `header array`, `drop rate`)
```
  1.  **config to be used**: must be dictionary type of `gazefilters.json` which contains information such as `Mappers`, `filters` and `Graph`.  
  2.  **length of circular buffer**: must be integer type to define the length of buffer to be used.  
  3.  **header array**: must be array which contains strings which will specify the individual data name of the data array to be updated. Examples: header_array = ['x_value', 'y_value', 'x_nom', 'y_nom', 'record_timestamp', 'sensor_timestamp', 'frame_rate',
                'is_event', 'event_id', 'direction']
  4.  **drop rate**: must be integer type. If it is zero, all data will be used. If it is more than 1, every 1 data will be collected then it will drop the amount of drop rate. For example: If the drop rate is 2, every 1 data will be collected then 2 data will be dropped.
### Example Usage
```
config_to_be_used = load_commented_json("gazefilters.json")
header_array = ['x_value', 'y_value', 'x_nom', 'y_nom', 'record_timestamp', 'sensor_timestamp', 'frame_rate',
                'is_event', 'event_id', 'direction']

example_updater = Updater(config_to_be_used, 100, header_array, 3)

out_put = example_updater.update(data)
```

## Updater Class Specifications
### Attributes
  1.  config: The dictionary version of `gazefilters.json` which contains information such as `Mappers`, `filters` and `Graph`.  
  2.  filter_config: The filter information of the config.  
  3.  circular_buffer: The circular buffer with max length which will be defined by user.  
  4.  self.buffer_max_length: The max length of buffer.  
  5.  self.header_array: The header array which will be defined by user.  
  6.  self.data_drop_rate: The drop rate which will be defined by user.  
  7.  count: The count to be used as a counter if data drop rate is greater than zero.  
### Methods
  1.  update(self, data_input): To store incoming data into circular buffer, update the buffer and return the last element of buffer.  
  2.  set_buffer(self, new_buffer_length): To update buffer.  
  3.  set_header_array(self, new_header_array): To update header array.  
  4.  set_drop_rate(self, new_drop_rate): To update drop rate.  
  5.  get_output_header_array(self): To get output header array.  

