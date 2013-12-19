import psycopg2 as psy
from Tkinter import *

try:
    # Connection String
    conn_string = "host='omsprod' dbname='inland_20130926' user='postgres' password='gis123!@#'"
    
    # Create independent connections
    conn = psy.connect(conn_string)
    
    # Create independent cursors
    cursor = conn.cursor()
    
except:
    print("Failed to create connection(s) to database.")
    exit()

def counter_label(label):
    def count():
        sql = u"SELECT COUNT(*) as total_nums FROM oms_logfiles.omslogs"
        cursor.execute(sql)
        totalCount = [total for total in cursor]
        strTotalCount = "{:,}".format(totalCount[0][0])
            
        #Update Label Counter in GUI
        label.config(text=strTotalCount, font=("Arial", 24))
        label.after(1000, count)
        
    count()
            

if __name__ == '__main__':
    #Define the GUI
    root = Tk()
    root.title("Total Row Count for Log Entries")
    label = Label(root, fg="blue", width=20, height=1, padx=1, pady=1)
    label.pack()
    button = Button(root, text='Stop', width=25, command=root.destroy)
    button.pack()
    counter_label(label)
    
    root.mainloop()
    
