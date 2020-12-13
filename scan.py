import nmap

class Scanner() :
     nm = nmap.PortScanner()
     def get_all_host(self):
         retData = []
         for ip in self.nm.all_hosts():
             host = self.nm[ip]
             mac = "-"
             vendorName = "-"
             if 'mac' in host['addresses']:
                 mac = host['addresses']['mac']
                 if mac in host['vendor']:
                     vendorName = host['vendor'][mac]

             status = host['status']['state']
             rHost = {'ip': ip, 'mac': mac, 'vendor': vendorName, 'status': status}
             retData.append(rHost)

         return retData
     def host_scan(self,host,argument):
         return self.nm.scan(hosts=host,arguments=argument)