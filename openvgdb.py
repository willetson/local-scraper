import sqlite3 as lite
import sys,re,time

months={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
mon={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12,'TBA':None}
debug=0

def parse_date(taaag):
    #returns month, year or just year
    if not(taaag):
        return {'Month':None,'Year':None}
    if re.match('\D\D\D \d\d?, \d\d\d\d',taaag):
        tag=re.findall('(\D\D\D) \d\d?, (\d\d\d\d)',taaag)[0]
        return {'Month':mon[tag[0]],'Year':tag[1]}
    elif re.match('\D\D\D\d\d?, \d\d\d\d',taaag):
        tag=re.findall('(\D\D\D)\d\d?, (\d\d\d\d)',taaag)[0]
        return {'Month':mon[tag[0]],'Year':tag[1]}
    elif re.match('\d\d\d\d',taaag):
        tag=re.findall('(\d\d\d\d)',taaag)[0]
        return {'Month':None,'Year':int(tag)}
    elif re.match('(\D\D\D), (\d\d\d\d)',taaag):
        tag=re.findall('(\D\D\D), (\d\d\d\d)',taaag)[0]
        return {'Month':mon[tag[0]],'Year':int(tag[1])}
    elif re.match('(\D+), (\d\d\d\d)',taaag):
        tag=re.findall('(\D+), (\d\d\d\d)',taaag)[0]
        return {'Month':months[tag[0]],'Year':int(tag[1])}
    elif re.match('(\D\D\D\D+) (\d\d\d\d)',taaag):
        tag=re.findall('(\D+) (\d\d\d\d)',taaag)[0]
        return {'Month':months[tag[0]],'Year':int(tag[1])}
    elif re.match('(\D\D\D) (\d\d\d\d)',taaag):
        tag=re.findall('(\D\D\D) (\d\d\d\d)',taaag)[0]
        return {'Month':mon[tag[0]],'Year':int(tag[1])}
    else:
        if debug==1:
            print(taaag)
        return {'Month':None,'Year':None}

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class vgdb:
    def __init__(self,db):
        con = lite.connect(db)
        con.row_factory = dict_factory
        self.cur = con.cursor()
        self.releases=self.cur.execute('SELECT * FROM RELEASES;').fetchall()


    def get_columns(self,table):
        columns=[]
        for column in self.cur.execute("PRAGMA table_info("+table+");").fetchall():
            columns.append(column['name'])
        return columns

    def get_tables(self):
        tables=[]
        for table in self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
            tables.append(table['name'])
        return tables

    def get_gameinfo(self,gameid):
#        game={}
        for rel in self.releases:
            if rel['romID']==gameid:
                release=rel.copy()
                release.update(parse_date(rel['releaseDate']))
                break
        return release

    def get_systems(self):
        self.cur.execute('SELECT * FROM SYSTEMS')
        s = self.cur.fetchall()
        self.systems={}
        for system in s:
#            print system
            self.systems[system['systemID']]=system['systemName']
        return self.systems

    def get_console(self,system):
        roms=self.cur.execute('SELECT * FROM ROMS where systemID='+str(system)).fetchall()
        games=[]
        append=games.append
        if debug==1:
            stime=time.time()
        for rom in roms:
            ndict=self.get_gameinfo(rom['romID']).copy()
            ndict.update(rom.items())
            append(ndict)
        if debug==1:
            print('Took %s seconds' % str(time.time()-stime))
#        print games
#            print dict(self.get_gameinfo(rom['romID']).items()+rom.items())
#            games.append(self.get_gameinfo(rom['romID']))
        return games

    def get_console_fg(self,system):
        rom=self.cur.execute('SELECT * FROM ROMS where systemID='+str(system)).fetchone()
#            games.append(self.get_gameinfo(rom['romID']))
        if rom==None:
            return []
        else:
            return dict(self.get_gameinfo(rom['romID']).items()+rom.items())
