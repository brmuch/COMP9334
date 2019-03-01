5. A transaction processing system is monitored for one hour. During this period, 5400 transactions are processed. What is the utilization of a disk if its average service time is equal to 30 msec per visit and the disk is visited three times on average by every transaction?
 
**Answer:**

		Obervation period T = 1h = 3600s
		and busy time B = 5400 * 3 * 30 * 10^-3 = 486s
		so utilization U = B / T = 486 / 3600 = 13.5%

6. The average delay experience by a packet when traversing a computer network is 100 msec. The average number of packets that cross the network per second is 128 packets/sec. What is the average number of concurrent packets in transit in the network at any time?

**Answer:**

        According to the Little's Law,
        throughout of device X = 128 packets/sec,
        average response time of the request Ravg = 100msec = 0.1sec
        so, 
        Navg = X * Ravg = 0.1 * 128 = 12.8 packets

7. A file server is monitored for 60 minutes, during which time 7200 requests are completed. The disk utilization is measured to be 30%. The average service time at this disk is 30 msec per file operation request. What is the average number of accesses to this accesses to this disk per file request?

**Answer:**

		From  question we can know that:
		observation time T = 60min = 3600s
		completed C = 7200 requests,
		then output rate X = C / T = 7200 / 3600 = 2 requests per sec,
		according to Utilisation Law
		mean service time per completed request S = U / X = 0.3 / 2 = 0.15 sec per requests
		so,
		the average number of accesses to this disk per file request is 0.15 / (30 * 10^3) = 5
     
    


