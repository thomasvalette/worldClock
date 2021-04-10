void = """     
     
     
     
     
"""

n0 = """▄▀▀▀▄
█   █
█   █
█   █
 ▀▀▀ """

n1 = """ ▄█  
▀ █  
  █  
  █  
▀▀▀▀▀"""

n2 = """▄▀▀▀▄
▀   █
  ▄▀ 
▄▀   
▀▀▀▀▀"""

n3 = """▄▀▀▀▄
▀   █
  ▀▀▄
▄   █
 ▀▀▀ """

n4 = """  ▄█ 
 █ █ 
█  █ 
▀▀▀█▀
   ▀ """

n5 = """█▀▀▀▀
█    
▀▀▀▀▄
    █
▀▀▀▀ """

n6 = """ ▄▀▀ 
█    
█▀▀▀▄
█   █
 ▀▀▀ """

n7 = """▀▀▀▀█
   █ 
  █  
 █   
 ▀   """

n8 = """▄▀▀▀▄
█   █
▄▀▀▀▄
█   █
 ▀▀▀ """

n9 = """▄▀▀▀▄
█   █
 ▀▀▀█
    █
 ▀▀▀ """

s0 = """     
  ▀  
     
  ▀  
     """


s1 = """     
█    
█▄▄  
█  █ 
▀  ▀ 
"""

s2 = """     
     
█▀█▀▄
█ █ █
▀ ▀ ▀
"""

s3 = """     
     
▄▀▀▀▀
 ▀▀▀▄
▀▀▀▀ 
"""

s4 = """  █  
 ▀   
     
     
     
"""

s5 = """ █ █ 
▀ ▀  
     
     
     
"""


def get_matching_str(num_str):
    switcher = {
        " " : void,
        "0" : n0,
        "1" : n1,
        "2" : n2,
        "3" : n3,
        "4" : n4,
        "5" : n5,
        "6" : n6,
        "7" : n7,
        "8" : n8,
        "9" : n9,
        ":" : s0,
        "h" : s1,
        "m" : s2,
        "s" : s3,
        "'" : s4,
        "''": s5
    }
    return switcher.get(num_str,void)


def combine_number_str(time_str):
    """ Return combined ascii representation of the time string passed
    """
    aggregate = []

    for number in time_str:
        number_str = get_matching_str(number)
        number_str_list = number_str.split("\n")
        aggregate.append(number_str_list)

    combined = []
    for i in range (0,5): # each number is a string of 5 lines
        line = ""
        for j in range(0,len(time_str)):
            line += aggregate[j][i] + "  "
        
        combined.append(line)

    return "\n".join(combined)