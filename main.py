import mysql.connector
import datetime

def dump_id(id_):
    with open("id_log.txt","w+") as file:
        file.write(str(id_))

def load_id():
    try:
        with open("id_log.txt") as file:
            return(int(file.read())+1)
    except:
        return 1 

def find_desc(user_input):
    for i in user_input:
        if "description" in (i.split()):
            new = i.replace("description ","").strip()
            return new
    return None
    
def find_amount(user_input):
    for i in user_input:
        if "amount" in (i.split()):
            new = i.replace("amount ","").strip()
            return int(new)
    return None

def find_id(user_input):
    try:
        trying = (user_input[0].split())[1].strip()
        if trying.isdigit() :
            return int(trying) 
    except :
        return None
    
def find_month(user_input):
    for i in user_input:
        if "month" in (i.split()):
            new = i.replace("month ","").strip()
            return int(new)
    return None

def add_expense(mydb,cursor,id_,date,desc,amount):
    comm = f"INSERT INTO LOG VALUES({id_},'{date}',{desc.capitalize()},{amount});"
    cursor.execute(comm)
    mydb.commit()
    dump_id(id_)

def delete_expense(mydb,cursor,id_):
    comm = f"DELETE FROM LOG WHERE id={id_};"
    cursor.execute(comm)
    mydb.commit()

def update_expense(mydb,cursor,id_,desc_,amount_):
    if(desc_!=None):
        cursor.execute(f"UPDATE LOG SET description={desc_} where id={id_};")
        mydb.commit()
    if(amount_!=None):
        cursor.execute(f"UPDATE LOG SET amount={amount_} where id={id_};")
        mydb.commit()

def view_expenses(mydb, cursor):
    print(f"{'Id':<5} {'Date':<12} {'Description':<30} {'Amount':<10}")
    print("-" * 60)  # Print a separator line
    cursor.execute("SELECT * FROM LOG;")    
    for i in cursor:
        formatted_date = i[1].strftime("%Y-%m-%d")
        print(f"{i[0]:<5} {formatted_date:<12} {i[2]:<30} {i[3]:<10}")

def summary_expense(mydb,cursor,month):
    if(month==None):
        cursor.execute("SELECT SUM(AMOUNT) FROM LOG;")
        for i in cursor:
            print(f"    Total expenditure : Rs.{int(i[0])}") 
    else:
        cursor.execute(f"SELECT SUM(AMOUNT) FROM LOG WHERE MONTH(date)={month};")
        for i in cursor:
            if(i[0]==None):
                amount = 0
            else:
                amount = int(i[0])
            print(f"    Total expenditure : Rs.{amount}")

def main():
    
    mydb = mysql.connector.connect(host="localhost",user="root",password="1234",database="expense")
    cursor = mydb.cursor()
    
    user_input = input().strip().lower().split("--")
    comm,id_,desc_,amount_,month_ = [user_input[0].strip(),find_id(user_input),find_desc(user_input),find_amount(user_input),find_month(user_input)]
    date = datetime.datetime.now().date()
    month = None
    
    if "add" in comm :
        add_expense(mydb,cursor,load_id(),date,desc_,amount_)
        main()
    elif "update" in comm:
        update_expense(mydb,cursor,id_,desc_,amount_)
        main()
    elif "delete" in comm:
        delete_expense(mydb,cursor,id_)
        main()
    elif "list" in comm:
        view_expenses(mydb,cursor)
        main()
    elif "summary" in comm:
        summary_expense(mydb,cursor,month_)
        main()
    elif "exit" in comm:
        return
    else:
        print(f"Invalid command entered !! Try again .....")
        main()

main()