from nmap.nmap.nmap import PortScanner

class Scanner() :
     nm = PortScanner()
     def get_all_host(self):
         print("---- get all host ----")
         host_list = self.nm.all_hosts()
         for h in host_list:
             print(h)
             if 'mac' in self.nm[h]['addresses']:
                 print(self.nm[h]['addresses'], self.nm[h]['vendor'])

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
             print("----- rHost -----")
             print(rHost)
             retData.append(rHost)
         return retData


     def host_scan(self,host,argument):
         return self.nm.scan(hosts=host,arguments=argument)

     def get_host_detail(self,ip):
         host_list = self.nm.all_hosts()
         for ip in host_list:
             print (ip)
         return "done"

     def refresh_host_detail(self,ip):
         print("test")