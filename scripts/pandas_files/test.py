def mmap_io(filename):
    with open(filename, mode="r", encoding="utf8") as f:
        etl_rules = [ line.strip() for line in f ]
        return etl_rules

file_name='scripts/pandas_files/csvfiles/test.map'
etl_rules=mmap_io(file_name)
for i in etl_rules:
    function_args=i.split("=>")
    operation=function_args[0]
    
    args=function_args[1].split("|")
    