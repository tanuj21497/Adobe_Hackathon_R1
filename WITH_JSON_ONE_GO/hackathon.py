import ijson
import csv

# function to get company bound point, "BILL TO " bounds point, "DETAILS " bounds point, "PAYMENT " bounds point
def u_l_m_r():
        
    left =0
    middle=0
    right =0

    upleft1=0
    left1 =0
    middle1=0
    right1 =0
    fname = "./output" + str(0) +"/structuredData.json"
    with open(fname, 'rb') as file:
        parser = ijson.parse(file)
        # ijson will parse the JSON file as a stream and will take very less memory
        i=0
        for prefix, event, value in parser:
            if(prefix == "elements.item.Bounds.item" and prefix_storer=="elements.item.Bounds"):
                if(i==0):
                    upleft1=value
                    i=1
                left=value
                middle=value
                right=value
                
                
                
            if(prefix=="elements.item.Text" and value[0:8] =="BILL TO "):
                left1 = left

            if(prefix=="elements.item.Text" and value[0:8] =="DETAILS "):
                middle1 = middle
            if(prefix=="elements.item.Text" and value[0:8] =="PAYMENT "):
                right1 = right




        
            prefix_storer = prefix
            
    return upleft1, left1, middle1, right1




# this function is to get the company name, address, details which are on top-left side of pdf and are stored in
# string, while string2 contains top-right most details like invoice number, issue date
def extract_s0(storer, string, string2):
    tokens = string.split() 
    index_num=[]
    index_2_comma=[]
    i2=0
    for i in range(len(tokens)):
        if(tokens[i].isdigit()):
            index_num.append(i)
        if(tokens[i][-1]=="," and i2<2):
            index_2_comma.append(i)
            i2+=1

    for i in range(len(tokens)):
        storer[5] = tokens[index_num[1]]
        if(i<index_num[0]):
            storer[3]= storer[3] + tokens[i] +" "
        if(i>=index_num[0] and i<=index_2_comma[0]):
            storer[4] =storer[4] + tokens[i] +" "

        if(i>index_2_comma[0] and i<=index_2_comma[1]):
            storer[0]= storer[0] + tokens[i] +" "
        if(i>index_2_comma[1] and i<index_num[1]):
            storer[1]= storer[1] + tokens[i]+" "
        
        if(i>index_num[0]+index_num[1]):
            storer[2] = storer[2] +  tokens[i]+" "

    storer[3] = storer[3].strip()
    storer[2] = storer[2].strip()
    storer[1] = storer[1].strip()
    storer[4] = (storer[4].strip())[:-1]
    storer[0] = (storer[0].strip())[:-1]

    tokens = string2.split() 

    storer[17] = tokens[1]
    storer[16] = tokens[-1]

# this function is to get the Client Name, email, phone number, street address, city from the string from the below
# portion of "BILL TO " side
def extract_s1(storer, string):
    tokens = string.split() 
    # index = tokens.index("Invoice#")
    ind=0
    for i in range(len(tokens)):
        if(tokens[i].isdigit()):
            ind= i
            break

    storer[10] = tokens[ind-1]

    storer[6] = tokens[ind]+" "+ tokens[ind+1]+ " " +tokens[ind+2]
    for i in range(ind+3, len(tokens)):
        storer[7] += tokens[i] +" "

    storer[7]=storer[7].strip()

    storer[9] = tokens[0] +" "+ tokens[1]
    
    for i in range(2, ind-1):
        storer[8]+=tokens[i]

    storer[8] = storer[8].strip()

# this function is to get the details of client, string is from below portion of middle element "DETAILS "
def extract_s2(storer, string):
    
    storer[14] = string.strip()

# this function is to get the due date from the string from below portion of "PAYMENT " side
def extract_s3(storer, string):
    string = string.strip()
    storer[15] = string[-10:]


# this function is to get the tax amount from portion after "Subtotal "
def extract_s4(storer, string):
    tokens = string.split() 
    for i in range(len(tokens)):
        if(tokens[i].isdigit()):
            storer[18] = tokens[i]
            break

    if(i==len(tokens)-1):
        storer[18] ="10"


# Making of our output file and opening it in write mode
file1 = open('ExtractedData.csv', 'w', newline='')
file1.close()

file1 = open('ExtractedData.csv', 'w', newline='')
writer = csv.writer(file1)

# storing first row of csv file as title names
first_row = ["Bussiness__City", "Bussiness__Country", "Bussiness__Description", "Bussiness__Name", "Bussiness__StreetAddress", "Bussiness__Zipcode", "Customer__Address__line1", "Customer__Address__line2", "Customer__Email", "Customer__Name", "Customer__PhoneNumber", "Invoice__BillDetails__Name", " Invoice__BillDetails__Quantity", "Invoice__BillDetails__Rate", "Invoice__Description", "Invoice__DueDate", "Invoice__IssueDate", "Invoice__Number", "Invoice__Tax"]
writer.writerow(first_row)

# storer is going to contain rows that need to be added one by one
storer = ["" for i in range(len(first_row))]
# item is going to contain the items ordered by client along with quantity etc
item =[]

# These are the bound values of BILL TO, DETAILS and PAYMENT block which will help in identifying the text below them


upleft, left, middle, right = u_l_m_r()

# string storing left side company details
s0=""
# string storing "BILL TO " below 
s1 =""
# string storing "DETAILS " below 
s2=""
# string storing "PAYMENT " below 
s3=""
# string storing "Subtotal " below 
s4=""
# string storing invoice and issue date (comapny right)
s5=""
# company flag
flag0 = True

