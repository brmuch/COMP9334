import numpy as np
import matplotlib.pyplot as plt
from threading import Thread, Lock
file_No = 0                                                     # output file Number 
                                                                # mrt_*.txt, fog_dep_*.txt, net_dep_*.txt and cloud_dep_*. 
seed = 0

suffix = ".txt"
mrt_f = "mrt_"
fog_dep_f = "fog_dep_"
net_dep_f = "net_dep_"
cloud_dep_f = "cloud_dep_"
class fog_cloud_sys:
    def __init__(self, mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end):
        self.mode = mode
        self.arrival = arrival
        self.service = service
        self.network = network
        self.fogTimeLimit = fogTimeLimit
        self.fogTimeToCloudTime = fogTimeToCloudTime
        self.time_end = time_end
                                                                # fog related variable (PS server)
        self.fogQueue = list()                                  # coming queue to fog (buffer)
        self.fogLog = dict()                                    # fog leave Log
        self.departureFromfog = dict()                          # all events departure from fog
        self.fogClock = 0                                       # fog main clock
        self.fogJobLs = list()                                  # job still work in fog
        self.fogQueue = [(self.arrival[i], self.service[i]) for i in range(len(self.arrival))]      # initial fogQueue
        if self.mode == "trace":
            self.fogQueue.append((self.time_end, self.time_end))
        else:
            self.fogQueue.append((self.time_end, float("inf")))
                                                                # network related variable
        self.networkQueue = list()                              # coming queue to network (buffer)
        self.networkLog = dict()                                # network leave Log
        self.networkLock = Lock()                               # network variable thread Lock
        self.networkClock = 0                                   # network main clock
        self.networkJobLs = list()                              # job still work in fog
                                                                # cloud related variable (PS server)
        self.cloudQueue = list()                                # coming queue to cloud
        self.cloudLog = dict()                                  # cloud leave Log
        self.cloudLock = Lock()                                 # cloud variable thread Lock
        self.cloudClock = 0                                     # main clock in cloud
        self.cloudJobLs = list()                                # job still work in cloud

        t0 = Thread(target=self.fog, name="fog")
        t1 = Thread(target=self.NetWork, name="network")
        t2 = Thread(target=self.cloud, name="cloud")

        t0.start()                                            # thread start
        t1.start()
        t2.start()
       
        t0.join()
        t2.join()

        # write response time into file
        f_mrt = open(mrt_f + str(file_No) + suffix, 'w')

        response_dict = {**self.departureFromfog, **self.cloudLog}
        total = 0

        for key, value in response_dict.items():
            total += (value - key)
        mean_response_time = total / len(response_dict)
        f_mrt.write(f"%.4f\n" % mean_response_time)
        f_mrt.close()

        print(f"response time: {mean_response_time}")
        print("-------------------")

        self.response_dict = response_dict

    def fog(self):                                              # simulation all event in fog (PS system)
        f_fog_dep = open(fog_dep_f + str(file_No) + suffix, 'w')

        while self.fogClock < self.time_end:
            # determine next event is departure or arrival
            if len(self.fogJobLs) > 0:                                      # if JobLs no empty (next event maybe departure or arrival) always do departure before arrival if they are happen same time
                result = self.has_departure(self.fogClock, self.fogJobLs, self.fogQueue[0][0], 1)
                if result == None:                                                           # next event is arrival
                    event = self.fogQueue.pop(0)
                    cost = (event[0] - self.fogClock) / len(self.fogJobLs)

                    for job in self.fogJobLs:
                        job[1] = job[1] - cost
                    
                    self.fogClock = event[0]
                    self.fogJobLs.append([event[0], min(self.fogTimeLimit, event[1])])
                else:                                                                         # next event is departure
                    self.fogJobLs.remove(result)
                    event = result
                    cost = event[1]

                    for job in self.fogJobLs:
                        job[1] = job[1] - cost

                    self.fogLog[event[0]] = self.fogClock + event[1] * (len(self.fogJobLs) + 1)
                    with self.networkLock:
                        if self.service[self.arrival.index(event[0])] > self.fogTimeLimit:
                            self.networkQueue.append((event[0], self.fogClock + event[1] * (len(self.fogJobLs) + 1)))
                        else:
                            self.departureFromfog[event[0]] = self.fogClock + event[1] * (len(self.fogJobLs) + 1)

                    self.fogClock += event[1] * (len(self.fogJobLs) + 1)
            else:                                                           # if JobLs is empty (next event must be arrival)
                event = self.fogQueue.pop(0)
                self.fogClock = event[0]
                self.fogJobLs.append([event[0], min(self.fogTimeLimit, event[1])])

                                                  # add tail
        with self.networkLock:
            self.networkQueue.append((self.time_end, self.time_end))
        
        print("fog thread end...")
        # write into file here
        for index in sorted(self.fogLog.keys()):
            f_fog_dep.write(f"%.4f\t%.4f\n" % (index, self.fogLog[index]))
        f_fog_dep.close()

    def NetWork(self):                                          # simulation all event in network
        f_net_dep = open(net_dep_f + str(file_No) + suffix, 'w')

        while self.networkClock < self.time_end:
            with self.networkLock:
                length = len(self.networkQueue)

            if length > 0:                                       # do something here
                event = self.networkQueue.pop(0)
                self.networkClock = event[1]
                
                if self.time_end > self.networkClock:
                #if self.networkClock != float("inf"):
                    self.networkJobLs.append((event[0], event[1], self.network[self.arrival.index(event[0])]))

                Buffer = list()
                for job in self.networkJobLs:
                    if job[1] + job[2] <= self.networkClock:        # time to departure
                        Buffer.append(job)
                
                # sorted Buffer here && put Buffer to Cloud network && remove that job in networkJobLs
                for job in Buffer:                                  # remove that job in networkJobLs
                    self.networkJobLs.remove(job)
                Buffer = [(i[0], i[1] + i[2]) for i in Buffer]
                Buffer = sorted(Buffer, key=lambda item: item[1])
                
                for job in Buffer:                                  # write into Log
                    self.networkLog[job[0]] = job[1]

                with self.cloudLock:                                # put buffer to cloud
                    self.cloudQueue.extend(Buffer)
            else:                                                # do nothing because no element in netQueue (wait for elements coming)
                pass

        with self.cloudLock:
            self.cloudQueue.append((self.time_end, self.time_end))
        
        print("network thread end....")
        # write into file here
        for index in sorted(self.networkLog.keys()):
            f_net_dep.write(f"%.4f\t%.4f\n" % (index, self.networkLog[index]))
        f_net_dep.close()

    def cloud(self):                                            # simulation all event in cloud (PS system)
        f_cloud_dep = open(cloud_dep_f + str(file_No) + suffix, 'w')

        while self.cloudClock < self.time_end:
            with self.cloudLock:
                length = len(self.cloudQueue)

            if length > 0:                                       # arrival in cloud Queue
                if len(self.cloudJobLs) > 0:                            # cloudJobLs not empty, arrival or departure event happen
                    result = self.has_departure(self.cloudClock, self.cloudJobLs, self.cloudQueue[0][1], 2)
                    if result != None:                                  # departure event happen
                        self.cloudJobLs.remove(result)

                        for job in self.cloudJobLs:
                            job[2] = job[2] - result[2]

                        self.cloudClock += result[2] * (len(self.cloudJobLs) + 1)
                        self.cloudLog[result[0]] = self.cloudClock
                    else:                                               # arrival event happen
                        event = self.cloudQueue.pop(0)
                        
                        cost = (event[1] - self.cloudClock) / len(self.cloudJobLs)

                        for job in self.cloudJobLs:
                            job[2] = job[2] - cost

                        self.cloudClock = event[1]
                        if self.cloudClock < self.time_end:
                            self.cloudJobLs.append([event[0], event[1], self.fogTimeToCloudTime * (self.service[self.arrival.index(event[0])] - self.fogTimeLimit)])
                else:                                                   # empty, just arrival event happen
                    event = self.cloudQueue.pop(0)
                    
                    self.cloudClock = event[1]
                    if self.cloudClock < self.time_end:
                        self.cloudJobLs.append([event[0], event[1], self.fogTimeToCloudTime * (self.service[self.arrival.index(event[0])] - self.fogTimeLimit)])
            else:                                                # no arrival in cloud Queue
                pass
        print("cloud thread end...")
        # write into file here
        for index in sorted(self.cloudLog.keys()):
            f_cloud_dep.write(f"%.4f\t%.4f\n" % (index, self.cloudLog[index]))
        f_cloud_dep.close()

    # Support funciton, determine whether has job leave before timelimit (PS server)
    # if has, return the leaving first, else return None
    def has_departure(self, now, jobLs, timelimit, i):
        mini = None
        
        for job in jobLs:
            if now + job[i] * len(jobLs) <= timelimit:
                if mini == None:
                    mini = job
                elif mini[i] > job[i]:
                    mini = job
                else:
                    pass 
        return mini

def simulation(mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end):
    fgc = fog_cloud_sys(mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end)
    return fgc.response_dict

# draw map, x, y is list
def draw(responseLs, fogTimeLimit):
    x = range(1, len(responseLs) + 1)
    y = list()
    for i in range(len(responseLs)):
        y.append(sum(responseLs[0:i + 1]) / (i + 1))

    plt.plot(x, y, color='b')
    plt.xlabel("k")
    plt.ylabel("Mean response time of first k jobs")
    plt.yticks()
    plt.title(f"Seed {seed}, fogTimeLimit {fogTimeLimit}")
    plt.show()