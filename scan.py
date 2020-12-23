from nmap.nmap.nmap import PortScanner

class Scanner() :
     nm = PortScanner()
     def get_all_host(self):
         print("---- get all host ----")
         host_list = self.nm.all_hosts()


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
         print("find ip")
         print(ip)
         for h in host_list:
             if str(ip) == str(h):
                 print("ip founded")
                 host = self.nm[ip]
                 return host
         return False


     def refresh_host_detail(self,ip):

         host_list = self.nm.all_hosts()

         for h in host_list:
             if str(ip) == str(h):
                 self.nm.scan(ip,arguments="-sS")
                 return self.nm[ip]

         return False