# client flag
flag1 = False

# "BILL TO " flag
flag2 = False

# "DETAILS " flag
flag3 = False
# "PAYMENT flag"
flag4 = False
# item flag
flag5 = False
# "Subtotal " flag
flag6 = False
# company details flag
upflag = False
prefix_storer=""
t=0
fname = "./output" + str(t) +"/structuredData.json"


# this for loop is gooing to run 100 times for 100 sample pdfs given
for t in range(1, 101):

    with open(fname, 'rb') as file:
        fname = "./output" + str(t) +"/structuredData.json"
        parser = ijson.parse(file)
        # ijson will parse the JSON file as a stream and will take very less memory
        
        for prefix, event, value in parser:
            # this if is going to help in getting text, below elifs are going to help in which string that text need
            # to be added, with the help of flags 
            if(prefix=="elements.item.Text"):

                # when "BILL TO " arrives make company Flag off and client flag on
                if(value=="BILL TO "):
                    flag1 =True
                    flag0= False
                    
                elif(len(value)>=8 and value[:8]=="BILL TO "):
                    s1 = s1+ value[8:]
                    flag1 =True
                    flag0= False
                    
                # if company flag is on then add text according to left and right portion
                elif(flag0==True):
                    # company details flag is on which means add company details(left portion) in s0 string
                    # and make it off again so that if next text is from right portion it will be added in s1
                    # if next text is from left portion company details flag will be made on in below elifs

                    if(upflag==True):

                        s0+=value
                        upflag=False
                    # company details flag is off which means add invoice(right portion) in s1 string
                    else:
                        s5+=value
                    
                # if we arrive at "ITEM " then off the all the CLIENT, BILL TO, PAYMENT, DETAILS flags
                elif(value=="ITEM "):
                    flag1 = False
                    flag2 = False
                    flag3 = False
                    flag4 = False
                    
                # if BILL TO flag is on then add  in BILL TO below text string
                elif(flag2==True):
                    s1 = s1+ value
                    flag2 =False
                
                # if DETAILS flag is on then add  in DETAILS below text string
                elif(flag3==True ):
                    if(value=="DETAILS "):
                        flag3 =False
                        continue
                    if(len(value)>=8 and value[:8]== "DETAILS "):
                        s2 = s2 + value[8:]
                    elif(len(value)>=8 and value[:8]!= "DETAILS "):
                        s2 = s2 + value
                    elif(len(value)<8):
                        s2 = s2 + value
                    flag3 =False
                    continue

                # if PAYMENT flag is on then add in PAYMENT below text string
                elif(flag4==True):
                    if(value=="PAYMENT "):
                        flag4 =False
                        continue
                    if(len(value)>=8 and value[:8]== "PAYMENT "):
                        s3 = s3 + value[8:]
                    elif(len(value)>=8 and value[:8]!= "PAYMENT "):
                        s3 = s3 + value
                    if(value!="PAYMENT "):
                        s3 = s3+ value
                    flag4 =False
                    continue

                # if we encounter "AMOUNT " then it will ON Item Flag which will help in storing item details
                elif(value=="AMOUNT "):
                    flag5 = True
                    
                # if we encounter "Subtotal " then it will mean all items are covered and added, and it will
                # OFF item flag but ON Subtotal Flag
                elif(value[:9]=="Subtotal "):
                    flag5=False
                    flag6=True
                    

                # as item flag is on items are going to be added in item list
                elif(flag5==True):
                    item.append(value.strip())
                    
                # as Subtotal flag is on string will add on until last all the values from which we will get the tax
                elif(flag6 == True):
                    s4+= value
                    
            #  this elif is to have "BILL TO " flag set so that its text get added in s1 string
            elif(prefix=="elements.item.Bounds.item" and abs(int(value)-left)<=1 and flag1==True and prefix_storer=="elements.item.Bounds"):
                flag2 =True
            
            #  this elif is to have "DETAILS " flag set so that its text get added in s2 string

            elif(prefix=="elements.item.Bounds.item" and abs(int(value)-middle)<=1 and flag1==True and prefix_storer=="elements.item.Bounds"):
                flag3 =True

            #  this elif is to have "PAYMENT " flag set so that its text get added in s3 string
            elif(prefix=="elements.item.Bounds.item" and abs(int(value)-right)<=1 and flag1==True and prefix_storer=="elements.item.Bounds"):
                flag4 =True
            # this elif is to have "Company Name" flag set so that its details below it get added in s0 and s5  
            elif(prefix=="elements.item.Bounds.item" and abs(int(value)-upleft)<=1 and flag0==True and prefix_storer=="elements.item.Bounds"):
                upflag =True
            
            # this will help in elif tags to identify the exactly first value of Bounds key
            prefix_storer = prefix

    # these fxns will help in storing value in storer
    extract_s0(storer, s0, s5)  
    extract_s1(storer, s1)  
    extract_s2(storer, s2)  
    extract_s3(storer, s3)  
    extract_s4(storer, s4)  

    # this for loop will add rows in csv by putting items in storer
    for j in range(int(len(item)/4)):
        # only 0 1 2 4 5 6 8 9 10.... type indexes are used because 3 7 11... contain Rates which we dont need
        storer[11] = item[0+j*4] 
        storer[12] = item[1+j*4]
        storer[13] = item[2+j*4]
        writer.writerow(storer)

    s0=""
    s1=""    
    s2=""    
    s3=""   
    s4=""
    s5=""
    item=[]
    flag0 = True
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    flag5 = False
    flag6 = False
    upflag = False

    storer = ["" for i in range(len(first_row))]


file1.close()

    












