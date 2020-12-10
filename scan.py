import nmap

class Scanner() :
     nm = nmap.PortScanner()
     def scanFromIp(self,host,argument):
         return self.nm.scan(hosts=host,arguments=argument)