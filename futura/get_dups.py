import psycopg2 as psy

try:
    # Connection String
    conn_string = "host='localhost' dbname='postgis' user='postgres' password='usouth'"
    
    # Create independent connections
    conn = psy.connect(conn_string)
    
    # Create independent cursors
    cursor = conn.cursor()
    
except:
    print("Failed to create connection(s) to database.")
    exit()

#Create a dictionary to store sorted number then count
#picks = {}

class stats():
    def __init__(self):
        self.name = ''
        self.stats = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,
                      11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,
                      21:0,22:0,23:0,24:0,25:0,26:0,27:0,28:0,29:0,30:0,
                      31:0,32:0,33:0,34:0,35:0,36:0,37:0,38:0,39:0,40:0,
                      41:0,42:0,43:0,44:0,45:0,46:0,47:0,48:0,49:0,50:0,
                      51:0,52:0,53:0,54:0,55:0,56:0,57:0,58:0,59:0,60:0,
                      61:0,62:0,63:0,64:0,65:0,66:0,67:0,68:0,69:0,70:0,
                      71:0,72:0,73:0,74:0,75:0}
        self.statsPower = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,
                           11:0,12:0,13:0,14:0,15:0}
        
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def printStats(self):
        print("Column " + self.name)
        for item in self.stats:
            print("{0:>2} was selected {1} times".format(item, self.stats[item]))
    
    def printStatsPower(self):
        print("Column " + self.name)
        for item in self.statsPower:
            print("{0:>2} was selected {1} times".format(item, self.statsPower[item]))
            
    def getMaxStats(self):
        favorite = {'pick':0,'value':0}
        for item in self.stats:
            if self.stats[item] > favorite['value']:
                favorite['pick'] = item
                favorite['value'] = self.stats[item]
        return favorite
    
    def getMaxStatsPower(self):
        favorite = {'pick':0,'value':0}
        for item in self.statsPower:
            if self.statsPower[item] > favorite['value']:
                favorite['pick'] = item
                favorite['value'] = self.statsPower[item]
        return favorite
    
#Create Objects to store column stats
one = stats()
one.setName('one')
two = stats()
two.setName('two')
three = stats()
three.setName('three')
four = stats()
four.setName('four')
five = stats()
five.setName('five')
six = stats()
six.setName('six')


#Select the numbers from the table
sql = u"SELECT * FROM numbers limit 15000000"
cursor.execute(sql)
#rows = cursor.fetchall()
for row in cursor:
    one.stats[row[0]] = one.stats.get(row[0])+1
    two.stats[row[1]] = two.stats.get(row[1])+1
    three.stats[row[2]] = three.stats.get(row[2])+1
    four.stats[row[3]] = four.stats.get(row[3])+1
    five.stats[row[4]] = five.stats.get(row[4])+1
    six.statsPower[row[5]] = six.statsPower.get(row[5])+1
    
one.printStats()
two.printStats()
three.printStats()
four.printStats()
five.printStats()
six.printStatsPower()

bestOne = one.getMaxStats()
print(bestOne['pick'], bestOne['value'])
bestTwo = two.getMaxStats()
print(bestTwo['pick'], bestTwo['value'])
bestThree = three.getMaxStats()
print(bestThree['pick'], bestThree['value'])
bestFour = four.getMaxStats()
print(bestFour['pick'], bestFour['value'])
bestFive = five.getMaxStats()
print(bestFive['pick'], bestFive['value'])
bestSix = six.getMaxStatsPower()
print(bestSix['pick'], bestSix['value'])
